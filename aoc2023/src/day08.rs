use std::collections::HashMap;
pub mod utils;

fn main() {
    let input = utils::read_input_lines("08");
    let part1_result = solve_part1(&input);
    println!("Part 1: {}", part1_result);
    let part2_result = solve_part2(&input);
    println!("Part 2: {:?}", part2_result);
}

pub fn solve_part1(input: &[String]) -> u32 {
    let mut network = HashMap::new();
    let instructions = Instructions::parse_line(&input[0]);

    for line in &input[2..] {
        let node = Node::parse_line(line);
        network.insert(node.key.clone(), node);
    }

    let mut current = network.get("AAA").unwrap();
    let mut n_steps = 0;

    for index in instructions.0.iter().cycle() {
        let next = &current.elements[*index as usize];
        current = network.get(next).unwrap();
        n_steps += 1;
        if current.key == "ZZZ" {
            break;
        }
    }

    return n_steps;
}

pub fn solve_part2(input: &[String]) -> Vec<u32> {
    let mut network = HashMap::new();
    let instructions = Instructions::parse_line(&input[0]);

    for line in &input[2..] {
        let node = Node::parse_line(line);
        network.insert(node.key.clone(), node);
    }

    let current_nodes: Vec<&Node> = network
        .iter()
        .filter(|(k, _)| k.ends_with('A'))
        .map(|(_, n)| n)
        .collect();
    let mut n_steps: Vec<u32> = current_nodes.iter().map(|_| 0).collect();

    for (start_index, start_node) in current_nodes.into_iter().enumerate() {
        let mut current = start_node;
        // let mut n_steps = 0;

        for index in instructions.0.iter().cycle() {
            let next = &current.elements[*index as usize];
            current = network.get(next).unwrap();
            n_steps[start_index] += 1;
            if current.key.ends_with("Z") {
                break;
            }
        }
    }

    return n_steps;
}

pub fn solve_part2_brute_force(input: &[String]) -> u32 {
    let mut network = HashMap::new();
    let instructions = Instructions::parse_line(&input[0]);

    for line in &input[2..] {
        let node = Node::parse_line(line);
        network.insert(node.key.clone(), node);
    }

    let mut current_nodes: Vec<&Node> = network
        .iter()
        .filter(|(k, _)| k.ends_with('A'))
        .map(|(_, n)| n)
        .collect();
    let mut n_steps = 0;

    for index in instructions.0.iter().cycle() {
        let next_elements: Vec<&String> = current_nodes
            .iter()
            .map(|&n| &n.elements[*index as usize])
            .collect();
        current_nodes = next_elements
            .iter()
            .map(|&k| network.get(k).unwrap())
            .collect();
        n_steps += 1;

        if current_nodes
            .iter()
            .map(|n| n.key.ends_with("Z"))
            .all(|x| x)
        {
            break;
        }
    }

    return n_steps;
}

pub struct Instructions(Vec<u8>);

impl Instructions {
    fn parse_line(line: &str) -> Instructions {
        let mut result = Vec::new();
        for c in line.trim().chars() {
            if c == 'L' {
                result.push(0)
            } else if c == 'R' {
                result.push(1)
            } else {
                panic!("Unknown instruction {}!", c);
            }
        }

        return Instructions(result);
    }
}

pub struct Node {
    pub key: String,
    pub elements: Vec<String>,
}

impl Node {
    pub fn parse_line(line: &str) -> Node {
        let (key, elements) = line.trim().split_once(" = ").unwrap();
        let elements = elements.split_once(", ").unwrap();

        Node {
            key: key.trim().to_string(),
            elements: vec![
                elements.0.replace("(", "").to_string(),
                elements.1.replace(")", "").to_string(),
            ],
        }
    }
}

#[cfg(test)]
pub mod tests {
    use crate::{solve_part1, solve_part2, solve_part2_brute_force, Instructions, Node};

    #[test]
    fn test_part1() {
        let input = "RL

        AAA = (BBB, CCC)
        BBB = (DDD, EEE)
        CCC = (ZZZ, GGG)
        DDD = (DDD, DDD)
        EEE = (EEE, EEE)
        GGG = (GGG, GGG)
        ZZZ = (ZZZ, ZZZ)"
            .lines()
            .map(|x| x.to_string())
            .collect::<Vec<String>>();

        let instructions = Instructions::parse_line(&input[0]);
        assert_eq!(instructions.0, vec![1, 0]);

        let node = Node::parse_line(&input[2]);
        assert_eq!(node.key, "AAA");
        assert_eq!(node.elements[0], "BBB");
        assert_eq!(node.elements[1], "CCC");
        assert_eq!(solve_part1(&input), 2);
    }
    #[test]
    fn test_part2() {
        let input = "LR

        11A = (11B, XXX)
        11B = (XXX, 11Z)
        11Z = (11B, XXX)
        22A = (22B, XXX)
        22B = (22C, 22C)
        22C = (22Z, 22Z)
        22Z = (22B, 22B)
        XXX = (XXX, XXX)"
            .lines()
            .map(|x| x.to_string())
            .collect::<Vec<String>>();

        assert_eq!(solve_part2_brute_force(&input), 6);
        assert_eq!(solve_part2(&input), vec![3, 2]);
    }
}
