use pyo3::prelude::*;
use rayon::prelude::*;
use regex::Regex;

/// This item will get inited with a list of patterns from the JSON file.
#[pyclass(name = "RegexEngine")]
pub struct RegexEngine {
    raw_patterns: Vec<String>,
    compiled_patterns: Vec<Regex>,
}

#[pymethods]
impl RegexEngine {
    /// Creates a new `RegexEngine` object.
    ///
    /// Parallization is done using the `rayon` crate.
    ///
    /// ### Arguments
    /// * `raw_patterns` - A list of raw Regex patterns to compile.
    #[new]
    fn new() -> Self {
        RegexEngine {
            raw_patterns: Vec::new(),
            compiled_patterns: Vec::new(),
        }
    }

    /// Adds a list of patterns to the `RegexEngine` object.
    /// The patterns are compiled and stored in the object.
    ///
    /// ### Arguments
    /// * `patterns` - A list of raw Regex patterns to compile.
    /// * `escape` - A boolean flag to escape the patterns before compiling.
    ///
    /// ### Returns
    /// The number of patterns that were successfully compiled.
    fn add_patterns(&mut self, patterns: Vec<String>, escape: bool) -> PyResult<usize> {
        let compiled_patterns: Vec<Regex> = patterns
            .par_iter()
            .filter_map(|pattern| {
                let pattern = if escape {
                    regex::escape(pattern)
                } else {
                    pattern.clone()
                };
                Regex::new(&pattern).ok()
            })
            .collect();

        let total_compiled_patterns: usize = compiled_patterns.len();

        self.raw_patterns.extend(patterns);
        self.compiled_patterns.extend(compiled_patterns);

        Ok(total_compiled_patterns)
    }

    /// Returns the raw patterns that were compiled.
    ///
    /// ### Returns
    /// A list of raw patterns that were compiled.
    /// The order of the patterns is the same as the order of the compiled patterns.
    /// The indexes of the raw patterns and the compiled patterns match.
    #[getter]
    fn raw_patterns(&self) -> Vec<String> {
        self.raw_patterns.clone()
    }

    /// Runs the compiled patterns against the provided content.
    ///
    /// ### Arguments
    /// * `content` - The content to match against.
    ///     
    /// ### Returns
    /// A list of indexes of the patterns that matched the content.
    fn search(&self, content: String) -> Vec<usize> {
        self.compiled_patterns
            .par_iter()
            .enumerate()
            .filter_map(|(index, regex)| {
                if regex.is_match(&content) {
                    return Some(index);
                }
                None
            })
            .collect()
    }
}

#[pymodule]
#[pyo3(name = "simple_fast_regex")]
fn simple_fast_regex(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<RegexEngine>()?;
    Ok(())
}
