# Sync VPS Configuration to GitHub

Sync VPS-specific Claude Code configuration to the vps/ directory in the claude-config repository.

## Purpose
- Sync VPS-optimized CLAUDE.md to version control
- Sync VPS-specific settings.local.json
- Sync VPS-specific slash commands only
- Maintain separate VPS configs with Makefile for easy installation
- Never mention AI/automation in commit messages

## Execution Steps

### Step 1: Verify Repository Location

Use Bash tool with command:
```bash
ls -la ~/github/claude-config
```

Description: "Verify claude-config repository location"

If directory doesn't exist:

Output: "Error: Repository not found at ~/github/claude-config. Please clone the repository first."

Exit command.

### Step 2: Create VPS Directory Structure

Use Bash tool with command:
```bash
mkdir -p ~/github/claude-config/vps/commands && echo "VPS directory structure created"
```

Description: "Create vps directory structure in repository"

### Step 3: Copy VPS-Specific Files

Use Bash tool with command:
```bash
echo "=== COPYING VPS CONFIGURATION ===" && cp ~/.claude/CLAUDE.md ~/github/claude-config/vps/ && echo "✓ Copied VPS global CLAUDE.md" && cp ~/.claude/settings.local.json ~/github/claude-config/vps/ && echo "✓ Copied VPS settings.local.json"
```

Description: "Copy VPS global configuration files"

### Step 4: Copy VPS-Specific Slash Commands

Use Bash tool with command:
```bash
echo "=== COPYING VPS SLASH COMMANDS ===" && for cmd in server-health backup ssl-renew monitor-logs docker-cleanup deploy rollback security-scan commit review-code; do if [ -f ~/.claude/commands/$cmd.md ]; then cp ~/.claude/commands/$cmd.md ~/github/claude-config/vps/commands/ && echo "✓ Copied $cmd.md"; fi; done
```

Description: "Copy VPS-specific slash commands"

### Step 5: Create/Update Makefile

Use Write tool to create file at `~/github/claude-config/vps/Makefile` with content:

```makefile
# VPS Claude Code Configuration Installer
# Run 'make install' to install VPS-specific configs

.PHONY: help install backup clean status

help:
	@echo "VPS Claude Code Configuration"
	@echo ""
	@echo "Available targets:"
	@echo "  make install   - Install VPS configs to ~/.claude/"
	@echo "  make backup    - Backup current configs before install"
	@echo "  make clean     - Remove installed VPS configs"
	@echo "  make status    - Show current configuration status"

install: backup
	@echo "=== Installing VPS Configuration ==="
	@echo ""
	@echo "Installing global CLAUDE.md..."
	@cp CLAUDE.md ~/.claude/CLAUDE.md
	@echo "✓ Installed CLAUDE.md"
	@echo ""
	@echo "Installing settings.local.json..."
	@cp settings.local.json ~/.claude/settings.local.json
	@echo "✓ Installed settings.local.json"
	@echo ""
	@echo "Installing VPS slash commands..."
	@mkdir -p ~/.claude/commands
	@cp commands/*.md ~/.claude/commands/
	@echo "✓ Installed $(shell ls commands/*.md | wc -l) slash commands"
	@echo ""
	@echo "=== Installation Complete ==="
	@echo "VPS configuration installed to ~/.claude/"

backup:
	@echo "=== Backing Up Current Configuration ==="
	@mkdir -p ~/.claude/backups
	@if [ -f ~/.claude/CLAUDE.md ]; then \
		cp ~/.claude/CLAUDE.md ~/.claude/backups/CLAUDE.md.backup.$$(date +%Y%m%d_%H%M%S); \
		echo "✓ Backed up CLAUDE.md"; \
	fi
	@if [ -f ~/.claude/settings.local.json ]; then \
		cp ~/.claude/settings.local.json ~/.claude/backups/settings.local.json.backup.$$(date +%Y%m%d_%H%M%S); \
		echo "✓ Backed up settings.local.json"; \
	fi
	@echo "Backups saved to ~/.claude/backups/"

clean:
	@echo "=== Removing VPS Configuration ==="
	@echo "This will remove VPS configs from ~/.claude/"
	@echo "Backups in ~/.claude/backups/ will be preserved"
	@read -p "Continue? [y/N] " confirm && [ "$$confirm" = "y" ] || exit 1
	@rm -f ~/.claude/CLAUDE.md
	@rm -f ~/.claude/settings.local.json
	@for cmd in $(shell ls commands/*.md 2>/dev/null | xargs -n1 basename); do \
		rm -f ~/.claude/commands/$$cmd; \
	done
	@echo "✓ VPS configuration removed"

status:
	@echo "=== VPS Configuration Status ==="
	@echo ""
	@echo "Global CLAUDE.md:"
	@if [ -f ~/.claude/CLAUDE.md ]; then \
		echo "  ✓ Installed ($$(wc -l < ~/.claude/CLAUDE.md) lines)"; \
	else \
		echo "  ✗ Not installed"; \
	fi
	@echo ""
	@echo "Settings:"
	@if [ -f ~/.claude/settings.local.json ]; then \
		echo "  ✓ Installed ($$(wc -l < ~/.claude/settings.local.json) lines)"; \
	else \
		echo "  ✗ Not installed"; \
	fi
	@echo ""
	@echo "VPS Slash Commands:"
	@for cmd in server-health backup ssl-renew monitor-logs docker-cleanup deploy rollback security-scan commit review-code; do \
		if [ -f ~/.claude/commands/$$cmd.md ]; then \
			echo "  ✓ $$cmd"; \
		else \
			echo "  ✗ $$cmd (missing)"; \
		fi; \
	done
	@echo ""
	@echo "Backups:"
	@if [ -d ~/.claude/backups ]; then \
		echo "  $$(ls ~/.claude/backups/ 2>/dev/null | wc -l) backup files in ~/.claude/backups/"; \
	else \
		echo "  No backups found"; \
	fi
```

### Step 6: Create README for VPS Directory

Use Write tool to create file at `~/github/claude-config/vps/README.md` with content:

```markdown
# VPS Claude Code Configuration

VPS-optimized configuration for Claude Code on Ubuntu 22.04 servers.

## What's Included

- **CLAUDE.md**: VPS-focused global instructions with server management guidance
- **settings.local.json**: VPS-specific permissions (96 lines, optimized)
- **commands/**: VPS-specific slash commands (15 total)

## VPS-Specific Slash Commands

### Server Management (5 new)
- `/server-health` - Comprehensive health monitoring
- `/backup` - Backup orchestration (DB, files, configs, SSL)
- `/ssl-renew` - SSL certificate renewal
- `/monitor-logs` - Real-time log monitoring
- `/docker-cleanup` - Safe Docker resource cleanup

### Development Workflow (10 kept)
- `/commit` - Git commit workflow
- `/deploy` - Deployment orchestration
- `/rollback` - Rollback procedures
- `/review-code` - Code review
- `/security-scan` - Security checks
- `/debug-assistant` - Debugging help
- `/env-sync` - Environment sync
- `/sync-config` - Config sync to GitHub
- `/task-init` - Task initialization
- `/screen-resume` - Screen session management

## Installation

```bash
cd ~/github/claude-config/vps
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
```

### Step 7: Check Git Status

Use Bash tool with command:
```bash
cd ~/github/claude-config && git status --porcelain
```

Description: "Check git status for changes"

Store output as GIT_STATUS.

If GIT_STATUS is empty:

Output: "No changes to commit. VPS configuration is already up to date."

Exit command.

Use Bash tool with command:
```bash
cd ~/github/claude-config && git status
```

Description: "Show detailed git status"

### Step 8: Stage All Changes

Use Bash tool with command:
```bash
cd ~/github/claude-config && git add vps/
```

Description: "Stage VPS configuration changes"

### Step 9: Generate Commit Message

Analyze GIT_STATUS to determine what changed in vps/ directory:

Check for patterns:
- If "vps/commands/" files changed: Note "VPS slash commands updated"
- If "vps/CLAUDE.md" changed: Note "VPS global instructions updated"
- If "vps/settings.local.json" changed: Note "VPS settings updated"
- If "vps/Makefile" changed or new: Note "VPS Makefile updated"
- If "vps/README.md" changed or new: Note "VPS README updated"

Construct commit message based on changes found.

Examples:
- "Update VPS configuration and slash commands"
- "Add new VPS server management commands"
- "Update VPS settings and global instructions"
- "Update VPS configuration - [current date]"

IMPORTANT: NEVER mention "Claude", "AI", "Generated", or "Co-Authored" in commit messages.

### Step 10: Commit Changes

Use Bash tool with command (replace {message} with generated message):
```bash
cd ~/github/claude-config && git commit -m "{message}"
```

Description: "Commit VPS configuration changes"

Store commit hash from output.

### Step 11: Push to GitHub

Use Bash tool with command:
```bash
cd ~/github/claude-config && git push
```

Description: "Push VPS configuration to GitHub"

### Step 12: Verify Success

Use Bash tool with command:
```bash
cd ~/github/claude-config && git log --oneline -1
```

Description: "Show last commit"

### Step 13: Provide Summary

Use Bash tool with command:
```bash
cd ~/github/claude-config && git diff --stat HEAD~1 vps/
```

Description: "Get VPS directory diff statistics"

Output summary:

```
## VPS Configuration Sync Complete

**Files synced to vps/ directory**:
- VPS global instructions (CLAUDE.md)
- VPS settings (settings.local.json)
- VPS slash commands (commands/)
- Installation Makefile
- README documentation

**Commands included**:
- server-health, backup, ssl-renew, monitor-logs, docker-cleanup
- commit, deploy, rollback, review-code, security-scan
- And 5 more VPS-relevant commands

**Changes**:
[Show git diff statistics]

**Commit**: [commit hash]
**Pushed to**: github.com/[username]/claude-config/vps/

✓ VPS configuration successfully synced to GitHub!

**To install on another VPS**:
```bash
cd ~/github/claude-config/vps
make install
```
```

## Error Handling

### Repository Not Found
- Provide clear error message
- Suggest cloning the repository
- Exit gracefully

### No Changes Detected
- Inform user VPS configuration is up to date
- Exit without committing

### Git Push Failure
- Show error message
- Suggest checking remote connection
- Offer to retry

### File Copy Errors
- Log which files failed to copy
- Continue with other files
- Report failures in summary

## Notes
- Syncs only VPS-specific configurations
- Separate from main config sync
- Includes Makefile for easy installation on new VPS
- Provides README for documentation
- Never mentions AI/automation in commits
- Handles missing directories gracefully
