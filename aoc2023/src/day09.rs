pub mod utils;

fn main() {
    let input = utils::read_input_lines("09");
    println!("--- Day 9: Mirage Maintenance ---");
    let part1_result = solve_part1(&input);
    println!("Part 1: {}", part1_result);
    let part2_result = solve_part2(&input);
    println!("Part 2: {}", part2_result);
}

pub fn solve_part1(input: &[String]) -> i32 {
    let mut next_values = Vec::new();

    for line in input.iter() {
        let mut last_values = Vec::new();
        let mut history = History::parse_line(line);

        while !history.all_zero() {
            last_values.push(history.0[history.0.len() - 1]);
            history = history.difference()
        }

        next_values.push(last_values.iter().sum())
    }

    return next_values.iter().sum();
}

pub fn solve_part2(input: &[String]) -> i32 {
    43
}

struct History(Vec<i32>);

impl History {
    fn parse_line(line: &str) -> History {
        let values: Vec<i32> = line
            .trim()
            .split_ascii_whitespace()
            .map(|v| v.parse().unwrap_or_else(|_| panic!("Cannot parse {:?}", v)))
            .collect();

        return History(values);
    }

    fn difference(&self) -> History {
        let mut new_values = Vec::new();
        for i in 0..(self.0.len() - 1) {
            new_values.push(self.0[i + 1] - self.0[i])
        }

        History(new_values)
    }

    fn all_zero(&self) -> bool {
        self.0.iter().all(|&x| x == 0)
    }
}

#[cfg(test)]
pub mod tests {
    use crate::{solve_part1, History};

    #[test]
    pub fn test_part1() {
        let input = "0 3 6 9 12 15
        1 3 6 10 15 21
        10 13 16 21 30 45"
            .lines()
            .map(|x| x.to_string())
            .collect::<Vec<String>>();

        let history = History::parse_line(&input[0]);
        assert_eq!(history.0[0], 0);
        assert_eq!(history.0[1], 3);

        assert_eq!(history.difference().0, vec![3, 3, 3, 3, 3]);
        assert_eq!(history.difference().difference().0, vec![0, 0, 0, 0]);
        assert_eq!(solve_part1(&input), 114);
    }
}
