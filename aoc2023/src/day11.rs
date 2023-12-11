use std::result;

pub mod utils;

fn main() {
    println!("--- Day 11: Cosmic Expansion ---");
    let input = utils::read_input_lines("11");
    let part1_result = solve_part1(&input);
    println!("Part 1: {}", part1_result);
    let part2_result = solve_part2(&input, 1_000_000);
    println!("Part 2: {}", part2_result);
}

pub fn solve_part1(input: &[String]) -> u64 {
    let grid = parse_input(input);
    let expanded_grid = expand_grid(&grid);

    let mut universes: Vec<(usize, usize)> = Vec::new();

    for (y, row) in expanded_grid.iter().enumerate() {
        for (x, val) in row.iter().enumerate() {
            if val == &'#' {
                universes.push((x, y))
            }
        }
    }

    let mut total_distance = 0;

    for (x1, y1) in universes.iter() {
        for (x2, y2) in universes.iter() {
            if x1 == x2 && y1 == y2 {
                continue;
            }
            let distance = x1.abs_diff(*x2) + y1.abs_diff(*y2);
            total_distance += distance;
        }
    }

    total_distance as u64 / 2
}

pub fn solve_part2(input: &[String], expansion_factor: u64) -> u64 {
    let grid = parse_input(input);

    let mut universes: Vec<(usize, usize)> = Vec::new();

    for (y, row) in grid.iter().enumerate() {
        for (x, val) in row.iter().enumerate() {
            if val == &'#' {
                universes.push((x, y))
            }
        }
    }
    let empty_rows = empty_rows(&grid);
    let empty_cols = empty_cols(&grid);

    let mut total_distance = 0;

    for (x1, y1) in universes.iter() {
        for (x2, y2) in universes.iter() {
            if x1 == x2 && y1 == y2 {
                continue;
            }
            let mut distance = 0;
            let x_range = if x1 <= x2 { *x1..*x2 } else { *x2..*x1 };
            for x in x_range {
                if empty_cols.contains(&x) {
                    distance += expansion_factor
                } else {
                    distance += 1
                }
            }
            let y_range = if y1 <= y2 { *y1..*y2 } else { *y2..*y1 };
            for x in y_range {
                if empty_rows.contains(&x) {
                    distance += expansion_factor
                } else {
                    distance += 1
                }
            }

            total_distance += distance;
        }
    }

    total_distance as u64 / 2
}

pub fn parse_input(input: &[String]) -> Vec<Vec<char>> {
    let mut result = Vec::new();
    for line in input {
        result.push(line.trim().chars().collect::<Vec<char>>())
    }

    result
}

pub fn empty_rows(grid: &Vec<Vec<char>>) -> Vec<usize> {
    let mut result = Vec::new();
    for (index, row) in grid.iter().enumerate() {
        if row.iter().all(|&c| c == '.') {
            result.push(index)
        }
    }

    result
}

pub fn empty_cols(grid: &Vec<Vec<char>>) -> Vec<usize> {
    let mut result = Vec::new();

    for col_idx in 0..grid[0].len() {
        let col: Vec<char> = grid.iter().map(|l| l[col_idx]).collect();
        if col.iter().all(|&c| c == '.') {
            result.push(col_idx)
        }
    }

    result
}

pub fn expand_grid(grid: &Vec<Vec<char>>) -> Vec<Vec<char>> {
    let empty_rows = empty_rows(&grid);
    let empty_cols = empty_cols(&grid);

    let mut expanded_grid = Vec::new();
    for (y, row) in grid.iter().enumerate() {
        let mut new_row = Vec::new();
        for (x, val) in row.iter().enumerate() {
            if empty_cols.contains(&x) {
                new_row.push(*val);
            }
            new_row.push(*val);
        }
        if empty_rows.contains(&y) {
            expanded_grid.push(new_row.clone())
        }
        expanded_grid.push(new_row)
    }

    expanded_grid
}

#[cfg(test)]
pub mod tests {
    use crate::{empty_cols, empty_rows, expand_grid, parse_input, solve_part1, solve_part2};

    #[test]
    pub fn test_part1() {
        let input = "...#......
        .......#..
        #.........
        ..........
        ......#...
        .#........
        .........#
        ..........
        .......#..
        #...#....."
            .lines()
            .map(|x| x.to_string())
            .collect::<Vec<String>>();

        let grid = parse_input(&input);
        assert_eq!(grid.len(), 10);
        assert_eq!(grid[0].len(), 10);

        assert_eq!(empty_rows(&grid), vec![3, 7]);
        assert_eq!(empty_cols(&grid), vec![2, 5, 8]);

        let expanded_grid = expand_grid(&grid);

        assert_eq!(expanded_grid.len(), 12);
        assert_eq!(expanded_grid[5].len(), 13);
        assert_eq!(expanded_grid[5][8], '#');
        assert_eq!(expanded_grid[5][9], '.');

        assert_eq!(solve_part1(&input), 374);
        assert_eq!(solve_part2(&input, 2), 374);
        assert_eq!(solve_part2(&input, 10), 1030);
        assert_eq!(solve_part2(&input, 100), 8410);
    }
}
