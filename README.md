# Amplifier Skills Tool Module

Tool for loading domain knowledge from skills in Amplifier.

## What Are Skills?

Skills are **folders of instructions, scripts, and resources that agents load dynamically to improve performance on specialized tasks** (see [Anthropic Skills](https://github.com/anthropics/skills)).

This module brings Anthropic Skills support to Amplifier, enabling:
- Progressive disclosure of domain knowledge
- Reusable instruction packages for specialized tasks
- Integration with Anthropic's skills ecosystem

## Quick Start with Anthropic Skills

```bash
# 1. Clone Anthropic's skills repository
git clone https://github.com/anthropics/skills ~/anthropic-skills

# 2. Install this module
cd amplifier-module-tool-skills
uv pip install -e .

# 3. Configure in your Amplifier profile
cat >> .amplifier/profiles/my-profile.md << 'EOF'
tools:
  - module: tool-skills
    config:
      skills_dirs:
        - ~/anthropic-skills
        - .amplifier/skills
EOF

# 4. Use with Amplifier
amplifier run --profile my-profile "List available skills"
```

All Anthropic skills are now available to your agent!

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

### With context-skills (Recommended)

Configure skills once in the context section - tool-skills reads from capability:

```yaml
session:
  context:
    module: context-skills
    config:
      skills_dirs:  # Single configuration
        - ~/anthropic-skills
        - .amplifier/skills

tools:
  - module: tool-skills  # No config needed - reads from context capability
```

### Standalone (Without context-skills)

```yaml
tools:
  - module: tool-skills
    config:
      skills_dirs:  # Configure directly if not using context-skills
        - ~/anthropic-skills
        - .amplifier/skills
```

**Default:** If not configured, uses `.amplifier/skills`

### Using Anthropic Skills

```bash
# Clone Anthropic's skills repository
git clone https://github.com/anthropics/skills ~/anthropic-skills

# Add to your profile
skills:
  dirs:
    - ~/anthropic-skills
    - .amplifier/skills
```

All skills from both directories become available to the agent.

## Skills Directory Structure

Skills follow the [Anthropic Skills format](https://github.com/anthropics/skills):

```
skills-directory/
├── design-patterns/
│   ├── SKILL.md          # Required: name and description in YAML frontmatter
│   └── examples/
│       └── module-pattern.md
├── python-standards/
│   ├── SKILL.md
│   ├── async-patterns.md
│   └── type-hints.md
└── module-development/
    └── SKILL.md
```

Default location: `.amplifier/skills/` (can configure multiple directories)

## SKILL.md Format

Skills use the [Anthropic Skills format](https://github.com/anthropics/skills) - YAML frontmatter with markdown body:

```markdown
---
name: skill-name  # Required: unique identifier (lowercase with hyphens)
description: What this skill does and when to use it  # Required: complete explanation
version: 1.0.0
license: MIT
metadata:  # Optional
  category: development
  complexity: medium
---

# Skill Name

Instructions the agent follows when skill is loaded.

## Quick Start

[Minimal example to get started]

## Detailed Instructions

[Step-by-step guidance]

## Examples

[Concrete examples]
```

**Required fields:** `name` and `description` in YAML frontmatter
**Format:** See [Anthropic Skills specification](https://github.com/anthropics/skills) for complete details

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

**Recommended:** Use with `amplifier-module-context-skills` for best experience.

Configure skills once - tool-skills reads from context capability:

```yaml
session:
  context:
    module: context-skills
    config:
      skills_dirs:  # Single configuration point
        - ~/anthropic-skills
        - .amplifier/skills

tools:
  - module: tool-skills  # No config - reads from capability
```

**How they work together:**
1. Context discovers skills and registers capability
2. Tool reads from capability (no duplicate discovery)
3. Agent sees skills automatically and can load on demand
4. Context tracks loaded skills (prevents redundant loading)

**Single configuration** via capability registry - no duplication needed.

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

