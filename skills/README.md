# Claude Code Skills

This directory contains custom skills for database exploration, GitLab CLI troubleshooting, and development workflow automation.

## Available Skills

### mariadb-database-explorer

**Purpose:** Comprehensive MariaDB database exploration and documentation tool.

**Location:** `.claude/skills/mariadb-database-explorer.md`

**Use When:** Need to explore, document, or analyze MariaDB database schemas.

### gitlab-cli-troubleshooter

**Purpose:** Diagnose and fix GitLab CLI (`glab`) configuration issues, set up smart shell functions.

**Location:** `.claude/skills/gitlab-cli-troubleshooter.md`

**Use When:** Experiencing `glab` 404 errors, authentication issues, or want to set up project-aware CLI functions.

## How to Use Skills

### Option 1: Using Skill Command (Recommended)

In your Claude Code chat, use the Skill tool:

```
mariadb-database-explorer
```

Claude will then ask you for the required parameters:
- `DATABASE_NAME`: The database to explore (e.g., "art1025", "corporativo")

### Option 2: Direct Invocation

You can also invoke skills directly in your conversation:

```
Use the mariadb-database-explorer skill to analyze the art1025 database
```

or with specific parameters:

```
Use mariadb-database-explorer skill with DATABASE_NAME="corporativo" and SAMPLE_SIZE=10
```

## Skill Parameters

### mariadb-database-explorer

**Required:**
- `DATABASE_NAME`: Target database name (e.g., "art1025", "corporativo", "cobranca")

**Optional:**
- `SAMPLE_SIZE`: Number of rows to sample (default: 5)
- `OUTPUT_FORMAT`: "json", "markdown", or "both" (default: "both")
- `STORE_IN_MCP`: Store in Memory MCP (default: true)

### gitlab-cli-troubleshooter

**No parameters required** - skill is interactive and will prompt for necessary information.

## Prerequisites

### For mariadb-database-explorer

1. **Environment Variables** (`.env` file):
   ```
   MARIADB_HOST=your_host
   MARIADB_PORT=3307
   MARIADB_USER=your_user
   MARIADB_PASSWORD=your_password
   ```

2. **MySQL Client**: Installed and accessible in PATH
   ```bash
   # Check if mysql is installed
   which mysql

   # Install if needed (macOS)
   brew install mysql-client

   # Add to PATH if needed
   export PATH="/opt/homebrew/opt/mysql-client/bin:$PATH"
   ```

3. **Database Access**: User must have SELECT permissions on target database

### For gitlab-cli-troubleshooter

1. **GitLab CLI (`glab`)**: Version 1.70+ installed
   ```bash
   # Check if glab is installed
   which glab
   glab version

   # Install if needed (macOS)
   brew install glab
   ```

2. **Personal Access Token**: GitLab PAT with `api` scope

3. **jq**: JSON processor for formatting output
   ```bash
   # macOS
   brew install jq

   # Linux
   apt-get install jq
   ```

4. **Shell**: zsh or bash (skill provides zsh examples)

## Output Files

The `mariadb-database-explorer` skill generates:

1. **JSON Schema**: `schema_analysis_{DATABASE_NAME}.json`
   - Complete database schema documentation
   - Table structures, relationships, indexes
   - Sample data and statistics

2. **Markdown Docs**: `SCHEMA_{DATABASE_NAME}.md`
   - Human-readable documentation
   - Table purposes and relationships
   - Integration recommendations

3. **Memory MCP**: Stores findings for future reference

## Example Usage

### mariadb-database-explorer

#### Explore the art1025 database
```
Use mariadb-database-explorer skill with DATABASE_NAME="art1025"
```

**Output:**
- `schema_analysis_art1025.json`
- `SCHEMA_art1025.md`
- Memory MCP entities created

#### Quick exploration without data samples
```
Use mariadb-database-explorer skill with DATABASE_NAME="cobranca" and SAMPLE_SIZE=0
```

#### Generate only markdown documentation
```
Use mariadb-database-explorer skill with DATABASE_NAME="corporativo", OUTPUT_FORMAT="markdown", STORE_IN_MCP=false
```

### gitlab-cli-troubleshooter

#### Fix glab 404 errors
```
Use gitlab-cli-troubleshooter skill
```

The skill will:
1. Diagnose authentication and API access
2. Identify project path/ID issues
3. Test direct API workarounds
4. Install smart shell functions (if needed)

#### Just install smart glab functions
```
I need smart glab functions for my GitLab instance
```

The skill will:
- Skip diagnostics
- Go directly to function installation
- Set up `gli`, `glv`, `gln`, `glapi` commands

## Troubleshooting

### General Issues

#### Skill not found

**Problem:** Claude says "Skill not found" or doesn't list the skill

**Solution:**
1. Check that skill `.md` file exists in `.claude/skills/`
2. Restart Claude Code or refresh the workspace
3. Verify you're in a directory with `.claude/skills/` accessible

### mariadb-database-explorer Issues

#### Connection errors

**Problem:** "Failed to connect to MariaDB server"

**Solutions:**
1. Verify `.env` file contains correct MariaDB credentials
2. Check network connectivity to database host
3. Ensure MySQL client is installed: `which mysql`
4. Test connection manually:
   ```bash
   mysql -h $MARIADB_HOST -P $MARIADB_PORT -u $MARIADB_USER -p
   ```

#### Permission errors

**Problem:** "Insufficient permissions to access database"

**Solutions:**
1. Verify user has SELECT privileges
2. Check database exists: `SHOW DATABASES;`
3. Contact database administrator for access

#### Large database timeouts

**Problem:** Skill times out on databases with 100+ tables

**Solutions:**
1. Use `SAMPLE_SIZE=0` to skip data sampling
2. Specify a subset of tables when prompted
3. Analyze the top 20 largest tables only

### gitlab-cli-troubleshooter Issues

#### "404 Not Found" errors

**Problem:** `glab mr list -R` returns 404

**Solution:** This is expected on custom GitLab instances - the skill will set up API-based workarounds.

#### Authentication failures

**Problem:** `glab auth status` shows not authenticated

**Solutions:**
1. Run: `glab auth login --hostname YOUR_GITLAB_HOST`
2. Ensure PAT has `api` scope
3. Verify network access to GitLab instance

#### Functions not loading

**Problem:** `gli` command not found after setup

**Solutions:**
1. Open **new terminal window** (don't just `source ~/.zshrc`)
2. Check for alias conflicts: `alias | grep gli`
3. Verify syntax: `zsh -n ~/.zshrc`

For detailed troubleshooting, see the skill file itself.

## Contributing New Skills

To add new skills to this directory:

1. Create a new `.md` file in `.claude/skills/`
2. Follow the skill format from existing skills
3. Update this README with skill documentation
4. Test the skill thoroughly
5. Commit and push to GitHub

## Sharing Skills

These skills are stored in the project repository and shared via Git:

1. Clone/pull the gefin-backend repository
2. Skills in `.claude/skills/` are automatically available
3. No additional installation required

## Support

For issues or questions:
1. Check the skill's documentation in the `.md` file
2. Review error messages and troubleshooting section
3. Consult the gefin-backend team

## Skill Development

### Creating New Skills

To add a new skill:

1. Create `.md` file in `.claude/skills/`
2. Follow existing skill structure:
   - Purpose and prerequisites
   - Step-by-step execution instructions
   - Common issues and solutions
   - Testing checklist
3. Update this README
4. Test thoroughly before committing

### Skill Structure Template

```markdown
# Skill Name

Brief description

## Purpose
What problem does this solve?

## When to Use This Skill
List of scenarios

## Prerequisites
Required tools and configuration

## Execution Steps
### Step 1: First Action
Detailed instructions...

## Common Issues and Solutions
Known problems and fixes

## Testing Checklist
Verification steps
```

---

**Last Updated**: 2025-10-21
**Skills**: 2 (mariadb-database-explorer, gitlab-cli-troubleshooter)
