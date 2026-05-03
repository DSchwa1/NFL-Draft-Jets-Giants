# NFL Draft Historical Comp Finder — 2026 Jets & Giants

A similarity-based framework that matches 2026 NFL Draft prospects to the most comparable historical first-round picks and returns a best case, median, and worst case outcome range — grounded entirely in what those historical players actually did in the NFL.

**Full writeup:** [2026 NFL Draft Analysis on Substack](https://substack.com/home/post/p-194461727?source=queue)

---

## Research Question

When a player is drafted at a specific slot with specific physical measurables and combine testing results, what does the historical record say about how players like that have actually turned out?

---

## Why It Matters

Draft-night player comps are usually subjective — two analysts watching the same player arrive at different names depending on which traits they weight. This model replaces the narrative with a systematic similarity search across 25 years of NFL Draft data. The output isn't a single prediction. It's a range: best case, median, and worst case, each anchored to a real player with a real career. That framing is directly useful for calibrating expectations before pick night — and for understanding how much variance actually lives at any given draft slot and position.

The analysis covers three picks ahead of the 2026 draft: **Jets 2**, **Giants 5**, and **Jets 16**, with multiple candidate prospects at each slot based on pre-draft consensus.

---

## Data Sources

| Source | Contents | Coverage |
|--------|----------|----------|
| [nflverse draft picks](https://github.com/nflverse/nflverse-data) | Draft slot, position, college, career wAV | All picks, 2000–2025 |
| [nflverse combine](https://github.com/nflverse/nflverse-data) | Height, weight, 40-yard dash, vertical, broad jump, 3-cone, shuttle | Combine attendees, 2000–present |

**Weighted Approximate Value (wAV)** is a career performance metric from Pro Football Reference that estimates total contribution on a single cross-position scale. The historical pool is **827 first-round picks** from 2000–2025.

---

## Methodology

### Normalizing for Career Length

Raw career wAV penalizes recently drafted players who haven't had time to accumulate value. The model uses **seasonal AV** — career wAV divided by years in the league — so comparisons are fair across draft classes.

### Similarity Algorithm

For each 2026 candidate:

1. Filter the historical pool to players drafted within ±10 picks of the candidate's slot
2. Score each measurable dimension (height, weight, 40-yard dash, vertical, broad jump, 3-cone, shuttle) on a 0–1 scale based on proximity
3. Weight and sum scores — **draft slot receives 3× weight** because where a team drafts a player reflects its consensus evaluation and sets the baseline expectation
4. Select the **top 5 most similar historical picks** as the comp set

### Strict vs. Loose Position Matching

Position labels have shifted significantly over 25 years — a 2005 "DE" is often a modern "EDGE." The model runs both versions:

- **Strict**: exact position label match only
- **Loose**: expanded groupings (e.g., all edge rushers regardless of label)

When strict and loose comps diverge meaningfully, it reveals how sensitive the conclusions are to positional classification — which is substantive information, not a modeling artifact.

### Outcome Ranges

Each candidate is summarized by:
- **Best case** — highest seasonal AV among the 5 comps
- **Median** — middle seasonal AV among the 5 comps
- **Worst case** — lowest seasonal AV among the 5 comps

Plus average Pro Bowl selections and average games played across the comp set.

---

## Key Findings

*Results below use strict position matching unless noted. Full tables with similarity scores, measurables, and career stats for all 80 comp entries are in `2026_draft_comp_results_v1.xlsx`.*

### Jets Pick 2 — DE candidates

Both Arvell Reese and David Bailey sit in historically volatile draft real estate. Pick-2 DE has produced transcendent pass rushers and bust-level outcomes in roughly equal measure. The worst-case in both strict comp sets is Dion Jordan (1.12 seasonal AV across 8 NFL seasons). The wide spread is a real signal about this slot, not a modeling quirk.

| Candidate | Best Case | Best Seasonal AV | Median | Median AV | Worst Case | Worst AV | Avg Games |
|-----------|-----------|:---:|--------|:---:|------------|:---:|:---:|
| Arvell Reese | Jadeveon Clowney | 5.25 | Abdul Carter | 4.00 | Dion Jordan | 1.12 | 80.6 |
| David Bailey | Travon Walker | 6.50 | Chase Young | 4.83 | Dion Jordan | 1.12 | 73.6 |

Bailey's loose comps (expanding to all pass rushers regardless of label) surface Will Anderson as the best case at 12.33 seasonal AV — the highest single best-case ceiling in the analysis.

### Giants Pick 5 — three candidates

Sonny Styles is the most methodologically interesting case: his loose comps (which match him to DBs based on measurables) surface Devon Witherspoon as best case, while his strict LB comps point to Khalil Mack. The two frames produce meaningfully different pictures of what kind of player he could become. Jeremiyah Love has the highest ceiling in the full dataset (LaDainian Tomlinson, 11.73 seasonal AV); strict and loose comps are identical for RB, a position-pure group.

| Candidate | Position | Best Case | Best Seasonal AV | Median | Median AV | Worst Case | Worst AV | Avg Games |
|-----------|----------|-----------|:---:|--------|:---:|------------|:---:|:---:|
| Sonny Styles | LB | Khalil Mack | 8.75 | A.J. Hawk | 5.00 | Isaiah Simmons | 3.33 | 115.0 |
| Jeremiyah Love | RB | LaDainian Tomlinson | 11.73 | Adrian Peterson | 6.73 | Darren McFadden | 3.90 | 111.0 |
| Caleb Downs | S | Kyle Hamilton | 7.75 | Jamal Adams | 5.22 | Karl Joseph | 2.67 | 92.6 |

### Jets Pick 16 — three candidates

WR comps are identical strict vs. loose for both receivers — wide receiver is a position-stable group with consistent labeling across the dataset. Olaivavega Ioane has the strongest floor of any candidate in the analysis: even his worst-case strict comp (Mike Iupati) carries a 6.09 seasonal AV, the highest worst-case floor across all eight players.

| Candidate | Position | Best Case | Best Seasonal AV | Median | Median AV | Worst Case | Worst AV | Avg Games |
|-----------|----------|-----------|:---:|--------|:---:|------------|:---:|:---:|
| Jordyn Tyson | WR | CeeDee Lamb | 10.83 | Rod Gardner | 4.17 | Michael Clayton | 2.75 | 102.2 |
| Makai Lemon | WR | CeeDee Lamb | 10.83 | Santana Moss | 5.14 | Corey Coleman | 2.00 | 94.6 |
| Olaivavega Ioane | G | Zack Martin | 9.36 | Chris Lindstrom | 7.00 | Mike Iupati | 6.09 | 128.4 |

---

## Limitations

- **No college production.** This version uses only combine measurables and draft slot. College stats — yards, touchdowns, dominator rating — are meaningful predictors of NFL success and are not included here.
- **Small comp pools at some positions.** Filtering to ±10 picks within a specific position can produce thin historical samples, especially for guards and safeties. Results are more stable for positions with more R1 representation (DE, WR).
- **Recency bias in some comps.** Players like Abdul Carter (2025) and Will Anderson (2023) are still active; their seasonal AV will increase. This slightly deflates some best-case and median estimates.
- **No injury or character signal.** Physical and athletic data carries no information about injury history, behavioral risk, or scheme fit — all of which materially affect outcomes.
- **Position label evolution is only partially addressed.** The strict/loose framework helps, but reclassifying all edge rushers or defensive backs across 25 years of label drift is an imperfect fix for a genuine data quality problem.

A Version 2 incorporating college production, year-by-year career value curves, and first-contract performance windows is in development.

---

## Repo Structure

```
.
├── 2026_draft_comp_results_v1.xlsx   # Full output: methodology, summary, all comps, raw data (4 sheets)
├── combine.csv                        # nflverse combine data — 8,968 players, 2000–present
├── pfr_draft_scraper.py               # Exploratory PFR scraper (final pipeline used nflverse directly)
└── README.md
```

**`2026_draft_comp_results_v1.xlsx` sheets:**

| Sheet | Contents |
|-------|----------|
| Introduction and Methodology | Full research design write-up |
| Summary | One row per candidate/method — best, median, worst case comps with seasonal AV, Pro Bowls, games |
| All_Comps | Full detail for all 80 comp entries: similarity scores, measurables, career stats |
| Raw Data | Underlying player pool used in the model |

---

## How to Run

The primary output is `2026_draft_comp_results_v1.xlsx`. Open the **Summary** tab for the headline results, or **All_Comps** for the full comp detail including similarity scores.

To reproduce or update the combine dataset:

```python
import nfl_data_py as nfl

combine = nfl.import_combine_data(range(2000, 2026))
combine.to_csv("combine.csv", index=False)

draft = nfl.import_draft_picks()
draft.to_csv("draft_picks.csv", index=False)
```

Install nfl_data_py: `pip install nfl-data-py`

---

## Future Improvements

- Incorporate college production (yards, touchdowns, dominator rating per position)
- Model year-by-year career value curves and first-contract performance windows (years 1–4) rather than career averages
- Extend to rounds 2–3 with adjusted pick windows and position-specific comp pools
- Migrate the similarity algorithm from spreadsheet to a reproducible Python script
- Build an interactive interface (Streamlit or Observable) for querying any prospect against the historical pool
