import networkx as nx
import numpy as np
from itertools import combinations

from pyrivet import rivet, hera
from pyrivet.matching_distance import find_offset, calculate_weight

from src.rivet_bifiltration import construct_bifiltration


def critical_points(metric_space, homology: int = 0) -> list:
    """
    Extract the critical grades of a RIVET bifiltration.
    """
    mb = rivet.betti(metric_space, homology=homology)

    points = set()

    for xi in (mb.xi_0, mb.xi_1, mb.xi_2):
        for xi_idx, yi_idx, _mult in xi:
            x = float(mb.dimensions.x_grades[xi_idx])
            y = float(mb.dimensions.y_grades[yi_idx])
            points.add((x, y))

    return sorted(points)


def wall_lines(points: list) -> list:
    """
    Construct slice lines through pairs of critical points.

    Only lines with slopes strictly between 0 and 90 degrees
    are used, matching the convention in pyrivet.matching_distance.
    """
    lines = set()

    for (x1, y1), (x2, y2) in combinations(points, 2):

        if x1 == x2 or y1 == y2:
            continue

        slope_deg = np.degrees(
            np.arctan2(y2 - y1, x2 - x1)
        )

        if slope_deg <= 0 or slope_deg >= 90:
            continue

        offset = find_offset(
            slope_deg,
            (x1, y1),
        )

        lines.add(
            (
                round(float(slope_deg), 10),
                round(float(offset), 10),
            )
        )

    return sorted(lines)


def fibered_matching_distance(
    module1,
    module2,
    metric_space1,
    metric_space2,
    homology: int = 0,
    normalize: bool = True,
) -> float:
    """
    Compute a matching-distance-style quantity using fibered
    persistence barcodes along critical/wall slices.

    This is specifically designed to also work when the
    appearance coordinate is degenerate, e.g. regular graphs.
    """

    points = (
        critical_points(metric_space1, homology)
        + critical_points(metric_space2, homology)
    )

    lines = wall_lines(points)

    if not lines:
        return 0.0

    bars1 = rivet.barcodes(module1, lines)
    bars2 = rivet.barcodes(module2, lines)

    raw_distances = hera.multi_bottleneck_distance(
        [bars for (_, bars) in bars1],
        [bars for (_, bars) in bars2],
    )

    raw_distances = np.asarray(
        raw_distances,
        dtype=float,
    )

    bounds1 = rivet.bounds(module1)
    bounds2 = rivet.bounds(module2)
    bounds = bounds1.common_bounds(bounds2)

    delta_x = (
        bounds.upper_right[0]
        - bounds.lower_left[0]
    )

    delta_y = (
        bounds.upper_right[1]
        - bounds.lower_left[1]
    )

    slopes = np.array(
        [line[0] for line in lines],
        dtype=float,
    )

    # ---------------------------------------------------------
    # Degenerate appearance coordinate.
    #
    # This happens for regular graphs because every vertex has
    # the same degree. In this case the 2D matching-distance
    # normalization is undefined, so use the unweighted
    # bottleneck distance of the fibered slices.
    # ---------------------------------------------------------

    if delta_x == 0 or delta_y == 0:
        return float(np.max(raw_distances))

    if normalize:
        weights = calculate_weight(
            slopes,
            True,
            delta_x,
            delta_y,
        )

        m = np.tan(np.radians(slopes))

        bottleneck_stretch = np.sqrt(
            (
                (m / delta_y) ** 2
                + (1 / delta_x) ** 2
            )
            / (m ** 2 + 1)
        )

        distances = (
            weights
            * raw_distances
            * bottleneck_stretch
        )

    else:
        weights = calculate_weight(
            slopes,
            False,
        )

        distances = (
            weights
            * raw_distances
        )

    return float(np.max(distances))


def matching_dist(
    G1: nx.Graph,
    G2: nx.Graph,
    degree: int = 0,
    max_dim: int = 2,
    Rips: bool = True,
    grid_size: int = 20,
    normalize: bool = True,
) -> float:
    """
    Compute the fibered-barcode matching distance between two
    degree-Rips bifiltrations.

    grid_size is retained for API compatibility with the previous
    RIVET implementation. The fibered implementation determines
    its slices from critical points instead.
    """

    if degree not in (0, 1):
        raise ValueError(
            "The RIVET implementation currently supports "
            "H_0 and H_1."
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

    return fibered_matching_distance(
        m1,
        m2,
        ms1,
        ms2,
        homology=degree,
        normalize=normalize,
    )


def check_if_graphs_are_isomorphic(
    G1: nx.Graph,
    G2: nx.Graph,
    max_dim: int = 2,
    Rips: bool = True,
    grid_size: int = 20,
    threshold: float = 1e-7,
    normalize: bool = True,
) -> bool:
    """
    Check whether the two graphs are distinguished by the
    fibered-barcode distances in H_0 and H_1.
    """

    graphs_are_isomorphic = True

    for degree in (0, 1):

        distance = matching_dist(
            G1,
            G2,
            degree=degree,
            max_dim=max_dim,
            Rips=Rips,
            grid_size=grid_size,
            normalize=normalize,
        )

        if distance > threshold:
            graphs_are_isomorphic = False
            break

    return graphs_are_isomorphic