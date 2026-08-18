import numpy as np
from itertools import combinations

from pyrivet import rivet, hera
from pyrivet.matching_distance import find_offset, calculate_weight


def critical_points(metric_space, homology: int = 0) -> list:
    mb = rivet.betti(metric_space, homology=homology)
    pts = set()
    for xi in (mb.xi_0, mb.xi_1, mb.xi_2):
        for (xi_idx, yi_idx, _mult) in xi:
            x = float(mb.dimensions.x_grades[xi_idx])
            y = float(mb.dimensions.y_grades[yi_idx])
            pts.add((x, y))
    return sorted(pts)


def wall_lines(points: list) -> list:
    lines = set()
    for (x1, y1), (x2, y2) in combinations(points, 2):
        if x1 == x2 or y1 == y2:
            continue
        slope_deg = np.degrees(np.arctan2(y2 - y1, x2 - x1))
        if slope_deg <= 0 or slope_deg >= 90:
            continue
        offset = find_offset(slope_deg, (x1, y1))
        lines.add((round(slope_deg, 10), round(offset, 10)))
    return sorted(lines)


def wall_matching_distance(
    module1,
    metric_space1,
    module2,
    metric_space2,
    homology: int = 0,
    normalize: bool = True,
) -> float:
    pts = critical_points(metric_space1, homology) + critical_points(metric_space2, homology)
    lines = wall_lines(pts)

    if not lines:
        return 0.0

    bars1 = rivet.barcodes(module1, lines)
    bars2 = rivet.barcodes(module2, lines)

    raw_distances = hera.multi_bottleneck_distance(
        [bars for (_, bars) in bars1],
        [bars for (_, bars) in bars2],
    )

    bounds1 = rivet.bounds(module1)
    bounds2 = rivet.bounds(module2)
    bounds = bounds1.common_bounds(bounds2)
    delta_x = bounds.upper_right[0] - bounds.lower_left[0]
    delta_y = bounds.upper_right[1] - bounds.lower_left[1]

    slopes = np.array([l[0] for l in lines])
    w = calculate_weight(slopes, normalize, delta_x, delta_y)

    return float(np.max(w * raw_distances))