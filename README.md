# Claude Code Configuration

My personal Claude Code configuration with global instructions, custom slash commands, and specialized subagents.

## Contents

- **Global Instructions**: `CLAUDE.md` - Universal coding standards and development workflow
- **Settings**: `settings.json` - Claude Code preferences and permissions
- **Configuration**: `.claude.json` - Editor mode and UI settings
- **Slash Commands**: `commands/` - 25 custom slash commands for common tasks
- **Subagents**: `agents/` - 39 specialized AI agents for different development tasks

## Quick Start

### Installation

1. Clone this repository:
```bash
git clone https://github.com/rafaelkamimura/claude-config.git ~/github/claude-config
```

2. Copy configuration files to your Claude directory:
```bash
# Copy global instructions
cp ~/github/claude-config/CLAUDE.md ~/.claude/CLAUDE.md

# Copy settings
cp ~/github/claude-config/settings.json ~/.claude/settings.json

# Copy editor configuration
cp ~/github/claude-config/.claude.json ~/.claude.json

# Copy all slash commands
cp -r ~/github/claude-config/commands ~/.claude/

# Copy all subagents
cp -r ~/github/claude-config/agents ~/.claude/
```

### Update Existing Configuration

To sync with the latest changes:
```bash
cd ~/github/claude-config
git pull

# Update files
cp CLAUDE.md ~/.claude/
cp settings.json ~/.claude/
cp .claude.json ~/.claude.json
cp -r commands ~/.claude/
cp -r agents ~/.claude/
```

## Global Instructions (CLAUDE.md)

The `CLAUDE.md` file contains universal coding standards and best practices:

- **Code Documentation Standards**: Docstrings over comments, language-specific formats
- **File Operations**: Tool hierarchy and best practices
- **Development Workflow**: Pre-task checklist, quality gates, git workflow
- **Tool Usage Guidelines**: MCP tools, search patterns, task management
- **Security & Quality Standards**: Security requirements, code quality, performance
- **Database Operations**: MariaDB/MySQL query execution patterns
- **Technical Debt Management**: Progress tracking, issue priorities

### Key Features

- Always use docstrings instead of inline comments
- Prefer editing existing files over creating new ones
- Run security checks for sensitive code changes
- Use specialized subagents for complex tasks
- Track technical debt systematically
- Follow language-specific best practices

## Settings

### settings.json
```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(cat:*)"
    ]
  },
  "alwaysThinkingEnabled": true
}
```

### .claude.json
- Vim editor mode enabled
- Auto-updates enabled
- IDE auto-connection enabled
- Shift+Enter keybinding installed

## Slash Commands (25 total)

Custom slash commands for common development tasks:

### Planning & Analysis
- `/brainstorm` - Structured brainstorming with multiple perspectives
- `/bslist` - Generate comprehensive task breakdowns
- `/task-init` - Intelligent task initialization with context loading
- `/read-specs` - Extract and analyze product specifications

### Code Quality
- `/review-code` - Comprehensive code review with security & performance checks
- `/debug-assistant` - Systematic debugging assistance
- `/perf-check` - Performance analysis and optimization recommendations
- `/security-scan` - Security vulnerability scanning
- `/tech-debt` - Technical debt analysis and tracking

### Development Workflow
- `/commit` - Generate conventional commit messages
- `/mr-draft` - Create comprehensive merge request descriptions
- `/test-suite` - Generate comprehensive test suites
- `/deploy` - Deployment checklist and verification
- `/rollback` - Safe rollback procedures

### Documentation
- `/write-documentation` - Generate comprehensive documentation
- `/handoff` - Create knowledge transfer documentation
- `/standup` - Generate standup updates from git history

### DevOps & Maintenance
- `/deps-update` - Dependency update with compatibility checks
- `/env-sync` - Environment configuration synchronization

### Specialized
- `/generate-interview` - Generate structured interview guides
- `/interview-analysis-template` - Interview analysis templates
- `/interview-context-storage` - Store interview context
- `/screen-resume` - Resume/restart screen sessions
- `/todo-worktree` - Git worktree TODO management
- `/pdf-to-markdown.py` - Python script for PDF conversion

## Specialized Subagents (39 total)

### Architecture & Design
- `backend-architect` - Design RESTful APIs and system architecture
- `frontend-developer` - Build Next.js applications with React
- `nextjs-app-router-developer` - Next.js App Router specialist
- `ui-ux-designer` - Design systems and user experience

### Code Quality & Testing
- `code-reviewer` - Expert code review specialist
- `test-automator` - Comprehensive test suite creation
- `debugger` - Debugging specialist for errors and issues
- `security-auditor` - Security vulnerability reviews

### Performance & Infrastructure
- `performance-engineer` - Application profiling and optimization
- `database-optimizer` - SQL query and schema optimization
- `cloud-architect` - AWS/Azure/GCP infrastructure design
- `deployment-engineer` - CI/CD and Docker configurations
- `devops-troubleshooter` - Production debugging and monitoring

### Language Specialists
- `python-pro` - Advanced Python development
- `typescript-expert` - Type-safe TypeScript development
- `golang-pro` - Idiomatic Go development
- `rust-pro` - Rust systems programming
- `php-developer` - Modern PHP development

### Framework Specialists
- `laravel-vue-developer` - Laravel + Vue3 full-stack
- `drupal-developer` - Drupal CMS development
- `directus-developer` - Directus headless CMS

### Domain Specialists
- `ai-engineer` - LLM applications and RAG systems
- `ml-engineer` - ML pipelines and model serving
- `blockchain-developer` - Smart contracts and DeFi
- `graphql-architect` - GraphQL schemas and federation
- `data-engineer` - ETL pipelines and data warehouses
- `data-scientist` - SQL queries and BigQuery operations

### Specialized Tools
- `mobile-developer` - React Native and Flutter apps
- `game-developer` - Unity/Unreal game development
- `payment-integration` - Stripe/PayPal integration
- `api-documenter` - OpenAPI/Swagger documentation
- `accessibility-specialist` - WCAG compliance
- `legacy-modernizer` - Refactor legacy code

### Trading & Finance (Specialized)
- `crypto-trader` - Cryptocurrency trading systems
- `crypto-analyst` - Market analysis and on-chain analytics
- `crypto-risk-manager` - Portfolio risk assessment
- `defi-strategist` - DeFi yield strategies
- `arbitrage-bot` - Cross-exchange arbitrage
- `quant-analyst` - Quantitative finance and backtesting

## Keeping Config Updated

### Sync Local Changes to Repository

When you update your local Claude configuration:

```bash
# Copy updated files to repo
cp ~/.claude/CLAUDE.md ~/github/claude-config/
cp ~/.claude/settings.json ~/github/claude-config/
cp ~/.claude.json ~/github/claude-config/
cp -r ~/.claude/commands ~/github/claude-config/
cp -r ~/.claude/agents ~/github/claude-config/

# Commit changes
cd ~/github/claude-config
git add .
git commit -m "Update Claude configuration"
git push
```

### Automated Sync Script

Create `~/.claude/sync-config.sh`:
```bash
#!/bin/bash
REPO=~/github/claude-config

cp ~/.claude/CLAUDE.md $REPO/
cp ~/.claude/settings.json $REPO/
cp ~/.claude.json $REPO/
cp -r ~/.claude/commands $REPO/
cp -r ~/.claude/agents $REPO/

cd $REPO
git add .
git commit -m "Auto-sync: $(date +'%Y-%m-%d %H:%M')"
git push

echo "Configuration synced to GitHub"
```

Make it executable:
```bash
chmod +x ~/.claude/sync-config.sh
```

## Usage Examples

### Using Slash Commands

```bash
# Initialize a new task with context loading
/task-init "Add user authentication feature"

# Review code for security and performance
/review-code

# Generate commit message from changes
/commit

# Create comprehensive documentation
/write-documentation
```

### Using Subagents

In Claude Code, invoke specialized agents with the Task tool:
- Security reviews: Use `security-auditor` subagent
- Performance optimization: Use `performance-engineer` subagent
- Database queries: Use `database-optimizer` subagent
- Architecture decisions: Use `backend-architect` subagent

## Security Note

This configuration does not include:
- API keys or authentication tokens
- Sensitive environment variables
- Private project configurations
- Personal credentials

These should be configured separately in your local environment.

## Contributing

To add new slash commands or subagents:

1. Create the command file in `commands/` directory
2. Create the subagent file in `agents/` directory
3. Test locally in `~/.claude/`
4. Sync to repository using the script above
5. Commit and push changes

## License

Personal configuration - free to use and adapt for your own Claude Code setup.

---

**Last Updated**: 2025-10-06
**Claude Code Version**: Latest
**Total Slash Commands**: 25
**Total Subagents**: 39
