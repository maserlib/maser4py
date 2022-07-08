# -*- coding: utf-8 -*-
from poetry2setup import build_setup_py
import argparse
from pathlib import Path
import logging
from black import format_str, FileMode

logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent


def main():
    """Generate setup.py file from pyproject.toml."""
    parser = argparse.ArgumentParser(
        description="Generate setup.py file from pyproject.toml"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=ROOT_DIR / "setup.py",
        help=f'Output file. Default: {ROOT_DIR / "setup.py"}',
    )

    args = parser.parse_args()

    with open(args.output, "w") as output_file:
        logger.info(f"Generating setup.py ({args.output})")
        content = format_str(build_setup_py().decode("utf8"), mode=FileMode())

        output_file.write(content)


if __name__ == "__main__":
    main()
