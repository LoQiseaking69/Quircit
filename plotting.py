import matplotlib.pyplot as plt
from qiskit.visualization import plot_histogram, plot_bloch_multivector

def update_circuit_diagram(figure, circuit):
    """Updates the circuit diagram."""
    figure.clear()
    circuit.draw('mpl', ax=figure.add_subplot(121))

def update_quantum_state(figure, state):
    """Updates the quantum state visualization."""
    plot_bloch_multivector(state, ax=figure.add_subplot(122))

def update_histogram(figure, counts):
    """Updates the histogram plot."""
    figure.clear()
    plot_histogram(counts, ax=figure.add_subplot(111))
