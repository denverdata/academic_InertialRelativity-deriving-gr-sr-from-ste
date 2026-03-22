#!/usr/bin/env python3
"""
Run all systems through UniformSphere and output to systems_output.md,
then build systems_table.md by parsing systems_output.md.
"""

import sys
import os
import re
import io
from decimal import Decimal, getcontext
from contextlib import redirect_stdout

# Add system_properties to import path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'system_properties'))

from uniform_sphere import UniformSphere
import constants

# Override precision after import (constants.py sets it to 50)
getcontext().prec = 100

# Define all systems: (number, mass, radius)
SYSTEMS = [
    (1,  '1.98892e30', '6.95700e8'),
    (2,  '1.98892e30', 'r_s'),
    (3,  '1e30',     '1e8'),
    (4,  '1e24',     '1e8'),
    (5,  '1e30',     '1e8'),
    (6,  '1e27',     '1e7'),
    (7,  '1e30',     '1e8'),
    (8,  '1e32',     '1e7'),
    (9,  '1e30',     '1e8'),
    (10, '1e20',     '1e7'),
    (11, '1e32',     '1e6'),
]


def generate_output(output_path):
    """
    Step 1: Run each system through UniformSphere, compute derived values,
    and write everything to systems_output.md.
    """
    # First pass: run all systems, collect data
    system_data = []
    G = constants.G
    c = constants.SPEED_OF_LIGHT
    for num, mass, radius in SYSTEMS:
        # If radius is 'r_s', compute Schwarzschild radius from mass
        if radius == 'r_s':
            m_dec = Decimal(mass)
            rs_dec = Decimal('2') * G * m_dec / (c * c)
            radius = str(rs_dec)
        sphere = UniformSphere(radius=radius, mass=mass, name='Sphere from CLI parameters')

        # Capture print_properties output
        f = io.StringIO()
        with redirect_stdout(f):
            sphere.print_properties()
        props_output = f.getvalue()

        # Recompute GTD at 100-digit precision for k calculation
        r = Decimal(radius)
        m = Decimal(mass)
        td_term = Decimal('2') * G * m / (r * c * c)
        td_factor = Decimal('1') - td_term
        if td_factor > Decimal('0'):
            gtd_hp = td_factor.sqrt()
        else:
            gtd_hp = Decimal('0')
        k = Decimal('1') - gtd_hp * gtd_hp

        p = sphere._properties
        system_data.append({
            'num': num,
            'mass': mass,
            'radius': radius,
            'props_output': props_output,
            'gtd_hp': gtd_hp,
            'k': k,
            'radius_raw': float(radius),
            'mass_raw': float(mass),
            'moi_raw': float(p['moment_of_inertia']),
            'rs_raw': float(p['schwarzschild_radius']),
        })

    # Second pass: compute ratios and write output
    output_lines = ['# System Properties Output\n']

    for idx, sd in enumerate(system_data):
        prev_idx = (idx - 1) % len(system_data)
        prev = system_data[prev_idx]

        r_ratio = sd['radius_raw'] / prev['radius_raw']
        m_ratio = sd['mass_raw'] / prev['mass_raw']
        i_ratio = sd['moi_raw'] / prev['moi_raw']
        m_ratio_cbrt = m_ratio ** (1.0/3.0)
        i_ratio_5rt = i_ratio ** (1.0/5.0)
        rs_over_r = sd['rs_raw'] / sd['radius_raw']

        # Format inputs to 6 significant figures
        m_float = float(sd['mass'])
        m_base, m_exp = f'{m_float:.5e}'.split('e')
        mass_fmt = f'{m_base}e{int(m_exp)}'
        r_float = float(sd['radius'])
        r_base, r_exp = f'{r_float:.5e}'.split('e')
        radius_fmt = f'{r_base}e{int(r_exp)}'

        output_lines.append(f'\n## System {sd["num"]}')
        output_lines.append(f'Mass: {mass_fmt} kg, Radius: {radius_fmt} m')
        output_lines.append('')

        output_lines.append('```')
        output_lines.append(sd['props_output'].rstrip())
        output_lines.append('```')

        output_lines.append('')
        output_lines.append(f"**Derived:** GTD (100-digit) = {sd['gtd_hp']:.50e}")
        output_lines.append(f"**Derived:** k = 1 - GTD² = {sd['k']:.50e}")
        output_lines.append(f"**Derived:** R/R_prev = {format_sci6(str(r_ratio))}")
        output_lines.append(f"**Derived:** M/M_prev = {format_sci6(str(m_ratio))}")
        output_lines.append(f"**Derived:** I/I_prev = {format_sci6(str(i_ratio))}")
        output_lines.append(f"**Derived:** (M/M_prev)^(1/3) = {format_sci6(str(m_ratio_cbrt))}")
        output_lines.append(f"**Derived:** (I/I_prev)^(1/5) = {format_sci6(str(i_ratio_5rt))}")
        output_lines.append(f"**Derived:** r_s/R = {format_sci6(str(rs_over_r))}")
        output_lines.append('')

    with open(output_path, 'w') as f:
        f.write('\n'.join(output_lines))


def format_gtd_from_raw(raw_gtd_str):
    """
    Format a raw GTD string (from systems_output.md) showing all trailing 9s
    plus six digits past the last 9, in scientific notation, with rounding.
    """
    # Parse the raw value — strip the "(dimensionless)" suffix
    val_str = raw_gtd_str.split()[0]
    gtd = Decimal(val_str)

    if gtd == Decimal('0'):
        return '0.00000e0'

    # Mantissa = gtd * 10, so we work in X.XXXe-1 form
    mantissa = gtd * 10
    mantissa_str = format(mantissa, '.45f')
    _, dec_part = mantissa_str.split('.')

    # Count leading 9s in the decimal part
    nine_count = 0
    for ch in dec_part:
        if ch == '9':
            nine_count += 1
        else:
            break

    # Extract seven digits past the last 9 (six to keep + one for rounding)
    remaining_start = nine_count
    seven_digits = dec_part[remaining_start:remaining_start + 7]

    # Round: if 7th digit >= 5, round up the 6th
    digits = list(seven_digits[:6])
    if len(seven_digits) >= 7 and int(seven_digits[6]) >= 5:
        carry = 1
        for i in range(5, -1, -1):
            d = int(digits[i]) + carry
            if d >= 10:
                digits[i] = '0'
                carry = 1
            else:
                digits[i] = str(d)
                carry = 0
                break
        if carry:
            nine_count += 1
            digits = ['0'] * 6

    six_digits = ''.join(digits)
    nines = '9' * nine_count
    return f"9.{nines}{six_digits}e-1"


def format_sci6(val_str):
    """Format a numeric string to scientific notation with 6 significant figures."""
    f = float(val_str)
    if f == 0:
        return '0.00000e0'
    s = f'{f:.5e}'
    base, exp = s.split('e')
    exp_val = int(exp)
    return f'{base}e{exp_val}'


def build_table(output_path, table_path):
    """
    Step 2: Parse systems_output.md and build systems_table.md.
    All values come from the output sheet.
    """
    with open(output_path, 'r') as f:
        content = f.read()

    # Split into system sections
    sections = re.split(r'\n## System (\d+)\n', content)
    # sections[0] is header, then alternating: number, body

    table_rows = []
    for i in range(1, len(sections), 2):
        num = sections[i]
        body = sections[i + 1]

        # Parse fields from the code block
        radius = re.search(r'Radius:\s+([\d.eE+\-]+)\s+m', body)
        mass = re.search(r'Mass:\s+([\d.eE+\-]+)\s+kg', body)
        moi = re.search(r'Moment Of Inertia:\s+([\d.eE+\-]+)\s+kg', body)
        rs = re.search(r'Schwarzschild Radius:\s+([\d.eE+\-]+)\s+m', body)
        # Read GTD from the derived high-precision line, not the code block
        gtd = re.search(r'GTD \(100-digit\) = ([\d.eE+\-]+)', body)
        k_match = re.search(r'k = 1 - GTD² = ([\d.eE+\-]+)', body)

        r_ratio = re.search(r'R/R_prev = ([\d.eE+\-]+)', body)
        m_ratio = re.search(r'M/M_prev = ([\d.eE+\-]+)', body)
        i_ratio = re.search(r'I/I_prev = ([\d.eE+\-]+)', body)
        m_cbrt = re.search(r'\(M/M_prev\)\^\(1/3\) = ([\d.eE+\-]+)', body)
        i_5rt = re.search(r'\(I/I_prev\)\^\(1/5\) = ([\d.eE+\-]+)', body)
        rs_over_r = re.search(r'r_s/R = ([\d.eE+\-]+)', body)

        table_rows.append({
            'num': num,
            'radius': format_sci6(radius.group(1)),
            'mass': format_sci6(mass.group(1)),
            'moi': format_sci6(moi.group(1)),
            'rs': format_sci6(rs.group(1)),
            'gtd': format_gtd_from_raw(gtd.group(1)),
            'k': format_sci6(k_match.group(1)),
            'r_ratio': r_ratio.group(1),
            'm_ratio': m_ratio.group(1),
            'i_ratio': i_ratio.group(1),
            'm_cbrt': m_cbrt.group(1),
            'i_5rt': i_5rt.group(1),
            'rs_over_r': rs_over_r.group(1),
        })

    # Write table
    header = '| System | Radius (m) | Mass (kg) | Moment of Inertia (kg·m²) | r_s (m) | r_s/R | GTD | k | R/R_prev | M/M_prev | (M/M)^1/3 | I/I_prev | (I/I)^1/5 |'
    sep = '|----------|------------|-----------|----------------------------|------------|----------|-------------------------------|------------|----------|----------|-----------|----------|-----------|'
    with open(table_path, 'w') as f:
        f.write('# System Properties Summary\n\n')
        f.write(header + '\n')
        f.write(sep + '\n')
        for row in table_rows:
            f.write(f"| System {row['num']} | {row['radius']} | {row['mass']} | {row['moi']} | {row['rs']} | {row['rs_over_r']} | {row['gtd']} | {row['k']} | {row['r_ratio']} | {row['m_ratio']} | {row['m_cbrt']} | {row['i_ratio']} | {row['i_5rt']} |\n")


def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(project_root, 'systems_output.md')
    table_path = os.path.join(project_root, 'systems_table.md')

    # Step 1: Generate systems_output.md
    generate_output(output_path)
    print(f'Wrote {output_path}')

    # Step 2: Parse systems_output.md → systems_table.md
    build_table(output_path, table_path)
    print(f'Wrote {table_path}')


if __name__ == '__main__':
    main()
