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
