import os
from hashlib import md5
from pathlib import Path
from typing import List

import imagesize

from pflows.typedef import Image


def get_image_info_fast(image_path: str):
    # Get file size without reading the entire file
    size_bytes = os.path.getsize(image_path)
    size_kb = int(round(size_bytes / 1024, 2))

    # Open the image and get dimensions without loading the entire image into memory
    width, height = imagesize.get(image_path)

    # Compute MD5 hash of the file without loading it entirely into memory
    hasher = md5()
    with open(image_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    image_hash = hasher.hexdigest()

    return width, height, size_kb, image_hash


def get_image_info(
    image_path: str, group_name: str, intermediate_ids: List[str] | None = None
) -> Image:
    width, height, size_kb, image_hash = get_image_info_fast(image_path)

    intermediate_ids = intermediate_ids or []
    image_path_obj = Path(image_path)
    if image_path_obj.name not in intermediate_ids:
        intermediate_ids.append(image_path_obj.name)

    image: Image = Image(
        id=image_hash,
        intermediate_ids=intermediate_ids,
        path=str(image_path),
        width=width,
        height=height,
        size_kb=size_kb,
        group=group_name,
    )
    return image
