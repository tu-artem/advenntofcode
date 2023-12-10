use std::io::SeekFrom;

pub mod utils;

fn main() {
    println!("--- Day 10: Pipe Maze ---");
    let input = utils::read_input_lines("10");
    let part1_result = solve_part1(&input);
    println!("Part 1: {}", part1_result);
    let part2_result = solve_part2(&input);
    println!("Part 2: {}", part2_result);
}

pub fn solve_part1(input: &[String]) -> u32 {
    let grid = Grid::from_input(input);

    let mut position1 = grid.start_position.clone();
    let mut position2 = grid.start_position.clone();

    // TODO: write this in code))
    position1.dx = -1;
    position2.dy = 1;

    let mut n_steps = 0;
    loop {
        position1.move_();
        let next_pipe_1 = &grid.values[position1.y as usize][position1.x as usize];
        position1.update_directions(next_pipe_1.value);

        position2.move_();
        let next_pipe_2 = &grid.values[position2.y as usize][position2.x as usize];
        position2.update_directions(next_pipe_2.value);
        n_steps += 1;
        if position1.x == position2.x && position1.y == position2.y {
            break;
        }
    }

    n_steps
}

pub fn solve_part2(input: &[String]) -> u32 {
    43
}

pub struct Pipe {
    pub value: char,
}

pub struct Grid {
    pub values: Vec<Vec<Pipe>>,
    pub start_position: Position,
}

#[derive(Clone)]
pub struct Position {
    pub x: i32,
    pub y: i32,
    pub dx: i32,
    pub dy: i32,
}

impl Position {
    pub fn new(x: i32, y: i32) -> Position {
        Position { x, y, dx: 0, dy: 0 }
    }

    pub fn move_(&mut self) -> &mut Self {
        self.x += self.dx;
        self.y += self.dy;
        self
    }
    pub fn update_directions(&mut self, c: char) -> &mut Self {
        match c {
            // L   dx=+1, dy=+1
            // F   dx=+1, dy=-1
            // 7   dx=-1, dy=-1
            // J   dx=-1, dy=+1
            // -   dx+=0, dy=+0
            // |   dx+=0, dy=+0
            'L' => {
                self.dx += 1;
                self.dy += 1
            }
            'F' => {
                self.dx += 1;
                self.dy += -1
            }
            '7' => {
                self.dx += -1;
                self.dy += -1
            }
            'J' => {
                self.dx += -1;
                self.dy += 1
            }
            '-' | '|' => {}
            '.' => panic!("We are outside the pipe, something is wrong!"),
            x => panic!("Uknown ttype {}", x),
        }

        self
    }
}

impl Grid {
    pub fn from_input(input: &[String]) -> Grid {
        let mut values = Vec::new();
        let mut start_position = Position::new(-1, -1);
        for (y, line) in input.iter().rev().enumerate() {
            let mut line_values: Vec<Pipe> = Vec::new();
            for (x, value) in line.trim().chars().enumerate() {
                line_values.push(Pipe { value });
                if value == 'S' {
                    start_position = Position::new(x as i32, y as i32)
                }
            }
            values.push(line_values);
        }

        Grid {
            values,
            start_position,
        }
    }
}

#[cfg(test)]
pub mod tests {
    use crate::{solve_part1, Grid};

    #[test]
    pub fn test_part1() {
        let input = "-L|F7
        7S-7|
        L|7||
        -L-J|
        L|-JF"
            .lines()
            .map(|x| x.to_string())
            .collect::<Vec<String>>();
        let grid = Grid::from_input(&input);
        assert_eq!(grid.values.len(), 5);
        assert_eq!(grid.start_position.x, 1);
        assert_eq!(grid.start_position.y, 3);

        let mut position1 = grid.start_position.clone();
        let mut position2 = grid.start_position.clone();

        position1.dx = 1;
        position1.move_();
        assert_eq!(position1.x, 2);
        let next_pipe = &grid.values[position1.y as usize][position1.x as usize];
        assert_eq!(next_pipe.value, '-');
        position1.update_directions(next_pipe.value);
        position1.move_();
        let next_pipe = &grid.values[position1.y as usize][position1.x as usize];
        assert_eq!(next_pipe.value, '7');
        position1.update_directions(next_pipe.value);
        position1.move_();
        assert_eq!(position1.x, 3);
        assert_eq!(position1.y, 2);
    }
}
