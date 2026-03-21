#!/usr/bin/env python3
"""
Run all systems through UniformSphere and output results to systems_output.md
and a summary table to systems_table.md.
"""

import sys
import os
from decimal import Decimal, getcontext

# Add system_properties to import path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'system_properties'))

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
    in scientific notation (mantissa x e-1), with proper rounding.
    """
    if gtd == Decimal('0'):
        return '0.00000e0'

    # Mantissa = gtd * 10, so we work in X.XXXe-1 form
    mantissa = gtd * 10

    # Get full decimal string representation
    mantissa_str = format(mantissa, '.45f')
    int_part, dec_part = mantissa_str.split('.')

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
        # Carry-propagate rounding
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
            # Rolled over into the 9s — add one more 9
            nine_count += 1
            digits = ['0'] * 6

    six_digits = ''.join(digits)
    nines = '9' * nine_count
    return f"9.{nines}{six_digits}e-1"


def format_sci6(value):
    """Format a Decimal in scientific notation with 6 significant figures, properly rounded."""
    if value == Decimal('0'):
        return '0.00000e0'
    # Use Decimal's own quantize for proper rounding at full precision,
    # then format via float (6 sig figs is well within float's 15-digit range)
    f = float(value)
    s = f'{f:.5e}'
    base, exp = s.split('e')
    exp_val = int(exp)
    return f'{base}e{exp_val}'


def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
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
