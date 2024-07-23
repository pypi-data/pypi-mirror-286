use pyo3::prelude::*;
use std::fmt;

/// Net types.
///
/// Args:
///     Wire (str): A wire.
///     Uwire (str): An uwire.
///     Tri (str): A tri.
///     Wor (str): A wor.
///     Wand (str): A wand.
///     Triand (str): A triand.
///     Trior (str): A trior.
///     Trireg (str): A trireg.
///     Tri0 (str): A tri0.
///     Tri1 (str): A tri1.
///     Supply0 (str): A supply0.
///     Supply1 (str): A supply1.
///     IMPLICIT (str): An implicit net type.
#[derive(Debug, Clone, PartialEq)]
#[pyclass(eq, eq_int)]
pub enum SvNetType {
    Wire,
    Uwire,
    Tri,
    Wor,
    Wand,
    Triand,
    Trior,
    Trireg,
    Tri0,
    Tri1,
    Supply0,
    Supply1,
    IMPLICIT,
}

#[pymethods]
impl SvNetType {
    fn __repr__(&self) -> String {
        self.to_string()
    }
}

impl fmt::Display for SvNetType {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            SvNetType::Wire => write!(f, "Wire"),
            SvNetType::Uwire => write!(f, "Uwire"),
            SvNetType::Tri => write!(f, "Tri"),
            SvNetType::Wor => write!(f, "Wor"),
            SvNetType::Wand => write!(f, "Wand"),
            SvNetType::Triand => write!(f, "Triand"),
            SvNetType::Trior => write!(f, "Trior"),
            SvNetType::Trireg => write!(f, "Trireg"),
            SvNetType::Tri0 => write!(f, "Tri0"),
            SvNetType::Tri1 => write!(f, "Tri1"),
            SvNetType::Supply0 => write!(f, "Supply0"),
            SvNetType::Supply1 => write!(f, "Supply1"),
            SvNetType::IMPLICIT => write!(f, "IMPLICIT"),
        }
    }
}
