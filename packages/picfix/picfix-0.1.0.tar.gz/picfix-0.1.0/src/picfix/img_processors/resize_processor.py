from PIL import Image

from picfix.logging import get_logger

logger = get_logger()


def resize_image(input_path: str, output_path: str, width: int, height: int) -> None:
    """
    Resize an image to the specified dimensions.

    Args:
        input_path (str): Path to the input image file.
        output_path (str): Path where the resized image will be saved.
        width (int): The desired width of the output image.
        height (int): The desired height of the output image.

    Raises:
        IOError: If there's an error opening or saving the image.
        ValueError: If the dimensions are invalid.
    """
    try:
        logger.info(f"Resizing image: {input_path}")
        logger.debug(f"Target dimensions: {width}x{height}")

        # open the image
        with Image.open(input_path) as img:
            # resize the image
            resized_image = img.resize((width, height))

            # save the image
            resized_image.save(output_path)
        logger.info(f"Resized image saved: {output_path}")
    except OSError as e:
        logger.error(f"Error opening or saving the image: {e}")
        raise

    except ValueError as e:
        logger.error(f"Invalid dimensions: {e}")
        raise

    except Exception as e:
        logger.error(f"Unexpected error during resize: {e}")
        raise
