use std::{
    fs::File,
    io::{BufRead, BufReader},
};

pub fn read_input_lines(day: &str) -> Vec<String> {
    let path = "input/day".to_string() + day + ".txt";
    let file = File::open(path).expect("no such file");
    let buf = BufReader::new(file);
    buf.lines()
        .map(|l| l.expect("Could not parse line"))
        .collect()
}
