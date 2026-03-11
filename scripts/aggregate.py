#!/usr/bin/env python3
"""Session aggregator for skillpulse activation logs.

Reads activation.jsonl → per-skill stats: frequency, recency, loaded_rate.

Usage:
    python3 aggregate.py                    # human-readable table
    python3 aggregate.py --json             # machine-readable JSON
    python3 aggregate.py --log /path/to.jsonl  # custom log path
"""

import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_LOG = Path.home() / ".local/share/emporium/activation.jsonl"


def parse_args():
    log_path = DEFAULT_LOG
    output_json = False
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--json":
            output_json = True
        elif args[i] == "--log" and i + 1 < len(args):
            i += 1
            log_path = Path(args[i])
        i += 1
    return log_path, output_json


def load_entries(path):
    if not path.exists():
        return []
    entries = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return entries


def aggregate(entries):
    skills = defaultdict(lambda: {
        "count": 0, "loaded": 0, "sessions": set(), "timestamps": []
    })
    for e in entries:
        sid = e.get("skill_id", "unknown")
        s = skills[sid]
        s["count"] += 1
        if e.get("loaded"):
            s["loaded"] += 1
        s["sessions"].add(e.get("session_id", ""))
        ts = e.get("timestamp", "")
        if ts:
            s["timestamps"].append(ts)

    now = datetime.now(timezone.utc)
    results = []
    for sid, s in sorted(skills.items(), key=lambda x: -x[1]["count"]):
        last_ts = max(s["timestamps"]) if s["timestamps"] else None
        days_ago = None
        if last_ts:
            try:
                dt = datetime.fromisoformat(last_ts.replace("Z", "+00:00"))
                days_ago = (now - dt).days
            except ValueError:
                pass
        results.append({
            "skill_id": sid,
            "activations": s["count"],
            "unique_sessions": len(s["sessions"]),
            "loaded_rate": round(s["loaded"] / s["count"], 2) if s["count"] else 0,
            "last_seen": last_ts,
            "days_ago": days_ago,
        })
    return results


def print_table(results):
    if not results:
        print("No activation data found.")
        return
    print(f"{'Skill':<30} {'Acts':>5} {'Sess':>5} {'Load%':>6} {'Last seen':<22} {'Age':>5}")
    print("-" * 80)
    for r in results:
        age = f"{r['days_ago']}d" if r["days_ago"] is not None else "?"
        print(f"{r['skill_id']:<30} {r['activations']:>5} {r['unique_sessions']:>5} "
              f"{r['loaded_rate']:>5.0%} {r['last_seen'] or '?':<22} {age:>5}")
    print(f"\nTotal: {sum(r['activations'] for r in results)} activations, "
          f"{len(results)} skills")


def main():
    log_path, output_json = parse_args()
    entries = load_entries(log_path)
    results = aggregate(entries)
    if output_json:
        json.dump(results, sys.stdout, indent=2)
        print()
    else:
        print_table(results)


if __name__ == "__main__":
    main()
