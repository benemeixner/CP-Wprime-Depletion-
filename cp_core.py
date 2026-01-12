# cp_core.py
"""Critical Power (CP) + W' calculator (inverse-time model).

Model:
  P = (W' / t) + CP
Let x = 1/t, y = P  ->  y = W' * x + CP

Inputs:
  - Mean power (W) for time trials of fixed durations (default 3, 5, 12 min)
Outputs:
  - CP in W
  - W' in J (and kJ)
  - Fit diagnostics (R², residuals)

Also provides utilities to compute the constant power needed to deplete
a given fraction of W' over a given duration:
  (P - CP) * duration = fraction * W'  ->  P = CP + fraction*W'/duration
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Tuple, Dict

import numpy as np


@dataclass
class CpWprimeResult:
    cp_w: float
    wprime_j: float
    r2: float
    residuals_w: List[float]
    durations_s: List[float]
    powers_w: List[float]


def fit_inverse_time_model(
    powers_w: Iterable[float],
    durations_s: Iterable[float],
) -> CpWprimeResult:
    """Fit CP and W' via least squares to P = W'/t + CP."""
    p = np.asarray(list(powers_w), dtype=float)
    t = np.asarray(list(durations_s), dtype=float)

    if p.size != t.size or p.size < 2:
        raise ValueError("Provide the same number of powers and durations (>=2).")

    if np.any(~np.isfinite(p)) or np.any(~np.isfinite(t)):
        raise ValueError("All powers and durations must be finite numbers.")

    if np.any(t <= 0):
        raise ValueError("All durations must be > 0 seconds.")

    x = 1.0 / t
    y = p

    A = np.vstack([x, np.ones_like(x)]).T
    a, b = np.linalg.lstsq(A, y, rcond=None)[0]  # a=W', b=CP

    y_hat = a * x + b
    resid = (y - y_hat).tolist()

    ss_res = float(np.sum((y - y_hat) ** 2))
    ss_tot = float(np.sum((y - float(np.mean(y))) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")

    return CpWprimeResult(
        cp_w=float(b),
        wprime_j=float(a),
        r2=float(r2),
        residuals_w=[float(r) for r in resid],
        durations_s=[float(v) for v in t.tolist()],
        powers_w=[float(v) for v in p.tolist()],
    )


def power_for_fraction_wprime(
    cp_w: float,
    wprime_j: float,
    fraction: float,
    duration_s: float,
) -> float:
    """Constant power (W) required to expend `fraction` of W' over `duration_s`."""
    if duration_s <= 0:
        raise ValueError("duration_s must be > 0")
    if fraction < 0:
        raise ValueError("fraction must be >= 0")
    return float(cp_w + (fraction * wprime_j) / duration_s)


def pretty_units(result: CpWprimeResult) -> Dict[str, float]:
    return {
        "CP_W": result.cp_w,
        "Wprime_J": result.wprime_j,
        "Wprime_kJ": result.wprime_j / 1000.0,
        "R2": result.r2,
    }
