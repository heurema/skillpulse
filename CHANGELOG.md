# Changelog

## 0.1.0

- PostToolUse hook: log all Skill tool activations to JSONL
- Fields: skill_id, loaded, followed, session_id, timestamp, plugin_name
- Log path: ~/.local/share/emporium/activation.jsonl (XDG spec)
- 2s self-kill watchdog, single jq call, atomic printf writes
