# test-structure — Skillpulse Plugin Structure Check

Verify that the skillpulse plugin has the expected directory structure
and required files in place. This is a structural integrity test that
does not invoke Claude Code or any AI model.

## Setup

No setup required. The plugin is expected to be present at
`devtools/skillpulse/` relative to the repository root.

## Input

Plugin root directory: `devtools/skillpulse/`

## Expected Output

All required files and directories exist:
- `README.md`
- `skills/` directory

## Validation

```bash
PLUGIN_ROOT="$(cd "../../../../devtools/skillpulse" && pwd)"
test -f "$PLUGIN_ROOT/README.md" && \
test -d "$PLUGIN_ROOT/skills"
```
