from enum import Enum

SvPackedDimension = tuple[str, str]
SvUnpackedDimension = tuple[str, str | None]

class SvVariable:
    identifier: str

    def __init__(self, identifier: str) -> None: ...

class SvInstance:
    module_identifier: str
    hierarchical_instance: str
    hierarchy: list[str]
    connections: list[list[str]]

    def __init__(
        self,
        module_identifier: str,
        hierarchical_instance: str,
        hierarchy: list[str],
        connections: list[list[str]],
    ) -> None: ...

class SvPortDirection(Enum):
    Inout = "Inout"
    Input = "Input"
    Output = "Output"
    Ref = "Ref"
    IMPLICIT = "IMPLICIT"

class SvData:
    modules: list[SvModule]

    def __init__(self, modules: list[SvModule]) -> None: ...

class SvPort:
    identifier: str
    direction: SvPortDirection
    packed_dimensions: list[SvPackedDimension]
    unpacked_dimensions: list[SvUnpackedDimension]

    def __init__(
        self,
        identifier: str,
        direction: SvPortDirection,
        packed_dimensions: list[SvPackedDimension],
        unpacked_dimensions: list[SvUnpackedDimension],
    ) -> None: ...

class SvModule:
    identifier: str
    filepath: str
    ports: list[SvPort]
    variables: list[SvVariable]
    instances: list[SvInstance]

    def __init__(
        self,
        identifier: str,
        filepath: str,
        ports: list[SvPort],
        variables: list[SvVariable],
    ) -> None: ...
    def render(self) -> str: ...

def read_sv_file(file_path: str) -> SvData: ...
