from pathlib import Path
from typing import List  # noqa: UP035

import typer
from pydantic import ValidationError

from picfix.img_processors.convert_processor import convert_image
from picfix.logging import get_logger
from picfix.models.convert_model import ConvertParams, ImageFormat

logger = get_logger()
convert_app = typer.Typer()


@convert_app.callback(invoke_without_command=True)
def convert(
    input_files: List[Path] = typer.Option(  # noqa: UP006
        ...,
        "--input",
        "-i",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Input image file(s)",
    ),
    output_dir: Path = typer.Option(
        ..., "--output", "-o", dir_okay=False, writable=True, help="Output image file"
    ),
    format: str = typer.Option(
        ...,
        "--format",
        "-f",
        help=f"Output format: {', '.join([f.value for f in ImageFormat])}",
    ),
):
    """
    Convert an image to a specified format.
    """
    try:
        params = ConvertParams(
            input_files=input_files,
            output_dir=output_dir,
            format=ImageFormat.from_string(format),
        )
    except ValidationError as e:
        typer.echo(f"Invalid input: {e}")
        raise typer.Exit(code=1) from e

    params.output_dir.mkdir(parents=True, exist_ok=True)

    for input_file in input_files:
        try:
            output_file = (
                params.output_dir / f"{input_file.stem}.{params.format.value.lower()}"
            )
            convert_image(
                input_path=str(input_file),
                output_path=str(output_file),
                format=params.format.value,
            )
            typer.echo(f"Converted: {input_file} -> {output_file}")
        except Exception as e:
            typer.echo(f"Error processing {input_file}: {e}", err=True)
    typer.echo("Conversion process completed.")
