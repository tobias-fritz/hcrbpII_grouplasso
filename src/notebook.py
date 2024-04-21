import numpy as np
from typing import Tuple
import networkx as nx
from group_lasso import GroupLasso


one_hot = {"A":0, "C":1, "D":2, "E":3, "F":4, "G":5, "H":6, "I":7, "K":8, "L":9, "M":10, "N":11, "P":12, "Q":13, "R":14, "S":15, "T":16, "V":17, "W":18, "Y":19}

def one_hot_encode(aa: str) -> np.ndarray:
    """One-hot encode an amino acid."""

    arr = np.zeros(20)
    arr[one_hot[aa]] = 1

    return arr

def get_seq(init_seq: str, mutant_str: str) -> str:
    """Generate a sequence from a mutant string
    
    Args:
        init_seq: str, the initial sequence
        mutant_str: str, the mutant string (e.g. "Q108K:K40L:T51V:R58W")
    Returns:
        str, the mutated sequence
    """

    mutations = mutant_str.split(":")
    seq = list(init_seq)
    
    try:
        for mut in mutations:
            pos = int(mut[1:-1])
            aa = mut[-1]
            seq[pos-1] = aa
    except ValueError:
        pass

    return "".join(seq)

def predict_new_maximum(gl: GroupLasso, wt_seq: str, mutant: str) -> float:
    """Predict the maximum absorption for a mutant.
    
    Args:
        gl: GroupLasso, the trained model
        wt_seq: str, the wild-type sequence
        mutant: str, the mutant string
    Returns:
        float, the predicted maximum absorption
    """
    
    seq = get_seq(wt_seq, mutant)
    X = np.array([one_hot_encode(aa) for aa in seq]).reshape(1, -1)
    return gl.predict(X)[0]

def find_greedy_mutant(target_wavelength: int, 
                       coefficients: np.ndarray, 
                       wt_seq: str,
                       WT_wavelength: int=576,
                       threshold: int=5) -> Tuple[str, int]:
    """Using a graph, find a mutant that is closest to the target absorption maximum.

    This approach is based on the idea that we can construct a graph where the nodes are the mutations and the
    associated shifts are weights.The graph is constructed by adding nodes for each mutation and edges between 
    all nodes that are at different positions. 
    The mutations leading to the target absorption maximum are then found using a greedy algorithm that keeps
    adding the mutation that brings the total shift closest to the target while removing the nodes at the same
    position. 

    Args:
        target_wavelength: int, the target absorption maximum
        coefficients: np.ndarray, the coefficients of the model
        WT_wavelength: int, the absorption maximum of the wild type
        threshold: int, the threshold for the target absorption maximum
    Returns:
        str, the mutations that lead to the target absorption maximum
        int, the new absorption maximum
    """

    # Get all the positions with non-zero coefficients
    non_zero_positions = np.where(np.any(coefficients != 0, axis=1))[0]
    non_zero_coefficients = coefficients[np.any(coefficients != 0, axis=1), :]
    wt_residues = np.asarray([one_hot_encode(aa) for aa in wt_seq])
    
    # Remove the wild type residue from the coefficients to get the pure shifts
    for i, pos in enumerate(non_zero_positions):
        wt_residue = wt_residues[pos]
        wt_mask = wt_residue != 0
        substraction = non_zero_coefficients[i, wt_mask]
        mask = non_zero_coefficients[i, :] != 0
        non_zero_coefficients[i, mask] -= substraction

    # Map all non zero mutations to their position and corresponding shift
    non_zero_aa = {pos:{aa:coef for aa, coef in zip(one_hot.keys(), non_zero_coefficients[i]) if coef != 0}\
                    for i, pos in enumerate(non_zero_positions)} # Dict[int, Dict[str, float]]
    
    # Creat a graph
    G = nx.Graph()
    # Add nodes for each mutation, with the shift as the node weight
    [G.add_node((pos, aa), weight=shift) for pos, aas in non_zero_aa.items() for aa, shift in aas.items()]
    # Add edges between all nodes that are at different positions
    [G.add_edge(node1, node2) for node1 in G.nodes for node2 in G.nodes if node1[0] != node2[0]]

    # Find the shortest path between the wild type and all other nodes
    path = []
    current_wavelength = WT_wavelength

    try:
        while abs(current_wavelength - target_wavelength) > threshold:
            # Find the mutation that brings the total shift closest to the target
            closest_node = min(G.nodes, key=lambda node: abs((current_wavelength + G.nodes[node]["weight"]) - target_wavelength))
            path.append(closest_node)
            current_wavelength += G.nodes[closest_node]["weight"]
            # Remove the nodes at the same position as the chosen node
            G.remove_nodes_from([node for node in G.nodes if node[0] == closest_node[0]])
    except ValueError:
        print("No path found!")
        return [], 0

    # write out the nodes and their contributions
    mutations = "; ".join([f"{wt_seq[pos]}{pos+1}{aa}({round(non_zero_aa[pos][aa])}nm)" for pos, aa in path])
    mutant_str = ":".join([f"{wt_seq[pos]}{pos+1}{aa}" for pos, aa in path])

    return mutant_str, mutations, current_wavelength