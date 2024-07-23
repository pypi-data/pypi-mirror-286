use pyo3::prelude::*;
use std::fmt;

/// Unpacked dimensions with optional right bound.
#[derive(Debug, Clone, PartialEq)]
#[pyclass]
pub struct SvUnpackedDimension {
    #[pyo3(get, set)]
    pub left_bound: String,
    #[pyo3(get, set)]
    pub right_bound: Option<String>,
}

#[pymethods]
impl SvUnpackedDimension {
    #[new]
    #[pyo3(signature = (left_bound, right_bound=None))]
    fn new(left_bound: String, right_bound: Option<String>) -> Self {
        SvUnpackedDimension {
            left_bound,
            right_bound,
        }
    }

    fn __repr__(&self) -> String {
        self.to_string()
    }
}

impl fmt::Display for SvUnpackedDimension {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match &self.right_bound {
            Some(right) => write!(f, "[{}:{}]", self.left_bound, right),
            None => write!(f, "[{}]", self.left_bound),
        }
    }
}
