---
name: documentation-agent
description: Continuously updates and maintains all project .md and .txt documentation files
type: skill
---

# Skill: documentation-agent

## Purpose

Maintain all project documentation files (.md and .txt). Update documentation whenever code changes, upgrades, refactoring, or new features are introduced.

## When to Use

Use this skill after significant code changes, new script creation, feature additions, or project structure modifications to ensure documentation stays current and synchronized with the codebase.

## Responsibilities

1. **Modify Existing Documentation**: Update existing docs to reflect code changes
2. **Add New Explanations**: Document new scripts, functions, and features
3. **Update Directory Descriptions**: Keep project structure documentation accurate
4. **Document Workflow Changes**: Record algorithmic or workflow modifications
5. **Create New Documentation**: Generate docs for newly added modules or features

## Documentation Triggers

Update documentation when:
- New scripts or modules are created
- Existing code is modified or improved
- Configuration files are updated
- Project architecture changes
- New dependencies are added
- Algorithms or workflows are modified

## Documentation Standards

- Clear, structured, and consistent formatting
- Accurate reflection of current code state
- Organized with proper headings and sections
- Include code examples where helpful
- Reference function/file names in backticks
- Maintain consistent terminology throughout

## Output

Documentation files updated in the `/docs` directory, ensuring future developers and users can understand the system and how recent changes affect the workflow.

## Critical Rules

- Always update documentation after code changes
- Never leave documentation out of sync with the codebase
- Create documentation for all new modules and features
- Keep explanations clear enough for new team members
