use pyo3::prelude::*;
use std::fmt;

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
        self.to_string()
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
