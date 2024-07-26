# PicFix

PicFix is a command-line tool for quick and easy image manipulation. It provides simple yet powerful commands to resize, convert, and optimize images.

## Features

- Resize images to specified dimensions
- Convert images between different formats
- Optimize images to reduce file size
- Support for multiple input files
- Logging for operation tracking and debugging

## Supported Image Formats

PicFix supports a wide range of image formats for both input and output:

- JPEG (.jpg, .jpeg)
- PNG (.png)
- WebP (.webp)
- GIF (.gif)
- BMP (.bmp)
- TIFF (.tiff, .tif)

Note: The actual support may vary depending on your system's Pillow installation. Some formats may be read-only or write-only. Optimization is currently focused on JPEG and PNG formats.

## Installation

To install PicFix, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/yourusername/picfix.git
cd picfix
```
2. Install dependencies using PDM:

```bash
pdm install
```

## Usage

PicFix provides two main commands: `resize` and `convert`.

### Resize Command

Resize one or more images to specified dimensions:

```bash
pdm run picfix resize -i <input_file> -o <output_directory> --width <width> --height <height>
```

Example:
```bash
pdm run picfix resize -i image.jpg -o resized_images --width 800 --height 600
```

### Convert Command

Convert one or more images to a specified format:

```bash
pdm run picfix convert -i <input_file> -o <output_directory> --format <format>
```

Example:

```bash
pdm run picfix convert -i image.png -o converted_images --format JPEG
```

### Optimize Command

Optimize one or more images to reduce file size:

```bash
pdm run picfix optimize -i <input_file> -o <output_directory> [options]
```

Options:
- `-q`, `--quality`: Set the quality for lossy compression (1-100, for JPEG)
- `-t`, `--target-size`: Set a target file size in KB
- `-s`, `--strip-metadata`: Remove metadata from the image

Example:

```bash
pdm run picfix optimize -i image.jpg -o optimized_images -q 85 -t 100 -s
```

This command will optimize image.jpg, aiming for a quality of 85 and a target size of 100KB, while also stripping metadata.

## Image Optimization

The optimize command uses different strategies for JPEG and PNG files:

- For JPEG: It adjusts the compression quality to meet the target size or reduce file size by at least 20%.
- For PNG: It uses color quantization, trying different color palette sizes to find the best balance between file size and image quality.

Note: PNG optimization might be limited for images with transparency.

## Development

PicFix uses PDM for dependency management. To set up the development environment:

1. Install PDM if you haven't already:

## Development

PicFix uses PDM for dependency management. To set up the development environment:

1. Install PDM if you haven't already:

```bash
pdm install
```

2. Install development dependencies:

```bash
pdm install -d
```

3. Run tests:

```bash
pdm run pytest
```

## Project Structure

- `src/picfix/`: Main package
- `commands/`: Command implementations
- `img_processors/`: Image processing logic
- `models/`: Data models for commands
- `tests/`: Test files (to be implemented)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).