from pathlib import Path
from typing import List, Optional  # noqa: UP035

from pydantic import BaseModel, Field  # type: ignore


class OptimizeParams(BaseModel):
    input_files: List[Path] = Field(..., description="Input image file(s)")  # noqa: UP006
    output_dir: Path = Field(..., description="Output directory")
    quality: Optional[int] = Field(
        None, ge=1, le=100, description="Quality level of lossy compression"
    )
    target_size: Optional[int] = Field(None, gt=0, description="Target file size in KB")
    strip_metadata: bool = Field(False, description="Strip metadata from image")
