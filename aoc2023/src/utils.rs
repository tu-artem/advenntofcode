use std::{
    fs::File,
    io::{BufRead, BufReader, Read},
};

pub fn read_input_lines(day: &str) -> Vec<String> {
    let path = "input/day".to_string() + day + ".txt";
    let file = File::open(path).expect("no such file");
    let buf = BufReader::new(file);
    buf.lines()
        .map(|l| l.expect("Could not parse line"))
        .collect()
}

pub fn read_input(day: &str) -> String {
    let path = "input/day".to_string() + day + ".txt";
    let file = File::open(path).expect("no such file");
    let mut buf = BufReader::new(file);
    let mut str = String::new();
    buf.read_to_string(&mut str).expect("cannot read string");

    str
}
