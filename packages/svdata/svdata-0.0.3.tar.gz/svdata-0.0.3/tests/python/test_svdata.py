from svdata import SvPortDirection, read_sv_file

ansi_module_a = read_sv_file("tests/systemverilog/ansi_module_a.sv").modules[0]


def test_module_name() -> None:
    assert ansi_module_a.identifier == "ansi_module_a"

    assert ansi_module_a.ports[0].identifier == "a"
    assert ansi_module_a.ports[0].direction == SvPortDirection.Input

    assert ansi_module_a.ports[1].identifier == "b"
    assert ansi_module_a.ports[1].direction == SvPortDirection.Input
    assert ansi_module_a.ports[1].unpacked_dimensions[0][0] == "2"
    assert ansi_module_a.ports[1].unpacked_dimensions[0][1] == "0"
    assert ansi_module_a.ports[1].packed_dimensions[0][0] == "1"
    assert ansi_module_a.ports[1].packed_dimensions[0][1] == "0"

    assert ansi_module_a.variables[0].identifier == "c"

    assert ansi_module_a.variables[1].identifier == "d"
