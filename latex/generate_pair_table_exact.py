#!/usr/bin/env python3
"""Generate LaTeX pair comparison tables with exact values from the spreadsheet.
10 significant digits, consistent scientific notation, original row labels."""

import re
from decimal import Decimal, getcontext
getcontext().prec = 50

def parse_md_table(filepath):
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

def fmt10(val_str):
    """Format to 10 significant digits in consistent scientific notation.
    ALWAYS shows X.XXXXXXXXX x 10^Y format, even for exponent 0."""
    val_str = val_str.strip()
    if val_str == '---' or val_str == '':
        return '---'

    # Parse the E-notation directly to avoid float precision loss
    m = re.match(r'^([+-]?)(\d+)\.?(\d*)[Ee]([+-]?\d+)$', val_str)
    if not m:
        # Try as plain number
        try:
            d = Decimal(val_str)
            if d == 0:
                return '$0$'
        except:
            return val_str
        # Convert to E notation and re-parse
        val_str = f'{d:E}'
        m = re.match(r'^([+-]?)(\d+)\.?(\d*)[Ee]([+-]?\d+)$', val_str)
        if not m:
            return val_str

    sign = m.group(1) if m.group(1) == '-' else ''
    int_part = m.group(2)
    frac_part = m.group(3)
    exp = int(m.group(4))

    # All digits of the mantissa
    all_digits = int_part + frac_part

    # Remove leading zeros (shouldn't happen for E notation but be safe)
    # The E notation should already have the form D.DDDDExx where D is 1-9

    # Take first 10 digits
    if len(all_digits) >= 10:
        digits10 = all_digits[:10]
    else:
        digits10 = all_digits + '0' * (10 - len(all_digits))

    # Format as X.XXXXXXXXX
    mstr = digits10[0] + '.' + digits10[1:]

    return f'${sign}{mstr} \\times 10^{{{exp}}}$'

def main():
    rows = parse_md_table('../pair_comparisons_v2_cases.md')

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

    # Keep columns: 0=M=M, 2=R=R, 3=P=P, 4=I=I, 5=General
    keep = [0, 2, 3, 4, 5]
    top_rows = [(label, [values[i] for i in keep]) for label, values in top_rows]
    bottom_rows = [(label, [values[i] for i in keep]) for label, values in bottom_rows]

    col_names = [r'Case 1 ($M\!=\!M$)', r'Case 2 ($R\!=\!R$)', r'Case 3 ($\rho\!=\!\rho$)', r'Case 4 ($I\!=\!I$)', 'General']

    # Use original spreadsheet labels, rendered in LaTeX
    prop_labels = {
        'm_1 (kg)':       r'$m_1$ (kg)',
        'm_2 (kg)':       r'$m_2$ (kg)',
        'r_1 (m)':        r'$r_1$ (m)',
        'r_2 (m)':        r'$r_2$ (m)',
        'ρ_1 (kg/m³)':    r'$\rho_1$ (kg/m$^3$)',
        'ρ_2 (kg/m³)':    r'$\rho_2$ (kg/m$^3$)',
        'I_1 (kg·m²)':    r'$I_1$ (kg$\cdot$m$^2$)',
        'I_2 (kg·m²)':    r'$I_2$ (kg$\cdot$m$^2$)',
        'D_1 (kg/m)':     r'$D_1$ (kg/m)',
        'D_2 (kg/m)':     r'$D_2$ (kg/m)',
        'D_1_norm':        r'$D_{1\_norm}$',
        'D_2_norm':        r'$D_{2\_norm}$',
        'r_s_1 (m)':      r'$r_{s\_1}$ (m)',
        'r_s_2 (m)':      r'$r_{s\_2}$ (m)',
        'gtd_1':           r'$gtd_1$',
        'gtd_2':           r'$gtd_2$',
        'dtd_1':           r'$dtd_1$',
        'dtd_2':           r'$dtd_2$',
    }

    ratio_labels = {
        'I_1/I_2':                              r'$I_1/I_2$',
        '(I_1/I_2)^(1/2)':                     r'$(I_1/I_2)^{(1/2)}$',
        'k_i=(ρ_1/ρ_2)^(1/5)*(r_1/r_2)':       r'$(\rho_1/\rho_2)^{(1/5)}\!\cdot\!(r_1/r_2)$',
        '(I_1/I_2)^(1/5)':                     r'$(I_1/I_2)^{(1/5)}$',
        '(*k) D_2/D_1':                         r'(*k) $D_2/D_1$',
        '(*G) gtd_1/gtd_2':                     r'(*G) $gtd_1/gtd_2$',
        'dtd_1/dtd_2':                           r'$dtd_1/dtd_2$',
        '(I_1/I_2)^(1/5)*(ρ_1/ρ_2)^(3/10)':    r'$(I_1/I_2)^{(1/5)}\!\cdot\!(\rho_1/\rho_2)^{(3/10)}$',
        '(*k) k_m=m_1/m_2':                     r'(*k) $k_m\!=\!m_1/m_2$',
        '(*k) k_r=r_1/r_2':                     r'(*k) $k_r\!=\!r_1/r_2$',
        'sqrt(D_1/D_2)':                         r'$\sqrt{D_1/D_2}$',
        'sqrt(D_1)/sqrt(D_2)':                   r'$\sqrt{D_1}/\sqrt{D_2}$',
        'sqrt(r_2/r_1)':                         r'$\sqrt{r_2/r_1}$',
        'sqrt(m_1/m_2)':                         r'$\sqrt{m_1/m_2}$',
        'sqrt(m_1/m_2)*sqrt(r_2/r_1)':           r'$\sqrt{m_1/m_2}\!\cdot\!\sqrt{r_2/r_1}$',
        '(dtd_1/dtd_2)²*(r_1/r_2)³':            r'$(dtd_1/dtd_2)^2\!\cdot\!(r_1/r_2)^3$',
        'sqrt(m_2²r_2/(m_1²r_1))':              r'$\sqrt{m_2^2 r_2/(m_1^2 r_1)}$',
        'sqrt((I_1/I_2)*(r_2/r_1)³)':           r'$\sqrt{(I_1/I_2)\!\cdot\!(r_2/r_1)^3}$',
        'sqrt(1-dtd_1²)/sqrt(1-dtd_2²)':        r'$\sqrt{1\!-\!dtd_1^2}/\sqrt{1\!-\!dtd_2^2}$',
    }

    # Table 1: System Properties
    print(r'\begin{table*}[ht]')
    print(r'\centering')
    print(r'\caption{System properties for each pair comparison case.}')
    print(r'\label{tab:pair_properties}')
    print(r'\normalsize')
    print(r'\begin{tabular}{@{} l l l l l l @{}}')
    print(r'\toprule')
    print(r' & ' + ' & '.join([r'\textbf{' + n + '}' for n in col_names]) + r' \\')
    print(r'\midrule')
    for label, values in top_rows:
        latex_label = prop_labels.get(label, label)
        formatted = [r'{\ttfamily ' + fmt10(v) + '}' for v in values]
        print(f'{latex_label} & ' + ' & '.join(formatted) + r' \\')
    print(r'\bottomrule')
    print(r'\end{tabular}')
    print(r'\end{table*}')
    print()

    # Table 2: Derived Ratios — reordered by value groups
    # Index mapping from original spreadsheet order:
    # 0:I_1/I_2  1:(I_1/I_2)^(1/2)  2:k_i  3:(I_1/I_2)^(1/5)
    # 4:D_2/D_1  5:gtd_1/gtd_2  6:dtd_1/dtd_2  7:(I_1/I_2)^(1/5)*(rho)^(3/10)
    # 8:k_m  9:k_r  10:sqrt(D_1/D_2)  11:sqrt(D_1)/sqrt(D_2)
    # 12:sqrt(r_2/r_1)  13:sqrt(m_1/m_2)  14:sqrt(m_1/m_2)*sqrt(r_2/r_1)
    # 15:(dtd/dtd)^2*(r/r)^3  16:sqrt(m2^2*r2/(m1^2*r1))  17:sqrt((I/I)*(r/r)^3)
    # 18:sqrt(1-dtd^2)/sqrt(1-dtd^2)

    # Paired groups by matching Case 1 values
    pairs = [
        [8, 13],    # k_m and sqrt(m_1/m_2)              = 1.000E+0
        [0, 15],    # I_1/I_2 and (dtd/dtd)^2*(r/r)^3  = 1.837E-11
        [2, 3],     # k_i and (I_1/I_2)^(1/5)           = 7.125E-3
        [5, 18],    # gtd_1/gtd_2 and sqrt(1-dtd^2)/...  = 9.922E-2
    ]
    k_idx = [1, 4, 9]
    dtd_idx = [6, 7, 10, 11, 12, 14, 16, 17]

    print(r'\begin{table*}[ht]')
    print(r'\centering')
    print(r'\caption{Derived ratios across constraint cases.}')
    print(r'\label{tab:pair_ratios}')
    print(r'\normalsize')
    print(r'\begin{tabular}{@{} l l l l l l @{}}')
    print(r'\toprule')
    print(r' & ' + ' & '.join([r'\textbf{' + n + '}' for n in col_names]) + r' \\')
    print(r'\midrule')

    def print_row(i):
        label, values = bottom_rows[i]
        latex_label = ratio_labels.get(label, label)
        formatted = [r'{\ttfamily ' + fmt10(v) + '}' for v in values]
        print(f'{latex_label} & ' + ' & '.join(formatted) + r' \\')

    # Section 1: Paired rows (top)
    for pi, pair in enumerate(pairs):
        for i in pair:
            print_row(i)
        if pi < len(pairs) - 1:
            print(r'[3pt]\hline\\[-6pt]')

    print(r'[3pt]\hline\\[-6pt]')

    # Section 2: k group (= 4.286E-6 in Case 1)
    for i in k_idx:
        print_row(i)

    print(r'[3pt]\hline\\[-6pt]')

    # Section 3: DTD group (= 4.830E+2 in Case 1)
    for i in dtd_idx:
        print_row(i)

    print(r'\bottomrule')
    print(r'\end{tabular}')
    print(r'\end{table*}')

if __name__ == '__main__':
    main()
