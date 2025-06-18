import importlib.resources as pkg_resources

from .mapping import MappingManager, Mapping


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
