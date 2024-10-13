## Winrates
We periodically (especially after large changes) conduct a large amount of games to measure the winrates with our best strategies
on all the characters. 

### Current Stats:
From October 2024: [release-03](https://github.com/xaved88/bottled_ai/releases/tag/release-03)

| Character | Strategy          | Winrate | AverageFloor | Runs |
| --------- | ----------------- | ------- | ------------ | ---- |
| Ironclad  | RequestedStrike   | 20%     | 32.7         | 50   |
| Silent    | ShivsNGiggles     | 40%     | 38.5         | 48   |
| Defect    | PwnderMyOrbs      | 33%     | 39.4         | 52   |
| Watcher   | PeacefulPummeling | 52%     | 45.86        | 50   |

More details can be found at [winrate_details/release-03.md](winrate_details/release-03.md)

### How we determine these winrates:
We randomly generate a number of seeds, and then have the bot play them! We aim for 50 runs for each character.

**Disclaimer**: 

This is not enough runs to attain high confidence! For example, Ironclad's winrate above gives it a 95% Confidence Interval from 8.9% to 31.1% (that's a really large scope).

However, it still is good enough to give us a general feeling and guess at where the bot's performing. If we wanted to reduce that margin of error to only +-3%, we'd need to run closer to 1000 games per character! (this is nearly 1 month of 24/7 gameplay for all 4 characters).
