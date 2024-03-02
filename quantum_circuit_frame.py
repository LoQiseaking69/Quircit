import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from qiskit import Aer, execute
import plotting
from quantum_circuit import QuantumCircuitManager

class QuantumCircuitFrame(wx.Frame):
    """ Frame for advanced quantum circuit visualization with expanded quantum gate selection and basic quantum state visualization. """
    NUM_QUBITS = 3
    GATE_CHOICES = ["Hadamard", "CNOT", "Pauli-X", "Pauli-Y", "Pauli-Z", "T", "S"]

    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(1000, 600))
        self.circuit_manager = QuantumCircuitManager(self.NUM_QUBITS)
        self.init_ui()

    def init_ui(self):
        """ Initialize the user interface components. """
        self.panel = wx.Panel(self)
        self.setup_controls()
        self.setup_layout()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.panel, -1, self.figure)
        self.Centre()
        self.Show(True)

    def setup_controls(self):
        """ Set up the control elements in the UI. """
        self.qubitChoice = wx.Choice(self.panel, choices=[f"Qubit {i}" for i in range(self.NUM_QUBITS)])
        self.qubitChoice.SetSelection(0)
        self.gateChoice = wx.Choice(self.panel, choices=self.GATE_CHOICES)
        self.gateChoice.SetSelection(0)
        self.addButton = wx.Button(self.panel, label="Add Gate")
        self.addButton.Bind(wx.EVT_BUTTON, self.on_add_gate)
        self.resetButton = wx.Button(self.panel, label="Reset Circuit")
        self.resetButton.Bind(wx.EVT_BUTTON, self.on_reset_circuit)
        self.runButton = wx.Button(self.panel, label="Run Circuit")
        self.runButton.Bind(wx.EVT_BUTTON, self.on_run_circuit)
        self.sensorDataButton = wx.Button(self.panel, label="Simulate Sensor Data")
        self.sensorDataButton.Bind(wx.EVT_BUTTON, self.on_simulate_sensor_data)

    def setup_layout(self):
        """ Arrange the layout of UI elements. """
        sizer = wx.BoxSizer(wx.VERTICAL)
        controls = [self.qubitChoice, self.gateChoice, self.addButton, self.resetButton, self.runButton, self.sensorDataButton]
        for control in controls:
            sizer.Add(control, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(self.canvas, 1, wx.EXPAND | wx.ALL, 5)
        self.panel.SetSizer(sizer)

    def on_add_gate(self, event):
        """ Handle the event for adding a gate to the quantum circuit. """
        qubit = self.qubitChoice.GetSelection()
        gate = self.gateChoice.GetString(self.gateChoice.GetSelection())
        self.circuit_manager.add_gate(gate, qubit)
        self.update_circuit_diagram()

    def on_reset_circuit(self, event):
        """ Reset the quantum circuit. """
        self.circuit_manager.reset_circuit()
        self.update_circuit_diagram()

    def on_run_circuit(self, event):
        """ Run the quantum circuit and display the result. """
        self.circuit_manager.circuit.measure(range(self.NUM_QUBITS), range(self.NUM_QUBITS))
        simulator = Aer.get_backend('qasm_simulator')
        result = execute(self.circuit_manager.circuit, simulator).result()
        counts = result.get_counts(self.circuit_manager.circuit)
        plotting.update_histogram(self.figure, counts)
        self.canvas.draw()

    def on_simulate_sensor_data(self, event):
        """ Simulate sensor data using QuantumCircuitManager. """
        self.circuit_manager.simulate_sensor_data()
        self.update_circuit_diagram()

    def update_circuit_diagram(self):
        """ Update the circuit diagram in the UI using plotting module. """
        state_simulator = Aer.get_backend('statevector_simulator')
        job = execute(self.circuit_manager.circuit, state_simulator)
        state = job.result().get_statevector()
        plotting.update_circuit_diagram(self.figure, self.circuit_manager.circuit)
        plotting.update_quantum_state(self.figure, state)
        self.canvas.draw()

if __name__ == '__main__':
    app = wx.App(False)
    frame = QuantumCircuitFrame(None, title='Advanced Quantum Circuit Visualization')
    app.MainLoop()