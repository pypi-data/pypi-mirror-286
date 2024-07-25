# puzzle-lib
A library for puzzle games.

## usage
```Rust
// import the library
use puzzle_lib::Puzzle;

fn main() {
    let puzzle = Puzzle::new(3, 3);
    // show the puzzle
    for i in 0..3{
        println!("{:?}", puzzle.puzzle[i]);
    }
    println!();
    // move the tile to the up
    puzzle.move_tile("U");
    // show the puzzle
    for i in 0..3{
        println!("{:?}", puzzle.puzzle[i]);
    }
}
```