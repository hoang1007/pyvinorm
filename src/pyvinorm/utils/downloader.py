import logging
import os
import requests
from pathlib import Path
import json

logger = logging.getLogger(__name__)

DEFAULT_CACHE_DIR = Path.home() / ".cache/pyvinorm"


class FileDownloader:
    def __init__(self, cache_dir: str = DEFAULT_CACHE_DIR):
        """
        Initialize the downloader with a cache directory.
        :param cache_dir: Directory to cache downloaded files.
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def download(self, url: str, filename: str = None) -> str:
        """
        Download a file from a URL and cache it locally.

        :param url: URL of the file to download.
        :param filename: Optional filename for the cached file.
        :return: Path to the downloaded file.
        """
        if not filename:
            filename = os.path.basename(url)
        file_path = self.cache_dir / filename

        if file_path.exists():
            logger.info(f"File already downloaded: {file_path}")
            return str(file_path)

        logger.info(f"Downloading {url} to {file_path}...")
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

        logger.info(f"File downloaded: {file_path}")
        return str(file_path)

    def list_cache(self):
        return [str(p) for p in self.cache_dir.iterdir() if p.is_file()]

    def clear_cache(self):
        for file in self.cache_dir.iterdir():
            if file.is_file():
                file.unlink()
        logger.info(f"Cleared cache in {self.cache_dir}")


class GhReleaseDownloader(FileDownloader):
    def __init__(self, version: str, cache_dir: str = DEFAULT_CACHE_DIR):
        super().__init__(cache_dir)
        self.version = version

    def download(self, filename: str) -> str:
        """
        Download the release file for the specified version.
        :param filename: Optional filename for the cached file.
        :return: Path to the downloaded file.
        """
        url = f"https://github.com/hoang1007/pyvinorm/releases/download/{self.version}/{filename}"
        return super().download(url, filename)
