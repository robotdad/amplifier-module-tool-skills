# Skills Modules Usage Examples

This directory contains examples showing how to use the skills modules with Amplifier.

## What Are Skills?

Skills are **folders of instructions, scripts, and resources that Claude loads dynamically** to improve performance on specialized tasks. See [Anthropic Skills](https://github.com/anthropics/skills) for the complete specification.

This module enables Anthropic Skills in Amplifier with progressive disclosure and multi-source support.

## Files

### `skills-example.md`

Complete Amplifier profile with skills support enabled.

**Features:**
- Skills-aware context manager
- Skills tool for explicit loading
- Example skills directory configuration
- Ready to use with Amplifier

**Usage:**

```bash
# Copy profile to your project
cp examples/skills-example.md .amplifier/profiles/

# Create skills directory
mkdir -p .amplifier/skills

# Add some skills (use examples from tests/fixtures/skills/)
cp -r amplifier-module-tool-skills/tests/fixtures/skills/* .amplifier/skills/

# Run with profile
amplifier run --profile skills-example "Show me available skills"
```

## Creating Your Own Skills

### Minimal Skill

```bash
mkdir -p .amplifier/skills/my-skill
cat > .amplifier/skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: Brief description of what this does and when to use it
version: 1.0.0
license: MIT
---

# My Skill

## Instructions

[Your guidance here]
EOF
```

### Skill with References

```bash
mkdir -p .amplifier/skills/advanced-skill
cd .amplifier/skills/advanced-skill

# Main skill
cat > SKILL.md << 'EOF'
---
name: advanced-skill
description: Advanced patterns with reference materials
---

# Advanced Skill

## Overview

Brief overview here.

## Detailed Topics

- See patterns.md for design patterns
- See examples.md for code examples
- See troubleshooting.md for common issues
EOF

# Reference materials
cat > patterns.md << 'EOF'
# Design Patterns

[Detailed patterns here]
EOF
```

## Skills Directory Organization

**Recommended structure:**

```
.amplifier/skills/
├── {domain}-{topic}/
│   ├── SKILL.md           # Main instructions (keep < 500 lines)
│   ├── reference.md       # Detailed reference (loaded on-demand)
│   ├── examples.md        # Code examples
│   └── advanced.md        # Advanced topics
```

## Integration Patterns

### With Context-Skills Module

Automatic metadata injection:

```yaml
session:
  context: context-skills
  config:
    auto_inject_metadata: true
```

Agent sees:
```
## Available Skills

**skill-name**: Description of what it does...
```

### With Tool-Skills Module

Explicit loading with multiple sources:

```yaml
tools:
  - module: tool-skills
    config:
      skills_dirs:  # Multiple directories
        - ~/anthropic-skills  # Cloned from github.com/anthropics/skills
        - .amplifier/skills   # Project-specific skills
```

Agent can:
- List: `load_skill(list=true)`
- Search: `load_skill(search="python")`
- Info: `load_skill(info="skill-name")`
- Load: `load_skill(skill_name="skill-name")`

### Using Anthropic Skills

```bash
# Clone Anthropic's skills repository
git clone https://github.com/anthropics/skills ~/anthropic-skills

# Configure in your profile to use both Anthropic skills and your own
config:
  skills_dirs:
    - ~/anthropic-skills
    - .amplifier/skills
```

All skills from both directories become available to your agent.

### Together (Recommended)

```yaml
session:
  context: context-skills  # Discovery
tools:
  - module: tool-skills    # Loading
```

**Result:**
- Agent sees what's available (context)
- Agent loads when needed (tool)
- 60-65% token savings from progressive disclosure
