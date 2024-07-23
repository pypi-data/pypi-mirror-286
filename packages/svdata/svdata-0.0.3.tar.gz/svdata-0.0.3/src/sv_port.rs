use crate::{
    sv_misc::{get_string, identifier},
    sv_packed_dimension::SvPackedDimension,
    sv_unpacked_dimension::SvUnpackedDimension,
};
use pyo3::prelude::*;
use std::fmt;
use sv_parser::{unwrap_node, PortDirection, RefNode, SyntaxTree};

#[derive(Debug, Clone, PartialEq)]
#[pyclass]
pub struct SvPort {
    #[pyo3(get, set)]
    pub identifier: String,
    #[pyo3(get, set)]
    pub direction: SvPortDirection,
    #[pyo3(get, set)]
    pub packed_dimensions: Vec<SvPackedDimension>,
    #[pyo3(get, set)]
    pub unpacked_dimensions: Vec<SvUnpackedDimension>,
}

#[derive(Debug, Clone, PartialEq)]
#[pyclass(eq, eq_int)]
pub enum SvPortDirection {
    Inout,
    Input,
    Output,
    Ref,
    IMPLICIT,
}

#[pymethods]
impl SvPortDirection {
    fn __repr__(&self) -> String {
        match self {
            SvPortDirection::Inout => "Inout".to_string(),
            SvPortDirection::Input => "Input".to_string(),
            SvPortDirection::Output => "Output".to_string(),
            SvPortDirection::Ref => "Ref".to_string(),
            SvPortDirection::IMPLICIT => "IMPLICIT".to_string(),
        }
    }
}

impl fmt::Display for SvPortDirection {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            SvPortDirection::Inout => write!(f, "inout"),
            SvPortDirection::Input => write!(f, "input"),
            SvPortDirection::Output => write!(f, "output"),
            SvPortDirection::Ref => write!(f, "ref"),
            SvPortDirection::IMPLICIT => write!(f, "implicit"),
        }
    }
}

pub fn port_declaration_ansi(
    p: &sv_parser::AnsiPortDeclaration,
    syntax_tree: &SyntaxTree,
) -> SvPort {
    SvPort {
        identifier: port_identifier(p, syntax_tree),
        direction: port_direction_ansi(p),
        packed_dimensions: port_packed_dimension_ansi(RefNode::AnsiPortDeclaration(p), syntax_tree),
        unpacked_dimensions: port_unpacked_dimension_ansi(
            RefNode::AnsiPortDeclaration(p),
            syntax_tree,
        ),
    }
}

fn port_identifier(node: &sv_parser::AnsiPortDeclaration, syntax_tree: &SyntaxTree) -> String {
    if let Some(id) = unwrap_node!(node, PortIdentifier) {
        identifier(id, syntax_tree).unwrap()
    } else {
        unreachable!()
    }
}

fn port_direction_ansi(node: &sv_parser::AnsiPortDeclaration) -> SvPortDirection {
    let dir = unwrap_node!(node, PortDirection);
    match dir {
        Some(RefNode::PortDirection(PortDirection::Input(_))) => SvPortDirection::Input,
        Some(RefNode::PortDirection(PortDirection::Output(_))) => SvPortDirection::Output,
        Some(RefNode::PortDirection(PortDirection::Ref(_))) => SvPortDirection::Ref,
        _ => SvPortDirection::Inout,
    }
}

pub fn port_packed_dimension_ansi(m: RefNode, syntax_tree: &SyntaxTree) -> Vec<SvPackedDimension> {
    let mut ret: Vec<SvPackedDimension> = Vec::new();

    for node in m {
        if let RefNode::PackedDimensionRange(x) = node {
            let range = unwrap_node!(x, ConstantRange);
            if let Some(RefNode::ConstantRange(sv_parser::ConstantRange { nodes })) = range {
                let (l, _, r) = nodes;
                let left = get_string(RefNode::ConstantExpression(l), syntax_tree).unwrap();
                let right = get_string(RefNode::ConstantExpression(r), syntax_tree).unwrap();

                ret.push((left, right));
            }
        }
    }

    ret
}

pub fn port_unpacked_dimension_ansi(
    m: RefNode,
    syntax_tree: &SyntaxTree,
) -> Vec<SvUnpackedDimension> {
    let mut ret: Vec<SvUnpackedDimension> = Vec::new();

    for node in m {
        match node {
            RefNode::UnpackedDimensionRange(x) => {
                let range = unwrap_node!(x, ConstantRange);
                if let Some(RefNode::ConstantRange(sv_parser::ConstantRange { nodes })) = range {
                    let (l, _, r) = nodes;
                    let left = get_string(RefNode::ConstantExpression(l), syntax_tree).unwrap();
                    let right = get_string(RefNode::ConstantExpression(r), syntax_tree).unwrap();

                    ret.push((left, Some(right)));
                }
            }
            RefNode::UnpackedDimensionExpression(x) => {
                let range = unwrap_node!(x, ConstantExpression).unwrap();
                let left = get_string(range, syntax_tree).unwrap();

                ret.push((left, None));
            }
            _ => (),
        }
    }

    ret
}
