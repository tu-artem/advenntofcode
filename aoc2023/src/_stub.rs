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
    
}