# Claude Code Configuration

My personal Claude Code configuration with global instructions, custom slash commands, specialized subagents, and reusable skills.

## Contents

- **Global Instructions**: `CLAUDE.md` - Universal coding standards and development workflow
- **Settings**: `settings.json` - Claude Code preferences and permissions
- **Configuration**: `.claude.json` - Editor mode and UI settings
- **Slash Commands**: `commands/` - 26 custom slash commands for common tasks
- **Subagents**: `agents/` - 39 specialized AI agents for different development tasks
- **Global Skills**: `skills/` - 5 reusable skills following Anthropic's official patterns
- **Makefile**: Easy setup, sync, and management commands

## Quick Start

### Installation (Recommended)

1. Clone this repository:
```bash
git clone https://github.com/rafaelkamimura/claude-config.git ~/github/claude-config
cd ~/github/claude-config
```

2. Install configuration using Makefile:
```bash
make install
```

That's it! All configuration files, slash commands, subagents, and global skills are now installed to `~/.claude/`.

### Manual Installation (Alternative)

<details>
<summary>Click to expand manual installation steps</summary>

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

# Copy all global skills
cp -r ~/github/claude-config/skills ~/.claude/
```
</details>

### Update Existing Configuration

To sync with the latest changes from GitHub:

```bash
cd ~/github/claude-config
git pull
make install
```

## Makefile Commands

The repository includes a comprehensive Makefile for easy management:

```bash
make install                  # Install configuration from repo to ~/.claude
make pull-local               # Update repo with current ~/.claude configuration
make sync                     # Pull local + commit + push changes to GitHub
make install-project-skills PATH=/path/to/project  # Install skills to project
make list-skills              # List available skills in repo
make status                   # Show git status and configuration diff
make clean                    # Remove backup files
make test                     # Verify configuration files
make help                     # Show this help message
```

### Installing Skills to a Project

To install global skills to a specific project:

```bash
cd ~/github/claude-config
make install-project-skills PATH=~/projects/my-app
```

This creates `.claude/skills/` in your project and copies all skills there.

## Global Instructions (CLAUDE.md)

The `CLAUDE.md` file contains universal coding standards and best practices:

- **Code Documentation Standards**: Docstrings over comments, language-specific formats
- **File Operations**: Tool hierarchy and best practices
- **Development Workflow**: Pre-task checklist, quality gates, git workflow
- **Tool Usage Guidelines**: MCP tools, search patterns, task management, Iterations UI
- **Writing Slash Commands**: Explicit tool invocations, parallel agent execution, user interaction patterns
- **Security & Quality Standards**: Security requirements, code quality, performance
- **Database Operations**: MariaDB/MySQL query execution patterns
- **Technical Debt Management**: Progress tracking, issue priorities

### Key Features

- Always use docstrings instead of inline comments
- Explicit tool invocations (not bash examples)
- Parallel agent execution patterns
- Claude Iterations UI optimization
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

## Slash Commands (26 total)

Custom slash commands for common development tasks following explicit tool invocation patterns:

### Planning & Analysis
- `/brainstorm` - Structured brainstorming with multiple perspectives
- `/bslist` - Generate comprehensive task breakdowns
- `/task-init` - Intelligent task initialization with context loading and 4 parallel agents
- `/read-specs` - Extract and analyze product specifications

### Code Quality
- `/review-code` - Comprehensive code review with 5 parallel agents (security, architecture, performance, testing)
- `/debug-assistant` - Systematic debugging assistance
- `/perf-check` - Performance analysis and optimization recommendations
- `/security-scan` - Security vulnerability scanning with Semgrep MCP integration
- `/tech-debt` - Technical debt analysis and tracking

### Development Workflow
- `/commit` - Smart git commit with task-aware staging and MR/PR chaining
- `/mr-draft` - Generate comprehensive PT-BR merge request documentation with gh/glab CLI integration
- `/test-suite` - Generate comprehensive test suites with intelligent test generation
- `/deploy` - Deployment checklist and verification
- `/rollback` - Safe rollback procedures

### Documentation
- `/write-documentation` - Generate comprehensive documentation
- `/handoff` - Create knowledge transfer documentation
- `/standup` - Generate standup updates from git history

### DevOps & Maintenance
- `/deps-update` - Dependency update with compatibility checks
- `/env-sync` - Environment configuration synchronization
- `/sync-config` - Sync all configuration and skills to GitHub repository

### Skills Management
- `/create-skill` - Create new Claude Code skills following Anthropic's official patterns

### Specialized
- `/generate-interview` - Generate structured interview guides
- `/interview-analysis-template` - Interview analysis templates
- `/interview-context-storage` - Store interview context
- `/screen-resume` - Resume/restart screen sessions
- `/todo-worktree` - Git worktree TODO management
- `/pdf-to-markdown.py` - Python script for PDF conversion

### Featured Commands

#### `/commit` - Smart Git Commit
- Automatically stages task-related files
- Generates conventional commit messages
- Excludes .env, logs, and temporary files
- Chains into `/mr-draft` for seamless PR creation
- Never mentions AI assistance in commit messages

#### `/mr-draft` - Merge Request Generator
- Analyzes branch commits and file changes
- Generates comprehensive PT-BR documentation
- Launches 5 parallel agents for analysis (architecture, code review, testing, database, security)
- Creates MR/PR using gh (GitHub) or glab (GitLab) CLI
- Professional formatting with review checklist

#### `/create-skill` - Skill Builder
- Interactive skill creation wizard
- Supports personal (`~/.claude/skills/`) and project (`.claude/skills/`) skills
- Generates proper YAML frontmatter and SKILL.md structure
- Includes 6 skill type templates (Code Generation, Analysis, Data Processing, Testing, Documentation, Workflow)
- Validates against Anthropic's official requirements
- Optional resources (markdown, scripts, schemas, templates)

## Global Skills (5 total)

Reusable skills following Anthropic's official skill patterns from https://github.com/anthropics/skills

### Development Skills

**📁 async-testing-expert/**
- Comprehensive async testing skill for Python and JavaScript
- Includes SKILL.md with detailed instructions
- Includes README.md with examples and best practices
- Includes `generate_test_template.py` script for automated test generation
- Handles async/await patterns, promises, fixtures, mocking

**📁 fastapi-clean-architecture/**
- FastAPI development following clean architecture principles
- Implements repository pattern, dependency injection, layered architecture
- Best practices for API design, testing, and deployment

### Domain-Specific Skills

**📁 brazilian-financial-integration/**
- Integration with Brazilian financial systems (Pix, boleto, banking APIs)
- Handles Brazilian tax calculations and compliance
- Payment gateway integration patterns

**📁 multi-system-sso-authentication/**
- Single Sign-On implementation across multiple systems
- OAuth2, SAML, JWT token management
- Session management and security best practices

### Database Skills

**📄 mariadb-database-explorer.md**
- Explore and query MariaDB/MySQL databases
- Database schema analysis and optimization
- Query execution and result formatting

## Specialized Subagents (39 total)

### Architecture & Design
- `backend-architect` - Design RESTful APIs and system architecture
- `frontend-developer` - Build Next.js applications with React
- `nextjs-app-router-developer` - Next.js App Router specialist
- `ui-ux-designer` - Design systems and user experience

### Code Quality & Testing
- `code-reviewer` - Expert code review specialist (used in `/review-code`)
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
cd ~/github/claude-config
make pull-local  # Pull configuration from ~/.claude to repo
make sync        # Pull local + commit + push to GitHub
```

The `make sync` command will:
1. Copy all files from `~/.claude/` to repository
2. Show git status of changes
3. Automatically commit with timestamp
4. Push to GitHub
5. Show confirmation with commit hash

### Manual Sync (if needed)

<details>
<summary>Click to expand manual sync steps</summary>

```bash
# Copy updated files to repo
cp ~/.claude/CLAUDE.md ~/github/claude-config/
cp ~/.claude/settings.json ~/github/claude-config/
cp ~/.claude.json ~/github/claude-config/
cp -r ~/.claude/commands ~/github/claude-config/
cp -r ~/.claude/agents ~/github/claude-config/
cp -r ~/.claude/skills ~/github/claude-config/

# Commit changes
cd ~/github/claude-config
git add .
git commit -m "Update Claude configuration"
git push
```
</details>

## Usage Examples

### Using Slash Commands

```bash
# Create a new skill
/create-skill

# Initialize a new task with context loading and parallel agent analysis
/task-init "Add user authentication feature"

# Review code with 5 parallel agents
/review-code

# Generate commit message and optionally create MR/PR
/commit

# Create comprehensive MR documentation with gh/glab integration
/mr-draft

# Create comprehensive documentation
/write-documentation

# Scan for security vulnerabilities
/security-scan
```

### Using Makefile

```bash
# Install configuration to new machine
git clone https://github.com/rafaelkamimura/claude-config.git ~/github/claude-config
cd ~/github/claude-config
make install

# List available skills
make list-skills

# Install skills to a project
make install-project-skills PATH=~/projects/my-app

# Update repo with local changes and push to GitHub
make sync

# Check what's changed
make status

# Verify everything is installed correctly
make test
```

### Using Skills

Skills are automatically available in Claude Code:

```bash
# For global skills (installed to ~/.claude/skills/)
# Just reference the skill in your conversation with Claude

# For project skills (installed to .claude/skills/)
cd ~/github/claude-config
make install-project-skills PATH=~/projects/my-app
# Skills will be available when working in that project
```

### Using Subagents

In Claude Code, invoke specialized agents with the Task tool:
- Security reviews: Use `security-auditor` subagent
- Performance optimization: Use `performance-engineer` subagent
- Database queries: Use `database-optimizer` subagent
- Architecture decisions: Use `backend-architect` subagent

Slash commands like `/review-code` and `/mr-draft` automatically launch multiple agents in parallel for comprehensive analysis.

## Security Note

This configuration does not include:
- API keys or authentication tokens
- Sensitive environment variables
- Private project configurations
- Personal credentials

These should be configured separately in your local environment.

## Creating New Content

### Adding New Slash Commands

1. Create the command file in `~/.claude/commands/`
2. Follow the patterns in `CLAUDE.md` (explicit tool invocations, Step structure)
3. Test the command locally
4. Sync to repository: `cd ~/github/claude-config && make sync`

### Adding New Skills

Use the `/create-skill` command:

```bash
/create-skill
```

This will guide you through:
- Skill name and description
- Scope (personal or project)
- Skill type (Code Generation, Analysis, Data Processing, etc.)
- Tool requirements
- Optional resources (markdown, scripts, schemas)

Or manually:
1. Create skill directory in `~/.claude/skills/[skill-name]/`
2. Create `SKILL.md` with YAML frontmatter
3. Follow Anthropic's patterns: https://github.com/anthropics/skills
4. Sync to repository: `cd ~/github/claude-config && make sync`

### Adding New Subagents

1. Create the subagent file in `~/.claude/agents/`
2. Follow existing subagent patterns
3. Test locally
4. Sync to repository: `cd ~/github/claude-config && make sync`

## Contributing

To contribute improvements:

1. Fork this repository
2. Make your changes
3. Test locally with `make install`
4. Submit a pull request

## Resources

- **Claude Code Documentation**: https://docs.claude.com/en/docs/claude-code
- **Skills Documentation**: https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview
- **Skills Repository**: https://github.com/anthropics/skills
- **Slash Commands Guide**: Documented in `CLAUDE.md`

## License

Personal configuration - free to use and adapt for your own Claude Code setup.

---

**Last Updated**: 2025-10-20
**Claude Code Version**: Latest
**Total Slash Commands**: 26
**Total Subagents**: 39
**Total Global Skills**: 5
**Makefile Targets**: 8
