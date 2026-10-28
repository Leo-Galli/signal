"""Build RSSI-versus-distance series from reader-supplied results."""

from __future__ import annotations

from typing import Any


def rssi_distance_series(
    doc: dict[str, Any],
) -> tuple[list[tuple[float, float]], int]:
    """Return ((distance_m, rssi_dbm), ...) and count of skipped blank points.

    Does not invent missing values. Points lacking either number are skipped.
    """
    if not isinstance(doc, dict):
        raise TypeError("doc must be a dict")
    points = doc.get("points")
    if not isinstance(points, list):
        raise ValueError("points must be a list")

    series: list[tuple[float, float]] = []
    skipped = 0
    for pt in points:
        if not isinstance(pt, dict):
            skipped += 1
            continue
        dist = pt.get("distance_m")
        rssi = pt.get("rssi_dbm")
        if dist is None or rssi is None:
            skipped += 1
            continue
        if isinstance(dist, bool) or isinstance(rssi, bool):
            skipped += 1
            continue
        if not isinstance(dist, (int, float)) or not isinstance(rssi, (int, float)):
            skipped += 1
            continue
        series.append((float(dist), float(rssi)))

    series.sort(key=lambda pair: pair[0])
    return series, skipped


def plot_rssi_distance(
    series: list[tuple[float, float]],
    out_path: str,
    *,
    title: str = "RSSI vs distance (reader measurements)",
) -> None:
    """Write a PNG using matplotlib Agg. Requires at least two points."""
    if len(series) < 2:
        raise ValueError("need at least two (distance_m, rssi_dbm) pairs to plot")

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    xs = [pair[0] for pair in series]
    ys = [pair[1] for pair in series]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(xs, ys, marker="o", color="#333333", linewidth=1.5)
    ax.set_xlabel("distance_m")
    ax.set_ylabel("rssi_dbm")
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
