---
name: md-updater
description: Maintains and updates project documentation files (README, Commands, Installation, Manual) whenever code or project structure changes
type: skill
---

# Skill: md-updater

## Purpose

Maintain and update project documentation whenever code or project structure changes. Review newly created or modified scripts, features, commands, or workflows and update relevant documentation files accordingly. Works with Markdown (.md), PDF (.pdf), and text (.txt) documentation formats.

## When to Use

Use this skill after any significant code changes, new script creation, feature additions, or project structure modifications to ensure documentation stays current.

## Core Documentation Files

### README.md
- Project overview and quick start guide
- Feature list and general usage instructions
- Version history and changelog summary

### Commands.md (and optionally Commands.txt)
- Complete list of available commands
- CLI arguments and usage examples
- Expected outputs and return codes

### Installation.md
- Environment setup instructions
- Dependency installation steps
- Configuration requirements
- Platform-specific notes (Windows, Linux, macOS)

### Manual.md
- Comprehensive user manual
- Detailed operational guidance
- Workflows and troubleshooting
- Advanced usage and configuration

## Update Triggers

Update documentation when:
- New scripts or features are added
- Command-line interfaces change
- Dependencies are added or updated
- Configuration formats change
- Workflows are modified
- Platform-specific behavior changes

## Documentation Standards

- Clear and well-structured with proper headings
- Consistent formatting and terminology
- Up-to-date with current codebase
- Easy to navigate for users and developers
- Include code examples and usage instructions

## Output Directory

All documentation files stored inside `/docs` directory to keep documentation organized and centralized.

## Critical Rules

- Always update docs after code changes
- Keep documentation synchronized with codebase
- Maintain consistent formatting across all files
- Include usage examples for all commands
- Document platform-specific differences
