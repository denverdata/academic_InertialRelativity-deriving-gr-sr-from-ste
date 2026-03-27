#!/usr/bin/env python3
"""
Generate the system properties table for the appendix of master.tex.

All values are taken directly from the paper's examples except:
  - I = 0.4 * M * R^2 (computed from paper's M and R)
  - Inter-row ratios (computed from paper's values)

Usage:
    python3 generate_table.py
    # produces system_table.tex in the same directory
"""

from decimal import Decimal, getcontext
import math
import os

getcontext().prec = 50

# ---------------------------------------------------------------------------
# Significant figures for output
# ---------------------------------------------------------------------------
SIG_FIGS = 5


def _sqrt_dec(x):
    """High-precision square root for Decimal via Newton's method."""
    if x <= 0:
        return Decimal(0)
    guess = Decimal(str(math.sqrt(float(x))))
    for _ in range(100):
        new = (guess + x / guess) / 2
        if new == guess:
            break
        guess = new
    return guess


def efmt(v):
    """Format in XE+Y / XE-Y notation with SIG_FIGS significant figures."""
    fv = float(v)
    if fv == 0:
        return "0"
    exp = math.floor(math.log10(abs(fv)))
    m = fv / 10**exp
    decimals = SIG_FIGS - 1
    if round(m, decimals) >= 10.0:
        exp += 1
        m = m / 10
    sign = "+" if exp >= 0 else "$-$"
    return f"{m:.{decimals}f}E{sign}{abs(exp)}"


def oneminus(v):
    """Format d tau/dt in 1-x or 1+x notation."""
    fv = float(v)
    if fv == 1.0:
        return "1.0000E+0"
    deficit = 1.0 - fv
    if deficit > 0:
        return f"1$-${efmt(deficit)}"
    else:
        return f"1+{efmt(abs(deficit))}"


# ---------------------------------------------------------------------------
# System data: ALL values from the paper's examples.
#
# Fields:
#   case    — case number (string)
#   label   — S_1 or S_2
#   M       — mass (kg), from paper
#   R       — radius (m), from paper
#   ddc     — D/D_crit for this system, from paper's stated k_i values
#   dtau    — individual d tau/dt = sqrt(1 - D/D_crit), from paper
#             (these appear as sqrt(1-k_i) in the paper's ratio formulas)
# ---------------------------------------------------------------------------
# For Case 1, the paper states:
#   S1: 2GM/(R1 c^2) = 4.24605E-6  (confirmation, line 465-466)
#   S2: at R=2954, r_s=2953.34 -> D/D_crit = r_s/R = 2953.34/2954 = 0.999777
#   d tau/dt at R1: 0.99999787697 (confirmation)
#   d tau/dt at R2: sqrt(1 - 2953.34/2954) = sqrt(0.000223) ~ 0.01495
#
# For Cases 2-5, the paper states k_i = D_i/D_crit directly:
#   Case 2: k1=1.48523E-5, k2=1.48523E-11
#   Case 3: k1=1.48523E-5, k2=1.48523E-7
#   Case 4: k1=1.48523E-5, k2=1.48523E-2
#   Case 5: k1=1.48523E-8, k2=1.48523E-10
# ---------------------------------------------------------------------------

_D = Decimal

# Physical constants for r_s = 2GM/c^2 (standard values)
G = _D("6.67430e-11")   # m^3 kg^-1 s^-2
c = _D("2.99792458e8")  # m/s

# Pre-compute individual d tau/dt from the paper's k_i values
def _dtau(k_str):
    """sqrt(1 - k) from a paper-stated k value."""
    k = _D(k_str)
    return _sqrt_dec(_D(1) - k)

SYSTEMS = [
    {
        "case": "1", "label": "S_1",
        "M": _D("1.989e30"), "R": _D("6.957e8"),
        "ddc": _D("4.24605e-6"),           # from paper confirmation
        "dtau": _dtau("4.24605e-6"),
    },
    {
        "case": "1", "label": "S_2",
        "M": _D("1.989e30"), "R": _D("2954.0"),
        "ddc": _D("2953.34") / _D("2954"), # r_s/R from paper
        "dtau": _sqrt_dec(_D(1) - _D("2953.34") / _D("2954")),
    },
    {
        "case": "2", "label": "S_1",
        "M": _D("1e30"), "R": _D("1e8"),
        "ddc": _D("1.48523e-5"),            # from paper
        "dtau": _dtau("1.48523e-5"),
    },
    {
        "case": "2", "label": "S_2",
        "M": _D("1e24"), "R": _D("1e8"),
        "ddc": _D("1.48523e-11"),           # from paper
        "dtau": _dtau("1.48523e-11"),
    },
    {
        "case": "3", "label": "S_1",
        "M": _D("1e30"), "R": _D("1e8"),
        "ddc": _D("1.48523e-5"),            # from paper
        "dtau": _dtau("1.48523e-5"),
    },
    {
        "case": "3", "label": "S_2",
        "M": _D("1e27"), "R": _D("1e7"),
        "ddc": _D("1.48523e-7"),            # from paper
        "dtau": _dtau("1.48523e-7"),
    },
    {
        "case": "4", "label": "S_1",
        "M": _D("1e30"), "R": _D("1e8"),
        "ddc": _D("1.48523e-5"),            # from paper (same system as cases 2,3)
        "dtau": _dtau("1.48523e-5"),
    },
    {
        "case": "4", "label": "S_2",
        "M": _D("1e32"), "R": _D("1e7"),
        "ddc": _D("1.48523e-2"),            # from paper
        "dtau": _dtau("1.48523e-2"),
    },
    {
        "case": "5", "label": "S_1",
        "M": _D("1e27"), "R": _D("1e8"),
        "ddc": _D("1.48523e-8"),            # from paper
        "dtau": _dtau("1.48523e-8"),
    },
    {
        "case": "5", "label": "S_2",
        "M": _D("1e24"), "R": _D("1e7"),
        "ddc": _D("1.48523e-10"),           # from paper
        "dtau": _dtau("1.48523e-10"),
    },
]

# ---------------------------------------------------------------------------
# STE and GR pair results — directly from the paper's examples.
# ---------------------------------------------------------------------------
PAIR_STE = {
    "1": _D("0.99999787696"),
    "2": _D("0.9999925737"),
    "3": _D("0.99999264807"),
    "4": _D("1.0"),
    "5": _D("0.99999999264810"),
}

PAIR_GR = {
    "1": _D("0.99999787697"),
    "2": _D("0.9999925737"),
    "3": _D("0.99999264807"),
    "4": _D("1.0"),
    "5": _D("0.99999999264810"),
}


def generate():
    """Build the LaTeX table from paper values. Only I, pair ratios, and
    inter-row ratios are computed. All per-system values come from the paper."""

    # Add computed I and r_s/R to each row
    rows = []
    for s in SYSTEMS:
        I_val = _D("0.4") * s["M"] * s["R"] * s["R"]
        r_s = _D(2) * G * s["M"] / (c * c)   # r_s = 2GM/c^2
        rs_over_R = r_s / s["R"]               # r_s/R
        rows.append({**s, "I": I_val, "r_s": r_s, "rs_over_R": rs_over_R})

    # Compute pair time dilation ratios: S1.dtau / S2.dtau for each case
    # (computed from the paper's per-system dtau values)
    pair_ratios = {}
    for pair_idx in range(5):
        s1 = rows[pair_idx * 2]
        s2 = rows[pair_idx * 2 + 1]
        case = s1["case"]
        if s2["dtau"] > 0:
            pair_ratios[case] = s1["dtau"] / s2["dtau"]
        else:
            pair_ratios[case] = None

    # Build LaTeX rows
    latex_rows = []
    n = len(rows)
    for i, row in enumerate(rows):
        cn = row["case"]
        num = i + 1
        is_s2 = (row["label"] == "S_2")

        # Per-system values from paper
        m_s = efmt(row["M"])
        r_s = efmt(row["R"])
        i_s = efmt(row["I"])           # computed: 0.4 * M * R^2
        ddc_s = efmt(row["ddc"])       # from paper
        rsr_s = efmt(row["rs_over_R"]) # computed: (M/D_crit) / R

        # STE d tau/dt: from the paper's inertia-derived k_i values
        ste_s = oneminus(row["dtau"])

        # GR d tau/dt: independently computed as sqrt(1 - 2GM/(Rc^2))
        gr_dtau = _sqrt_dec(_D(1) - row["rs_over_R"])
        gr_s = oneminus(gr_dtau)

        # Ratios to prior row (wraps: row 1 compares to row 10)
        prev = rows[(i - 1) % n]
        mr = efmt(row["M"] / prev["M"])
        rr = efmt(row["R"] / prev["R"])
        ir = efmt(row["I"] / prev["I"])
        if prev["dtau"] > 0 and row["dtau"] > 0:
            dr = efmt(row["dtau"] / prev["dtau"])
        else:
            dr = "0"

        cols = [
            str(num), cn, f"${row['label']}$",
            m_s, r_s, i_s, ddc_s, rsr_s,
            ste_s, gr_s,
            mr, rr, ir, dr,
        ]
        latex_rows.append(" & ".join(cols) + r" \\")

    header = r"""\begin{table*}[t]
\centering
\caption{System properties and time dilation for Cases 1--5, comparing STE and Schwarzschild results. Ratios are to the preceding row.}
\label{tab:system_properties}
\resizebox{\textwidth}{!}{%
\begin{tabular}{rclllllllllllll}
\toprule
\# & Case & Sys & $M$ (kg) & $R$ (m) & $I$ (kg\,m$^2$) & $D/D_{crit}$ & $r_s/R$ & STE $d\tau/dt$ & GR $d\tau/dt$ & $M_n/M_{n\text{-}1}$ & $R_n/R_{n\text{-}1}$ & $I_n/I_{n\text{-}1}$ & $(d\tau/dt)_n/(d\tau/dt)_{n\text{-}1}$ \\
\midrule"""

    footer = r"""\bottomrule
\end{tabular}}
\end{table*}"""

    body = "\n".join(latex_rows)
    return f"{header}\n{body}\n{footer}\n"


if __name__ == "__main__":
    table = generate()
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "system_table.tex")
    with open(out_path, "w") as f:
        f.write(table)
    print(f"Written to {out_path}")
    print()
    print(table)
