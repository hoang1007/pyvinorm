import importlib.resources as pkg_resources

from .mapping import MappingManager, Mapping
from .lm import LanguageModelManager, LanguageModel
from pyvinorm.utils.downloader import GhReleaseDownloader


def init_resources():
    """
    Initialize mappings from files.
    """
    for resource in pkg_resources.contents("pyvinorm.resources.mapping"):
        if resource.endswith(".txt"):
            with pkg_resources.path("pyvinorm.resources.mapping", resource) as path:
                mapping_name = resource[:-4]  # Remove the '.txt' extension
                MappingManager.register_mapping(
                    mapping_name, Mapping.from_file(str(path))
                )

    filepath = GhReleaseDownloader("v0.2.0").download("trigram-v1.0.bin")
    LanguageModelManager.register_language_model(LanguageModel.from_file(filepath))
