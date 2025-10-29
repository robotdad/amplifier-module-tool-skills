---
profile:
  name: skills-example
  version: "1.0.0"
  description: "Example profile demonstrating skills support"

session:
  orchestrator:
    module: loop-streaming
    source: git+https://github.com/microsoft/amplifier-module-loop-streaming@main
  context:
    module: context-simple
    source: git+https://github.com/microsoft/amplifier-module-context-simple@main
    config:
      max_tokens: 200000

providers:
  - module: provider-anthropic
    source: git+https://github.com/microsoft/amplifier-module-provider-anthropic@main
    config:
      priority: 1
      default_model: claude-sonnet-4-5

tools:
  - module: tool-filesystem
    source: git+https://github.com/microsoft/amplifier-module-tool-filesystem@main
  - module: tool-bash
    source: git+https://github.com/microsoft/amplifier-module-tool-bash@main
  - module: tool-skills
    source: git+https://github.com/robotdad/amplifier-module-tool-skills@main
    config:
      skills_dirs:  # Configure directly when not using context-skills
        - .amplifier/skills
        # - ~/anthropic-skills  # Uncomment if you cloned github.com/anthropics/skills

hooks:
  - module: hooks-streaming-ui
    source: git+https://github.com/microsoft/amplifier-module-hooks-streaming-ui@main
  - module: hooks-logging
    source: git+https://github.com/microsoft/amplifier-module-hooks-logging@main
---

# Skills-Enabled Profile

This profile demonstrates Amplifier's support for [Anthropic Skills](https://github.com/anthropics/skills) - folders of instructions that agents load dynamically for specialized tasks.

## What This Enables

Skills provide on-demand loading of domain knowledge:
- Discover skills via `load_skill(list=true)`
- Load full content only when needed (60-65% token savings)
- Support multiple skill sources (Anthropic + your own)

**Note**: This profile uses `tool-skills` in standalone mode (without `context-skills`). Skills are discovered on-demand rather than auto-injected into system instruction.

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
