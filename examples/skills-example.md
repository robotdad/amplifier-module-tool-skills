---
profile:
  name: skills-example
  version: "1.0.0"
  description: "Example profile demonstrating skills support"

session:
  orchestrator:
    module: loop-basic
  context:
    module: context-skills
    config:
      base_context: context-simple
      skills_dirs:  # Multiple sources supported
        - .amplifier/skills  # Project-specific skills
        # - ~/anthropic-skills  # Uncomment if you cloned github.com/anthropics/skills
      auto_inject_metadata: true
      max_tokens: 200000

providers:
  - module: provider-anthropic
    config:
      priority: 1
      default_model: claude-sonnet-4-5

tools:
  - module: tool-filesystem
  - module: tool-bash
  - module: tool-skills
    config:
      skills_dirs:  # Same directories as context
        - .amplifier/skills
        # - ~/anthropic-skills  # Uncomment if you cloned github.com/anthropics/skills

hooks:
  - module: hooks-logging
---

# Skills-Enabled Profile

This profile demonstrates Amplifier's support for [Anthropic Skills](https://github.com/anthropics/skills) - folders of instructions that Claude loads dynamically for specialized tasks.

## What This Enables

Skills provide progressive disclosure of domain knowledge:
- See available skills automatically in system instruction
- Load full content only when needed (60-65% token savings)
- Support multiple skill sources (Anthropic + your own)

## Quick Start

### With Test Skills (Included)

```bash
# Copy profile
cp examples/skills-example.md .amplifier/profiles/

# Copy test skills
mkdir -p .amplifier/skills
cp -r tests/fixtures/skills/* .amplifier/skills/

# Run
amplifier run --profile skills-example "List available skills"
```

### With Anthropic Skills (Recommended)

```bash
# Clone Anthropic skills
git clone https://github.com/anthropics/skills ~/anthropic-skills

# Uncomment the ~/anthropic-skills line in this profile

# Run
amplifier run --profile skills-example "List available skills"
```

## Workflow

When working with skills:
1. Available skills listed in system instruction (automatic)
2. Load when needed: use `load_skill` tool
3. Follow guidelines from loaded skills
4. Skills persist across conversation turns

## Configuration

**Default**: Looks for skills in `.amplifier/skills/`

**Multiple sources**: Uncomment `~/anthropic-skills` to add Anthropic's skill library

**Custom locations**: Edit `skills_dirs` to point to your skill directories
