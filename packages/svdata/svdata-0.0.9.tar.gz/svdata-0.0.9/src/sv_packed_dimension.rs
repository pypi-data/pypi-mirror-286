use pyo3::prelude::*;
use std::fmt;

/// Packed dimensions.
/// The first element is the left bound, the second is the right bound.
/// Packed dimensions with left and right bounds.
#[derive(Debug, Clone, PartialEq)]
#[pyclass]
pub struct SvPackedDimension {
    #[pyo3(get, set)]
    pub left_bound: String,
    #[pyo3(get, set)]
    pub right_bound: String,
}

#[pymethods]
impl SvPackedDimension {
    #[new]
    fn new(left_bound: String, right_bound: String) -> Self {
        SvPackedDimension {
            left_bound,
            right_bound,
        }
    }

    fn __repr__(&self) -> String {
        self.to_string()
    }
}

impl fmt::Display for SvPackedDimension {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "[{}:{}]", self.left_bound, self.right_bound)
    }
}
