#!/usr/bin/env python3
"""
Script to replace id attribute values with inkscape:label values in SVG files.
This keeps both attributes but uses the inkscape:label value as the new id value.
This version preserves the original formatting of the SVG file.
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

from lxml import etree


def label_to_valid_id(label):
    """Convert a label to a valid XML ID."""
    # Convert to valid id (replace spaces and special chars)
    new_id = re.sub(r"[^a-zA-Z0-9_-]", "_", label)

    # Ensure id starts with letter or underscore
    if new_id and not re.match(r"^[a-zA-Z_]", new_id):
        new_id = "_" + new_id

    return new_id


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
        # Copy the original file to backup, don't rename it
        shutil.copy2(svg_path, backup_path)

    # Parse the SVG file with lxml
    try:
        tree = etree.parse(str(svg_path))
        root = tree.getroot()
    except Exception as e:
        print(f"Error parsing SVG file: {e}")
        return False

    # Define namespaces
    namespaces = {
        "inkscape": "http://www.inkscape.org/namespaces/inkscape",
        "sodipodi": "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd",
    }

    # Find all elements with inkscape:label attribute
    elements_with_label = root.xpath("//*[@inkscape:label]", namespaces=namespaces)

    replacement_count = 0
    for elem in elements_with_label:
        # Get the inkscape:label value
        label = elem.get("{http://www.inkscape.org/namespaces/inkscape}label")
        if label:
            # Convert to valid ID
            new_id = label_to_valid_id(label)
            # Set the new ID
            elem.set("id", new_id)
            replacement_count += 1

    # Determine output path
    if output_path is None:
        output_path = svg_path

    # If optimization is requested, optimize first, then do the replacement
    if optimize:
        try:
            print("Optimizing SVG with svgo first...")
            # First, write the current tree to the output file
            tree.write(
                str(output_path),
                encoding="utf-8",
                xml_declaration=True,
                pretty_print=True,
            )

            # Use svgo with custom config to preserve inkscape:label but remove old IDs
            config_path = Path(__file__).parent.parent / "svgo.config.js"
            subprocess.run(
                ["svgo", "--config", str(config_path), "--pretty", str(output_path)],
                capture_output=True,
                text=True,
                check=True,
            )
            print("SVG optimized successfully")

            # Now parse the optimized content and do the replacement
            optimized_tree = etree.parse(str(output_path))
            optimized_root = optimized_tree.getroot()

            # Find all elements with inkscape:label attribute in optimized content
            optimized_elements = optimized_root.xpath(
                "//*[@inkscape:label]", namespaces=namespaces
            )

            replacement_count = 0
            for elem in optimized_elements:
                # Get the inkscape:label value
                label = elem.get("{http://www.inkscape.org/namespaces/inkscape}label")
                if label:
                    # Convert to valid ID
                    new_id = label_to_valid_id(label)
                    # Set the new ID
                    elem.set("id", new_id)
                    replacement_count += 1

            # Write the final result
            optimized_tree.write(
                str(output_path),
                encoding="utf-8",
                xml_declaration=True,
                pretty_print=True,
            )

        except subprocess.CalledProcessError as e:
            print(f"Warning: svgo optimization failed: {e}")
            print(f"svgo stderr: {e.stderr}")
            # Fall back to normal processing without optimization
            tree.write(
                str(output_path),
                encoding="utf-8",
                xml_declaration=True,
                pretty_print=True,
            )
        except FileNotFoundError:
            print("Warning: svgo not found. Install it with: npm install -g svgo")
            # Fall back to normal processing without optimization
            tree.write(
                str(output_path),
                encoding="utf-8",
                xml_declaration=True,
                pretty_print=True,
            )
        except Exception as e:
            print(f"Warning: Error running svgo: {e}")
            # Fall back to normal processing without optimization
            tree.write(
                str(output_path),
                encoding="utf-8",
                xml_declaration=True,
                pretty_print=True,
            )
    else:
        # Write the modified content without optimization
        try:
            tree.write(
                str(output_path),
                encoding="utf-8",
                xml_declaration=True,
                pretty_print=True,
            )
        except Exception as e:
            print(f"Error writing file: {e}")
            return False

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
