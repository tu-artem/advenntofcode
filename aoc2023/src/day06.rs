fn main() {
    // Time:        46     85     75     82
    // Distance:   208   1412   1257   1410
    let part1_result = solve_part1();
    println!("Part 1: {}", part1_result);
    let part2_result = solve_part2();
    println!("Part 2: {}", part2_result);
}

fn solve_part1() -> usize {
    let races = vec![
        Race::new(46, 208),
        Race::new(85, 1412),
        Race::new(75, 1257),
        Race::new(82, 1410),
    ];

    races
        .into_iter()
        .map(|r| r.n_ways_to_beat_record())
        .product()
}

fn solve_part2() -> usize {
    Race::new(46857582, 208141212571410).n_ways_to_beat_record()
}

pub struct Race {
    pub time: u64,
    pub record: u64,
}

impl Race {
    fn new(time: u64, record: u64) -> Race {
        Race { time, record }
    }

    fn n_ways_to_beat_record(&self) -> usize {
        let distances = calculate_distances(self.time);

        distances.into_iter().filter(|&d| d > self.record).count()
    }
}

pub fn calculate_distances(race_time: u64) -> Vec<u64> {
    let mut distances = Vec::new();
    for hold_time in 0..=race_time {
        distances.push(hold_time * (race_time - hold_time));
    }

    distances
}

#[cfg(test)]
mod tests {
    use crate::{calculate_distances, Race};

    #[test]
    fn test_distances() {
        assert_eq!(calculate_distances(7), vec![0, 6, 10, 12, 12, 10, 6, 0])
    }

    #[test]
    fn test_race() {
        let race = Race {
            time: 15,
            record: 40,
        };

        assert_eq!(race.n_ways_to_beat_record(), 8);
    }
}
