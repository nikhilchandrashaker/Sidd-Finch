# Sidd Finch dataset: data dictionary

Sidd Finch is a fictional pitcher from George Plimpton's 1985 Sports Illustrated April Fools' story. **Every row in this dataset is simulated.** The data comes from the same simplified models as the Sidd Finch Lab project, so treat it as practice data, not evidence about real pitching. Regenerate it with `python generate_dataset.py` (fixed seed 1985).

## Files

| File | Rows | Grain |
| --- | --- | --- |
| `finch_pitches.csv` | 7,012 | One row per pitch, 25 simulated starts for each cohort |
| `finch_games.csv` | 50 | One row per simulated start |
| `finch_kinetic_chain.csv` | 3,125 | One row per combination of five segment multipliers (0.5, 1.0, 1.5, 2.0, 2.5) |
| `finch_benchmarks.csv` | 4 | One row per reference pitch |

## finch_pitches.csv

| Column | Meaning |
| --- | --- |
| cohort | `Finch` or `MLB average` (a comparison pitcher around 94 mph) |
| game_id | Start ID, `F###` for Finch and `M###` for the comparison cohort |
| pitch_num | Pitch count within the start |
| batter_num | Batter faced within the start |
| outs_before | Outs when the pitch was thrown |
| balls, strikes | Count before the pitch |
| release_speed_mph | Speed at release, with a small fatigue drop and random noise |
| extension_ft | Release extension toward the plate |
| flight_time_ms | Release to plate: (60.5 ft minus extension) divided by speed, no drag |
| time_left_ms | Flight time minus a fixed 150 ms swing, floored at 0 |
| gravity_drop_ft | Drop from gravity alone, with no spin |
| kinetic_energy_j | Ball energy, using a 0.145 kg ball |
| hitter_reaction_ms | The batter's simulated reaction time, drawn once per batter |
| in_zone | 1 if the pitch was a strike-zone pitch |
| swing | 1 if the batter swung (only at strike-zone pitches, 65 percent of the time) |
| whiff | 1 if the batter swung and missed |
| whiff_prob | Modeled chance of a miss given a swing |
| outcome | `ball`, `called_strike`, `swinging_strike`, `in_play_out`, or the end-of-at-bat labels `swinging_strike_strikeout`, `called_strike_strikeout`, `ball_walk` |

## finch_games.csv

cohort, game_id, pitches, strikeouts, walks, balls_in_play, avg_speed_mph, max_speed_mph, swings, whiffs, whiff_rate. Each start runs to 27 outs.

## finch_kinetic_chain.csv

| Column | Meaning |
| --- | --- |
| legs_mult, trunk_mult, shoulder_mult, elbow_mult, wrist_mult | Multiplier on each segment's share of a 94 mph baseline (12, 20, 24, 22, 16 mph) |
| release_speed_mph | Sum of the scaled segments |
| kinetic_energy_j | Ball energy at that speed |
| elbow_torque_nm | Torque assumed to scale as 64 N·m times (speed / 94) squared |
| ligament_load_ratio | Elbow torque divided by an assumed 33 N·m ligament failure load |
| flight_time_ms | Flight time at 6.5 ft of extension |

## finch_benchmarks.csv

pitcher, speed_mph, flight_time_ms, kinetic_energy_j, energy_vs_avg, gravity_drop_ft at 6.5 ft of extension.

## Known limitations

- Fouls, baserunners, pitch types, spin, and drag are not modeled, so contact is always an out and strikeouts are rare for the comparison cohort.
- Finch's whiff probability is essentially 100 percent on swings, which is what the model produces at 168 mph, so Finch rows carry little variation in that column.
- The kinetic chain split, the torque scaling, and the 33 N·m ligament value are teaching assumptions.
- The delivery simulation's 3D motion output is not included.
