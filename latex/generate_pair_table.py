#!/usr/bin/env python3
"""Generate LaTeX pair comparison tables from pair_comparisons_v2_cases.md"""

import re
import sys
from decimal import Decimal

def parse_md_table(filepath):
    """Parse the markdown table into rows of (label, [values])."""
    rows = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('|--') or line.startswith('| metric'):
                continue
            if line.startswith('|'):
                parts = [p.strip() for p in line.split('|')[1:-1]]
                if len(parts) >= 8:
                    label = parts[0]
                    values = parts[1:8]
                    rows.append((label, values))
    return rows

def fmt(val_str, sig=6):
    """Format a numeric string to sig significant figures in LaTeX scientific notation."""
    val_str = val_str.strip()
    if val_str == '---' or val_str == '':
        return '---'

    try:
        d = Decimal(val_str)
    except:
        return val_str

    if d == 0:
        return '$0$'

    sign = '-' if d < 0 else ''
    d = abs(d)

    # Get the exponent
    # Convert to string in scientific notation
    s = f'{float(d):.{sig-1}e}'
    mantissa, exp = s.split('e')
    exp = int(exp)
    mantissa = float(mantissa)

    # Clean up mantissa
    if mantissa == int(mantissa) and abs(mantissa) < 10:
        mstr = f'{mantissa:.{sig-1}f}'
    else:
        mstr = f'{mantissa:.{sig-1}f}'

    # Remove trailing zeros after decimal for cleanliness, but keep at least one
    if '.' in mstr:
        mstr = mstr.rstrip('0')
        if mstr.endswith('.'):
            mstr += '0'

    if exp == 0:
        return f'${sign}{mstr}$'
    else:
        return f'${sign}{mstr} \\times 10^{{{exp}}}$'

def main():
    rows = parse_md_table('../pair_comparisons_v2_cases.md')

    # Split into top table (properties) and bottom table (ratios)
    # The tables are separated by a blank conceptual boundary
    # Top table: rows 0-17 (m_1 through dtd_2)
    # Bottom table: rows 18 onwards (I_1/I_2 through end)

    # Find the split point - second occurrence of I_1/I_2
    top_rows = []
    bottom_rows = []
    found_split = False
    for label, values in rows:
        if label.startswith('I_1/I_2') and len(top_rows) > 0:
            found_split = True
        if found_split:
            bottom_rows.append((label, values))
        else:
            top_rows.append((label, values))

    # Drop columns: index 1 (case1b) and index 6 (General2)
    keep = [0, 2, 3, 4, 5]  # M=M, R=R, P=P, I=I, General
    top_rows = [(label, [values[i] for i in keep]) for label, values in top_rows]
    bottom_rows = [(label, [values[i] for i in keep]) for label, values in bottom_rows]

    ncols = len(keep)

    # Column headers
    col_headers = [
        r'\makecell{\textbf{M=M} \\ \scriptsize $M_{1,2}\!=\!2\!\times\!10^{30}$ \\ \scriptsize $R_1\!=\!3\!\times\!10^{3}$ \\ \scriptsize $R_2\!=\!7\!\times\!10^{8}$}',
        r'\makecell{\textbf{R=R} \\ \scriptsize $R_{1,2}\!=\!10^{8}$ \\ \scriptsize $M_1\!=\!10^{30}$ \\ \scriptsize $M_2\!=\!10^{24}$}',
        r'\makecell{\textbf{$\rho=\rho$} \\ \scriptsize $\rho_{1,2}\!=\!2.39\!\times\!10^{5}$ \\ \scriptsize $R_1\!=\!10^{8}$ \\ \scriptsize $R_2\!=\!10^{7}$}',
        r'\makecell{\textbf{I=I} \\ \scriptsize $I_{1,2}\!=\!4\!\times\!10^{45}$ \\ \scriptsize $M_1\!=\!10^{32}$ \\ \scriptsize $M_2\!=\!10^{30}$}',
        r'\makecell{\textbf{General} \\ \scriptsize $M_1\!=\!10^{20}$, $R_1\!=\!2\!\times\!10^{-7}$ \\ \scriptsize $M_2\!=\!10^{30}$, $R_2\!=\!10^{7}$}',
    ]

    # LaTeX label mappings for properties
    prop_labels = {
        'm_1 (kg)': r'$M_1$ (kg)',
        'm_2 (kg)': r'$M_2$ (kg)',
        'r_1 (m)': r'$R_1$ (m)',
        'r_2 (m)': r'$R_2$ (m)',
        'ρ_1 (kg/m³)': r'$\rho_1$ (kg/m$^3$)',
        'ρ_2 (kg/m³)': r'$\rho_2$ (kg/m$^3$)',
        'I_1 (kg·m²)': r'$I_1$ (kg\,m$^2$)',
        'I_2 (kg·m²)': r'$I_2$ (kg\,m$^2$)',
        'D_1 (kg/m)': r'$D_1$ (kg/m)',
        'D_2 (kg/m)': r'$D_2$ (kg/m)',
        'D_1_norm': r'$D_{1,\text{norm}}$',
        'D_2_norm': r'$D_{2,\text{norm}}$',
        'r_s_1 (m)': r'$r_{s,1}$ (m)',
        'r_s_2 (m)': r'$r_{s,2}$ (m)',
        'gtd_1': r'GTD$_1$',
        'gtd_2': r'GTD$_2$',
        'dtd_1': r'DTD$_1$',
        'dtd_2': r'DTD$_2$',
    }

    ratio_labels = {
        'I_1/I_2': r'$I_1/I_2$',
        '(I_1/I_2)^(1/2)': r'$(I_1/I_2)^{1/2}$',
        'k_i=(ρ_1/ρ_2)^(1/5)*(r_1/r_2)': r'$k_i = (\rho_1/\rho_2)^{1/5}(R_1/R_2)$',
        '(I_1/I_2)^(1/5)': r'$(I_1/I_2)^{1/5}$',
        '(*k) D_2/D_1': r'$D_2/D_1$',
        '(*G) gtd_1/gtd_2': r'GTD$_1$/GTD$_2$',
        'dtd_1/dtd_2': r'DTD$_1$/DTD$_2$ $(\ast)$',
        '(I_1/I_2)^(1/5)*(ρ_1/ρ_2)^(3/10)': r'$(I_1/I_2)^{1/5}(\rho_1/\rho_2)^{3/10}$ $(\ast)$',
        '(*k) k_m=m_1/m_2': r'$M_1/M_2$',
        '(*k) k_r=r_1/r_2': r'$R_1/R_2$',
        'sqrt(D_1/D_2)': r'$\sqrt{D_1/D_2}$ $(\ast)$',
        'sqrt(D_1)/sqrt(D_2)': r'$\sqrt{D_1}/\sqrt{D_2}$ $(\ast)$',
        'sqrt(r_2/r_1)': r'$\sqrt{R_2/R_1}$',
        'sqrt(m_1/m_2)': r'$\sqrt{M_1/M_2}$',
        'sqrt(m_1/m_2)*sqrt(r_2/r_1)': r'$\sqrt{M_1/M_2} \cdot \sqrt{R_2/R_1}$ $(\ast)$',
        '(dtd_1/dtd_2)²*(r_1/r_2)³': r'$(\text{DTD}_1/\text{DTD}_2)^2(R_1/R_2)^3$ $(\ast)$',
        'sqrt(m_2²r_2/(m_1²r_1))': r'$\sqrt{M_2^2 R_2/(M_1^2 R_1)}$',
        'sqrt((I_1/I_2)*(r_2/r_1)³)': r'$\sqrt{(I_1/I_2)(R_2/R_1)^3}$ $(\ast)$',
        'sqrt(1-dtd_1²)/sqrt(1-dtd_2²)': r'$\sqrt{1-\text{DTD}_1^2}/\sqrt{1-\text{DTD}_2^2}$',
    }

    # Generate Table 1: System Properties
    print(r'\begin{table*}[ht]')
    print(r'\centering')
    print(r'\caption{System properties for each pair comparison case. M=M: static mass (near Schwarzschild radius). M=M*: static mass (beyond collapse). R=R: static radius. $\rho=\rho$: constant density. I=I: constant inertia. Gen/Gen2: unconstrained general cases.}')
    print(r'\label{tab:pair_properties}')
    print(r'\scriptsize')
    print(r'\begin{tabular}{@{} l ' + 'c ' * ncols + r'@{}}')
    print(r'\toprule')
    print(r'\textbf{Property} & ' + ' & '.join(col_headers) + r' \\')
    print(r'\midrule')

    for label, values in top_rows:
        latex_label = prop_labels.get(label, label)
        formatted = [fmt(v) for v in values]
        print(f'{latex_label} & ' + ' & '.join(formatted) + r' \\')

    print(r'\bottomrule')
    print(r'\end{tabular}')
    print(r'\end{table*}')
    print()

    # Generate Table 2: Derived Ratios
    print(r'\begin{table*}[ht]')
    print(r'\centering')
    print(r'\caption{Derived ratios across constraint cases. Rows marked $(\ast)$ are universally equal to DTD$_1$/DTD$_2$. The constant-density STE scale factor $(I_1/I_2)^{1/5}$ equals the DTD ratio only under constant density ($\rho = \rho$). The inertia recovery identity $(\text{DTD}_1/\text{DTD}_2)^2(R_1/R_2)^3 = I_1/I_2$ holds in every case.}')
    print(r'\label{tab:pair_ratios}')
    print(r'\scriptsize')
    print(r'\begin{tabular}{@{} l ' + 'c ' * ncols + r'@{}}')
    print(r'\toprule')
    print(r'\textbf{Ratio} & ' + ' & '.join(col_headers) + r' \\')
    print(r'\midrule')

    for label, values in bottom_rows:
        latex_label = ratio_labels.get(label, label)
        formatted = [fmt(v) for v in values]
        print(f'{latex_label} & ' + ' & '.join(formatted) + r' \\')

    print(r'\bottomrule')
    print(r'\end{tabular}')
    print(r'\end{table*}')

if __name__ == '__main__':
    main()
