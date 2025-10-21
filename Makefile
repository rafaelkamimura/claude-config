.PHONY: help install update sync status clean test

# Default target
help:
	@echo "Claude Code Configuration Management"
	@echo ""
	@echo "Available targets:"
	@echo "  make install    - Install configuration from repo to ~/.claude"
	@echo "  make update     - Update repo with current ~/.claude configuration"
	@echo "  make sync       - Commit and push changes to GitHub"
	@echo "  make status     - Show git status and configuration diff"
	@echo "  make clean      - Remove backup files"
	@echo "  make test       - Verify configuration files"
	@echo "  make help       - Show this help message"

# Install configuration from repo to ~/.claude
install:
	@echo "Installing Claude Code configuration..."
	@mkdir -p ~/.claude
	@mkdir -p ~/.claude/commands
	@mkdir -p ~/.claude/agents
	@mkdir -p ~/.claude/skills
	@echo "Copying global instructions..."
	@cp CLAUDE.md ~/.claude/CLAUDE.md
	@echo "Copying settings..."
	@[ -f settings.json ] && cp settings.json ~/.claude/settings.json || echo "No settings.json found"
	@echo "Copying editor configuration..."
	@[ -f .claude.json ] && cp .claude.json ~/.claude.json || echo "No .claude.json found"
	@echo "Copying slash commands..."
	@cp -r commands/* ~/.claude/commands/
	@echo "Copying subagents..."
	@[ -d agents ] && cp -r agents/* ~/.claude/agents/ || echo "No agents directory found"
	@echo "Copying global skills..."
	@[ -d skills ] && cp -r skills/* ~/.claude/skills/ || echo "No skills directory found"
	@echo ""
	@echo "✓ Installation complete!"
	@echo ""
	@echo "Configuration installed to:"
	@echo "  - ~/.claude/CLAUDE.md (global instructions)"
	@echo "  - ~/.claude/settings.json (settings)"
	@echo "  - ~/.claude/commands/ (slash commands)"
	@echo "  - ~/.claude/agents/ (subagents)"
	@echo "  - ~/.claude/skills/ (global skills)"

# Update repo with current ~/.claude configuration
update:
	@echo "Updating repository with local configuration..."
	@echo "Copying from ~/.claude to repository..."
	@cp ~/.claude/CLAUDE.md ./
	@[ -f ~/.claude/settings.json ] && cp ~/.claude/settings.json ./ || echo "No settings.json"
	@[ -f ~/.claude.json ] && cp ~/.claude.json ./ || echo "No .claude.json"
	@[ -d ~/.claude/commands ] && cp -r ~/.claude/commands ./ || echo "No commands directory"
	@[ -d ~/.claude/agents ] && cp -r ~/.claude/agents ./ || echo "No agents directory"
	@[ -d ~/.claude/skills ] && cp -r ~/.claude/skills ./ || echo "No skills directory"
	@echo "✓ Repository updated with local configuration"
	@echo ""
	@make status

# Commit and push changes to GitHub
sync: update
	@echo "Syncing to GitHub..."
	@git add .
	@if git diff --cached --quiet; then \
		echo "No changes to commit"; \
	else \
		git commit -m "Update configuration - $$(date +'%Y-%m-%d %H:%M')"; \
		git push; \
		echo ""; \
		echo "✓ Changes pushed to GitHub"; \
		git log --oneline -1; \
	fi

# Show git status and configuration diff
status:
	@echo "Git status:"
	@git status --short
	@echo ""
	@echo "Files in repository:"
	@ls -lh CLAUDE.md commands/ 2>/dev/null | grep -E '^-|^d' || true
	@echo ""
	@echo "Files in ~/.claude:"
	@ls -lh ~/.claude/CLAUDE.md ~/.claude/commands/ 2>/dev/null | grep -E '^-|^d' || true

# Remove backup files
clean:
	@echo "Cleaning backup files..."
	@find . -name "*.bak" -delete
	@find . -name "*~" -delete
	@find . -name ".DS_Store" -delete
	@echo "✓ Backup files removed"

# Verify configuration files
test:
	@echo "Verifying configuration files..."
	@echo -n "Checking CLAUDE.md... "
	@[ -f CLAUDE.md ] && echo "✓" || echo "✗ MISSING"
	@echo -n "Checking commands directory... "
	@[ -d commands ] && echo "✓" || echo "✗ MISSING"
	@echo -n "Checking ~/.claude/CLAUDE.md... "
	@[ -f ~/.claude/CLAUDE.md ] && echo "✓" || echo "✗ NOT INSTALLED"
	@echo -n "Checking ~/.claude/commands... "
	@[ -d ~/.claude/commands ] && echo "✓" || echo "✗ NOT INSTALLED"
	@echo ""
	@echo "Slash commands available:"
	@[ -d commands ] && ls -1 commands/*.md | sed 's|commands/||g' | sed 's|.md||g' | sed 's|^|  /|' || echo "  None found"
	@echo ""
	@[ -d skills ] && echo "Global skills available:" && ls -1 skills/ | sed 's|^|  |' || echo "No global skills"
