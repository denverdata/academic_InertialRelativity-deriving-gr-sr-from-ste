# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

Compile the LaTeX paper (from the `latex/` directory):
```bash
# Using latexmk (preferred, handles all passes automatically)
cd latex && latexmk -pdf master.tex

# Full build with bibliography (manual)
cd latex && pdflatex master.tex && bibtex master && pdflatex master.tex && pdflatex master.tex

# Quick compile (no bibliography update)
cd latex && pdflatex master.tex

# Clean auxiliary files
cd latex && latexmk -c
```

Python utilities (run from repo root):
```bash
# Generate appendix table (outputs latex/system_table.tex)
cd latex && python3 generate_table.py

# Generate STE isometric scaling diagram (outputs latex/ste_example.pdf)
cd latex && python3 ste_example_diagram.py

# Run all 11 system calculations (outputs systems_output.md, systems_table.md)
python3 run_all_systems.py

# Extract plain-text reading copy from LaTeX (outputs master_plain.txt)
python3 extract_text.py
```

## Repository Structure

| Path | Purpose |
|------|---------|
| `latex/master.tex` | Primary deliverable — the academic preprint paper (RSC journal template) |
| `latex/rsc.bib` | BibTeX bibliography (all citations live here) |
| `latex/rsc.bst` | RSC bibliography style file — do not modify |
| `latex/master_template.tex` | Original unmodified RSC template — do not use as content source |
| `latex/master_backup.tex` | Backup of prior revision |
| `latex/generate_table.py` | Generates `system_table.tex` appendix table from example systems |
| `latex/ste_example_diagram.py` | Generates `ste_example.pdf` isometric scaling diagram |
| `referenced_docs/derivation_lean_v3.txt` | Canonical content source for the derivation — serves as literal content source for the paper |
| `referenced_docs/*.pdf` | Author's prior published works (source for page numbers in bib) |
| `project/project_theoretical_foundation.md` | Author's stated objectives, core formulas, and final document requirements |
| `system_properties/` | Python package: `UniformSphere`, `UniformDisc`, physical constants, high-precision Decimal arithmetic |
| `run_all_systems.py` | Calculates properties of 11 physical systems using `system_properties` |
| `extract_text.py` | Converts `master.tex` to plain-text reading copy |
| `supporting_materials/` | Background notes and prior thinking (not primary sources) |
| `output/` | Draft outputs and intermediate documents |

## Paper Structure (master.tex)

Sections in order: Introduction → Inertial Relativity → The Space-Time Equivalence (STE) → General and Special Relativity → Expressions of Relative Inertial Linear Scale → Unification of GR and SR → Analysis and Conclusion → Special-Case Derivations (appendix, 9+ cases)

The LaTeX template structure (two-column RSC journal format) must not be altered. All page setup, header/footer, and font commands in the preamble are locked per template instructions embedded in comments.

## Core Physics (from `project/project_theoretical_foundation.md`)

The paper's central claim is **Inertial Relativity**: that GR and SR are edge cases of the Space-Time Equivalence (STE):

$$\frac{T_1}{T_2} = \left(\frac{I_2}{I_1}\right)^{1/5} \quad \text{[rotational --- moment of inertia]}$$

$$\frac{T_1}{T_2} = \left(\frac{M_2}{M_1}\right)^{1/3} \quad \text{[linear --- mass only]}$$

Key prior works cited in `latex/rsc.bib`:
- `degerlia2025` — "Introducing Inertial Density" (Schwarzschild threshold as M/R constant)
- `degerlia2025universe` — "The Universe of Light" (STE origin)

## Python Computation

`system_properties/` provides high-precision (100 decimal places) physics calculations via `UniformSphere` and `UniformDisc` classes. Constants in `constants.py` (G, c, π) are defined to high precision. `run_all_systems.py` instantiates 11 systems and computes: moment of inertia, Schwarzschild radius, gravitational time dilation, k factor, and inter-system ratios. Output feeds into the paper's appendix tables via `generate_table.py`.
