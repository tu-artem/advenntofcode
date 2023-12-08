use std::cmp::Ordering;
use std::collections::HashMap;

pub mod utils;

fn main() {
    let input = utils::read_input_lines("07");
    let part1_result = solve_part1(&input);
    println!("Part 1: {}", part1_result);
    let part2_result = solve_part2(&input);
    println!("Part 2: {}", part2_result);
}

#[derive(PartialEq, PartialOrd, Debug, Eq, Ord)]
pub enum HandType {
    FiveOfAKind = 6,
    FourOfAKind = 5,
    FullHouse = 4,
    ThreeOfAKind = 3,
    TwoPair = 2,
    OnePair = 1,
    HighCard = 0,
}

#[derive(PartialEq, PartialOrd, Debug, Eq, Hash, Ord)]
pub enum Card {
    _2 = 2,
    _3 = 3,
    _4 = 4,
    _5 = 5,
    _6 = 6,
    _7 = 7,
    _8 = 8,
    _9 = 9,
    T = 10,
    J = 11,
    Q = 12,
    K = 13,
    A = 14,
}

impl Card {
    fn from_char(c: char) -> Card {
        match c {
            '2' => Card::_2,
            '3' => Card::_3,
            '4' => Card::_4,
            '5' => Card::_5,
            '6' => Card::_6,
            '7' => Card::_7,
            '8' => Card::_8,
            '9' => Card::_9,
            'T' => Card::T,
            'J' => Card::J,
            'Q' => Card::Q,
            'K' => Card::K,
            'A' => Card::A,
            x => panic!("Unknown card {}!", x),
        }
    }
}
#[derive(Debug)]
pub struct Hand {
    pub cards: Vec<Card>,
    pub bid: u32,
}

impl Hand {
    pub fn new(cards: String, bid: u32) -> Hand {
        let cards = cards.chars().map(|c| Card::from_char(c)).collect();
        Hand { cards, bid }
    }

    pub fn parse_line(line: String) -> Hand {
        let (cards, bid) = line.trim().split_once(' ').unwrap();

        Hand::new(cards.to_string(), bid.parse().unwrap())
    }

    pub fn hand_type(&self) -> HandType {
        let mut counts: HashMap<&Card, u32> = HashMap::new();
        for char in self.cards.iter() {
            if counts.contains_key(&char) {
                *counts.get_mut(&char).unwrap() += 1
            } else {
                counts.insert(char, 1);
            }
        }
        let mut counts_of_counts: HashMap<u32, u32> = HashMap::new();
        for (_, v) in counts.iter() {
            if counts_of_counts.contains_key(v) {
                *counts_of_counts.get_mut(&v).unwrap() += 1
            } else {
                counts_of_counts.insert(*v, 1);
            }
        }

        if counts_of_counts.contains_key(&5) {
            return HandType::FiveOfAKind;
        };

        if counts_of_counts.contains_key(&4) {
            return HandType::FourOfAKind;
        }
        if counts_of_counts.contains_key(&3) && counts_of_counts.contains_key(&2) {
            return HandType::FullHouse;
        }
        if counts_of_counts.contains_key(&3) {
            return HandType::ThreeOfAKind;
        }

        if counts_of_counts.get(&2) == Some(&2) {
            return HandType::TwoPair;
        }

        if counts_of_counts.get(&2) == Some(&1) {
            return HandType::OnePair;
        }

        return HandType::HighCard;
    }
}

impl PartialOrd for Hand {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Hand {
    fn cmp(&self, other: &Self) -> Ordering {
        let self_type = self.hand_type();
        let other_type = other.hand_type();
        if self_type != other_type {
            return self_type.cmp(&other_type);
        } else {
            for (c1, c2) in self.cards.iter().zip(other.cards.iter()) {
                if c1 == c2 {
                    continue;
                } else {
                    return c1.cmp(c2);
                }
            }
            return Ordering::Equal;
        }
    }
}

impl PartialEq for Hand {
    fn eq(&self, other: &Self) -> bool {
        self.cards == other.cards
    }
}

impl Eq for Hand {}

pub fn solve_part1(input: &[String]) -> u32 {
    let mut hands: Vec<Hand> = input
        .into_iter()
        .map(|x| Hand::parse_line(x.to_string()))
        .collect();
    hands.sort();
    hands
        .into_iter()
        .enumerate()
        .map(|(rank, hand)| (1 + rank as u32) * hand.bid)
        .sum()
}

pub fn solve_part2(input: &[String]) -> u32 {
    43
}

#[cfg(test)]
pub mod tests {
    use crate::{solve_part1, Card, Hand, HandType};

    #[test]
    fn test_order() {
        let input = "32T3K 765
        T55J5 684
        KK677 28
        KTJJT 220
        QQQJA 483"
            .lines()
            .map(|x| x.to_string())
            .collect::<Vec<String>>();
        let mut hands: Vec<Hand> = input
            .iter()
            .map(|x| Hand::parse_line(x.to_string()))
            .collect();

        assert_eq!(hands.len(), 5);
        assert_eq!(
            hands[0].cards,
            vec![Card::_3, Card::_2, Card::T, Card::_3, Card::K]
        );
        assert_eq!(hands[0].bid, 765);

        assert_eq!(hands[0].hand_type(), HandType::OnePair);
        assert_eq!(hands[4].hand_type(), HandType::ThreeOfAKind);

        assert!(hands[0] < hands[1]);
        assert!(hands[2] < hands[4]);

        hands.sort();

        // print!("{:?}", hands);

        assert_eq!(solve_part1(&input), 6440);
    }
}
