# MariaDB Database Explorer

Comprehensive skill for discovering, analyzing, and documenting MariaDB databases. Works with any database accessible via the configured MariaDB connection.

## Purpose

Systematically explore and document MariaDB database schemas, relationships, and data patterns. Generates comprehensive documentation for integration planning, data migration, or system understanding.

## Skill Parameters

**Required:**
- `DATABASE_NAME`: Target database to explore (e.g., "art1025", "corporativo", "cobranca")

**Optional:**
- `SAMPLE_SIZE`: Number of rows to sample per table (default: 5)
- `OUTPUT_FORMAT`: Documentation format - "json", "markdown", or "both" (default: "both")
- `STORE_IN_MCP`: Store findings in Memory MCP (default: true)

## Prerequisites

Before executing this skill, ensure:
1. `.env` file exists with MariaDB credentials:
   - `MARIADB_HOST`
   - `MARIADB_PORT`
   - `MARIADB_USER`
   - `MARIADB_PASSWORD`
2. `mysql` client is installed and accessible
3. User has SELECT permissions on target database

## Execution Steps

### Step 1: Validate Connection and Database

Use Bash tool with command:
```bash
mysql -h "$MARIADB_HOST" -P "$MARIADB_PORT" -u "$MARIADB_USER" -p"$MARIADB_PASSWORD" -e "USE {DATABASE_NAME}; SELECT 1"
```
Description: "Validate connection to {DATABASE_NAME} database"

If connection fails:
- Output: "Failed to connect to {DATABASE_NAME}. Check credentials and database name."
- Exit skill

### Step 2: Database Discovery

Use Bash tool to execute these commands in sequence:

**2.1 List all databases:**
```bash
mysql -h "$MARIADB_HOST" -P "$MARIADB_PORT" -u "$MARIADB_USER" -p"$MARIADB_PASSWORD" -e "SHOW DATABASES;"
```
Description: "List all available databases on server"

**2.2 List all tables in target database:**
```bash
mysql -h "$MARIADB_HOST" -P "$MARIADB_PORT" -u "$MARIADB_USER" -p"$MARIADB_PASSWORD" {DATABASE_NAME} -e "SHOW TABLES;"
```
Description: "List all tables in {DATABASE_NAME}"

**2.3 Get table row counts:**
```bash
mysql -h "$MARIADB_HOST" -P "$MARIADB_PORT" -u "$MARIADB_USER" -p"$MARIADB_PASSWORD" {DATABASE_NAME} -e "SELECT TABLE_NAME, TABLE_ROWS, ROUND((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024, 2) AS 'Size_MB' FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{DATABASE_NAME}' ORDER BY TABLE_ROWS DESC;"
```
Description: "Get row counts and sizes for all tables"

### Step 3: Schema Analysis

For EACH table in the database:

**3.1 Describe table structure:**
```bash
mysql -h "$MARIADB_HOST" -P "$MARIADB_PORT" -u "$MARIADB_USER" -p"$MARIADB_PASSWORD" {DATABASE_NAME} -e "DESCRIBE {TABLE_NAME};"
```
Description: "Describe {TABLE_NAME} structure"

**3.2 Get detailed column information:**
```bash
mysql -h "$MARIADB_HOST" -P "$MARIADB_PORT" -u "$MARIADB_USER" -p"$MARIADB_PASSWORD" {DATABASE_NAME} -e "SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_KEY, COLUMN_DEFAULT, EXTRA FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{DATABASE_NAME}' AND TABLE_NAME = '{TABLE_NAME}' ORDER BY ORDINAL_POSITION;"
```
Description: "Get detailed column info for {TABLE_NAME}"

**3.3 Identify foreign keys:**
```bash
mysql -h "$MARIADB_HOST" -P "$MARIADB_PORT" -u "$MARIADB_USER" -p"$MARIADB_PASSWORD" {DATABASE_NAME} -e "SELECT CONSTRAINT_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA = '{DATABASE_NAME}' AND TABLE_NAME = '{TABLE_NAME}' AND REFERENCED_TABLE_NAME IS NOT NULL;"
```
Description: "Get foreign keys for {TABLE_NAME}"

**3.4 Get indexes:**
```bash
mysql -h "$MARIADB_HOST" -P "$MARIADB_PORT" -u "$MARIADB_USER" -p"$MARIADB_PASSWORD" {DATABASE_NAME} -e "SHOW INDEX FROM {TABLE_NAME};"
```
Description: "Get indexes for {TABLE_NAME}"

**NOTE:** For databases with many tables (>50), ask user if they want to analyze all tables or specify a subset.

### Step 4: Data Sampling

For each table (or user-specified subset):

```bash
mysql -h "$MARIADB_HOST" -P "$MARIADB_PORT" -u "$MARIADB_USER" -p"$MARIADB_PASSWORD" {DATABASE_NAME} -e "SELECT * FROM {TABLE_NAME} LIMIT {SAMPLE_SIZE};"
```
Description: "Sample {SAMPLE_SIZE} rows from {TABLE_NAME}"

### Step 5: Relationship Mapping

Analyze foreign key relationships to create an entity relationship diagram:

```bash
mysql -h "$MARIADB_HOST" -P "$MARIADB_PORT" -u "$MARIADB_USER" -p"$MARIADB_PASSWORD" {DATABASE_NAME} -e "SELECT TABLE_NAME, COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA = '{DATABASE_NAME}' AND REFERENCED_TABLE_NAME IS NOT NULL ORDER BY TABLE_NAME;"
```
Description: "Map all foreign key relationships in {DATABASE_NAME}"

### Step 6: Pattern Detection

Analyze the database to identify:

**6.1 Naming conventions:**
- Check if tables use ptBR (Portuguese) or English names
- Identify common prefixes/suffixes
- Document naming patterns

**6.2 Data patterns:**
- Identify lookup/reference tables (small, static data)
- Identify transaction tables (large, growing data)
- Identify audit/history tables
- Find views (tables starting with VI_, V_, etc.)

**6.3 Business domain:**
- Analyze table names and columns to infer business domain
- Group related tables by functionality
- Identify core vs auxiliary tables

### Step 7: Generate Documentation

**7.1 Create JSON documentation:**

Use Write tool to create: `schema_analysis_{DATABASE_NAME}.json` in the project root directory.

Structure:
```json
{
  "database_name": "{DATABASE_NAME}",
  "analysis_date": "YYYY-MM-DD",
  "total_tables": 0,
  "total_size_mb": 0.0,
  "naming_convention": "ptBR|English|Mixed",
  "business_domain": "Description of what this database manages",
  "tables": [
    {
      "name": "table_name",
      "rows": 0,
      "size_mb": 0.0,
      "primary_key": ["column1"],
      "foreign_keys": [
        {
          "column": "fk_column",
          "references": "other_table.other_column"
        }
      ],
      "columns": [
        {
          "name": "column_name",
          "type": "data_type",
          "nullable": true|false,
          "key": "PRI|UNI|MUL|null",
          "default": "value|null",
          "extra": "auto_increment|etc"
        }
      ],
      "indexes": [
        {
          "name": "index_name",
          "columns": ["col1", "col2"],
          "unique": true|false
        }
      ],
      "sample_data": []
    }
  ],
  "relationships": [
    {
      "from_table": "table1",
      "from_column": "column1",
      "to_table": "table2",
      "to_column": "column2"
    }
  ]
}
```

**7.2 Create Markdown documentation:**

Use Write tool to create: `SCHEMA_{DATABASE_NAME}.md` in the project root directory.

Structure:
```markdown
# {DATABASE_NAME} Database Schema Documentation

Generated: YYYY-MM-DD

## Overview

- **Database Name**: {DATABASE_NAME}
- **Total Tables**: X
- **Total Size**: X MB
- **Naming Convention**: ptBR/English/Mixed
- **Business Domain**: Description

## Database Purpose

[Inferred purpose based on table analysis]

## Table Statistics

| Table Name | Rows | Size (MB) | Type |
|------------|------|-----------|------|
| table1     | 1000 | 10.5      | Transaction |
| table2     | 50   | 0.2       | Lookup |

## Schema Details

### Table: {TABLE_NAME}

**Purpose**: [Inferred from table name and columns]

**Statistics:**
- Rows: X
- Size: X MB
- Primary Key: column1, column2

**Columns:**

| Column | Type | Nullable | Key | Default | Extra |
|--------|------|----------|-----|---------|-------|
| id     | int  | NO       | PRI | NULL    | auto_increment |

**Foreign Keys:**

| Column | References |
|--------|------------|
| fk_col | other_table.id |

**Indexes:**

| Index Name | Columns | Unique |
|------------|---------|--------|
| idx_name   | col1    | NO     |

**Sample Data:**

```
[First 5 rows]
```

[Repeat for each table]

## Relationships

```
table1.fk_id -> table2.id
table3.fk_id -> table1.id
```

## Integration Opportunities

[If analyzing for gefin-backend integration, identify potential sync points]

## Recommendations

[Based on analysis, provide recommendations for:]
- Data migration strategies
- Integration approaches
- Performance considerations
- Data quality concerns
```

### Step 8: Store in Memory MCP (if enabled)

Use mcp__memory__create_entities tool to create entities:

```json
{
  "entities": [
    {
      "name": "{DATABASE_NAME}",
      "entityType": "MariaDB_Database",
      "observations": [
        "Contains X tables with Y total rows",
        "Primary purpose: [business domain]",
        "Key tables: [list of main tables]",
        "Naming convention: [ptBR/English]",
        "Schema documented in: schema_analysis_{DATABASE_NAME}.json"
      ]
    }
  ]
}
```

Use mcp__memory__create_relations tool to link to related entities:

```json
{
  "relations": [
    {
      "from": "{DATABASE_NAME}",
      "to": "gefin-backend",
      "relationType": "potential_integration_source"
    }
  ]
}
```

### Step 9: Generate Summary Report

Output a comprehensive summary:

```
# {DATABASE_NAME} Database Analysis Complete

## Key Findings

- **Total Tables**: X
- **Total Records**: X million
- **Database Size**: X MB
- **Business Domain**: [description]

## Table Breakdown

- **Transaction Tables**: X (large, growing data)
- **Lookup Tables**: X (small, static data)
- **Audit/History Tables**: X
- **Views**: X

## Naming Conventions

[ptBR/English analysis]

## Top 10 Largest Tables

1. table1 - X rows (X MB)
2. table2 - X rows (X MB)
...

## Key Relationships

[Main foreign key relationships]

## Documentation Generated

✓ JSON Schema: schema_analysis_{DATABASE_NAME}.json
✓ Markdown Docs: SCHEMA_{DATABASE_NAME}.md
✓ Memory MCP: Entities and relations stored

## Integration Potential

[If applicable, suggest how this database could integrate with gefin-backend]

## Next Steps

1. Review documentation files
2. Identify specific tables/data needed for integration
3. Plan migration/sync strategy if needed
4. Consult with domain experts on business rules
```

## Error Handling

**Connection Errors:**
- Output: "Failed to connect to MariaDB server. Check .env credentials."
- Provide troubleshooting steps

**Database Not Found:**
- Output: "Database '{DATABASE_NAME}' not found."
- List available databases for reference

**Permission Errors:**
- Output: "Insufficient permissions to access {DATABASE_NAME}."
- Suggest checking user grants

**Large Database Warning:**
- If database has >100 tables, ask user:
  - "This database has X tables. Analyze all or specify a subset?"
  - Options: "All tables", "Top 20 by size", "Specify table names"

## Usage Examples

### Example 1: Explore art1025 database
```
User: Use mariadb-database-explorer skill with DATABASE_NAME="art1025"
```

### Example 2: Quick exploration without samples
```
User: Use mariadb-database-explorer skill with DATABASE_NAME="cobranca" and SAMPLE_SIZE=0
```

### Example 3: Markdown only
```
User: Use mariadb-database-explorer skill with DATABASE_NAME="corporativo", OUTPUT_FORMAT="markdown", STORE_IN_MCP=false
```

## Notes

- This skill uses READ-ONLY operations (SELECT, SHOW, DESCRIBE)
- No data is modified or deleted
- Password appears in process list briefly (use with caution on shared systems)
- Large databases may take several minutes to analyze completely
- Generated files are stored in the project root directory

## Integration with gefin-backend

When exploring databases for potential integration with gefin-backend:
1. Look for tables related to billing, publications, or users
2. Identify primary keys and foreign key relationships
3. Check for timestamp columns for sync strategies
4. Document data types for mapping to Pydantic models
5. Note any ptBR naming conventions for consistency

---

**Skill Version**: 1.0.0
**Last Updated**: 2025-01-23
**Author**: Claude Code (gefin-backend project)
