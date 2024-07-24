from enum import Enum
from typing import Sequence

class SvPackedDimension:
    left_bound: str
    right_bound: str

    def __init__(self, left_bound: str, right_bound: str) -> None: ...

class SvUnpackedDimension:
    left_bound: str
    right_bound: str | None

    def __init__(self, left_bound: str, right_bound: str | None) -> None: ...

class SvVariable:
    identifier: str
    packed_dimensions: Sequence[SvPackedDimension]
    unpacked_dimensions: Sequence[SvUnpackedDimension]

    def __init__(
        self,
        identifier: str,
        packed_dimensions: Sequence[SvPackedDimension],
        unpacked_dimensions: Sequence[SvUnpackedDimension],
    ) -> None: ...

class SvInstance:
    module_identifier: str
    instance_identifier: str
    connections: Sequence[Sequence[str]]

    def __init__(
        self,
        module_identifier: str,
        instance_identifier: str,
        connections: Sequence[Sequence[str]],
    ) -> None: ...
    def add_connection(self, connection: Sequence[str]): ...

class SvPortDirection(Enum):
    Inout = "Inout"
    Input = "Input"
    Output = "Output"
    Ref = "Ref"
    IMPLICIT = "IMPLICIT"

class SvData:
    modules: Sequence[SvModule]

    def __init__(self, modules: Sequence[SvModule]) -> None: ...

class SvPort:
    identifier: str
    direction: SvPortDirection
    packed_dimensions: Sequence[SvPackedDimension]
    unpacked_dimensions: Sequence[SvUnpackedDimension]

    def __init__(
        self,
        identifier: str,
        direction: SvPortDirection,
        packed_dimensions: Sequence[SvPackedDimension],
        unpacked_dimensions: Sequence[SvUnpackedDimension],
    ) -> None: ...

class SvModule:
    identifier: str
    filepath: str
    ports: Sequence[SvPort]
    variables: Sequence[SvVariable]
    instances: Sequence[SvInstance]

    def __init__(
        self,
        identifier: str,
        filepath: str,
        ports: Sequence[SvPort],
        variables: Sequence[SvVariable],
        instances: Sequence[SvInstance],
    ) -> None: ...
    def add_variable(self, variable: SvVariable): ...
    def add_instance(self, instance: SvInstance): ...
    def add_port(self, port: SvPort): ...

def read_sv_file(file_path: str) -> SvData: ...
