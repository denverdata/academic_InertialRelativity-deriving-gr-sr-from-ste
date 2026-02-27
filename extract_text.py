#!/usr/bin/env python3
"""
extract_text.py — Convert master.tex to a clean plain-text reading copy.

Produces: numbered sections, abstract, body paragraphs, bibliography.
Omits:    DOI/GitHub links, page numbers, footnotes, template markup.

Usage (run from anywhere):
    python3 extract_text.py             → writes master_plain.txt
    python3 extract_text.py --stdout    → prints to stdout
"""

import re, sys, os, textwrap

# ── paths (relative to this script, not the working directory) ────────────────
HERE      = os.path.dirname(os.path.abspath(__file__))
LATEX_DIR = os.path.join(HERE, 'latex')
TEX       = os.path.join(LATEX_DIR, 'master.tex')
BBL       = os.path.join(LATEX_DIR, 'master.bbl')
OUT       = os.path.join(HERE, 'master_plain.txt')
WIDTH     = 80   # paragraph wrap width (0 = no wrapping)


# ── text cleaning ─────────────────────────────────────────────────────────────

def clean(text):
    """Strip LaTeX markup and return readable plain text."""
    # Strip comments
    text = re.sub(r'(?<!\\)%[^\n]*', '', text)
    # Non-breaking space tilde
    text = text.replace('~', ' ')
    # Display math → placeholder
    text = re.sub(r'\$\$.*?\$\$', '[equation]', text, flags=re.DOTALL)
    # Inline math → short placeholder
    text = re.sub(r'\$[^$\n]+\$', '[eq]', text)
    # Citations / labels / refs
    text = re.sub(r'\\cite\{[^}]*\}', '', text)
    text = re.sub(r'\\label\{[^}]*\}', '', text)
    text = re.sub(r'\(\\ref\{[^}]*\}\)', '(eq.)', text)
    text = re.sub(r'\\(?:eq)?ref\{[^}]*\}', 'eq.', text)
    # Hyperlinks → keep display text only
    text = re.sub(r'\\href\{[^}]*\}\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\nolinkurl\{([^}]*)\}', r'\1', text)
    text = re.sub(r'\\url\{([^}]*)\}', r'\1', text)
    # Drop footnotes entirely
    text = re.sub(r'\\footnote(?:text)?\{[^}]*\}', '', text)
    # Unwrap formatting commands (keep their content)
    for cmd in ['textbf', 'textit', 'emph', 'textrm', 'texttt', 'textsc',
                'noindent', 'text', 'mathrm', 'mathit', 'mathbf', 'mathbb',
                'normalsize', 'large', 'Large', 'LARGE', 'small', 'tiny',
                'mbox', 'hbox']:
        text = re.sub(r'\\' + cmd + r'\{([^{}]*)\}', r'\1', text)
    # Generic \cmd{content} → content
    text = re.sub(r'\\[a-zA-Z]+\*?\{([^{}]*)\}', r'\1', text)
    # Bare commands → space
    text = re.sub(r'\\[a-zA-Z]+\*?', ' ', text)
    # Remove remaining LaTeX punctuation
    text = re.sub(r'[{}\\]', '', text)
    # Typographic normalization
    text = text.replace('---', '\u2014').replace('--', '\u2013')
    text = text.replace('``', '\u201c').replace("''", '\u201d').replace('`', '\u2018')
    # Clean up spaces before punctuation left by stripped commands
    text = re.sub(r' +([.,;:!?])', r'\1', text)
    # Collapse whitespace
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()


def wrap(text):
    if not WIDTH or not text:
        return text
    return textwrap.fill(text, WIDTH)


# ── header: title, author, abstract ──────────────────────────────────────────

def get_title(src):
    m = re.search(r'\\LARGE\{\\textbf\{([^}]+)\}\}', src)
    return clean(m.group(1)) if m else ''


def get_author(src):
    """Extract author name, stripping affiliation superscripts."""
    m = re.search(r'\\large\{(Thomas[^}]+)\}', src)
    if not m:
        return ''
    a = re.sub(r'\$[^$]*\$', '', m.group(1))       # drop superscripts
    a = re.sub(r'\\[a-zA-Z]+\{[^}]*\}', '', a)
    a = re.sub(r'\\[a-zA-Z]+', '', a)
    a = re.sub(r'[{},$^\u2020]', '', a)
    return a.strip().rstrip(',').strip()


def get_dates(src):
    """Return list of date strings from the header."""
    return [clean(m.group(1))
            for m in re.finditer(r'\\small\{((?:Originally|Revision)[^}]+)\}', src)]


def get_abstract(src):
    m = re.search(r'ABSTRACT:\s*(.*?)(?=\\end\{tabular\})', src, re.DOTALL)
    return clean(m.group(1)) if m else ''


# ── bibliography ──────────────────────────────────────────────────────────────

def get_refs(path):
    if not os.path.exists(path):
        return []
    text = open(path).read()
    # Remove the \begin/\end{thebibliography} wrapper
    text = re.sub(r'\\(?:begin|end)\{thebibliography\}\{?[^}]*\}?', '', text)
    items = re.split(r'\\bibitem\{[^}]+\}', text)[1:]
    refs = []
    for item in items:
        t = item.replace('\\newblock', ' ')
        t = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', t)
        t = re.sub(r'\\[a-zA-Z]+', ' ', t)
        t = re.sub(r'[{}~]', ' ', t)
        t = t.replace('---', '\u2014').replace('--', '\u2013')
        t = re.sub(r'\s+', ' ', t).strip()
        if t:
            refs.append(t)
    return refs


# ── body ──────────────────────────────────────────────────────────────────────

def process_body(src):
    """Parse the document body; return a list of output lines."""

    # Isolate body (everything after the title/abstract block)
    m = re.search(r'%%%END OF TITLE, AUTHORS AND ABSTRACT%%%', src)
    body = src[m.end():] if m else src

    # Strip structural noise
    body = re.sub(r'%%%[^\n]*\n', '', body)          # strip all %%%... comment lines
    body = re.sub(r'^\\footnotetext.*$', '', body, flags=re.MULTILINE)
    body = re.sub(r'\\renewcommand[^\n]+', '', body)
    body = re.sub(r'\\rmfamily|\\normalfont|\\upshape', '', body)
    body = re.sub(r'\\vspace\{[^}]*\}', '', body)
    body = re.sub(r'\\bibliography(?:style)?\{[^}]*\}', '', body)
    body = re.sub(r'\\balance|\\clearpage|\\end\{document\}', '', body)

    # Equation environments → marker line
    body = re.sub(
        r'\\begin\{equation\}.*?\\end\{equation\}',
        '\n[EQUATION]\n', body, flags=re.DOTALL)

    # Remove other environments entirely
    for env in ['align', 'eqnarray', 'figure', 'table', 'tabular', 'mdframed']:
        body = re.sub(
            r'\\begin\{' + env + r'\*?\}.*?\\end\{' + env + r'\*?\}',
            '', body, flags=re.DOTALL)

    # ── line-by-line pass ─────────────────────────────────────────────────
    sec = sub = ssub = 0
    para = []   # accumulates lines of current paragraph
    out  = []

    def flush():
        """Emit current paragraph if non-empty."""
        text = clean(' '.join(para))
        text = re.sub(r'\s+', ' ', text).strip()
        para.clear()
        if len(text) > 4:
            out.append(wrap(text))
            out.append('')

    for line in body.split('\n'):
        s = line.strip()

        # Equation placeholder
        if s == '[EQUATION]':
            flush()
            out.append('[equation]')
            out.append('')
            continue

        # \section{...}
        m = re.match(r'\\section\{([^}]+)\}(.*)', s)
        if m:
            flush()
            sec += 1; sub = 0; ssub = 0
            out += ['', f'{sec}. {clean(m.group(1)).upper()}', '']
            if m.group(2).strip():
                para.append(m.group(2).strip())
            continue

        # \subsection{...}
        m = re.match(r'\\subsection\{([^}]+)\}(.*)', s)
        if m:
            flush()
            sub += 1; ssub = 0
            out += ['', f'  {sec}.{sub} {clean(m.group(1))}', '']
            if m.group(2).strip():
                para.append(m.group(2).strip())
            continue

        # \subsubsection{...}
        m = re.match(r'\\subsubsection\{([^}]+)\}(.*)', s)
        if m:
            flush()
            ssub += 1
            out += ['', f'    {sec}.{sub}.{ssub} {clean(m.group(1))}', '']
            if m.group(2).strip():
                para.append(m.group(2).strip())
            continue

        # Skip \begin{...} / \end{...} lines
        if re.match(r'\\(begin|end)\{', s):
            continue

        # Blank line → paragraph break
        if s == '':
            flush()
            continue

        para.append(s)

    flush()
    return out


# ── main ──────────────────────────────────────────────────────────────────────

def main():
    to_stdout = '--stdout' in sys.argv
    src = open(TEX).read()
    out = []

    # Title
    title = get_title(src)
    if title:
        out += [title, '']

    # Author + dates
    author = get_author(src)
    if author:
        out.append(author)
    for d in get_dates(src):
        out.append(d)
    out.append('')

    # Abstract
    abstract = get_abstract(src)
    if abstract:
        out += ['ABSTRACT', '', wrap(abstract), '']

    # Body sections
    out += process_body(src)

    # References
    refs = get_refs(BBL)
    if refs:
        out += ['', 'REFERENCES', '']
        for i, ref in enumerate(refs, 1):
            out.append(wrap(f'[{i}]  {ref}'))
        out.append('')

    text = '\n'.join(out)

    if to_stdout:
        print(text)
    else:
        with open(OUT, 'w') as f:
            f.write(text)
        print(f'Written: {OUT}', file=sys.stderr)


if __name__ == '__main__':
    main()
