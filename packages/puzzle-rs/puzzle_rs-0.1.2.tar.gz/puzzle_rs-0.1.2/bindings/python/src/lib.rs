use pyo3::prelude::*;
use puzzle_lib::Puzzle;

#[pyclass]
pub struct PuzzleCore {
    inner: Puzzle
}

#[pymethods]
impl PuzzleCore {
    #[new]
    pub fn new(mode: usize) -> Self {
        PuzzleCore {
            inner: Puzzle::new(mode),
        }
    }
    pub fn move_sequence(&mut self, sequence: &str) -> bool {
        self.inner.move_sequence(sequence)
    }
    
    pub fn get_puzzle(&self) -> Vec<Vec<i32>> {
        self.inner.puzzle.clone()
    }

    pub fn move_tile<'a>(&'a mut self, direction: &'a str) -> &str {
        self.inner.move_tile(direction)
    }
    
    pub fn duration(&self) -> String {
        self.inner.duration()
    }
    
    pub fn get_cmds_str(&self) -> String {
        self.inner.cmds_str.clone()
    }
    
    pub fn get_mode(&self) -> usize {
        self.inner.mode
    }
}

#[pymodule]
fn puzzle_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PuzzleCore>()?;
    Ok(())
}