# The Sidd Finch Lab

An interactive baseball analytics and biomechanics project about Sidd Finch, the fictional New York Mets pitching prospect from George Plimpton's 1985 Sports Illustrated April Fools' story, who supposedly threw a 168 mph fastball.

Sidd Finch is not a real person. Every number in this project is a modeled estimate built for teaching and exploration, not a prediction or measurement.

## What is in the project

| Section | What it does |
| --- | --- |
| Scouting report | Short fictional profile drawn from the Plimpton story |
| Pitch lab | Sliders for velocity, extension, and hitter reaction time. Outputs flight time, gravity drop, decision time, and modeled whiff rate |
| Biomechanics | Kinetic chain model with five sliders (legs, trunk, shoulder, elbow, wrist) that sum to a release speed, with ball energy and an estimated elbow torque compared to ligament strength |
| Benchmarks | Table comparing Finch to an average MLB fastball, a 100 mph pitch, and Aroldis Chapman's record pitch |
| Game simulator | Monte Carlo simulation of a 27-out start using the pitch lab settings and a control (strike %) slider |

## How to run it

It is a single self-contained HTML file with no dependencies and no build step. Open `sidd-finch-lab.html` in any modern browser.

## Models and assumptions

**Flight time.** `time = (60.5 ft - extension) / (speed in ft/s)`. Drag is ignored, so real flight times run slightly longer, roughly 8 to 10 percent.

**Gravity drop.** `0.5 * g * t^2` with no spin. Real pitches also experience Magnus force, which this model leaves out.

**Whiff rate.** A logistic curve on the gap between the hitter's reaction time and the time remaining after a 150 ms swing. It is tuned so a 94 mph fastball is missed about 22 percent of the time. This curve is invented, not fitted to data.

**Kinetic chain.** The 94 mph baseline is split into legs 12, trunk 20, shoulder 24, elbow 22, and wrist 16 mph. Each slider multiplies one segment. The split is a simplified teaching model.

**Ball energy.** `0.5 * 0.145 kg * v^2`. Energy grows with the square of speed, so 168 mph carries about 3.2 times the energy of 94 mph.

**Elbow torque.** Scaled from an assumed 64 N·m at 94 mph by `(v/94)^2`, compared against a ligament failure load of about 33 N·m. Published biomechanics studies report elite pitchers' elbow torque in the 60 to 70 N·m range and ulnar collateral ligament strength around 30 to 35 N·m. The squared scaling is a crude assumption.

**Game simulator.** Each pitch is a strike with probability equal to control. Strikes are swung at 65 percent of the time, and swings miss at the modeled whiff rate. Contact is an out in play. Three strikes is a strikeout, four balls is a walk, and the game runs to 27 outs. Fouls are ignored.

## Limitations

- No drag, spin, or pitch movement
- No real Statcast data
- Whiff, chain, and torque models are illustrative
- The simulator ignores baserunners, fouls, and fatigue

## Ideas for extending it

- Fit the whiff curve to real Statcast swing data
- Add drag and Magnus force for a true flight path
- Model fatigue and pitch counts across a season
- Add pitch-by-pitch motion capture comparisons

## Credits

Character from George Plimpton, "The Curious Case of Sidd Finch," Sports Illustrated, April 1, 1985. Team colors are New York Mets blue and orange.
