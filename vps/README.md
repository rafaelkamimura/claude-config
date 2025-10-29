# VPS Claude Code Configuration

VPS-optimized configuration for Claude Code on Ubuntu 22.04 servers.

## What's Included

- **CLAUDE.md**: VPS-focused global instructions with server management guidance
- **settings.local.json**: VPS-specific permissions (96 lines, optimized)
- **commands/**: VPS-specific slash commands (16 total)

## VPS-Specific Slash Commands

### Server Management (5 new)
- `/server-health` - Comprehensive health monitoring
- `/backup` - Backup orchestration (DB, files, configs, SSL)
- `/ssl-renew` - SSL certificate renewal
- `/monitor-logs` - Real-time log monitoring
- `/docker-cleanup` - Safe Docker resource cleanup

### Development Workflow (11 kept)
- `/commit` - Git commit workflow
- `/deploy` - Deployment orchestration
- `/rollback` - Rollback procedures
- `/review-code` - Code review
- `/security-scan` - Security checks
- `/debug-assistant` - Debugging help
- `/env-sync` - Environment sync
- `/sync-config` - Config sync to GitHub
- `/sync-vps-config` - VPS config sync to GitHub
- `/task-init` - Task initialization
- `/screen-resume` - Screen session management

## Installation

```bash
cd ~/claude-config/vps
make install
```

This will:
1. Backup your current configuration
2. Install VPS-optimized global CLAUDE.md
3. Install VPS-specific settings.local.json
4. Install all VPS slash commands

## Makefile Commands

```bash
make help      # Show available commands
make install   # Install VPS configuration
make backup    # Backup current configuration
make clean     # Remove VPS configuration
make status    # Show installation status
```

## Manual Installation

If you prefer manual installation:

```bash
# Global instructions
cp CLAUDE.md ~/.claude/CLAUDE.md

# Settings
cp settings.local.json ~/.claude/settings.local.json

# Slash commands
cp commands/*.md ~/.claude/commands/
```

## Differences from Standard Config

**Removed**:
- macOS-specific content and commands
- Development machine workflows
- Personal computer setup instructions
- Azure DevOps, Interview, HR commands
- 25 irrelevant slash commands (archived)

**Added**:
- VPS server management sections
- Emergency procedures and troubleshooting
- Server monitoring and maintenance
- Docker and Nginx optimization guides
- SSL certificate management
- Automated backup scripts

**Optimized**:
- Settings: 39% smaller (no macOS pollution)
- Commands: 71% fewer options (VPS-relevant only)
- Global config: 25% more concise, 100% VPS-focused

## System Requirements

- Ubuntu 22.04 LTS (tested)
- Claude Code CLI installed
- Server services: Nginx, Docker, MariaDB/MySQL
- Root or sudo access

## Maintenance

Keep your VPS configuration in sync:

```bash
# From VPS server, run:
/sync-vps-config

# This will sync changes back to GitHub
```

## Version

**Last Updated**: 2025-10-29
**Optimized For**: VPS servers running production services
**Server Specs**: 4 CPU cores, 16GB RAM, Ubuntu 22.04 LTS
