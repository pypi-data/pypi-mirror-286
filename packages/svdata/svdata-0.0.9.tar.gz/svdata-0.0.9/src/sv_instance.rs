use pyo3::prelude::*;
use std::fmt;
use sv_parser::{unwrap_node, RefNode, SyntaxTree};

use crate::sv_misc::{get_string, identifier};

#[derive(Debug, Clone, PartialEq)]
#[pyclass]
pub struct SvInstance {
    #[pyo3(get, set)]
    pub module_identifier: String,
    #[pyo3(get, set)]
    pub instance_identifier: String,
    #[pyo3(get, set)]
    pub connections: Vec<Vec<String>>,
}

#[pymethods]
impl SvInstance {
    #[new]
    fn new() -> Self {
        SvInstance {
            module_identifier: String::new(),
            instance_identifier: String::new(),
            connections: Vec::new(),
        }
    }
    fn __repr__(&self) -> String {
        self.to_string()
    }
}

impl fmt::Display for SvInstance {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "  {} {} (",
            self.module_identifier, self.instance_identifier
        )?;

        if self.connections.len() > 1 {
            writeln!(f)?;

            for connection in &self.connections[..self.connections.len() - 1] {
                writeln!(f, "    .{}({}),", connection[0], connection[1])?;
            }

            writeln!(
                f,
                "    .{}({})",
                self.connections.last().unwrap()[0],
                self.connections.last().unwrap()[1]
            )?;
            write!(f, "  );")?;
        }

        if self.connections.len() == 1 {
            write!(
                f,
                ".{}({})",
                self.connections.last().unwrap()[0],
                self.connections.last().unwrap()[1]
            )?;
            write!(f, ");")?;
        }

        Ok(())
    }
}

pub fn module_instance(p: &sv_parser::ModuleInstantiation, syntax_tree: &SyntaxTree) -> SvInstance {
    SvInstance {
        module_identifier: inst_module_identifier(p, syntax_tree),
        instance_identifier: inst_instance_identifier(p, syntax_tree),
        connections: inst_connections(p, syntax_tree),
    }
}

// Find module identifier for the instantiation (child module)
fn inst_module_identifier(p: &sv_parser::ModuleInstantiation, syntax_tree: &SyntaxTree) -> String {
    if let Some(id) = unwrap_node!(p, ModuleIdentifier) {
        identifier(id, syntax_tree).unwrap()
    } else {
        unreachable!()
    }
}

// Find hierarchical instance for the instantiation
fn inst_instance_identifier(
    p: &sv_parser::ModuleInstantiation,
    syntax_tree: &SyntaxTree,
) -> String {
    if let Some(id) = unwrap_node!(p, InstanceIdentifier) {
        identifier(id, syntax_tree).unwrap()
    } else {
        unreachable!()
    }
}

// Finding connections for the instantiation
fn inst_connections(
    p: &sv_parser::ModuleInstantiation,
    syntax_tree: &SyntaxTree,
) -> Vec<Vec<String>> {
    let mut ret: Vec<Vec<String>> = Vec::new();

    for node in p {
        match node {
            // Port connection by name
            RefNode::NamedPortConnection(x) => {
                // Connection in child module
                let left = unwrap_node!(node.clone(), PortIdentifier).unwrap();
                let left = identifier(left, syntax_tree).unwrap();
                // Connection in parent module
                if let Some(right_node) = unwrap_node!(node.clone(), HierarchicalIdentifier) {
                    let right_name = identifier(right_node, syntax_tree).unwrap();
                    let mut right_index = String::new();
                    for select_node in x {
                        if let RefNode::Select(y) = select_node {
                            for expression_node in y {
                                if let RefNode::HierarchicalIdentifier(_) = expression_node {
                                    if let Some(right_node) =
                                        unwrap_node!(expression_node.clone(), Identifier)
                                    {
                                        right_index = identifier(right_node, syntax_tree).unwrap();
                                    } else {
                                        unreachable!()
                                    }
                                } else if let RefNode::IntegralNumber(_) = expression_node {
                                    if let Some(right_node) =
                                        unwrap_node!(expression_node.clone(), DecimalNumber)
                                    {
                                        right_index = get_string(right_node, syntax_tree).unwrap();
                                    } else {
                                        unreachable!()
                                    }
                                }
                            }
                        }
                    }
                    // Push connection to ret
                    if right_index.is_empty() {
                        // If no indexing
                        ret.push([left, right_name].to_vec());
                    } else {
                        // If there is indexing
                        let right = format!("{right_name}[{right_index}]");
                        ret.push([left, right].to_vec());
                    }
                } else {
                    ret.push([left, String::new()].to_vec());
                }
            }
            // Port connection by order
            RefNode::OrderedPortConnection(x) => {
                if let Some(right_node) = unwrap_node!(node.clone(), HierarchicalIdentifier) {
                    let right_name = identifier(right_node, syntax_tree).unwrap();
                    // TODO: Mutating a string is a bit dodgy here.
                    let mut right_index = String::new();
                    for select_node in x {
                        if let RefNode::Select(y) = select_node {
                            for expression_node in y {
                                if let RefNode::HierarchicalIdentifier(_) = expression_node {
                                    if let Some(right_node) =
                                        unwrap_node!(expression_node.clone(), Identifier)
                                    {
                                        right_index = identifier(right_node, syntax_tree).unwrap();
                                    } else {
                                        unreachable!()
                                    }
                                } else if let RefNode::IntegralNumber(_) = expression_node {
                                    if let Some(right_node) =
                                        unwrap_node!(expression_node.clone(), DecimalNumber)
                                    {
                                        right_index = get_string(right_node, syntax_tree).unwrap();
                                    } else {
                                        unreachable!()
                                    }
                                }
                            }
                        }
                    }
                    // Push connection to ret
                    if right_index.is_empty() {
                        // If no indexing
                        ret.push([right_name].to_vec());
                    } else {
                        // If there is indexing
                        let right = format!("{right_name}[{right_index}]");
                        ret.push([right].to_vec());
                    }
                }
            }
            _ => (),
        }
    }

    ret
}
