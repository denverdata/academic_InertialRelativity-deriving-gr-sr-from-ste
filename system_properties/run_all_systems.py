#!/usr/bin/env python3
"""
Run all systems through UniformSphere and output results to systems_output.md
and a summary table to systems_table.md.
"""

import sys
import os
from decimal import Decimal, getcontext

# Ensure we can import from this directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from uniform_sphere import UniformSphere

# Set high precision for k calculation
getcontext().prec = 50

# Define all systems: (number, mass, radius, description)
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

def format_gtd(gtd):
    """
    Format GTD showing all trailing 9s plus six digits past the last 9
    in scientific notation (mantissa x e-1).
    """
    if gtd == Decimal('0'):
        return '0.00000e0'

    # Work with the full decimal string
    # GTD is always < 1 and >= 0, so in sci notation it's X.XXXe-1
    # where mantissa = gtd * 10
    mantissa = gtd * 10

    # Convert to string with enough precision
    mantissa_str = format(mantissa, '.40f')  # plenty of digits

    # Parse: integer part is always '9', find run of 9s after decimal
    # mantissa_str looks like "9.99999..."
    if '.' not in mantissa_str:
        return f"{float(gtd):.5e}"

    int_part, dec_part = mantissa_str.split('.')

    # Count leading 9s in the decimal part
    nine_count = 0
    for ch in dec_part:
        if ch == '9':
            nine_count += 1
        else:
            break

    # Take six digits after the last 9
    remaining_start = nine_count
    six_digits = dec_part[remaining_start:remaining_start + 6]

    # Build the formatted mantissa
    nines = '9' * nine_count
    formatted = f"9.{nines}{six_digits}e-1"

    return formatted


def format_k(gtd):
    """Calculate k = 1 - GTD^2."""
    k = Decimal('1') - gtd * gtd
    return k


def format_sci6(value):
    """Format a Decimal in scientific notation with 6 significant figures."""
    f = float(value)
    if f == 0:
        return '0.00000e0'
    s = f'{f:.5e}'
    # Clean up exponent formatting
    base, exp = s.split('e')
    exp_val = int(exp)
    return f'{base}e{exp_val}'


def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(project_root, 'systems_output.md')
    table_path = os.path.join(project_root, 'systems_table.md')

    output_lines = ['# System Properties Output\n']
    table_rows = []

    for num, mass, radius in SYSTEMS:
        sphere = UniformSphere(radius=radius, mass=mass, name='Sphere from CLI parameters')

        # Build header
        output_lines.append(f'\n## System {num}')
        output_lines.append(f'Mass: {mass} kg, Radius: {radius} m')
        output_lines.append('')

        # Capture print_properties output
        import io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            sphere.print_properties()
        props_output = f.getvalue()

        # Calculate derived values
        p = sphere._properties
        gtd = p['gravitational_time_dilation']
        k = Decimal('1') - gtd * gtd

        # Append k to properties output
        output_lines.append('```')
        output_lines.append(props_output.rstrip())
        output_lines.append('```')
        output_lines.append('')
        output_lines.append(f"**Derived:** k = 1 - GTD² = {k:.50e}")
        output_lines.append('')

        # Extract values for table
        r = Decimal(radius)
        m = Decimal(mass)
        moi = p['moment_of_inertia']
        rs = p['schwarzschild_radius']

        table_rows.append({
            'num': num,
            'radius': format_sci6(r),
            'mass': format_sci6(m),
            'moi': format_sci6(moi),
            'rs': format_sci6(rs),
            'gtd': format_gtd(gtd),
            'k': format_sci6(k),
        })

    # Write systems_output.md
    with open(output_path, 'w') as f:
        f.write('\n'.join(output_lines))

    # Write systems_table.md
    header = '| System | Radius (m) | Mass (kg) | Moment of Inertia (kg·m²) | r_s (m) | GTD | k |'
    sep = '|----------|------------|-----------|----------------------------|------------|-------------------------------|------------|'
    with open(table_path, 'w') as f:
        f.write('# System Properties Summary\n\n')
        f.write(header + '\n')
        f.write(sep + '\n')
        for row in table_rows:
            f.write(f"| System {row['num']} | {row['radius']} | {row['mass']} | {row['moi']} | {row['rs']} | {row['gtd']} | {row['k']} |\n")

    print(f'Wrote {output_path}')
    print(f'Wrote {table_path}')


if __name__ == '__main__':
    main()
