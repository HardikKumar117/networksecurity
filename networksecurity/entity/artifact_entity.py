from dataclasses import dataclass 
# dataclass is a decorator that automatically generates special methods for classes used for storing data


@dataclass
class DataIngestionArtifact:
    trained_file_path:str
    test_file_path:str
    