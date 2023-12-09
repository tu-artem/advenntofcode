pub mod utils;

fn main() {
    let input = utils::read_input_lines("05");
    let part1_result = solve_part1(&input);
    println!("Part 1: {}", part1_result);
    let part2_result = solve_part2(&input);
    println!("Part 2: {}", part2_result);
}

pub fn solve_part1(input: &[String]) -> u32 {
    42
}

pub fn solve_part2(input: &[String]) -> u32 {
    43
}

#[cfg(test)]
pub mod tests {
    #[test]
    pub fn test_part1() {
        let input = "0 3 6 9 12 15
        1 3 6 10 15 21
        10 13 16 21 30 45"
            .lines()
            .map(|x| x.to_string())
            .collect::<Vec<String>>();
    }
}