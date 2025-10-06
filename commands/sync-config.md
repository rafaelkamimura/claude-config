# Sync Configuration to GitHub

Sync all Claude Code configuration files to the GitHub repository.

## Task

You are helping sync the user's Claude Code configuration to their GitHub repository.

### Steps

1. **Verify Repository Location**
   ```bash
   ls -la ~/github/claude-config
   ```

2. **Copy All Configuration Files**
   ```bash
   # Copy global instructions
   cp ~/.claude/CLAUDE.md ~/github/claude-config/

   # Copy settings
   cp ~/.claude/settings.json ~/github/claude-config/

   # Copy editor configuration
   cp ~/.claude.json ~/github/claude-config/ 2>/dev/null || echo "No .claude.json found"

   # Copy all slash commands
   cp -r ~/.claude/commands ~/github/claude-config/

   # Copy all subagents
   cp -r ~/.claude/agents ~/github/claude-config/
   ```

3. **Check Git Status**
   ```bash
   cd ~/github/claude-config && git status
   ```

4. **Stage All Changes**
   ```bash
   cd ~/github/claude-config && git add .
   ```

5. **Commit Changes**
   IMPORTANT: NEVER mention "Claude" or "AI" in commit messages.

   Use this format:
   ```bash
   cd ~/github/claude-config && git commit -m "Update configuration files - $(date +'%Y-%m-%d')"
   ```

   Or if there are specific changes:
   - "Add new slash commands"
   - "Update global coding standards"
   - "Add new specialized subagents"
   - "Update settings and preferences"

6. **Push to GitHub**
   ```bash
   cd ~/github/claude-config && git push
   ```

7. **Verify Success**
   ```bash
   cd ~/github/claude-config && git log --oneline -1
   ```

8. **Summary**
   Provide a brief summary:
   - Number of files changed
   - What was updated (commands, agents, settings, etc.)
   - Commit hash
   - Confirmation that changes are pushed to GitHub

## Important Rules

- NEVER mention "Claude", "AI", "Generated", or "Co-Authored" in commit messages
- Use simple, descriptive commit messages
- Always verify the repository exists before copying files
- Show git status before and after committing
- Confirm successful push to GitHub
