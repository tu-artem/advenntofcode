pub mod utils;

fn main() {
    println!("It's day 3!");
    let input = utils::read_input_lines("03");
    let part1_result = part1(&input);
    println!("Part 1: {}", part1_result);
    let part2_result = part2(&input);
    println!("Part 2: {}", part2_result);
}

pub struct Symbol {
    pub x: isize,
    pub y: isize,
    pub value: char,
}

impl Symbol {
    pub fn is_gear(&self) -> bool {
        self.value == '*'
    }
}

pub struct Number {
    pub x: isize,
    pub y: isize,
    pub len: usize,
    pub value: u32,
}

pub struct Grid {
    pub numbers: Vec<Number>,
    pub symbols: Vec<Symbol>,
}

impl Grid {
    pub fn new() -> Self {
        Grid {
            numbers: Vec::new(),
            symbols: Vec::new(),
        }
    }

    // pub fn extend(&mut self, other: &mut Grid) {
    //     self.numbers.append(&mut other.numbers);
    //     self.symbols.append(&mut other.symbols);
    // }
}

pub fn parse_lines(lines: &Vec<String>) -> Grid {
    let mut grid = Grid::new();
    for (y, line) in lines.into_iter().enumerate() {
        let mut buff = String::new();
        for (x, c) in line.trim().char_indices() {
            if c == '.' {
                if buff.len() > 0 {
                    let number = Number {
                        x: (x - buff.len()) as isize,
                        y: y as isize,
                        len: buff.len(),
                        value: buff.parse::<u32>().unwrap(),
                    };
                    grid.numbers.push(number);
                    buff.clear();
                }
                continue;
            } else if c.is_ascii_digit() {
                buff.push(c);
            } else {
                // c is a Symbol
                let symbol = Symbol {
                    x: x as isize,
                    y: y as isize,
                    value: c,
                };
                grid.symbols.push(symbol);
                if buff.len() > 0 {
                    let number = Number {
                        x: (x - buff.len()) as isize,
                        y: y as isize,
                        len: buff.len(),
                        value: buff.parse::<u32>().unwrap(),
                    };
                    grid.numbers.push(number);
                    buff.clear();
                }
            }
        }
        if buff.len() > 0 {
            let number = Number {
                x: (line.trim().len() - buff.len()) as isize,
                y: y as isize,
                len: buff.len(),
                value: buff.parse::<u32>().unwrap(),
            };
            grid.numbers.push(number);
            buff.clear();
        }
    }
    grid
}

pub fn is_adjacent(n: &Number, s: &Symbol) -> bool {
    if n.y.abs_diff(s.y) <= 1 && (-1 <= s.x - n.x && s.x - n.x <= n.len as isize) {
        return true;
    }

    false
}

pub fn part1(input: &Vec<String>) -> u32 {
    let grid = parse_lines(&input);
    let mut sum = 0;

    for n in grid.numbers.iter() {
        for s in grid.symbols.iter() {
            if is_adjacent(n, s) {
                sum += n.value;
            }
        }
    }
    sum
}

pub fn part2(input: &Vec<String>) -> u32 {
    let grid = parse_lines(&input);
    let mut sum = 0;

    for s in grid.symbols.iter() {
        if s.is_gear() {
            let mut adjusents = Vec::new();
            for n in grid.numbers.iter() {
                if is_adjacent(n, s) {
                    adjusents.push(n);
                }
            }
            if adjusents.len() == 2 {
                let power = adjusents[0].value * adjusents[1].value;
                sum += power
            }
        }
    }
    sum
}

mod tests {
    use crate::{is_adjacent, parse_lines, part1, part2, Number, Symbol};

    #[test]
    fn test_all() {
        let input = "467..114..
        ...*......
        ..35..633.
        ......#...
        617*......
        .....+.58.
        ..592.....
        ......755.
        ...$.*....
        .664.598.."
            .lines()
            .map(|x| x.to_string())
            .collect::<Vec<String>>();

        let result = part1(&input);
        assert_eq!(result, 4361);

        let result2 = part2(&input);
        assert_eq!(result2, 467835);
    }

    #[test]
    fn test_adjusent() {
        let n = Number {
            x: 0,
            y: 0,
            len: 3,
            value: 123,
        };
        let s = Symbol {
            x: 2,
            y: 1,
            value: '*',
        };

        assert!(is_adjacent(&n, &s));
    }
}
