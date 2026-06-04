# Finance knowledge base

A growing library of US financial history — the **context** behind the daily brief. Each
era file documents what happened, what the **Fed** did, what the **government** did, and how
it hit the US and markets. The numeric series behind these eras live in `data/timeline.jsonl`
(daily, 1998→now), and `src/eras.py` is the machine-readable index (it also shades the eras
on the dashboard's **Trends** tab).

## How to use it

Run **`/finance`** in `claude` (this folder). The agent:
- teaches you an era and **ties it to the real data** (e.g. what the 2s10s curve and HY
  spreads did going into the GFC, pulled from the timeline),
- quizzes you and follows up on what you got wrong,
- and — when you ask about something not yet covered — **researches it and writes a new file
  here**, so the library grows as you learn.

You are both the **teacher and the learner**; this directory is the shared, durable memory
(git-versioned, syncs across machines). Edit the files freely — your notes are part of it.

## Structure

- `eras/<key>.md` — one market era each (the `key` matches `src/eras.py`).
- `topics/<name>.md` — cross-era concepts (QE, the yield curve, credit spreads, the Fed's
  dual mandate…), written on demand as you go.
- `glossary.md` — quick definitions.

## The eras (see `src/eras.py` for exact dates)

dotcom · housing-boom · gfc · zirp-qe · euro-debt · normalization · covid · inflation · higher-for-longer
