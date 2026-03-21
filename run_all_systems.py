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

# Set high precision for derived calculations
getcontext().prec = 50

# Define all systems: (number, mass, radius)
SYSTEMS = [
    (1,  '1.989e30', '6.957e8'),
    (2,  '1.989e30', '2953'),
    (3,  '1e30',     '1e8'),
    (4,  '1e24',     '1e8'),
    (5,  '1e30',     '1e8'),
    (6,  '1e27',     '1e7'),
    (7,  '1e30',     '1e8'),
    (8,  '1e32',     '1e7'),
    (9,  '1e30',     '1e8'),
    (10, '1e20',     '1e7'),
]


def generate_output(output_path):
    """
    Step 1: Run each system through UniformSphere, compute derived values,
    and write everything to systems_output.md.
    """
    output_lines = ['# System Properties Output\n']

    for num, mass, radius in SYSTEMS:
        sphere = UniformSphere(radius=radius, mass=mass, name='Sphere from CLI parameters')

        # Format inputs to 6 significant figures
        m_float = float(mass)
        m_base, m_exp = f'{m_float:.5e}'.split('e')
        mass_fmt = f'{m_base}e{int(m_exp)}'
        r_float = float(radius)
        r_base, r_exp = f'{r_float:.5e}'.split('e')
        radius_fmt = f'{r_base}e{int(r_exp)}'

        output_lines.append(f'\n## System {num}')
        output_lines.append(f'Mass: {mass_fmt} kg, Radius: {radius_fmt} m')
        output_lines.append('')

        # Capture print_properties output
        f = io.StringIO()
        with redirect_stdout(f):
            sphere.print_properties()
        props_output = f.getvalue()

        output_lines.append('```')
        output_lines.append(props_output.rstrip())
        output_lines.append('```')

        # Derived calculations — output below the code block
        gtd = sphere._properties['gravitational_time_dilation']
        k = Decimal('1') - gtd * gtd

        # Format k to 6 significant figures in scientific notation
        k_float = float(k)
        if k_float == 0:
            k_formatted = '0.00000e0'
        else:
            k_base, k_exp = f'{k_float:.5e}'.split('e')
            k_formatted = f'{k_base}e{int(k_exp)}'

        output_lines.append('')
        output_lines.append(f"**Derived:** k = 1 - GTD² = {k_formatted}")
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
        gtd = re.search(r'Gravitational Time Dilation:\s+([\d.eE+\-]+(?:\s*\(dimensionless\))?)', body)
        k_match = re.search(r'k = 1 - GTD² = ([\d.eE+\-]+)', body)

        table_rows.append({
            'num': num,
            'radius': format_sci6(radius.group(1)),
            'mass': format_sci6(mass.group(1)),
            'moi': format_sci6(moi.group(1)),
            'rs': format_sci6(rs.group(1)),
            'gtd': format_gtd_from_raw(gtd.group(1)),
            'k': format_sci6(k_match.group(1)),
        })

    # Write table
    header = '| System | Radius (m) | Mass (kg) | Moment of Inertia (kg·m²) | r_s (m) | GTD | k |'
    sep = '|----------|------------|-----------|----------------------------|------------|-------------------------------|------------|'
    with open(table_path, 'w') as f:
        f.write('# System Properties Summary\n\n')
        f.write(header + '\n')
        f.write(sep + '\n')
        for row in table_rows:
            f.write(f"| System {row['num']} | {row['radius']} | {row['mass']} | {row['moi']} | {row['rs']} | {row['gtd']} | {row['k']} |\n")


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
