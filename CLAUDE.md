# Global Claude Instructions

This file provides universal guidance for Claude Code sessions across all projects.

## Priority
Always check for and prioritize project-specific `CLAUDE.md` files in the current working directory or project root. Those instructions override these global defaults.

## Code Documentation Standards

### Core Principle: Docstrings Over Comments
- **NEVER** add inline comments in methods - use docstrings instead
- **ALWAYS** use language-appropriate docstrings for public functions and classes
- **ALWAYS** include type hints/annotations for better LSP integration
- Write self-documenting code with descriptive variable and function names
- Comments only acceptable for complex algorithms or non-obvious business logic

### Language-Specific Docstring Formats
```python
# Python - Use triple quotes
def calculate_total(items: List[Item]) -> float:
    """Calculate the total price of all items.

    Args:
        items: List of Item objects with price attribute

    Returns:
        Total sum of all item prices
    """
```

```javascript
// JavaScript/TypeScript - Use JSDoc
/**
 * Calculate the total price of all items
 * @param {Item[]} items - Array of items with price property
 * @returns {number} Total sum of all item prices
 */
```

```go
// Go - Use standard comments above declarations
// CalculateTotal returns the sum of all item prices
// It iterates through the provided items slice and accumulates their prices
func CalculateTotal(items []Item) float64 {
```

## File Operations

### Universal File Management Rules
- **NEVER** create files unless absolutely necessary
- **ALWAYS** prefer editing existing files over creating new ones
- **NEVER** proactively create documentation files (*.md) unless explicitly requested
- **ALWAYS** use Read tool before Edit tool
- **ALWAYS** use absolute paths for file operations
- **PREFER** MultiEdit over multiple Edit operations for the same file

### Tool Hierarchy for File Operations
1. `Read` → `Edit` → `Write` (in that order of preference)
2. Use `mcp__filesystem__*` tools for complex operations
3. Use `Grep`/`Glob` for file discovery before reading
4. Avoid bash commands like `cat`, `sed`, `awk` for file operations

## Development Workflow

### Pre-Task Checklist
1. Check for project documentation:
   - `CLAUDE.md` (project-specific instructions)
   - `README.md` (project overview)
   - `ROADMAP.md` (development roadmap)
   - `CHECKLIST.md` (task tracking)
2. Identify project type (check for `package.json`, `go.mod`, `pyproject.toml`, etc.)
3. Verify available tools and dependencies
4. Review recent git history if applicable

### Standard Quality Gates
Before any commit or significant change:
1. **Format**: Run code formatters (prettier, black, gofmt)
2. **Lint**: Run linters (eslint, flake8, golint)
3. **Type Check**: Run type checkers if available (mypy, tsc)
4. **Test**: Run test suite and ensure all tests pass
5. **Security**: Run security scans for sensitive changes

### Git Workflow Standards
- Use conventional commits: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`
- Never commit with failing tests
- Never commit code with security vulnerabilities
- Include file references with line numbers in commit messages when appropriate

## Tool Usage Guidelines

### Claude Code Iterations UI (New Feature - 2025-10-18)

Claude Code now features an **Iterations UI** that provides better visibility into multi-step workflows.

#### How to Optimize for Iterations UI

**Structure Work in Clear Phases**:
```markdown
✅ GOOD - Clear iteration boundaries:
1. First, I'll analyze the requirements
   [Use Read/Grep tools, present findings]

2. Now I'll implement the feature
   [Use Edit/Write tools, make changes]

3. Finally, I'll test the changes
   [Use Bash tool for tests, show results]
```

**Provide Progress Updates**:
```markdown
✅ Output clear phase transitions:
"Analysis complete. Moving to implementation..."
"Implementation done. Running tests..."
```

**Group Related Tool Calls**:
```markdown
✅ Execute related operations together:
- Read all necessary files in one iteration
- Make all related edits in one iteration
- Run all tests in one iteration

❌ Don't alternate unnecessarily:
- Read file 1
- Edit file 1
- Read file 2
- Edit file 2
```

**Use TodoWrite for Visibility**:
```markdown
✅ Create todos at start of complex tasks
✅ Update todo status between iterations
✅ User can see progress in UI
```

**Benefits of Iterations UI**:
- Users see clear progress through multi-step tasks
- Easier to understand what's happening at each stage
- Better context for when to interrupt or provide feedback
- Natural breakpoints for user interaction

**Best Practices**:
1. Start with analysis/planning iteration
2. Group implementation work logically
3. End with validation/testing iteration
4. Use TodoWrite to show overall progress
5. Output clear transition messages between phases

### Tool Selection Hierarchy
1. **MCP tools** (`mcp__*`) when available
2. **Native Claude tools** (Read, Edit, Grep, Glob, etc.)
3. **Specialized agents** (Task tool with appropriate subagent)
4. **Bash commands** (only when necessary)

### Explicit Tool Invocation Rules
**CRITICAL**: Always use explicit tool names in instructions, not bash examples or pseudocode.

**WRONG** (Documentation style):
```markdown
- Read project files: `cat CLAUDE.md`
- Check git status: `git status --porcelain`
```

**CORRECT** (Executable instructions):
```markdown
- Use Read tool to read `CLAUDE.md`
- Use Bash tool with command: `git status --porcelain`, description: "Check git status"
```

### Parallel Agent Invocation
When invoking multiple agents, be explicit about parallel execution:

**WRONG**:
```markdown
Use these agents:
- backend-architect: Check architecture
- test-automator: Check tests
```

**CORRECT**:
```markdown
Use Task tool to launch agents IN PARALLEL (single message with multiple Task tool invocations):

1. Task tool call:
   - subagent_type: "backend-architect"
   - prompt: "Analyze architecture for: [specific task]"

2. Task tool call:
   - subagent_type: "test-automator"
   - prompt: "Identify test requirements for: [specific task]"

Wait for all agents to complete before proceeding.
```

### User Interaction Points
Be explicit about when to wait for user input:

**WRONG**:
```markdown
STOP → "Enter your choice:"
```

**CORRECT**:
```markdown
Output: "Enter your choice:"
WAIT for user's next message.
```

Or use AskUserQuestion tool for structured input.

### Search and Analysis Patterns
- Use `Grep` for content searching
- Use `Glob` for file pattern matching
- Use `Task` agent for complex multi-step analysis
- Avoid `find` and bash `grep` commands

### Task Management
- Use `TodoWrite` for tasks with 3+ steps
- Mark tasks as `in_progress` before starting
- Update status immediately upon completion
- One task should be `in_progress` at a time

### Specialized Subagents Usage
When using the Task tool, select appropriate subagent:
- `security-auditor`: Security-sensitive changes
- `performance-engineer`: Database/query optimization
- `backend-architect`: Architecture decisions
- `test-automator`: Test coverage improvements
- `database-optimizer`: SQL and schema changes
- `python-pro`: Python-specific optimizations
- `debugger`: Error analysis and troubleshooting
- `code-reviewer`: Code quality reviews

## Writing Slash Commands

### Command Structure Principles

Slash commands in `~/.claude/commands/` should be **executable instructions**, not documentation.

#### Bad Command (Documentation Style)
```markdown
### Phase 1: Load Context
1. **Read files**
   ```bash
   cat CLAUDE.md
   ls -la
   ```
2. **Use agents**: backend-architect, test-automator
```

#### Good Command (Executable Style)
```markdown
### Step 1: Load Context

Use Read tool to read `CLAUDE.md` file.

Use Bash tool:
- Command: `ls -la`
- Description: "List project files"

Use Task tool to launch agents IN PARALLEL (single message with 2 Task invocations):
1. Task(subagent_type="backend-architect", prompt="...")
2. Task(subagent_type="test-automator", prompt="...")

Wait for all agents to complete.
```

### Command Writing Checklist

**Tool Invocations**:
- ✅ Use explicit tool names: "Use Read tool", "Use Bash tool", "Use Task tool"
- ✅ Specify all required parameters clearly
- ✅ Include command descriptions for Bash tool
- ❌ Don't write bash examples in code blocks as instructions
- ❌ Don't use pseudocode or abstract function calls

**Agent Invocations**:
- ✅ Explicitly state "Use Task tool to launch agents IN PARALLEL"
- ✅ Specify exact subagent_type and prompt for each agent
- ✅ State "Wait for all agents to complete" when needed
- ❌ Don't just list agent names without tool invocation syntax
- ❌ Don't assume I'll infer parallel execution

**User Interaction**:
- ✅ Use "Output: [message]" followed by "WAIT for user's next message"
- ✅ Or use AskUserQuestion tool for structured input
- ✅ Be explicit about what you're waiting for
- ❌ Don't use ambiguous "STOP →" markers
- ❌ Don't assume I know when to pause

**Structure**:
- ✅ Use flat "Step 1, Step 2" structure (not deep nesting)
- ✅ Keep steps concrete and actionable
- ✅ Include error handling instructions
- ❌ Don't use complex "Phase 1.2.3" hierarchies
- ❌ Don't write essays - keep it directive

### Example: Well-Structured Command

```markdown
# Command Name

Brief description of what this command does.

## Execution Steps

### Step 1: Gather Information

Use Read tool to read `./config.json`.

If file doesn't exist, output: "No config found" and skip to Step 3.

### Step 2: Analyze with Agents

Use Task tool to launch 2 agents IN PARALLEL (single message):

1. Task tool call:
   - subagent_type: "security-auditor"
   - prompt: "Check config for security issues: [config content]"

2. Task tool call:
   - subagent_type: "code-reviewer"
   - prompt: "Review config structure: [config content]"

Wait for both agents to complete.

### Step 3: Present Results

Output the analysis results.

Then output: "Proceed with changes? (yes/no)"

WAIT for user's next message.

### Step 4: Execute Changes

If user said yes:
- Use Edit tool to modify config
- Use Bash tool: `git add config.json`, description: "Stage config changes"

If user said no:
- Output: "Changes cancelled"
- Exit command

## Error Handling

If Read tool fails: Continue without config
If agent fails: Proceed with partial analysis
If git command fails: Warn user and continue
```

### Common Mistakes to Avoid

**Mistake 1: Documentation Instead of Instructions**
```markdown
❌ BAD:
"Run tests with pytest: `pytest --cov`"

✅ GOOD:
"Use Bash tool with command: `pytest --cov`, description: 'Run tests with coverage'"
```

**Mistake 2: Unclear Agent Invocation**
```markdown
❌ BAD:
"Analyze using: backend-architect, security-auditor"

✅ GOOD:
"Use Task tool to launch 2 agents IN PARALLEL (single message with 2 Task invocations):
1. Task(subagent_type='backend-architect', prompt='...')
2. Task(subagent_type='security-auditor', prompt='...')
Wait for both agents to complete."
```

**Mistake 3: Ambiguous User Interaction**
```markdown
❌ BAD:
"STOP → Ask user for input"

✅ GOOD:
"Output: 'Enter your choice (1-3):'
WAIT for user's next message with their choice."
```

**Mistake 4: Too Many Nested Phases**
```markdown
❌ BAD:
### Phase 1: Setup
  #### Sub-phase 1.1: Context
    ##### Step 1.1.1: Files
      ###### Action 1.1.1.a: Read

✅ GOOD:
### Step 1: Read Context Files
### Step 2: Analyze Context
### Step 3: Present Summary
```

## Security & Quality Standards

### Security Requirements
- Always run security checks on authentication code
- Never log or expose secrets/API keys
- Validate all user inputs
- Use parameterized queries for database operations
- Check dependencies for known vulnerabilities

### Code Quality Standards
- Maintain test coverage (follow project requirements)
- Ensure proper error handling with logging
- Follow SOLID principles where applicable
- Implement proper separation of concerns
- Use dependency injection for testability

### Performance Considerations
- Profile before optimizing
- Use appropriate data structures
- Implement caching where beneficial
- Consider async operations for I/O
- Monitor query performance

## Database Operations

### MariaDB/MySQL Query Execution
When working with MariaDB/MySQL databases, use the `mysql` command directly from bash with environment variables:

#### Loading Environment Variables
```bash
# First, load the .env file if it exists
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Or source the .env file
set -a && source .env && set +a
```

#### Direct Query Execution
```bash
# Execute a single query using environment variables
mysql -h "$DB_HOST" -P "${DB_PORT:-3306}" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" -e "SELECT * FROM users LIMIT 10;"

# Execute multiple queries
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" <<EOF
SHOW TABLES;
DESCRIBE users;
SELECT COUNT(*) FROM posts;
EOF

# Export query results to CSV
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" \
    -e "SELECT * FROM orders WHERE created_at > '2024-01-01'" \
    --batch --silent | sed 's/\t/,/g' > export.csv
```

#### Common Database Operations
```bash
# Check database connection
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" -e "SELECT 1"

# Show database structure
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" -e "SHOW TABLES"

# Describe table schema
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" -e "DESCRIBE table_name"

# Check table sizes
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" -e "
SELECT table_name,
       ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)'
FROM information_schema.tables
WHERE table_schema = '$DB_NAME'
ORDER BY (data_length + index_length) DESC;"

# Run SQL file
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < migration.sql
```

#### Best Practices for Database Queries
- Always use environment variables from `.env` file
- Never hardcode credentials in commands
- Use `--batch` flag for script-friendly output
- Add `--silent` to suppress column headers when needed
- Use heredocs (<<EOF) for multi-line queries
- Always validate `.env` file exists before sourcing
- Consider using `--ssl` flag for production connections
- Use `EXPLAIN` to analyze query performance before running complex queries

## Technical Debt Management

### Issue Priority Classifications
- 🔴 **Critical**: Security vulnerabilities, broken builds, data loss risks
- 🟠 **High**: Performance issues, architecture violations, failing tests
- 🟡 **Medium**: Code quality, maintainability, missing documentation
- 🟢 **Low**: Enhancements, nice-to-have features, minor refactoring

### Documentation Standards
Maintain when present:
- `ROADMAP.md`: Strategic planning and milestones
- `CHECKLIST.md`: Tactical task tracking
- `ARCHITECTURE.md`: System design decisions
- `CONTRIBUTING.md`: Development guidelines

### Progress Tracking
```bash
# Count remaining vs completed tasks
grep -c "\- \[ \]" CHECKLIST.md  # Remaining
grep -c "\- \[x\]" CHECKLIST.md  # Completed

# Review critical issues
grep -A5 "🔴\|CRITICAL" CHECKLIST.md
```

## Context Detection

### Project Type Identification
Check for these indicators in order:
1. **Python**: `pyproject.toml`, `requirements.txt`, `setup.py`
2. **Node.js**: `package.json`, `yarn.lock`, `package-lock.json`
3. **Go**: `go.mod`, `go.sum`
4. **Rust**: `Cargo.toml`, `Cargo.lock`
5. **Java**: `pom.xml`, `build.gradle`
6. **C/C++**: `CMakeLists.txt`, `Makefile`, `.clang-format`

### Tool Availability Verification
```bash
# Check for build tools
which make npm go cargo python rye

# List MCP resources if available
# Use ListMcpResourcesTool when needed

# Verify project-specific tools
ls -la Makefile package.json go.mod
```

### Priority Resolution Matrix
When requirements conflict:
1. Security overrides everything
2. Project-specific CLAUDE.md overrides global
3. Explicit user requests override defaults
4. Test stability over new features
5. Performance over aesthetics

## Global Preferences

### Language-Specific Preferences
- **Python**: Use `rye` for dependency management and running Python code
- **JavaScript/TypeScript**: Use `npm` or `yarn` as found in project
- **Go**: Use standard `go` toolchain and modules
- **Rust**: Use `cargo` for all operations

### Data Handling
- **Serialization**: Prefer Pydantic models for Python validation
- **Configuration**: Use environment variables for secrets
- **Database**: Use ORMs with proper migrations
- **API Design**: RESTful with clear versioning

### Output Standards
- No emojis in any output or code
- Never mention AI-generated or co-authored attributions in commits or comments
- Use clear, concise language in all communications
- Provide file paths with line numbers for code references

## Common Commands Reference

### Universal Quality Commands
```bash
# Python projects
make test         # Or: pytest
make lint         # Or: rye run lint
make format       # Or: rye run format

# Node.js projects
npm test          # Or: yarn test
npm run lint      # Or: yarn lint
npm run format    # Or: yarn format

# Go projects
go test ./...
go fmt ./...
go vet ./...

# Rust projects
cargo test
cargo fmt
cargo clippy
```

### Debugging Commands
```bash
# View recent changes
git diff HEAD~1
git log --oneline -10

# Check file structure
find . -type f -name "*.py" | head -20
ls -la src/ lib/ internal/

# Verify dependencies
pip list  # or: rye list
npm ls    # or: yarn list
go mod tidy
```

### Emergency Procedures
For critical issues:
1. **STOP** all non-critical work
2. Create backup of current state
3. Document issue in CHECKLIST.md with 🔴 priority
4. Fix issue with appropriate subagent
5. Verify fix with comprehensive testing
6. Document resolution and lessons learned

---

**Last Updated**: 2025-10-20
**Version**: 2.1.0

**Changelog**:
- v2.1.0 (2025-10-20):
  - Added comprehensive slash command writing guidelines with explicit tool invocation rules
  - Added parallel agent execution patterns and user interaction semantics
  - Added Claude Code Iterations UI optimization guidelines (new feature from 2025-10-18)
- v2.0.0 (2025-01-16): Initial comprehensive global instructions

*This file provides universal defaults for Claude Code sessions. Project-specific CLAUDE.md files override these settings.*