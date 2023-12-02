pub mod utils;

fn main() {
    println!("It's day 02!");
    let input = utils::read_input_lines("02");
    let part1_result = part1(&input);
    println!("Part 1: {}", part1_result);
}

struct Draw {
    pub red: u32,
    pub green: u32,
    pub blue: u32,
}

impl Draw {
    pub fn empty() -> Self {
        Draw {
            red: 0,
            green: 0,
            blue: 0,
        }
    }
}

struct Game {
    pub id: u32,
    pub draws: Vec<Draw>,
}

impl Game {
    fn new(id: u32) -> Self {
        Game {
            id,
            draws: Vec::new(),
        }
    }

    fn add_draw(&mut self, draw: Draw) -> &Self {
        self.draws.push(draw);
        self
    }

    fn from_line(line: &str) -> Self {
        let (g, d) = line.split_once(": ").unwrap();

        let id = g.trim().replace("Game ", "").parse::<u32>().unwrap();

        let mut game = Game::new(id);

        for draw_line in d.trim().split("; ") {
            let mut draw = Draw::empty();
            for cubes in draw_line.split(", ") {
                let (value, color) = cubes.split_once(' ').unwrap();
                match color {
                    "red" => draw.red = value.parse().unwrap(),
                    "green" => draw.green = value.parse().unwrap(),
                    "blue" => draw.blue = value.parse().unwrap(),
                    _ => panic!("This should not have happened!"),
                }
            }
            game.add_draw(draw);
        }

        game
    }

    fn is_valid(&self, r: u32, g: u32, b: u32) -> bool {
        self.draws
            .iter()
            .all(|x| (x.red <= r) & (x.green <= g) & (x.blue <= b))
    }
}

fn part1(input: &[String]) -> u32 {
    let (r, g, b) = (12, 13, 14);
    let games: Vec<Game> = input.iter().map(|x| Game::from_line(x)).collect();
    // return 42;
    games
        .iter()
        .filter(|&x| x.is_valid(r, g, b))
        .map(|x| x.id)
        .sum()
}

#[cfg(test)]
mod tests {
    use crate::{part1, Game};

    #[test]
    fn test_part1() {
        let input = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
        Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
        Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
        Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"
            .to_string()
            .lines()
            .map(|x| x.to_string())
            .collect::<Vec<String>>();

        assert_eq!(part1(&input), 8);
    }
    #[test]
    fn test_one_game() {
        let line = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green";

        let game = Game::from_line(line);

        assert_eq!(game.id, 1);
        assert_eq!(game.draws.len(), 3);
        assert_eq!(game.draws[1].red, 1);
        assert_eq!(game.draws[2].red, 0);
        assert_eq!(game.draws[2].green, 2);

        assert!(game.is_valid(12, 13, 14));
    }

    #[test]
    fn test_invalid_game() {
        let line = "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red";

        let game = Game::from_line(line);

        assert_eq!(game.id, 3);

        assert!(!game.is_valid(12, 13, 14));
    }
}
