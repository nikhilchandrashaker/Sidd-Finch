"""Generate the synthetic Sidd Finch dataset. Sidd Finch is fictional, so every row is simulated.
Usage: python generate_dataset.py   (writes CSVs next to this file; seed fixed for reproducibility)"""
import itertools, math, random, csv

SEED = 1985
GAMES_PER_COHORT = 25
FT_TO_PLATE, MPH_TO_FPS, BALL_KG = 60.5, 1.46667, 0.145
SEG_BASE = [12, 20, 24, 22, 16]  # legs, trunk, shoulder, elbow, wrist (mph at a 94 mph baseline)

def flight_ms(v, ext): return (FT_TO_PLATE - ext) / (v * MPH_TO_FPS) * 1000
def ke_j(v): return 0.5 * BALL_KG * (v * 0.44704) ** 2
def whiff_prob(v, ext, react):
    gap = react - (flight_ms(v, ext) - 150)
    ref_gap = 170 - (flight_ms(94, 6.5) - 150)
    k = math.log(.22 / .78) - ref_gap / 18
    return 1 / (1 + math.exp(-(gap / 18 + k)))
def torque_nm(v): return 64 * (v / 94) ** 2

COHORTS = {  # mean speed, sd, extension mean, extension sd, strike rate, fatigue mph per pitch
    "Finch": (168.0, 1.6, 6.5, 0.15, 0.55, 0.030),
    "MLB average": (94.0, 2.4, 6.3, 0.35, 0.62, 0.012),
}

def play_game(rng, cohort, game_id):
    mu, sd, em, esd, ctrl, fat = COHORTS[cohort]
    rows, pitch_num, outs, batter = [], 0, 0, 0
    while outs < 27:
        batter += 1
        react = min(215, max(130, rng.gauss(170, 12)))
        balls = strikes = 0
        while True:
            pitch_num += 1
            v = mu - fat * pitch_num + rng.gauss(0, sd)
            ext = rng.gauss(em, esd)
            c = max(0.3, ctrl - 0.0006 * pitch_num)
            in_zone = rng.random() < c
            swing = whiff = 0
            if in_zone:
                if rng.random() < 0.65:
                    swing = 1
                    whiff = 1 if rng.random() < whiff_prob(v, ext, react) else 0
                    outcome = "swinging_strike" if whiff else "in_play_out"
                else:
                    outcome = "called_strike"
            else:
                outcome = "ball"
            rows.append(dict(
                cohort=cohort, game_id=game_id, pitch_num=pitch_num, batter_num=batter, outs_before=outs,
                balls=balls, strikes=strikes, release_speed_mph=round(v, 1), extension_ft=round(ext, 2),
                flight_time_ms=round(flight_ms(v, ext), 1), time_left_ms=round(max(0, flight_ms(v, ext) - 150), 1),
                gravity_drop_ft=round(0.5 * 32.174 * (flight_ms(v, ext) / 1000) ** 2, 2),
                kinetic_energy_j=round(ke_j(v), 1), hitter_reaction_ms=round(react, 1),
                in_zone=int(in_zone), swing=swing, whiff=whiff,
                whiff_prob=round(whiff_prob(v, ext, react), 4), outcome=outcome))
            if outcome == "in_play_out": outs += 1; break
            if outcome in ("swinging_strike", "called_strike"):
                strikes += 1
                if strikes == 3: rows[-1]["outcome"] += "_strikeout"; outs += 1; break
            else:
                balls += 1
                if balls == 4: rows[-1]["outcome"] = "ball_walk"; break
    return rows

def main():
    rng = random.Random(SEED)
    pitches, games = [], []
    for cohort in COHORTS:
        for g in range(1, GAMES_PER_COHORT + 1):
            gid = f"{'F' if cohort == 'Finch' else 'M'}{g:03d}"
            r = play_game(rng, cohort, gid); pitches += r
            sw = sum(x["swing"] for x in r)
            games.append(dict(cohort=cohort, game_id=gid, pitches=len(r),
                strikeouts=sum(x["outcome"].endswith("strikeout") for x in r),
                walks=sum(x["outcome"] == "ball_walk" for x in r),
                balls_in_play=sum(x["outcome"] == "in_play_out" for x in r),
                avg_speed_mph=round(sum(x["release_speed_mph"] for x in r) / len(r), 1),
                max_speed_mph=max(x["release_speed_mph"] for x in r),
                swings=sw, whiffs=sum(x["whiff"] for x in r),
                whiff_rate=round(sum(x["whiff"] for x in r) / sw, 3) if sw else ""))
    def write(name, rows):
        with open(name, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    write("finch_pitches.csv", pitches)
    write("finch_games.csv", games)
    levels = [0.5, 1.0, 1.5, 2.0, 2.5]
    chain = []
    for combo in itertools.product(levels, repeat=5):
        v = sum(b * m for b, m in zip(SEG_BASE, combo))
        chain.append(dict(legs_mult=combo[0], trunk_mult=combo[1], shoulder_mult=combo[2], elbow_mult=combo[3],
            wrist_mult=combo[4], release_speed_mph=round(v, 1), kinetic_energy_j=round(ke_j(v), 1),
            elbow_torque_nm=round(torque_nm(v), 1), ligament_load_ratio=round(torque_nm(v) / 33, 2),
            flight_time_ms=round(flight_ms(v, 6.5), 1)))
    write("finch_kinetic_chain.csv", chain)
    ref = [("Average MLB fastball", 93.8), ("Hard thrower", 100.0), ("Aroldis Chapman (record pitch)", 105.8), ("Sidd Finch (fictional)", 168.0)]
    write("finch_benchmarks.csv", [dict(pitcher=n, speed_mph=v, flight_time_ms=round(flight_ms(v, 6.5), 1),
        kinetic_energy_j=round(ke_j(v), 1), energy_vs_avg=round(ke_j(v) / ke_j(93.8), 2),
        gravity_drop_ft=round(0.5 * 32.174 * (flight_ms(v, 6.5) / 1000) ** 2, 2)) for n, v in ref])
    print(len(pitches), "pitches,", len(games), "games,", len(chain), "chain rows")

if __name__ == "__main__":
    main()
