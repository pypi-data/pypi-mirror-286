from pathlib import Path
from typing import List  # noqa: UP035

from pydantic import BaseModel, Field


class ResizeParams(BaseModel):
    input_files: List[Path] = Field(..., description="Input image file(s)")  # noqa: UP006
    output_dir: Path = Field(..., description="Output directory")
    width: int = Field(..., gt=0, description="Width of the resized image")
    height: int = Field(..., gt=0, description="Height of the resized image")
