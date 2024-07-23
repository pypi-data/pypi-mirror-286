from pathlib import Path

import aiofiles


async def save_to_file_async(
    file_content: bytes | str,
    path: str | Path,
) -> None:
    if isinstance(file_content, str):
        file_content = file_content.encode()
    async with aiofiles.open(path, "wb") as file:
        await file.write(file_content)
        await file.flush()
    return None


async def load_from_file_async(
    path: str | Path,
) -> bytes:
    async with aiofiles.open(path, "rb") as file:
        return await file.read()


async def load_from_file_str_async(
    path: str | Path,
    encoding: str = "utf-8",
) -> str:
    async with aiofiles.open(path, encoding=encoding) as file:
        return await file.read()
