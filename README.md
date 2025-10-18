# Amplifier Skills Tool Module

Tool for loading domain knowledge from skills.

## Prerequisites

- **Python 3.11+**
- **[UV](https://github.com/astral-sh/uv)** - Fast Python package manager

### Installing UV

```bash
# macOS/Linux/WSL
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Purpose

Provides explicit skill discovery and loading capabilities for Amplifier agents. Skills are reusable knowledge packages that provide specialized expertise, workflows, and best practices.

## Contract

**Module Type:** Tool
**Mount Point:** `tools`
**Entry Point:** `amplifier_module_tool_skills:mount`

## What Are Skills?

Skills are **progressive disclosure knowledge packages**:

- **Level 1 (Metadata)**: Name + description (~100 tokens) - Always visible
- **Level 2 (Content)**: Full markdown body (~1-5k tokens) - Loaded on demand
- **Level 3 (References)**: Additional files (0 tokens until accessed)

**Token Efficiency Example:**
```
Without Skills: 6000 tokens of guidelines always loaded
With Skills: 300 tokens metadata + 2000 tokens when needed
Savings: 60-65% token reduction
```

## Tools Provided

### `load_skill`

Load domain knowledge from an available skill.

**Operations:**

1. **List skills**: `load_skill(list=true)` - Show all available skills
2. **Search skills**: `load_skill(search="pattern")` - Filter by keyword
3. **Get metadata**: `load_skill(info="skill-name")` - Metadata only
4. **Load content**: `load_skill(skill_name="skill-name")` - Full content

**Input Schema:**

```json
{
  "type": "object",
  "properties": {
    "skill_name": {"type": "string"},
    "list": {"type": "boolean"},
    "search": {"type": "string"},
    "info": {"type": "string"}
  }
}
```

**Output:**

- **List mode**: Array of `{name, description}` objects
- **Search mode**: Filtered array of matching skills
- **Info mode**: Metadata object (name, description, version, license, path)
- **Load mode**: `{content, skill_name, loaded_from}` object

## Configuration

```yaml
tools:
  - module: tool-skills
    config:
      skills_dir: .amplifier/skills  # Where to find skills
```

## Skills Directory Structure

```
.amplifier/skills/
├── design-patterns/
│   ├── SKILL.md
│   └── examples/
│       └── module-pattern.md
├── python-standards/
│   ├── SKILL.md
│   ├── async-patterns.md
│   └── type-hints.md
└── module-development/
    └── SKILL.md
```

## SKILL.md Format

Required YAML frontmatter with markdown body:

```markdown
---
name: skill-name
description: What this skill does and when to use it. Include when to use it.
version: 1.0.0
license: MIT
metadata:
  category: development
  complexity: medium
---

# Skill Name

## Quick Start

[Minimal example to get started]

## Detailed Instructions

[Step-by-step guidance]

## Advanced Features

See additional-guide.md for details.

## Examples

[Concrete examples]
```

## Usage Examples

### In Agent Definition

```markdown
---
meta:
  name: module-creator
  description: Creates new Amplifier modules

tools:
  - module: tool-filesystem
  - module: tool-bash
  - module: tool-skills  # Enable skills
    config:
      skills_dir: .amplifier/skills
---

You are an Amplifier module creator.

Before creating modules:
1. Call load_skill(list=true) to see available guidelines
2. Load module-development skill for patterns
3. Follow the guidance from the skill
```

### Agent Workflow

```
User: "Create a new tool module for database access"

Agent thinks: "I should check for module development guidelines"

Agent calls: load_skill(search="module")
Response: "**module-development**: Guide for creating modules..."

Agent calls: load_skill(skill_name="module-development")
Response: [Full guide with protocols, entry points, patterns]

Agent uses: Creates module following the skill's patterns
```

### Progressive Loading Example

```python
# Small footprint initially - just metadata
result = await tool.execute({"list": True})
# Returns: ~300 tokens (list of 3 skills)

# Load only what's needed
result = await tool.execute({"skill_name": "python-standards"})
# Returns: ~2000 tokens (full skill content)

# Agent can then read references directly via filesystem
# .amplifier/skills/python-standards/async-patterns.md
# Only loaded if agent needs it
```

## Integration with context-skills

Works seamlessly with `amplifier-module-context-skills`:

```yaml
session:
  context: context-skills  # Auto-injects metadata

tools:
  - module: tool-skills    # Explicit loading
```

**How they work together:**
1. Context injects metadata into system instruction
2. Agent sees available skills automatically
3. Agent calls tool to load full content when needed
4. Context tracks loaded skills (prevents redundant loading)

## Creating Skills

### Simple Skill Example

```bash
mkdir -p .amplifier/skills/my-skill
cat > .amplifier/skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: Does something useful. Use when you need X.
version: 1.0.0
license: MIT
---

# My Skill

## Purpose

[What this skill does]

## Usage

[How to use it]

## Examples

[Complete examples]
EOF
```

### Skill with References

```bash
mkdir -p .amplifier/skills/advanced-skill
cd .amplifier/skills/advanced-skill

# Main skill file
cat > SKILL.md << 'EOF'
---
name: advanced-skill
description: Advanced patterns
---

# Advanced Skill

## Quick Start

[Brief example]

## Detailed Guides

- See patterns.md for design patterns
- See examples.md for complete examples
EOF

# Reference files (loaded on-demand)
echo "# Patterns Guide" > patterns.md
echo "# Examples" > examples.md
```

## Testing

```bash
# Run unit tests
make test

# Run specific test
uv run pytest tests/test_tool.py::test_list_skills -v

# Run integration tests
uv run pytest tests/test_integration.py -v
```

## Development

```bash
# Install dependencies
make install

# Format and check code
make check

# Run all tests
make test
```

## Dependencies

- `amplifier-core` - Core protocols and types
- `pyyaml>=6.0` - YAML parsing

## Contributing

See main Amplifier repository for contribution guidelines.

## License

MIT

