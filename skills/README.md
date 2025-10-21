# Claude Code Skills for gefin-backend

This directory contains custom skills for exploring and analyzing databases in the gefin-backend project.

## Available Skills

### mariadb-database-explorer

**Purpose:** Comprehensive MariaDB database exploration and documentation tool.

**Location:** `.claude/skills/mariadb-database-explorer.md`

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

## Prerequisites

Before using these skills, ensure:

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

### Explore the art1025 database
```
Use mariadb-database-explorer skill with DATABASE_NAME="art1025"
```

**Output:**
- `schema_analysis_art1025.json`
- `SCHEMA_art1025.md`
- Memory MCP entities created

### Quick exploration without data samples
```
Use mariadb-database-explorer skill with DATABASE_NAME="cobranca" and SAMPLE_SIZE=0
```

### Generate only markdown documentation
```
Use mariadb-database-explorer skill with DATABASE_NAME="corporativo", OUTPUT_FORMAT="markdown", STORE_IN_MCP=false
```

## Troubleshooting

### Skill not found

**Problem:** Claude says "Skill not found" or doesn't list the skill

**Solution:**
1. Ensure you're in the gefin-backend project directory
2. Check that `.claude/skills/mariadb-database-explorer.md` exists
3. Restart Claude Code or refresh the workspace

### Connection errors

**Problem:** "Failed to connect to MariaDB server"

**Solutions:**
1. Verify `.env` file contains correct MariaDB credentials
2. Check network connectivity to database host
3. Ensure MySQL client is installed: `which mysql`
4. Test connection manually:
   ```bash
   mysql -h $MARIADB_HOST -P $MARIADB_PORT -u $MARIADB_USER -p
   ```

### Permission errors

**Problem:** "Insufficient permissions to access database"

**Solutions:**
1. Verify user has SELECT privileges
2. Check database exists: `SHOW DATABASES;`
3. Contact database administrator for access

### Large database timeouts

**Problem:** Skill times out on databases with 100+ tables

**Solutions:**
1. Use `SAMPLE_SIZE=0` to skip data sampling
2. Specify a subset of tables when prompted
3. Analyze the top 20 largest tables only

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

---

**Last Updated**: 2025-01-23
**Maintained By**: gefin-backend team
