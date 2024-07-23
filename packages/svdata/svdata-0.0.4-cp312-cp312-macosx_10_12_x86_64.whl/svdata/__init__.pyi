from enum import Enum

SvPackedDimension = tuple[str, str]
SvUnpackedDimension = tuple[str, str | None]

class SvVariable:
    identifier: str

class SvInstance:
    module_identifier: str
    hierarchical_instance: str
    hierarchy: list[str]
    connections: list[list[str]]

class SvPortDirection(Enum):
    Inout = "Inout"
    Input = "Input"
    Output = "Output"
    Ref = "Ref"
    IMPLICIT = "IMPLICIT"

class SvData:
    modules: list[SvModule]

class SvPort:
    identifier: str
    direction: SvPortDirection
    packed_dimensions: list[SvPackedDimension]
    unpacked_dimensions: list[SvUnpackedDimension]

class SvModule:
    identifier: str
    filepath: str
    ports: list[SvPort]
    variables: list[SvVariable]

    def render(self) -> str: ...

def read_sv_file(file_path: str) -> SvData: ...
