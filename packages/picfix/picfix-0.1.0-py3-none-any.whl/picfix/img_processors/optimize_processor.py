import io
from pathlib import Path
from typing import Optional

from PIL import Image

from picfix.logging import get_logger

logger = get_logger()


def optimize_image(
    input_path: str,
    output_path: str,
    quality: Optional[int] = None,
    target_size: Optional[int] = None,
    strip_metadata: bool = False,
) -> None:
    try:
        with Image.open(input_path) as img:
            format = img.format
            if format not in ["JPEG", "PNG"]:
                raise ValueError(f"Unsupported format for optimization: {format}")

            original_size = get_file_size(input_path)
            logger.info(f"Original size: {original_size / 1024:.2f} KB")

            if strip_metadata:
                img = strip_exif(img)

            if format == "JPEG":
                optimized_img = optimize_jpeg(img, quality, target_size)
                save_kwargs = {
                    "format": "JPEG",
                    "optimize": True,
                    "quality": quality or 85,
                }
            else:  # PNG
                optimized_img = optimize_png(img, target_size)
                save_kwargs = {"format": "PNG", "optimize": True}

            optimized_img.save(output_path, **save_kwargs)  # type: ignore

            new_size = get_file_size(output_path)
            logger.info(f"Optimized size: {new_size / 1024:.2f} KB")
            logger.info(
                f"Size reduction: {(original_size - new_size) / original_size * 100:.2f}%"
            )

    except (OSError, ValueError) as e:
        logger.error(f"Error optimizing image {input_path}: {e}")
        raise


def get_file_size(path: str) -> int:
    return Path(path).stat().st_size


def strip_exif(img: Image.Image) -> Image.Image:
    data = list(img.getdata())  # type: ignore
    image_without_exif = Image.new(img.mode, img.size)
    image_without_exif.putdata(data)  # type: ignore
    return image_without_exif


def optimize_jpeg(
    img: Image.Image, quality: Optional[int], target_size: Optional[int]
) -> Image.Image:
    if quality is None:
        quality = 85  # default quality

    if target_size:
        quality = binary_search_quality(img, target_size, quality)
    else:
        # If no target size, try to reduce by at least 20%
        original_size = get_image_size(img)
        while quality > 20:
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG", quality=quality, optimize=True)
            if buffer.tell() < original_size * 0.8:
                break
            quality -= 5

    return img  # The quality will be applied when saving


def optimize_png(img: Image.Image, target_size: Optional[int]) -> Image.Image:
    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):  # type: ignore
        logger.info("PNG has transparency, optimization might be limited")

    original_size = get_image_size(img, format="PNG")
    best_img = img
    best_size = original_size

    # Try different optimization techniques
    for colors in [256, 128, 64, 32, 16, 8, 4, 2]:
        quantized = img.quantize(colors=colors)  # type: ignore
        new_size = get_image_size(quantized, format="PNG")

        if new_size < best_size:
            best_img = quantized
            best_size = new_size

        if target_size and new_size <= target_size * 1024:
            logger.info(f"Target size reached with {colors} colors")
            return quantized

    if best_size < original_size:
        logger.info(f"Best optimization achieved: {best_size / 1024:.2f} KB")
        return best_img
    else:
        logger.info("Unable to optimize PNG further")
        return img


def binary_search_quality(img: Image.Image, target_size: int, max_quality: int) -> int:
    low, high = 1, max_quality
    while low <= high:
        mid = (low + high) // 2
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=mid, optimize=True)
        if buffer.tell() / 1024 <= target_size:
            low = mid + 1
        else:
            high = mid - 1
    return high


def get_image_size(img: Image.Image, format: str = "JPEG") -> int:
    buffer = io.BytesIO()
    img.save(buffer, format=format, optimize=True)
    return buffer.tell()
