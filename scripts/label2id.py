#!/usr/bin/env python3
import sys

from lxml import etree


def replace_ids(infile, outfile=None):
    tree = etree.parse(infile)
    root = tree.getroot()

    # inkscape namespace
    ns = {"ink": "http://www.inkscape.org/namespaces/inkscape"}

    # Replace id with inkscape:label
    for elem in root.xpath("//*[@ink:label]", namespaces=ns):
        label = elem.get("{http://www.inkscape.org/namespaces/inkscape}label")
        if label:
            elem.set("id", label)

    # Save output file
    # Overwrite the original if an output file is not provided
    if outfile is None:
        outfile = infile
    tree.write(outfile, pretty_print=True, xml_declaration=True, encoding="utf-8")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Use: python3 replace_ids.py input.svg [output.svg]")
        sys.exit(1)

    infile = sys.argv[1]
    outfile = sys.argv[2] if len(sys.argv) > 2 else None
    replace_ids(infile, outfile)
