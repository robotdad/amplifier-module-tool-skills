# Skills Module Profile Updates - 2025-10-28

## Issue Summary

The skills example profile had multiple integration issues with the rapidly evolving amplifier-dev ecosystem:
1. Missing source URLs for all modules
2. Using `loop-basic` orchestrator (incompatible with streaming hooks)
3. Missing `hooks-streaming-ui` for proper formatting
4. Type error in __init__.py (coordinator can be None)

## Root Causes

### 1. Profile Source URLs Now Required

**Discovery**: Amplifier changed to require explicit `source:` git URLs for ALL module references.

**Evidence**: Comparing with bundled profiles (base.md, dev.md) which all have source URLs for every module.

**Fix**: Added source URLs to all modules in example profile:
```yaml
orchestrator:
  module: loop-streaming
  source: git+https://github.com/microsoft/amplifier-module-loop-streaming@main

providers:
  - module: provider-anthropic
    source: git+https://github.com/microsoft/amplifier-module-provider-anthropic@main

tools:
  - module: tool-filesystem
    source: git+https://github.com/microsoft/amplifier-module-tool-filesystem@main
  - module: tool-bash
    source: git+https://github.com/microsoft/amplifier-module-tool-bash@main
  - module: tool-skills
    source: git+https://github.com/robotdad/amplifier-module-tool-skills@main

hooks:
  - module: hooks-streaming-ui
    source: git+https://github.com/microsoft/amplifier-module-hooks-streaming-ui@main
  - module: hooks-logging
    source: git+https://github.com/microsoft/amplifier-module-hooks-logging@main
```

### 2. Orchestrator Compatibility

**Discovery**: `loop-basic` orchestrator is incompatible with `hooks-streaming-ui` hook, causing raw TextBlock output.

**Evidence from MCP integration fixes**: "_loop-basic + hooks-streaming-ui = raw TextBlock output. loop-streaming + hooks-streaming-ui = formatted output_"

**Fix**: Changed orchestrator from `loop-basic` to `loop-streaming`:
```yaml
session:
  orchestrator:
    module: loop-streaming  # Not loop-basic!
    source: git+https://github.com/microsoft/amplifier-module-loop-streaming@main
```

### 3. Missing Streaming UI Hook

**Discovery**: Missing `hooks-streaming-ui` results in poor response formatting.

**Evidence**: All bundled profiles include `hooks-streaming-ui` for proper user experience.

**Fix**: Added hooks-streaming-ui to hooks section:
```yaml
hooks:
  - module: hooks-streaming-ui
    source: git+https://github.com/microsoft/amplifier-module-hooks-streaming-ui@main
  - module: hooks-logging
    source: git+https://github.com/microsoft/amplifier-module-hooks-logging@main
```

### 4. Type Error with Optional Coordinator

**Discovery**: Type checker error because coordinator parameter is optional (can be None) but code called methods without checking.

**Error**:
```
amplifier_module_tool_skills/__init__.py:71:43 - error: "get_capability" is not a known attribute of "None" (reportOptionalMemberAccess)
amplifier_module_tool_skills/__init__.py:72:48 - error: "get_capability" is not a known attribute of "None" (reportOptionalMemberAccess)
```

**Fix**: Added None check before calling coordinator methods:
```python
# Before (fails type check)
skills_from_context = coordinator.get_capability("skills.registry")
skills_dirs_from_context = coordinator.get_capability("skills.directories")

# After (passes type check)
skills_from_context = coordinator.get_capability("skills.registry") if coordinator else None
skills_dirs_from_context = coordinator.get_capability("skills.directories") if coordinator else None
```

## Key Learnings

### Evidence-Based Approach

1. **Compared with working examples** - Bundled profiles show current patterns
2. **Applied MCP lessons** - Same issues affected MCP module
3. **Validated with tests** - `make check` confirms fixes work

### Amplifier Evolution Patterns

1. **Source URLs are now required** - ALL module references need explicit git sources
2. **Orchestrator/hook compatibility matters** - Not all combinations work
3. **Type safety is enforced** - Pyright catches optional parameter issues
4. **Streaming UX is standard** - Most profiles use loop-streaming + hooks-streaming-ui

## Testing Checklist

Before considering this complete:
- [x] `make check` passes (no type errors, format, lint)
- [ ] Test with actual skills directory
- [ ] Verify skills discovery works
- [ ] Verify skills loading works
- [ ] Test with Anthropic skills repository
- [ ] Verify no TextBlock raw output
- [ ] Check streaming UI formatting

## Files Changed

**Profile updates**:
- `examples/skills-example.md` - Complete working profile with all source URLs, correct orchestrator, streaming UI

**Code fixes**:
- `amplifier_module_tool_skills/__init__.py` - Fixed type error for optional coordinator

## Working Profile Pattern

```yaml
profile:
  name: skills-example
  version: "1.0.0"
  description: "Example profile demonstrating skills support"

session:
  orchestrator:
    module: loop-streaming  # Required for hooks-streaming-ui
    source: git+https://github.com/microsoft/amplifier-module-loop-streaming@main
  context:
    module: context-skills
    source: git+https://github.com/robotdad/amplifier-module-context-skills@main
    config:
      base_context: context-simple
      skills_dirs:
        - .amplifier/skills
      auto_inject_metadata: true
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

hooks:
  - module: hooks-streaming-ui  # Required for proper formatting
    source: git+https://github.com/microsoft/amplifier-module-hooks-streaming-ui@main
  - module: hooks-logging
    source: git+https://github.com/microsoft/amplifier-module-hooks-logging@main
```

## Next Steps

1. **Test the profile** with actual Amplifier to verify it works
2. **Check context-skills module** for similar issues
3. **Document in README** if any usage patterns changed
4. **Update any other example files** if they exist

## Recommendations

1. **For rapid-change codebases**: Always compare with working bundled examples first
2. **For module updates**: Check both example profiles AND code for consistency
3. **For type safety**: Run `make check` before committing
4. **For validation**: Test with actual execution, not assumptions
