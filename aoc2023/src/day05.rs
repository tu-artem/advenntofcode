pub mod utils;

fn main() {
    let input = utils::read_input("05");
    let part1_result = solve_part1(&input);
    println!("Part 1: {}", part1_result);
    let part2_result = solve_part2(&input);
    println!("Part 2: {}", part2_result);
}

pub struct Mapping {
    pub destination_start: u64,
    pub source_start: u64,
    pub length: u64,
}

impl Mapping {
    fn new(destination_start: u64, source_start: u64, length: u64) -> Mapping {
        Mapping {
            destination_start,
            source_start,
            length,
        }
    }

    fn from_string(s: &str) -> Mapping {
        let v: Vec<&str> = s.split_ascii_whitespace().collect();

        Mapping::new(
            v[0].parse().unwrap(),
            v[1].parse().unwrap(),
            v[2].parse().unwrap(),
        )
    }

    fn has_source(&self, source: u64) -> bool {
        source >= self.source_start && source < self.source_start + self.length
    }

    fn get_destination(&self, source: u64) -> u64 {
        if !self.has_source(source) {
            panic!("Source does not belong here!")
        }
        source + self.destination_start - self.source_start
    }
}

pub fn parse_input(input: &str) -> (Vec<u64>, Vec<Vec<Mapping>>) {
    let mut lines = input.lines();
    let seeds: Vec<u64> = lines
        .next()
        .unwrap()
        .replace("seeds:", "")
        .trim()
        .split_ascii_whitespace()
        .map(|x| x.parse::<u64>().unwrap())
        .collect();

    let mut mappings: Vec<Vec<Mapping>> = Vec::new();
    let mut current_mappings: Vec<Mapping> = Vec::new();
    for line in lines {
        // let trimmed = line.trim();
        if line.trim().is_empty() {
            continue;
        }
        if line.ends_with("map:") {
            if !current_mappings.is_empty() {
                mappings.push(current_mappings)
            }
            current_mappings = Vec::new();
        } else {
            let mapping = Mapping::from_string(line.trim());
            current_mappings.push(mapping);
        }
    }
    if !current_mappings.is_empty() {
        mappings.push(current_mappings)
    }

    (seeds, mappings)
}

pub fn find_locations(seeds: Vec<u64>, mappings: Vec<Vec<Mapping>>) -> Vec<u64> {
    let mut locations: Vec<u64> = Vec::new();
    for seed in seeds {
        let mut soil = seed;
        for mapping in &mappings[0] {
            if mapping.has_source(seed) {
                soil = mapping.get_destination(seed)
            }
        }
        let mut fertilizer = soil;
        for mapping in &mappings[1] {
            if mapping.has_source(soil) {
                fertilizer = mapping.get_destination(soil)
            }
        }
        let mut water = fertilizer;
        for mapping in &mappings[2] {
            if mapping.has_source(fertilizer) {
                water = mapping.get_destination(fertilizer)
            }
        }
        let mut light = water;
        for mapping in &mappings[3] {
            if mapping.has_source(water) {
                light = mapping.get_destination(water)
            }
        }
        let mut temperature = light;
        for mapping in &mappings[4] {
            if mapping.has_source(light) {
                temperature = mapping.get_destination(light)
            }
        }
        let mut humidity = temperature;
        for mapping in &mappings[5] {
            if mapping.has_source(temperature) {
                humidity = mapping.get_destination(temperature)
            }
        }
        let mut location = humidity;
        for mapping in &mappings[6] {
            if mapping.has_source(humidity) {
                location = mapping.get_destination(humidity)
            }
        }
        locations.push(location);
        // println!("{} - {} - {} - {} - {} - {} - {} - {}", seed, soil, fertilizer, water, light, temperature, humidity, location)
    }

    locations
}

pub fn solve_part1(input: &str) -> u64 {
    let (seeds, mappings) = parse_input(input);

    let locations = find_locations(seeds, mappings);

    *locations.iter().min().unwrap()
}

pub fn solve_part2(input: &str) -> u64 {
    42
}

#[cfg(test)]
pub mod tests {
    use crate::{parse_input, solve_part1, solve_part2, Mapping};

    #[test]
    fn test_part1_and_part2() {
        let input = "seeds: 79 14 55 13

        seed-to-soil map:
        50 98 2
        52 50 48
        
        soil-to-fertilizer map:
        0 15 37
        37 52 2
        39 0 15
        
        fertilizer-to-water map:
        49 53 8
        0 11 42
        42 0 7
        57 7 4
        
        water-to-light map:
        88 18 7
        18 25 70
        
        light-to-temperature map:
        45 77 23
        81 45 19
        68 64 13
        
        temperature-to-humidity map:
        0 69 1
        1 0 69
        
        humidity-to-location map:
        60 56 37
        56 93 4"
            .trim();

        let (seeds, mappings) = parse_input(input);

        assert_eq!(seeds, vec![79, 14, 55, 13]);
        assert_eq!(mappings.len(), 7);

        assert_eq!(solve_part1(input), 35);
        // assert_eq!(solve_part2(input), 46);
    }

    #[test]
    fn test_map() {
        let mapping = Mapping::new(52, 50, 48);

        assert!(mapping.has_source(50));
        assert!(mapping.has_source(97));
        assert!(!mapping.has_source(99));

        assert_eq!(mapping.get_destination(79), 81);
        assert_eq!(mapping.get_destination(55), 57);
    }
}
