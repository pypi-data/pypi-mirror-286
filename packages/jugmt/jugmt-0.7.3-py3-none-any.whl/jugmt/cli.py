"""
Command-Line Interface
======================

Produces .html and .json when given .docx documents
"""

from argparse import ArgumentParser, Namespace
from pathlib import Path

import jugmt.schema
from jugmt.document import FigureDocument


def parse_args() -> Namespace:
    """Return command-line arguments"""

    parser = ArgumentParser(
        description="Extract table information from .docx documents"
    )
    parser.add_argument(
        "document", nargs="*", type=Path, help="path to one or more .docx document(s)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="directory where the output will be saved",
        default=Path("output"),
    )
    parser.add_argument(
        "--skip-validate",
        action="store_true",
        help="skip post-parse validation",
    )
    parser.add_argument(
        "--dump-schema",
        action="store_true",
        help=f"dump schema({jugmt.schema.FILENAME}) and exit",
    )

    args = parser.parse_args()
    if not args.document and not args.dump_schema:
        parser.error("the following arguments are required: document")

    return args


def main() -> int:
    """CLI entrypoint"""

    args = parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    if args.dump_schema:
        FigureDocument.to_schema_file(args.output / jugmt.schema.FILENAME)
        return 0

    for path in args.document:
        document, errors = FigureDocument().from_docx(path)

        (args.output / path.stem).with_suffix(".figures.html").write_text(
            document.to_html()
        )
        (args.output / path.stem).with_suffix(".figures.json").write_text(
            document.to_json()
        )

        if args.skip_validate:
            continue

        document.check()

    return 0
