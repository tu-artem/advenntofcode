pub mod utils;
use itertools::Itertools;

fn main() {
    println!("--- Day 12: Hot Springs ---");
    let input = utils::read_input_lines("12");
    let part1_result = solve_part1(&input);
    println!("Part 1: {}", part1_result);
    let part2_result = solve_part2(&input);
    println!("Part 2: {}", part2_result);
}

pub fn solve_part1(input: &[String]) -> u32 {
    let entries: Vec<Entry> = input.iter().map(|line| parse_line(line)).collect();

    entries.iter().map(|e| e.variants().len()).sum::<usize>() as u32
}

pub fn solve_part2(input: &[String]) -> u32 {
    43
}

pub struct Entry {
    pub springs: Vec<char>,
    pub groups: Vec<u8>,
}

impl Entry {
    pub fn is_valid(&self) -> bool {
        if self.springs.iter().any(|&s| s == '?') {
            return false;
        }

        let mut consecutive_damage = self
            .springs
            .iter()
            .scan(0, |state, &x| {
                if x == '#' {
                    *state += 1
                } else {
                    *state = 0
                };
                Some(*state)
            })
            .peekable();

        let mut result = Vec::new();
        while let Some(val) = consecutive_damage.next() {
            if consecutive_damage.peek() == Some(&0) && val != 0 {
                result.push(val)
            }
            if consecutive_damage.peek() == None && val != 0 {
                result.push(val)
            }
        }

        result == self.groups
    }

    pub fn n_unknown(&self) -> usize {
        self.springs.iter().filter(|&s| s == &'?').count()
    }

    pub fn variants(&self) -> Vec<Entry> {
        let mut result: Vec<Entry> = Vec::new();
        let n_unknown = self.n_unknown();

        let values = vec!['.', '#'];
        let it = itertools::repeat_n(values.iter(), n_unknown).multi_cartesian_product();
        for group in it {
            let mut group_iter = group.iter();
            let variant: Vec<char> = self
                .springs
                .iter()
                .map(|&v| {
                    if v == '?' {
                        **group_iter.next().unwrap()
                    } else {
                        v
                    }
                })
                .collect();
            let entry = Entry {
                springs: variant,
                groups: self.groups.clone(),
            };
            if entry.is_valid() {
                result.push(entry)
            }
        }
        result
    }
}

pub fn parse_line(line: &str) -> Entry {
    let (springs, groups) = line.trim().split_once(' ').unwrap();

    Entry {
        springs: springs.chars().collect(),
        groups: groups
            .split(',')
            .map(|f| f.trim().parse::<u8>().unwrap())
            .collect(),
    }
}

#[cfg(test)]
pub mod tests {
    use crate::{parse_line, solve_part1, Entry};

    #[test]
    pub fn test_part1() {
        let correct_input = "#.#.### 1,1,3
        .#...#....###. 1,1,3
        .#.###.#.###### 1,3,1,6
        ####.#...#... 4,1,1
        #....######..#####. 1,6,5
        .###.##....# 3,2,1"
            .lines()
            .map(|x| x.to_string())
            .collect::<Vec<String>>();

        let entries: Vec<Entry> = correct_input.iter().map(|x| parse_line(x)).collect();
        assert_eq!(entries[0].groups, vec![1, 1, 3]);
        assert!(entries[0].is_valid());
        assert!(entries[2].is_valid());
        assert!(entries[3].is_valid());
        assert!(entries[4].is_valid());
        assert!(entries[5].is_valid());

        let invalid = ".#...#....###. 1,1,2";
        let invalid_entry = parse_line(invalid);
        assert!(!invalid_entry.is_valid());

        let input_with_unknowns = "???.### 1,1,3
        .??..??...?##. 1,1,3
        ?#?#?#?#?#?#?#? 1,3,1,6
        ????.#...#... 4,1,1
        ????.######..#####. 1,6,5
        ?###???????? 3,2,1"
            .lines()
            .map(|x| x.to_string())
            .collect::<Vec<String>>();

        let entries: Vec<Entry> = input_with_unknowns.iter().map(|x| parse_line(x)).collect();
        assert_eq!(entries[0].n_unknown(), 3);
        assert_eq!(entries[1].n_unknown(), 5);

        assert_eq!(entries[0].variants().len(), 1);
        assert_eq!(entries[5].variants().len(), 10);

        assert_eq!(solve_part1(&input_with_unknowns), 21);
    }
}
