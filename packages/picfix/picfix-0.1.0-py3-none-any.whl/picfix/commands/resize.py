from pathlib import Path

import typer
from pydantic import ValidationError
from rich.console import Console

from picfix.img_processors.resize_processor import resize_image
from picfix.logging import get_logger
from picfix.models.resize_model import ResizeParams

logger = get_logger()
resize_app = typer.Typer()
console = Console()


@resize_app.callback(invoke_without_command=True)
def resize(
    input_files: list[Path] = typer.Option(
        ...,
        "--input",
        "-i",
        exists=True,
        dir_okay=False,
        readable=True,
        help="Input image file(s)",
    ),
    output_dir: Path = typer.Option(
        ..., "--output", "-o", dir_okay=True, writable=True, help="Output directory"
    ),
    width: int = typer.Option(  # noqa: UP007
        ...,
        "--width",
        "-w",
        help="Width of the resized image",
    ),
    height: int = typer.Option(  # noqa: UP007
        ...,
        "--height",
        "-h",
        help="Height of the resized image",
    ),
):
    """
    Resize one or more images to the specified dimensions.
    """
    try:
        params = ResizeParams(
            input_files=input_files,
            output_dir=output_dir,
            width=width,
            height=height,
        )
    except ValidationError as e:
        typer.echo(f"Invalid input: {e}")
        raise typer.Exit(code=1) from e

    params.output_dir.mkdir(parents=True, exist_ok=True)

    for input_file in input_files:
        try:
            output_file = output_dir / f"resized_{input_file.name}"
            logger.info(f"Resizing image: {input_file}")
            resize_image(
                input_path=str(input_file),
                output_path=str(output_file),
                width=width,
                height=height,
            )
            logger.info(f"Image resized successfully: {output_file}")
            typer.echo(f"Image resized and saved to {output_file}")
        except Exception as e:
            logger.error(f"Error resizing image {input_file}: {e}")
            typer.echo(f"Error processing {input_file}: {e}", err=True)

    typer.echo("Resize operation completed.")
