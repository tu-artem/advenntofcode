pub mod utils;

use std::collections::HashSet;


fn main() {
    println!("It's day 4!");
    let input = utils::read_input_lines("04");
    let part1_result = solve_part1(&input);
    println!(" Part 1: {}", part1_result);
    let part2_result = solve_part2(&input);
    println!(" Part 2: {}", part2_result);
}

pub fn solve_part1(input: &Vec<String>) -> u32 {
    let cards: Vec<_> = input.iter().map(|x| ScratchCard::parse_line(x.trim())).collect();

    cards.iter().map(|x| x.worth()).sum()
}

pub fn solve_part2(input: &Vec<String>) -> u32 {
    let cards: Vec<_> = input.iter().map(|x| ScratchCard::parse_line(x.trim())).collect();
    let mut on_hand_cards: Vec<u32> = cards.iter().map(|_| 1).collect();

    for card in cards.iter() {
        let on_hand = on_hand_cards[card.id as usize - 1];
        let number_of_won = card.n_matches();
        for won_card_id in (card.id + 1)..=(card.id + number_of_won) {
            on_hand_cards[won_card_id as usize - 1] += on_hand; 
        }
    };

    on_hand_cards.iter().sum()
}

pub struct ScratchCard {
    pub id: u32,
    pub winning_numbers: Vec<u32>,
    pub card_numbers: Vec<u32>,
}

impl ScratchCard {
    fn parse_line(line: &str) -> ScratchCard {
        let (id, numbers) = line.split_once(": ").unwrap();

        let (w, c) = numbers.split_once('|').unwrap();

        let winning_numbers: Vec<u32> = w
            .split_ascii_whitespace()
            .into_iter()
            .map(|x| x.parse().unwrap())
            .collect();
        let card_numbers: Vec<u32> = c
            .split_ascii_whitespace()
            .into_iter()
            .map(|x| x.parse().unwrap())
            .collect();

        ScratchCard {
            id: id.replace("Card", "").trim().parse().unwrap(),
            winning_numbers,
            card_numbers,
        }
    }

    fn matches(&self) -> Vec<u32> {
        let hs_card: HashSet<&u32> = self.card_numbers.iter().collect();
        let hs_winning: HashSet<&u32> = self.winning_numbers.iter().collect();

        let intersection: Vec<u32> = hs_card.intersection(&hs_winning).map(|x| **x).collect();
        
        intersection
    }

    fn n_matches(&self) -> u32 {
        self.matches().len() as u32
    }

    fn worth(&self) -> u32 {
        let matches = self.matches();
        match matches.len() {
            0 => 0,
            l =>   2_u32.pow(l as u32 - 1)
        }
        
    }
}
#[cfg(test)]
mod tests {
    use crate::{ScratchCard, solve_part1, solve_part2};

    #[test]
    fn test_one_line() {
        let line = "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53";

        let card = ScratchCard::parse_line(line);
        assert_eq!(card.id, 1);

        assert_eq!(card.worth(), 8);
    }

    #[test]
    fn test_part1_and_2() {
        let input = "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
        Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
        Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
        Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
        Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
        Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"
        .lines()
        .map(|x| x.to_string())
        .collect::<Vec<String>>();

        assert_eq!(solve_part1(&input), 13);

        assert_eq!(solve_part2(&input), 30);
    }
}
