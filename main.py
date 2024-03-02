import wx
from quantum_circuit_frame import QuantumCircuitFrame

if __name__ == '__main__':
    app = wx.App(False)
    frame = QuantumCircuitFrame(None, title='Advanced Quantum Circuit Visualization')
    app.MainLoop()
