from qiskit import QuantumCircuit
import numpy as np

class QuantumCircuitManager:
    """Manages the quantum circuit operations."""

    def __init__(self, num_qubits):
        self.num_qubits = num_qubits
        self.circuit = QuantumCircuit(num_qubits, num_qubits)

    def reset_circuit(self):
        """Resets the quantum circuit to its initial state."""
        self.circuit = QuantumCircuit(self.num_qubits, self.num_qubits)

    def add_gate(self, gate, qubit):
        """Adds a gate to the quantum circuit."""
        gate_actions = {
            "Hadamard": lambda: self.circuit.h(qubit),
            "CNOT": lambda: self.circuit.cx(qubit, (qubit + 1) % self.num_qubits),
            "Pauli-X": lambda: self.circuit.x(qubit),
            "Pauli-Y": lambda: self.circuit.y(qubit),
            "Pauli-Z": lambda: self.circuit.z(qubit),
            "T": lambda: self.circuit.t(qubit),
            "S": lambda: self.circuit.s(qubit)
        }
        gate_actions.get(gate, lambda: None)()

    def simulate_sensor_data(self):
        """Simulates sensor data and applies corresponding quantum gates."""
        simulated_data = np.random.randint(2, size=self.num_qubits)
        for i, bit in enumerate(simulated_data):
            if bit == 1:
                self.circuit.x(i)
