"""
Command-Line Interface
======================

Produces organized and semantically enriched ``.json`` documents from
"figure-documents".
"""

from argparse import ArgumentParser, Namespace
from pathlib import Path

import senfd
import senfd.schema
from senfd.documents import CategorizedFigureDocument


def parse_args() -> Namespace:
    """Return command-line arguments"""

    parser = ArgumentParser(description="Semantically organize and enrich figures")
    parser.add_argument(
        "document", nargs="*", type=Path, help="path to one or more .json document(s)"
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
        help=f"dump schema({senfd.schema.FILENAME}) and exit",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="print the version and exit",
    )
    args = parser.parse_args()
    if not args.document and not args.dump_schema and not args.version:
        parser.error("the following arguments are required: document")

    return args


def main() -> int:
    """Command-line entrypoint"""

    args = parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    if args.version:
        print(senfd.__version__)
        return 0

    if args.dump_schema:
        CategorizedFigureDocument.to_schema_file(
            args.output / CategorizedFigureDocument.FILENAME_SCHEMA
        )
        return 0

    for path in args.document:
        document = CategorizedFigureDocument.from_figure_document_file(path)
        document.to_json_file(
            args.output
            / Path(path.name).with_suffix(CategorizedFigureDocument.SUFFIX_JSON).name
        )

        if args.skip_validate:
            continue

        if not document.is_valid():
            print("Document is invalid, see above for details.")

    return 0
