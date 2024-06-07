use pyo3::prelude::*;

mod builder;
mod html;
mod wu;


use builder::build_htmldiff;

#[pyfunction]
fn _htmldiff(a: &str, b: &str) -> String {
    let mut diff = String::new();
    build_htmldiff(a, b, |s: &str| diff.push_str(s));
    diff
}

#[pymodule]
#[pyo3(name="htmldiff")]
fn htmldiff(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(_htmldiff, m)?)?;
    Ok(())
}
