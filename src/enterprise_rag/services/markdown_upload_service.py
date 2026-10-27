from pathlib import PurePath

from fastapi import HTTPException, UploadFile, status


_ALLOWED_SUFFIXES = {".md", ".markdown"}


async def read_markdown_file(file: UploadFile, max_upload_bytes: int) -> tuple[str, str]:
    """Read a markdown file and return its title and content."""
    path = PurePath(file.filename or "")
    if path.suffix.lower() not in _ALLOWED_SUFFIXES:
        raise HTTPException(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Only .md files are allowed")

    data = await file.read(max_upload_bytes + 1)  # read one extra byte to detect "too big"
    if len(data) > max_upload_bytes:
        raise HTTPException(status.HTTP_413_CONTENT_TOO_LARGE, "File is too large")

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "File must be UTF-8 text")

    if not text.strip():
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "File is empty")

    return path.stem, text

