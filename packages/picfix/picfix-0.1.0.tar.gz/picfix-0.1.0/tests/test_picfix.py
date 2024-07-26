import io
from pathlib import Path
from typing import BinaryIO

import pytest
from picfix.img_processors.convert_processor import convert_image
from picfix.img_processors.optimize_processor import optimize_image
from picfix.img_processors.resize_processor import resize_image
from PIL import Image


# Helper function to create a test image
def create_test_image(
    size: tuple[int, int] = (100, 100),
    color: tuple[int, int, int] = (255, 0, 0),
    format: str = "PNG",
) -> BinaryIO:
    image: Image.Image = Image.new("RGB", size, color)
    buffer: BinaryIO = io.BytesIO()
    image.save(buffer, format=format)
    buffer.seek(0)
    return buffer


# Fixture to create a temporary directory
@pytest.fixture
def temp_dir(tmp_path: Path) -> Path:
    return tmp_path


def test_resize_image(temp_dir: Path) -> None:
    input_path: Path = temp_dir / "test_input.png"
    output_path: Path = temp_dir / "test_output.png"

    # Create a test image and save it
    with open(input_path, "wb") as f:
        f.write(create_test_image().getvalue())  # type: ignore

    # Resize the image
    resize_image(str(input_path), str(output_path), 50, 50)

    # Check if the output file exists and has the correct size
    assert output_path.exists()
    with Image.open(output_path) as img:
        assert img.size == (50, 50)


def test_convert_image(temp_dir: Path) -> None:
    input_path: Path = temp_dir / "test_input.png"
    output_path: Path = temp_dir / "test_output.jpg"

    # Create a test image and save it
    with open(input_path, "wb") as f:
        f.write(create_test_image().getvalue())  # type: ignore

    # Convert the image
    convert_image(str(input_path), str(output_path), "JPEG")

    # Check if the output file exists and has the correct format
    assert output_path.exists()
    with Image.open(output_path) as img:
        assert img.format == "JPEG"


def test_optimize_image(temp_dir: Path) -> None:
    input_path: Path = temp_dir / "test_input.jpg"
    output_path: Path = temp_dir / "test_output.jpg"

    # Create a test image and save it
    with open(input_path, "wb") as f:
        f.write(create_test_image(format="JPEG").getvalue())  # type: ignore

    original_size: int = input_path.stat().st_size

    # Optimize the image
    optimize_image(str(input_path), str(output_path), quality=50)

    # Check if the output file exists and is smaller than the input
    assert output_path.exists()
    assert output_path.stat().st_size < original_size


def test_optimize_image_with_target_size(temp_dir: Path) -> None:
    input_path: Path = temp_dir / "test_input.jpg"
    output_path: Path = temp_dir / "test_output.jpg"

    # Create a test image and save it
    with open(input_path, "wb") as f:
        f.write(create_test_image(size=(1000, 1000), format="JPEG").getvalue())  # type: ignore

    target_size: int = 50  # KB

    # Optimize the image
    optimize_image(str(input_path), str(output_path), target_size=target_size)

    # Check if the output file exists and is close to the target size
    assert output_path.exists()
    assert (
        abs(output_path.stat().st_size / 1024 - target_size) < 5
    )  # Allow 5KB tolerance
