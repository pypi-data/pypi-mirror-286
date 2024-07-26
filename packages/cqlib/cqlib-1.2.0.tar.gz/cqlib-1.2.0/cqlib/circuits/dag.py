# This code is part of cqlib.
#
# Copyright (C) 2024 China Telecom Quantum Group, QuantumCTek Co., Ltd.,
# Center for Excellence in Quantum Information and Quantum Physics.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Circuits as Directed Acyclic Graphs."""

import networkx as nx

from cqlib.circuits.circuit import Circuit
from cqlib.circuits.instruction_data import InstructionData
from cqlib.circuits.parameter import Parameter


def circuit_to_dag(circuit: Circuit) -> nx.DiGraph:
    """
    Convert a quantum circuit into a Directed Acyclic Graph (DAG).

    Each operation in the circuit is added as a node in the DAG.
    Directed edges are created between nodes to maintain the operational
    dependencies determined by the qubits each operation acts upon.
    This ensures that operations are ordered correctly relative to the qubits they use.

    Args:
        circuit (Circuit): The quantum circuit to convert, containing a sequence of operations.

    Returns:
        nx.DiGraph: The directed acyclic graph representation of the circuit.
    """
    dag = nx.DiGraph()
    qubit_last_nodes = {}

    for op in circuit.instruction_sequence:
        if not isinstance(op, InstructionData):
            raise TypeError(f"{op} must be instance of InstructionData")
        dag.add_node(op, label=str(op))
        for qubit in op.qubits:
            if qubit in qubit_last_nodes:
                dag.add_edge(qubit_last_nodes[qubit], op)
            qubit_last_nodes[qubit] = op

    return dag


def dag_to_circuit(dag: nx.DiGraph) -> Circuit:
    """
    Converts a Directed Acyclic Graph (DAG) back into a quantum circuit.
    The DAG is expected to have nodes representing quantum operations
    (InstructionData) and edges defining the order of these operations.

    Args:
        dag (nx.DiGraph): The DAG to convert, where nodes are operations
            and edges represent execution dependency.

    Returns:
        Circuit: A quantum circuit reconstructed from the DAG.
    """
    if not nx.is_directed_acyclic_graph(dag):
        raise ValueError("The provided graph must be acyclic to form a valid quantum circuit.")

    circuit = Circuit(0)
    topological_order: list[InstructionData] = list(nx.topological_sort(dag))

    for node in topological_order:
        if not isinstance(node, InstructionData):
            raise ValueError(f"{node} in the DAG must be instance of InstructionData")
        for qubit in node.qubits:
            if qubit not in circuit.qubits:
                circuit.add_qubit(qubit)
        for param in node.instruction.params:
            if isinstance(param, Parameter) and param not in circuit.parameters:
                circuit.add_parameter(param)
        circuit.append_instruction_data(node)

    return circuit
