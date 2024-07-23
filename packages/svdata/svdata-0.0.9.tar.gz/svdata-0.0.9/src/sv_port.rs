use crate::{
    sv_misc::{get_string, identifier},
    sv_packed_dimension::SvPackedDimension,
    sv_port_direction::SvPortDirection,
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

#[pymethods]
impl SvPort {
    #[new]
    fn new(
        identifier: String,
        direction: SvPortDirection,
        packed_dimensions: Vec<SvPackedDimension>,
        unpacked_dimensions: Vec<SvUnpackedDimension>,
    ) -> Self {
        SvPort {
            identifier,
            direction,
            packed_dimensions,
            unpacked_dimensions,
        }
    }

    fn __repr__(&self) -> String {
        self.to_string()
    }
}

impl fmt::Display for SvPort {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.direction)?;

        write!(f, " logic ")?;
        for packed_dimension in &self.packed_dimensions {
            write!(f, "{}", packed_dimension)?;
        }

        if self.packed_dimensions.is_empty() {
            write!(f, "{}", self.identifier)?;
        } else {
            write!(f, " {}", self.identifier)?;
        }

        for unpacked_dimension in &self.unpacked_dimensions {
            write!(f, "{}", unpacked_dimension)?;
        }

        Ok(())
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
                let left_bound = get_string(RefNode::ConstantExpression(l), syntax_tree).unwrap();
                let right_bound = get_string(RefNode::ConstantExpression(r), syntax_tree).unwrap();

                ret.push(SvPackedDimension {
                    left_bound,
                    right_bound,
                });
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
                    let left_bound =
                        get_string(RefNode::ConstantExpression(l), syntax_tree).unwrap();
                    let right_bound =
                        get_string(RefNode::ConstantExpression(r), syntax_tree).unwrap();

                    ret.push(SvUnpackedDimension {
                        left_bound,
                        right_bound: Some(right_bound),
                    });
                }
            }
            RefNode::UnpackedDimensionExpression(x) => {
                let range = unwrap_node!(x, ConstantExpression).unwrap();
                let left_bound = get_string(range, syntax_tree).unwrap();

                ret.push(SvUnpackedDimension {
                    left_bound,
                    right_bound: None,
                });
            }
            _ => (),
        }
    }

    ret
}
