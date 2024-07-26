from pathlib import Path
from typing import Optional

import typer

from picfix.img_processors.optimize_processor import optimize_image
from picfix.logging import get_logger
from picfix.models.optimize_model import OptimizeParams

logger = get_logger()
optimize_app = typer.Typer()


@optimize_app.callback(invoke_without_command=True)
def optimize(
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
    quality: Optional[int] = typer.Option(
        None,
        "--quality",
        "-q",
        min=1,
        max=100,
        help="Quality level for lossy compression",
    ),
    target_size: Optional[int] = typer.Option(
        None, "--target-size", "-t", help="Target file size in KB"
    ),
    strip_metadata: bool = typer.Option(
        False, "--strip-metadata", "-s", help="Strip metadata from image"
    ),
):
    """
    Optimize one or more images to reduce file size.
    """
    try:
        params = OptimizeParams(
            input_files=input_files,
            output_dir=output_dir,
            quality=quality,
            target_size=target_size,
            strip_metadata=strip_metadata,
        )
    except ValueError as e:
        typer.echo(f"Invalid input: {e}")
        raise typer.Exit(code=1) from e

    params.output_dir.mkdir(parents=True, exist_ok=True)

    for input_file in input_files:
        try:
            output_file = params.output_dir / f"optimize_{input_file}"
            optimize_image(
                input_path=str(input_file),
                output_path=str(output_file),
                quality=params.quality,
                target_size=params.target_size,
                strip_metadata=params.strip_metadata,
            )
            typer.echo(f"Optimized: {input_file} -> {output_file}")
        except Exception as e:
            logger.error(f"Error optimizing image {input_file}: {e}")
            typer.echo(f"Error processing {input_file}: {e}", err=True)

    typer.echo("Optimization completed.")
