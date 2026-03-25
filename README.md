```
         __   _ ____            __
   _____/ /__(_) / /___  __  __/ /_______
  / ___/ //_/ / / / __ \/ / / / / ___/ _ \
 (__  ) ,< / / / / /_/ / /_/ / (__  )  __/
/____/_/|_/_/_/_/ .___/\__,_/_/____/\___/
               /_/
```

**Skill telemetry for Claude Code.**

[![Claude Code Plugin](https://img.shields.io/badge/Claude_Code-plugin-5b21b6?style=flat-square)](https://skill7.dev)
[![Version](https://img.shields.io/badge/version-0.1.0-5b21b6?style=flat-square)]()
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> Track what your skills actually do.

---

## The problem

You have skills installed. You see them fire. But you have no idea:
- Which skills the model actually **follows** vs just loads and ignores
- How often each skill activates across sessions
- Whether a skill change improved or degraded quality

Claude Code's built-in telemetry tracks tool calls, not skill adherence. No existing tool captures the `followed` signal -- whether the model executed a skill's instructions after loading it.

## What skillpulse does

A `PostToolUse` hook that intercepts every `Skill` tool call and logs it to local JSONL:

```json
{
  "skill_id": "signum:signum",
  "timestamp": "2026-03-11T08:48:18Z",
  "session_id": "20260311_114818_93074",
  "loaded": true,
  "followed": null,
  "plugin_name": "skillpulse"
}
```

**Key fields:**
- `loaded` -- did the skill body get retrieved?
- `followed` -- did the model execute the skill's instructions? (null until fingerprinting is implemented)
- `session_id` -- group activations by session

**Design choices:**
- 2-second watchdog timeout -- never blocks your workflow
- Filters for `Skill` tool only -- ignores all other tool calls
- JSONL append-only -- zero dependencies, zero cloud, survives crashes

## Install

```bash
claude mcp add-json skillpulse '{"source": {"source": "url", "url": "https://github.com/heurema/skillpulse.git"}}'
```

<details>
<summary>Manual install (from source)</summary>

```bash
git clone https://github.com/heurema/skillpulse.git ~/.claude/plugins/skillpulse
```

</details>

## Usage

Skillpulse works automatically after install -- no commands needed. Every skill activation is logged to:

```
~/.local/share/emporium/activation.jsonl
```

### Aggregator

View per-skill stats:

```bash
python3 scripts/aggregate.py          # human-readable table
python3 scripts/aggregate.py --json   # machine-readable
```

```
Skill                           Acts  Sess  Load% Last seen              Age
--------------------------------------------------------------------------------
herald:news-digest                 2     2  100% 2026-03-04T08:36:04Z    7d
arbiter                            1     1  100% 2026-03-04T08:07:52Z    7d
signum:signum                      1     1  100% 2026-03-04T08:48:18Z    7d

Total: 4 activations, 3 skills
```

## Why this matters

Skillpulse is the foundation for **EvoSkill** -- a pipeline where skills improve themselves based on usage data:

1. **skillpulse** logs activations (you are here)
2. **aggregator** computes per-skill frequency, recency, load rate
3. **bench** runs skills against test tasks, measures pass rate
4. **evolver** proposes skill improvements based on failures

Without activation data, skill improvement is guesswork.

## Privacy

Everything runs locally. No data leaves your machine. Logs are plain JSONL files you can inspect, edit, or delete at any time.

## See also

- [skill7.dev](https://skill7.dev) -- plugin catalog and docs
- [EvoSkill research](https://github.com/heurema/skillpulse/wiki) -- self-improving skill systems

## License

[MIT](LICENSE)
