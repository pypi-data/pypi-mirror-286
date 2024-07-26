from PIL import Image

from picfix.logging import get_logger
from picfix.models.convert_model import ImageFormat

logger = get_logger()


def convert_image(input_path: str, output_path: str, format: str) -> None:
    """
    Convert an image to the specified format.

    Args:
        input_path (str): Path to the input image file.
        output_path (str): Path where the converted image will be saved.
        format (str): The desired output format.

    Raises:
        ValueError: If the format is unsupported.
        IOError: If there's an error opening or saving the image.
    """
    try:
        output_format = ImageFormat(format.upper())

        with Image.open(input_path) as img:
            if format == ImageFormat.JPEG and img.mode in ("RGBA", "LA"):
                img = img.convert("RGB")
                logger.info(f"Converted image from {img.mode} to RGB for JPEG format")

            img.save(output_path, format=output_format.value)
            logger.info(f"Image converted successfully: {input_path} -> {output_path}")

    except ValueError as e:
        logger.error(f"Unsupported format for image {input_path}: {e}")
        raise
    except OSError as e:
        logger.error(f"Error opening or saving image {input_path}: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error converting image {input_path}: {e}")
        raise
