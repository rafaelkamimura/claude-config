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

### Tool Selection Hierarchy
1. **MCP tools** (`mcp__*`) when available
2. **Native Claude tools** (Read, Edit, Grep, Glob, etc.)
3. **Specialized agents** (Task tool with appropriate subagent)
4. **Bash commands** (only when necessary)

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

**Last Updated**: 2025-01-16
**Version**: 2.0.0

*This file provides universal defaults for Claude Code sessions. Project-specific CLAUDE.md files override these settings.*