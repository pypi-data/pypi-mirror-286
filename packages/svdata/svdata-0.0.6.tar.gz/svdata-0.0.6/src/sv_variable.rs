use crate::{
    sv_misc::{get_string, identifier},
    sv_packed_dimension::SvPackedDimension,
    sv_unpacked_dimension::SvUnpackedDimension,
};
use pyo3::prelude::*;
use std::fmt;
use sv_parser::{unwrap_node, RefNode, SyntaxTree};
#[derive(Debug, Clone, PartialEq)]
#[pyclass]
pub struct SvVariable {
    #[pyo3(get, set)]
    pub identifier: String,
    #[pyo3(get, set)]
    pub packed_dimensions: Vec<SvPackedDimension>,
    #[pyo3(get, set)]
    pub unpacked_dimensions: Vec<SvUnpackedDimension>,
}

#[pymethods]
impl SvVariable {
    #[new]
    fn new(
        identifier: String,
        packed_dimensions: Vec<SvPackedDimension>,
        unpacked_dimensions: Vec<SvUnpackedDimension>,
    ) -> Self {
        SvVariable {
            identifier,
            packed_dimensions,
            unpacked_dimensions,
        }
    }

    fn __repr__(&self) -> String {
        self.to_string()
    }
}

impl fmt::Display for SvVariable {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        // Start with "logic "
        write!(f, "logic ")?;

        // Write packed dimensions
        for (dim1, dim2) in &self.packed_dimensions {
            write!(f, "[{}:{}]", dim1.as_str(), dim2.as_str())?;
        }

        // Write the identifier with or without leading space
        if self.packed_dimensions.is_empty() {
            write!(f, "{}", self.identifier)?;
        } else {
            write!(f, " {}", self.identifier)?;
        }

        // Write unpacked dimensions
        for (dim1, dim2) in &self.unpacked_dimensions {
            let dim_str = match dim2 {
                Some(d2) => format!("[{}:{}]", dim1.as_str(), d2.as_str()),
                None => format!("[{}]", dim1.as_str()),
            };
            write!(f, "{}", dim_str)?;
        }

        // End with ";"
        write!(f, ";")?;

        Ok(())
    }
}

pub fn variable_declaration(
    p: &sv_parser::ModuleCommonItem,
    syntax_tree: &SyntaxTree,
) -> SvVariable {
    SvVariable {
        identifier: variable_identifier(p, syntax_tree),
        packed_dimensions: port_packed_dimension_ansi(RefNode::ModuleCommonItem(p), syntax_tree),
        unpacked_dimensions: port_unpacked_dimension_ansi(
            RefNode::ModuleCommonItem(p),
            syntax_tree,
        ),
    }
}

fn variable_identifier(node: &sv_parser::ModuleCommonItem, syntax_tree: &SyntaxTree) -> String {
    if let Some(id) = unwrap_node!(node, VariableIdentifier) {
        identifier(id, syntax_tree).unwrap()
    } else if let Some(id) = unwrap_node!(node, NetIdentifier) {
        identifier(id, syntax_tree).unwrap()
    } else {
        unreachable!()
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
