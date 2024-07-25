use rand::Rng;
use std::time::{SystemTime, UNIX_EPOCH};

const DIRECTION_DIST: phf::Map<&'static str, [i32; 2]> = phf::phf_map! {
    "U" => [-1, 0],
    "D" => [1, 0],
    "L" => [0, -1],
    "R" => [0, 1]
};

const DIRECTION_LIST: [&str; 4] = ["U", "D", "L", "R"];


pub struct Puzzle {
    pub cmds_str: String,
    pub mode: usize,
    pub puzzle: Vec<Vec<i32>>,
    correct_puzzle: Vec<Vec<i32>>,
    pub start_time: u128,
    pub end_time: u128,
}

impl Puzzle {
    pub fn new(mode: usize) -> Self {
        let mut puzzle = vec![vec![0; mode]; mode];
        let mut correct_puzzle = vec![vec![0; mode]; mode];
        let mut num = 1;

        for i in 0..mode {
            for j in 0..mode {
                puzzle[i][j] = num;
                correct_puzzle[i][j] = num;
                num += 1;
            }
        }

        puzzle[mode - 1][mode - 1] = 0;
        correct_puzzle[mode - 1][mode - 1] = 0;

        let start_time = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .expect("Time went backwards")
            .as_millis();

        let mut instance = Puzzle {
            cmds_str: String::new(),
            mode,
            puzzle,
            correct_puzzle,
            start_time,
            end_time: 0,
        };

        instance.shuffle();
        instance
    }

    fn find_0(&self) -> Option<(usize, usize)> {
        for (i, row) in self.puzzle.iter().enumerate() {
            for (j, &value) in row.iter().enumerate() {
                if value == 0 {
                    return Some((i, j));
                }
            }
        }
        None
    }

    pub fn move_tile<'a>(&'a mut self, direction: &'a str) -> &str {
        self.cmds_str.push_str(direction);
        if let Some((r, c)) = self.find_0() {
            if (r == 0 && direction == "U")
                || (r == self.mode - 1 && direction == "D")
                || (c == 0 && direction == "L")
                || (c == self.mode - 1 && direction == "R")
            {
                return "";
            }

            if let Some(&[dr, dc]) = DIRECTION_DIST.get(direction) {
                let rr = (r as i32 + dr) as usize;
                let cc = (c as i32 + dc) as usize;

                let num1 = self.puzzle[rr][cc];
                self.puzzle[r][c] = num1;
                self.puzzle[rr][cc] = 0;
                return direction;
            }
        }
        ""
    }

    pub fn check(&mut self) -> bool {
        for i in 0..self.mode {
            for j in 0..self.mode {
                if self.puzzle[i][j] != self.correct_puzzle[i][j] {
                    return false;
                }
            }
        }
        self.end_time = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .expect("Time went backwards")
            .as_millis();
        true
    }

    pub fn move_sequence(&mut self, sequence: &str) -> bool {
        let uppercase = sequence.to_uppercase();
        self.cmds_str.clear();
        for command in uppercase.chars() {
            let command_str = command.to_string();
            let _ = self.move_tile(&command_str);

            if self.check() {
                return true;
            }
        }
        false
    }

    pub fn shuffle(&mut self) {
        let mut rng = rand::thread_rng();
        for _ in 0..1000 {
            let random_direction = DIRECTION_LIST[rng.gen_range(0..4)];
            self.move_tile(random_direction);
        }
    }

    pub fn duration(&self) -> String {
        let time_now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .expect("Time went backwards")
            .as_millis();
        let duration = time_now - self.start_time;
        self.format_duration(duration)
    }

    fn format_duration(&self, duration: u128) -> String {
        let hours = duration / 3600000;
        let minutes = (duration % 3600000) / 60000;
        let seconds = (duration % 60000) / 1000;
        format!("{}:{}:{}", hours, minutes, seconds)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_works() {
        let puzzle = Puzzle::new(4);
        for i in 0..4{
            println!("{:?}", puzzle.puzzle[i]);
        }
        println!();
        assert_eq!(puzzle.puzzle.len(), 4);
    }

    #[test]
    fn it_works_mode3() {
        let mut puzzle = Puzzle::new(3);
        for i in 0..3{
            println!("{:?}", puzzle.puzzle[i]);
        }
        println!();
        puzzle.move_tile("U");
        for i in 0..3{
            println!("{:?}", puzzle.puzzle[i]);
        }
        println!();
        assert_eq!(puzzle.puzzle.len(), 3);
    }
}
