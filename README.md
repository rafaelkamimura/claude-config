# Claude Configuration

My personal Claude Code configuration and custom agents.

## Contents

- **Configuration**: 
  - `.claude.json` - Main Claude configuration (editor mode, tips, etc.)
  - `settings.json` - Claude settings

- **Custom Agents**:
  - `agents/` - Collection of custom subagents for specialized tasks

## Features

- Vim editor mode enabled
- Auto-updates enabled
- IDE auto-connection enabled
- Shift+Enter keybinding installed
- Custom subagents for various development tasks

## Installation

1. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/claude-config.git ~/github/claude-config
```

2. Copy configuration files:
```bash
# Copy main configuration
cp ~/github/claude-config/.claude.json ~/.claude.json

# Copy settings
cp ~/github/claude-config/settings.json ~/.claude/settings.json

# Copy agents
cp -r ~/github/claude-config/agents ~/.claude/
```

## Custom Agents

The `agents/` directory contains custom subagents for specialized tasks. To use them in Claude Code:

1. Type `/agents` to see available agents
2. Use `@agent-name` to invoke a specific agent

## Note

This configuration does not include any sensitive information like API keys or authentication tokens. Those should be configured separately in your environment.