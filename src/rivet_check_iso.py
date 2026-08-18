import networkx as nx

from src.rivet_bifiltration import construct_bifiltration
from src.fibered_lines import wall_matching_distance


def matching_dist(
    G1: nx.Graph,
    G2: nx.Graph,
    degree: int = 0,
    max_dim: int = 2,
    Rips: bool = True,
) -> float:
    """
    Compute the wall-based matching distance between the RIVET
    degree-Rips bifiltrations of G1 and G2.
    """
    if degree not in (0, 1):
        raise ValueError(
            "The RIVET implementation currently supports H_0 and H_1."
        )

    m1, ms1 = construct_bifiltration(
        G1,
        max_dim=max_dim,
        Rips=Rips,
        homology=degree,
    )

    m2, ms2 = construct_bifiltration(
        G2,
        max_dim=max_dim,
        Rips=Rips,
        homology=degree,
    )

    return wall_matching_distance(
        m1, ms1, m2, ms2,
        homology=degree,
    )


def check_if_graphs_are_isomorphic(
    G1: nx.Graph,
    G2: nx.Graph,
    max_dim: int = 2,
    Rips: bool = True,
    threshold: float = 1e-7,
) -> bool:
    """
    Checks whether two graphs are distinguished by the wall-based
    matching distances of their RIVET degree-Rips bifiltrations.

    Both H_0 and H_1 are tested.
    """
    graphs_are_isomorphic = True

    for degree in (0, 1):
        distance = matching_dist(
            G1,
            G2,
            degree=degree,
            max_dim=max_dim,
            Rips=Rips,
        )

        if distance > threshold:
            graphs_are_isomorphic = False
            break

    return graphs_are_isomorphic