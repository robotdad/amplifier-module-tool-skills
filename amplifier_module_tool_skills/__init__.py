"""
Amplifier tool for loading domain knowledge from skills.
Provides explicit skill discovery and loading capabilities.
"""

import logging
from pathlib import Path
from typing import Any

from amplifier_module_tool_skills.discovery import discover_skills
from amplifier_module_tool_skills.discovery import extract_skill_body

logger = logging.getLogger(__name__)


async def mount(coordinator: Any, config: dict[str, Any] | None = None) -> None:
    """
    Mount the skills tool.

    Args:
        coordinator: Module coordinator
        config: Tool configuration

    Returns:
        Optional cleanup function
    """
    config = config or {}
    tool = SkillsTool(config)
    await coordinator.mount("tools", tool, name=tool.name)
    logger.info("Mounted SkillsTool")
    return


class SkillsTool:
    """Tool for loading domain knowledge from skills."""

    name = "load_skill"
    description = (
        "Load domain knowledge from an available skill. Skills provide "
        "specialized knowledge, workflows, best practices, and standards. "
        "Use when you need domain expertise, coding guidelines, or "
        "architectural patterns. Call with list=true to see all skills."
    )

    def __init__(self, config: dict[str, Any]):
        """
        Initialize skills tool.

        Args:
            config: Tool configuration
        """
        self.config = config
        skills_dir = config.get("skills_dir", ".amplifier/skills")
        self.skills_dir = Path(skills_dir)
        self.skills = discover_skills(self.skills_dir)
        logger.info(f"Discovered {len(self.skills)} skills from {self.skills_dir}")

    @property
    def input_schema(self) -> dict:
        """Return JSON schema for tool parameters."""
        return {
            "type": "object",
            "properties": {
                "skill_name": {
                    "type": "string",
                    "description": "Name of skill to load (e.g., 'design-patterns', 'python-standards')",
                },
                "list": {"type": "boolean", "description": "If true, return list of all available skills"},
                "search": {"type": "string", "description": "Search term to filter skills by name or description"},
                "info": {
                    "type": "string",
                    "description": "Get metadata for a specific skill without loading full content",
                },
            },
        }

    async def execute(self, input: dict[str, Any]) -> Any:
        """
        Execute skill tool operation.

        Args:
            input: Tool parameters

        Returns:
            Tool result with skill content or list
        """
        # Import here to avoid circular dependency
        from amplifier_core import ToolResult

        # List mode
        if input.get("list"):
            return self._list_skills()

        # Search mode
        if search_term := input.get("search"):
            return self._search_skills(search_term)

        # Info mode
        if skill_name := input.get("info"):
            return self._get_skill_info(skill_name)

        # Load mode
        skill_name = input.get("skill_name")
        if not skill_name:
            return ToolResult(
                success=False, error={"message": "Must provide skill_name, list=true, search='term', or info='name'"}
            )

        return self._load_skill(skill_name)

    def _list_skills(self) -> Any:
        """List all available skills."""
        from amplifier_core import ToolResult

        if not self.skills:
            return ToolResult(success=True, output={"message": f"No skills found in {self.skills_dir}"})

        skills_list = []
        for name, metadata in sorted(self.skills.items()):
            skills_list.append({"name": name, "description": metadata.description})

        lines = ["Available Skills:", ""]
        for skill in skills_list:
            lines.append(f"**{skill['name']}**: {skill['description']}")

        return ToolResult(success=True, output={"message": "\n".join(lines), "skills": skills_list})

    def _search_skills(self, search_term: str) -> Any:
        """Search skills by name or description."""
        from amplifier_core import ToolResult

        matches = {}
        for name, metadata in self.skills.items():
            if search_term.lower() in name.lower() or search_term.lower() in metadata.description.lower():
                matches[name] = metadata

        if not matches:
            return ToolResult(success=True, output={"message": f"No skills matching '{search_term}'"})

        lines = [f"Skills matching '{search_term}':", ""]
        results = []
        for name, metadata in sorted(matches.items()):
            lines.append(f"**{name}**: {metadata.description}")
            results.append({"name": name, "description": metadata.description})

        return ToolResult(success=True, output={"message": "\n".join(lines), "matches": results})

    def _get_skill_info(self, skill_name: str) -> Any:
        """Get metadata for a skill without loading full content."""
        from amplifier_core import ToolResult

        if skill_name not in self.skills:
            available = ", ".join(sorted(self.skills.keys()))
            return ToolResult(
                success=False, error={"message": f"Skill '{skill_name}' not found. Available: {available}"}
            )

        metadata = self.skills[skill_name]
        info = {
            "name": metadata.name,
            "description": metadata.description,
            "version": metadata.version,
            "license": metadata.license,
            "path": str(metadata.path),
        }

        if metadata.metadata:
            info["metadata"] = metadata.metadata

        return ToolResult(success=True, output=info)

    def _load_skill(self, skill_name: str) -> Any:
        """Load full skill content."""
        from amplifier_core import ToolResult

        if skill_name not in self.skills:
            available = ", ".join(sorted(self.skills.keys()))
            return ToolResult(
                success=False, error={"message": f"Skill '{skill_name}' not found. Available: {available}"}
            )

        metadata = self.skills[skill_name]
        body = extract_skill_body(metadata.path)

        if not body:
            return ToolResult(success=False, error={"message": f"Failed to load content from {metadata.path}"})

        logger.info(f"Loaded skill: {skill_name}")

        return ToolResult(
            success=True,
            output={
                "content": f"# {skill_name}\n\n{body}",
                "skill_name": skill_name,
                "loaded_from": str(self.skills_dir),
            },
        )
