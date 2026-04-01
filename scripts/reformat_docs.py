#!/usr/bin/env python3
"""
Reformat all markdown docs: convert pipe tables to HTML tables
and apply other formatting improvements.
"""

import os
import re
import sys


def split_table_row(line):
    """Split a markdown table row into cells, handling escaped pipes."""
    # Remove leading/trailing pipes and whitespace
    line = line.strip()
    if line.startswith('|'):
        line = line[1:]
    if line.endswith('|'):
        line = line[:-1]

    # Split on unescaped pipes
    cells = []
    current = ''
    i = 0
    while i < len(line):
        if line[i] == '\\' and i + 1 < len(line) and line[i + 1] == '|':
            current += '|'
            i += 2
        elif line[i] == '|':
            cells.append(current.strip())
            current = ''
            i += 1
        else:
            current += line[i]
            i += 1
    cells.append(current.strip())
    return cells


def is_separator_row(line):
    """Check if a line is a markdown table separator row like |---|---|."""
    line = line.strip()
    if not line.startswith('|') or not line.endswith('|'):
        return False
    # Remove outer pipes
    inner = line[1:-1]
    # Each cell should be dashes with optional colons for alignment
    cells = inner.split('|')
    for cell in cells:
        cell = cell.strip()
        if not re.match(r'^:?-+:?$', cell):
            return False
    return True


def is_table_row(line):
    """Check if a line looks like a markdown table row."""
    line = line.strip()
    if not line:
        return False
    if not line.startswith('|'):
        return False
    # Count unescaped pipes
    pipe_count = 0
    i = 0
    while i < len(line):
        if line[i] == '\\' and i + 1 < len(line) and line[i + 1] == '|':
            i += 2
        elif line[i] == '|':
            pipe_count += 1
            i += 1
        else:
            i += 1
    return pipe_count >= 2


def convert_table_to_html(header_line, separator_line, data_lines):
    """Convert a markdown table to HTML table."""
    headers = split_table_row(header_line)

    html_lines = ['<table>']
    html_lines.append('  <thead>')
    html_lines.append('    <tr>')
    for h in headers:
        html_lines.append(f'      <th>{h}</th>')
    html_lines.append('    </tr>')
    html_lines.append('  </thead>')
    html_lines.append('  <tbody>')

    for data_line in data_lines:
        cells = split_table_row(data_line)
        # Pad cells to match header count
        while len(cells) < len(headers):
            cells.append('')
        html_lines.append('    <tr>')
        for cell in cells[:len(headers)]:
            html_lines.append(f'      <td>{cell}</td>')
        html_lines.append('    </tr>')

    html_lines.append('  </tbody>')
    html_lines.append('</table>')

    return '\n'.join(html_lines)


def process_content(content):
    """Process markdown content: convert tables and improve formatting."""
    lines = content.split('\n')
    result = []
    i = 0
    in_code_block = False
    in_frontmatter = False
    frontmatter_count = 0

    while i < len(lines):
        line = lines[i]

        # Track frontmatter (YAML between --- at start of file)
        if i == 0 and line.strip() == '---':
            in_frontmatter = True
            result.append(line)
            i += 1
            continue
        if in_frontmatter:
            result.append(line)
            if line.strip() == '---':
                in_frontmatter = False
            i += 1
            continue

        # Track code blocks (``` or {% code %})
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            result.append(line)
            i += 1
            continue

        if in_code_block:
            result.append(line)
            i += 1
            continue

        # Detect markdown table: header row + separator row
        if (is_table_row(line) and
            i + 1 < len(lines) and
            is_separator_row(lines[i + 1])):

            header_line = line
            separator_line = lines[i + 1]
            data_lines = []
            j = i + 2

            while j < len(lines) and is_table_row(lines[j]):
                data_lines.append(lines[j])
                j += 1

            html_table = convert_table_to_html(header_line, separator_line, data_lines)
            result.append(html_table)
            i = j
            continue

        result.append(line)
        i += 1

    output = '\n'.join(result)

    # Formatting improvements: ensure blank line before headings
    # (but not if already there or at start of file or after frontmatter)
    output = re.sub(r'([^\n])\n(#{1,6} )', r'\1\n\n\2', output)

    # Ensure blank line after headings
    output = re.sub(r'(#{1,6} [^\n]+)\n([^\n#])', r'\1\n\n\2', output)

    # Remove triple+ blank lines, keep at most double
    output = re.sub(r'\n{4,}', '\n\n\n', output)

    return output


def process_file(filepath):
    """Process a single markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip files with no markdown tables
    if '|' not in content:
        return False

    new_content = process_content(content)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False


def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    modified_count = 0
    total_count = 0

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip hidden directories
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]

        for filename in filenames:
            if not filename.endswith('.md'):
                continue

            filepath = os.path.join(dirpath, filename)
            total_count += 1

            try:
                if process_file(filepath):
                    modified_count += 1
                    print(f"  Converted: {os.path.relpath(filepath, root_dir)}")
            except Exception as e:
                print(f"  ERROR: {os.path.relpath(filepath, root_dir)}: {e}")

    print(f"\nDone. Modified {modified_count} of {total_count} markdown files.")


if __name__ == '__main__':
    main()
