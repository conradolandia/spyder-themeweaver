#!/usr/bin/env python3
"""
Script to replace id attribute values with inkscape:label values in SVG files.
This keeps both attributes but uses the inkscape:label value as the new id value.
This version preserves the original formatting of the SVG file.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path


def label2id(svg_file_path, output_path=None, backup=True, optimize=False):
    """
    Replace id attribute values with inkscape:label values in an SVG file.
    This version preserves the original formatting.

    Args:
        svg_file_path (str): Path to the input SVG file
        output_path (str, optional): Path for the output file. If None, overwrites input.
        backup (bool): Whether to create a backup of the original file
        optimize (bool): Whether to optimize the output with svgo --pretty
    """
    svg_path = Path(svg_file_path)

    if not svg_path.exists():
        print(f"Error: File {svg_file_path} does not exist")
        return False

    # Create backup if requested
    if backup and output_path is None:
        backup_path = svg_path.with_suffix(svg_path.suffix + ".backup")
        print(f"Creating backup: {backup_path}")
        svg_path.rename(backup_path)
        svg_path = backup_path

    # Read the original file
    try:
        with open(svg_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return False

    # Pattern to find elements with both id and inkscape:label attributes
    # This pattern looks for: <tag ... id="something" ... inkscape:label="something" ...>
    pattern = (
        r'<([^>\s]+)([^>]*?)\s+id="([^"]*)"([^>]*?)\s+inkscape:label="([^"]*)"([^>]*?)>'
    )

    def replace_match(match):
        tag = match.group(1)
        before_id = match.group(2)
        between_attrs = match.group(4)
        inkscape_label = match.group(5)
        after_label = match.group(6)

        # Convert inkscape:label to valid id (replace spaces and special chars)
        new_id = re.sub(r"[^a-zA-Z0-9_-]", "_", inkscape_label)

        # Ensure id starts with letter or underscore
        if new_id and not re.match(r"^[a-zA-Z_]", new_id):
            new_id = "_" + new_id

        return f'<{tag}{before_id} id="{new_id}"{between_attrs} inkscape:label="{inkscape_label}"{after_label}>'

    # Apply the replacement
    new_content = re.sub(pattern, replace_match, content)

    # Count replacements
    matches = re.findall(pattern, content)
    replacement_count = len(matches)

    # Determine output path
    if output_path is None:
        output_path = svg_path

    # Write the modified content
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(new_content)
    except Exception as e:
        print(f"Error writing file: {e}")
        return False

    # Optimize with svgo if requested
    if optimize:
        try:
            print("Optimizing SVG with svgo...")
            subprocess.run(
                ["svgo", "--pretty", str(output_path)],
                capture_output=True,
                text=True,
                check=True,
            )
            print("SVG optimized successfully")
        except subprocess.CalledProcessError as e:
            print(f"Warning: svgo optimization failed: {e}")
            print(f"svgo stderr: {e.stderr}")
        except FileNotFoundError:
            print("Warning: svgo not found. Install it with: npm install -g svgo")
        except Exception as e:
            print(f"Warning: Error running svgo: {e}")

    print(f"Successfully processed {replacement_count} elements")
    print(f"Output written to: {output_path}")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Replace id values with inkscape:label values in SVG files"
    )
    parser.add_argument("input_file", help="Input SVG file path")
    parser.add_argument(
        "-o", "--output", help="Output file path (default: overwrites input)"
    )
    parser.add_argument(
        "--no-backup", action="store_true", help="Do not create backup file"
    )
    parser.add_argument(
        "--optimize", action="store_true", help="Optimize output with svgo --pretty"
    )

    args = parser.parse_args()

    success = label2id(
        args.input_file, args.output, backup=not args.no_backup, optimize=args.optimize
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
