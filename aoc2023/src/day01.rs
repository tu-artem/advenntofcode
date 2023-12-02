pub mod utils;

fn main() {
    let input = utils::read_input_lines("01");
    let part1_result = part1(&input);
    println!("Part 1: {}", part1_result);
    let part2_result = part2(&input);
    println!("Part 2: {}", part2_result);
}

fn part1(input: &[String]) -> u32 {
    input.iter().map(|x| calibration_value(x.as_str())).sum()
}

fn part2(input: &[String]) -> u32 {
    input
        .iter()
        .map(|x| calibration_value_two(x.as_str()))
        .sum()
}

fn calibration_value(s: &str) -> u32 {
    let first_digit = s
        .chars()
        .find(|x| x.is_ascii_digit())
        .expect("No digits in string!");
    let last_digit = s
        .chars()
        .rev()
        .find(|x| x.is_ascii_digit())
        .expect("No digits in string!");

    let mut cv = String::new();
    cv.push(first_digit);
    cv.push(last_digit);

    cv.parse::<u32>().unwrap()
}

fn calibration_value_two(s: &str) -> u32 {
    let valid_digits = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "1", "2",
        "3", "4", "5", "6", "7", "8", "9",
    ];

    let indices: Vec<_> = valid_digits
        .map(|x| s.match_indices(x).collect::<Vec<_>>())
        .into_iter()
        .flatten()
        .collect();

    let first_value = indices.iter().min_by(|x, y| x.0.cmp(&y.0)).unwrap().1;

    let last_value = indices.iter().max_by(|x, y| x.0.cmp(&y.0)).unwrap().1;

    let first_value = valid_digits.iter().position(|&x| x == first_value).unwrap();
    let last_value = valid_digits.iter().position(|&x| x == last_value).unwrap();

    let first_digit = if first_value <= 9 {
        first_value.to_string()
    } else {
        valid_digits[first_value].to_string()
    };
    let last_digit = if last_value <= 9 {
        last_value.to_string()
    } else {
        valid_digits[last_value].to_string()
    };

    let mut cv = String::new();
    cv.push_str(&first_digit);
    cv.push_str(&last_digit);

    cv.parse::<u32>().unwrap()
}

#[cfg(test)]
mod tests {
    use crate::{calibration_value, calibration_value_two, part1};

    #[test]
    fn test_part1() {
        let input = "1abc2
        pqr3stu8vwx
        a1b2c3d4e5f
        treb7uchet"
            .to_string()
            .lines()
            .map(|x| x.to_string())
            .collect::<Vec<String>>();

        let result = part1(&input);
        assert_eq!(result, 142);
    }
    #[test]
    fn test_calibration_value() {
        assert_eq!(calibration_value("1abc2"), 12);
        assert_eq!(calibration_value("pqr3stu8vwx"), 38);
        assert_eq!(calibration_value("a1b2c3d4e5f"), 15);
        assert_eq!(calibration_value("treb7uchet"), 77);
        assert_eq!(calibration_value("11"), 11);
        assert_eq!(calibration_value("7"), 77);
    }

    #[test]
    fn test_calibration_value_two() {
        assert_eq!(calibration_value_two("1abc2"), 12);
        assert_eq!(calibration_value_two("pqr3stu8vwx"), 38);
        assert_eq!(calibration_value_two("a1b2c3d4e5f"), 15);
        assert_eq!(calibration_value_two("treb7uchet"), 77);
        assert_eq!(calibration_value_two("11"), 11);
        assert_eq!(calibration_value_two("oneone"), 11);
        assert_eq!(calibration_value_two("onetwoone"), 11);
        assert_eq!(calibration_value_two("sevenseven"), 77);

        assert_eq!(calibration_value_two("two1nine"), 29);
        assert_eq!(calibration_value_two("eightwothree"), 83);
        assert_eq!(calibration_value_two("abcone2threexyz"), 13);
        assert_eq!(calibration_value_two("xtwone3four"), 24);
        assert_eq!(calibration_value_two("4nineeightseven2"), 42);
        assert_eq!(calibration_value_two("zoneight234"), 14);
        assert_eq!(calibration_value_two("7pqrstsixteen"), 76);
    }
}
