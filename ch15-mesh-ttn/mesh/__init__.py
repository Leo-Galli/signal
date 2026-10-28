"""Chapter 15 helpers: airtime compare, regions, secret scan."""

from mesh.airtime import airtime_ms, symbol_time_s
from mesh.compare import compare_mesh_vs_uplink
from mesh.regions import REGION_LABELS, normalize_region
from mesh.secrets_scan import scan_text, scan_paths

__all__ = [
    "airtime_ms",
    "symbol_time_s",
    "compare_mesh_vs_uplink",
    "REGION_LABELS",
    "normalize_region",
    "scan_text",
    "scan_paths",
]
