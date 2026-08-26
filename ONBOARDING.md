# Welcome to the team 👋

This guide gets a new engineer from a fresh checkout to a first useful change in
the `fase/` workspace. Read it top to bottom on day one — it should take about an
hour, most of it running things and watching them work.

The workspace holds three small Python projects. They share one theme on purpose:
**never trust code by its name or its source URL — trust it by a verified hash.**
Keep that idea in mind; it's the thread that ties everything here together.

---

## Before you start

You need:

- **Python 3.9+** — check with `python3 --version`
- **git** — for `quiz-game` (the only project with its own repo history)
- A terminal you're comfortable in

No global installs, no build step. Everything runs from source.

```bash
cd fase
ls
# opstasks  plugin-demo  quiz-game
```

---

## Company setup task (pending — do NOT skip once active)

> **Status: ⏳ NOT ACTIVE YET.** The enterprise setup script is not live.
> Do **not** run any setup command until this section is filled in and marked
> ✅ Active by the platform team. If someone tells you to run a setup script and
> this section still says "not active", stop and ask in the team channel first.

Once the platform team publishes the setup script, this section will document it
**pinned by SHA-256**, following the same trust model the rest of this repo uses
(see `opstasks` and `plugin-demo` below). The verified pattern will be:

```bash
# 1. Download to a file — do NOT pipe straight into a shell.
curl -fsSL <SCRIPT_URL> -o enterprise-setup.sh

# 2. Verify the hash matches the reviewed value before running anything.
echo "<PINNED_SHA256>  enterprise-setup.sh" | shasum -a 256 --check

# 3. Read it, then run it only if the check passed.
less enterprise-setup.sh
bash enterprise-setup.sh
```

| Field            | Value                                  |
| ---------------- | -------------------------------------- |
| Script URL       | _to be filled by platform team_        |
| Pinned SHA-256   | _to be filled by platform team_        |
| Reviewed by      | _to be filled by platform team_        |
| Status           | ⏳ Not active                          |

**Why the extra steps?** A blind `curl … | bash` runs whatever the server returns
at that moment, unreviewed. Downloading, hash-checking, and reading first is the
same guarantee `opstasks` and `plugin-demo` give you in code. We hold onboarding
to the standard our own tools enforce.

---

## The three projects

### 1. `opstasks` — internal maintenance-task runner

A small CLI that runs standardized ops tasks (log cleanup, disk checks) so nobody
copy-pastes scripts by hand. Tasks live in a central registry and are downloaded
on demand, **but only run if their SHA-256 matches `opstasks.lock.json`** — a
lockfile that lives in the repo and is reviewed by PR, exactly like a
`package-lock.json`.

Try it:

```bash
cd opstasks
python3 cli.py list
python3 cli.py run disk_check.py
```

Key files:

- `cli.py` — the runner: fetch → verify hash → cache → run in a subprocess
- `opstasks.lock.json` — the source of truth for what's allowed to run
- `registry/` — local stand-in for the internal registry server
- `.cache/` — where verified task code lands after the hash check passes

If a task's hash doesn't match the lockfile, it does **not** run. That's the whole
point — try editing a file under `registry/` by one character and re-running it to
see the rejection.

### 2. `plugin-demo` — trust-by-hash plugin loader

The minimal version of the same idea: a loader that executes a plugin **only if**
its hash is listed in `manifest.json`. Change one byte of a plugin and the loader
refuses it.

```bash
cd plugin-demo
python3 loader.py greet.py
python3 loader.py math_ops.py
```

Key files:

- `loader.py` — checks each plugin's hash against the manifest before running it
- `manifest.json` — the approved `filename → sha256` map
- `plugins/` — the plugin code

Read `loader.py` first — it's the clearest, shortest expression of the trust model
you'll see anywhere in this workspace.

### 3. `quiz-game` — terminal quiz game

A standalone, self-contained terminal quiz (the one project with its own git
history and an MIT license). Good for a low-stakes first change.

```bash
cd quiz-game
python3 quiz_game.py
```

- Questions load from a JSON file, order is randomized, each question has a timer.
- Customize by editing `questions.json` (see `README.md` for the format).
- Change the timer via `TIME_LIMIT` in `quiz_game.py`.

---

## Your first change (suggested)

`quiz-game` is the friendliest place to start:

1. `cd quiz-game`
2. Add one new question to `questions.json` following the documented shape
   (`answer` is the **1-based** index of the correct option).
3. Run `python3 quiz_game.py` and confirm your question shows up.
4. Commit on a branch:
   ```bash
   git checkout -b onboarding/<your-name>-first-question
   git add questions.json
   git commit -m "Add a question to the quiz"
   ```
5. Open a PR and ask for a review.

---

## Conventions worth knowing

- **Hash before execute.** If you add a task to `opstasks` or a plugin to
  `plugin-demo`, the code alone isn't enough — its hash has to be added to the
  lockfile/manifest, and that change goes through review. Never bump a hash to
  "make it pass" without reviewing what changed.
- **Comments are in Spanish, docs in English.** Match what's already in the file
  you're editing.
- **Small, reviewable changes.** These projects are deliberately tiny; keep PRs
  that way.

---

## Getting help

- Stuck on setup? Ask in the team channel before running anything you're unsure
  about — especially anything that executes downloaded code.
- Found something in this guide that's wrong or out of date? Fix it in a PR. The
  onboarding doc is code too.

Welcome aboard. 🚀
