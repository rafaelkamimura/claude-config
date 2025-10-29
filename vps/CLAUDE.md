# Global Claude Instructions - VPS Server Edition

This file provides universal guidance for Claude Code sessions on this VPS server.

## Priority
Always check for and prioritize project-specific `CLAUDE.md` files in the current working directory or project root. Those instructions override these global defaults.

## VPS Server Context

This is an **Ubuntu 22.04 VPS** running production services. All guidance should prioritize:
1. **Stability** - Don't break running services
2. **Security** - Audit all changes for vulnerabilities
3. **Performance** - Optimize for server workloads
4. **Reliability** - Ensure services restart after reboot

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
func CalculateTotal(items []Item) float64 {
```

## File Operations

### Universal File Management Rules
- **NEVER** create files unless absolutely necessary
- **ALWAYS** prefer editing existing files over creating new ones
- **NEVER** proactively create documentation files (*.md) unless explicitly requested
- **ALWAYS** use Read tool before Edit tool
- **ALWAYS** use absolute paths for file operations

### Tool Hierarchy for File Operations
1. `Read` → `Edit` → `Write` (in that order of preference)
2. Use `mcp__filesystem__*` tools for complex operations
3. Use `Grep`/`Glob` for file discovery before reading
4. **NEVER** use bash commands like `cat`, `sed`, `awk` for file operations - use dedicated tools

## VPS Server Management

### System Monitoring Commands
```bash
# Quick health check
free -h && df -h && uptime

# Monitor active connections
ss -tuln | grep LISTEN

# Check service status
systemctl status nginx docker

# View recent logs
journalctl -u nginx -n 50 --no-pager
journalctl -u docker -n 50 --no-pager
```

### Docker Management
```bash
# Container lifecycle
docker ps -a
docker logs -f <container>
docker restart <container>

# Cleanup (run regularly)
docker container prune -f
docker image prune -a -f
docker volume prune -f

# Resource usage
docker stats --no-stream
```

### Nginx Management
```bash
# ALWAYS test before reload
nginx -t

# Reload after config changes
systemctl reload nginx

# View logs
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log
```

### MariaDB/MySQL Query Execution
When working with MariaDB/MySQL databases, use the `mysql` command directly:

```bash
# First, load .env file if it exists
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Execute query using environment variables
mysql -h "$DB_HOST" -P "${DB_PORT:-3306}" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" -e "SELECT * FROM users LIMIT 10;"

# Execute multiple queries
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" <<EOF
SHOW TABLES;
DESCRIBE users;
SELECT COUNT(*) FROM posts;
EOF

# Check database connection
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" -e "SELECT 1"

# Show table structure
mysql -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" -e "DESCRIBE table_name"
```

**Best Practices**:
- Always use environment variables from `.env` file
- Never hardcode credentials in commands
- Use `--batch` flag for script-friendly output
- Add `--silent` to suppress column headers when needed

## Development Workflow

### Pre-Task Checklist
1. Check for project documentation:
   - `CLAUDE.md` (project-specific instructions)
   - `README.md` (project overview)
   - `.env` (environment configuration)
2. Identify project type (check for `package.json`, `go.mod`, `pyproject.toml`, etc.)
3. Verify services are running: `systemctl status nginx docker`
4. Review recent git history if applicable

### Standard Quality Gates
Before any commit or significant change:
1. **Test**: Run test suite and ensure all tests pass
2. **Security**: Run security scans for sensitive changes
3. **Lint**: Run linters if available
4. **Service Check**: Ensure services still work after changes

### Git Workflow Standards
- Use conventional commits: `feat:`, `fix:`, `docs:`, `chore:`, `security:`
- Never commit with failing tests
- Never commit code with security vulnerabilities
- Never commit secrets (.env files, credentials, API keys)
- Include file references with line numbers in commit messages

## Tool Usage Guidelines

### Claude Code Iterations UI

Structure work in clear phases for better visibility:

```markdown
✅ GOOD - Clear iteration boundaries:
1. First, I'll analyze the requirements
   [Use Read/Grep tools, present findings]

2. Now I'll implement the changes
   [Use Edit/Write tools, make changes]

3. Finally, I'll verify everything works
   [Use Bash tool for tests, show results]
```

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
4. **Bash commands** (only for system operations)

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
- `database-optimizer`: SQL and schema changes
- `python-pro`: Python-specific optimizations
- `debugger`: Error analysis and troubleshooting
- `devops-troubleshooter`: Production debugging and system outages

## Security & Quality Standards

### Security Requirements
- Always run security checks on authentication code
- Never log or expose secrets/API keys
- Validate all user inputs
- Use parameterized queries for database operations
- Check dependencies for known vulnerabilities
- Review auth logs regularly: `grep "Failed password" /var/log/auth.log`

### VPS Security Checklist
```bash
# Check firewall status
ufw status verbose

# Review recent authentication attempts
last -20
grep "Failed password" /var/log/auth.log | tail -20

# SSL certificate expiry
certbot certificates

# Check for security updates
apt update && apt list --upgradable | grep -i security
```

## Emergency Procedures

### Service Recovery

#### Nginx Failed
```bash
# Check status and logs
systemctl status nginx --no-pager
nginx -t
journalctl -u nginx -n 50 --no-pager

# Fix and restart
nginx -t  # Fix any errors first
systemctl restart nginx
```

#### Docker Failed
```bash
# Check status
systemctl status docker --no-pager
journalctl -u docker -n 50 --no-pager

# Restart
systemctl restart docker

# Verify containers
docker ps -a
```

#### Out of Disk Space
```bash
# Check usage
df -h
du -sh /* | sort -h

# Quick cleanup
docker system prune -a -f
journalctl --vacuum-time=3d
apt autoremove -y && apt autoclean

# Find large files
find /var -type f -size +100M -exec ls -lh {} \;
```

#### High CPU/Memory Usage
```bash
# Identify culprit
ps aux --sort=-%cpu | head -10
ps aux --sort=-%mem | head -10

# Check Docker containers
docker stats --no-stream

# Check specific service
systemctl status <service> --no-pager
```

### Security Incident Response
1. Check active connections: `ss -tuln`
2. Review auth logs: `tail -100 /var/log/auth.log`
3. Check running processes: `ps aux | grep -v "^\["`
4. Review Nginx access logs for suspicious patterns
5. If compromised, isolate server and notify stakeholders

## Automated Maintenance

### Daily Maintenance Script
```bash
#!/bin/bash
# /root/scripts/maintenance.sh
# Run daily: 0 2 * * * /root/scripts/maintenance.sh

# Clean Docker
docker system prune -f

# Clean logs older than 7 days
journalctl --vacuum-time=7d

# Clean package cache
apt autoremove -y && apt autoclean

# Log completion
echo "Maintenance complete: $(date)" >> /var/log/maintenance.log
```

### Weekly Backup Script
```bash
#!/bin/bash
# /root/scripts/backup.sh

BACKUP_DIR="/backup"
DATE=$(date +%Y%m%d)

# Database backup
docker exec <db_container> mysqldump -u root -p<password> --all-databases > $BACKUP_DIR/db_$DATE.sql

# Web files backup
tar -czf $BACKUP_DIR/web_$DATE.tar.gz /var/www/

# Nginx config backup
tar -czf $BACKUP_DIR/nginx_$DATE.tar.gz /etc/nginx/

# Keep only last 7 backups
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete
```

## Performance Optimization

### Nginx Performance Tuning
Key configuration parameters already optimized:
- `worker_processes auto` (matches CPU cores)
- `worker_connections 2048`
- `multi_accept on`
- `keepalive_timeout 30`
- `gzip` enabled with compression level 5
- SSL session cache: 100m

### Docker Performance
- Prune unused resources regularly
- Monitor container resources: `docker stats`
- Set resource limits in docker-compose.yml if needed

### System Performance Monitoring
```bash
# CPU and load
uptime
top -bn1 | head -20

# Memory
free -h

# Disk I/O
iostat -x 1 3  # if sysstat installed

# Network
ss -s
netstat -i
```

## Project Type Detection

### Common Project Indicators
1. **Python**: `requirements.txt`, `pyproject.toml`, `setup.py`
2. **Node.js**: `package.json`, `yarn.lock`, `package-lock.json`
3. **Go**: `go.mod`, `go.sum`
4. **PHP**: `composer.json`, `composer.lock`
5. **Docker**: `docker-compose.yml`, `Dockerfile`

### Tool Availability Verification
```bash
# Check for build tools
which make npm python3 node docker docker-compose

# Verify Python dependencies
python3 --version
pip3 list

# Verify Node dependencies
node --version
npm list --depth=0
```

## Common VPS Operations

### SSL Certificate Management
```bash
# Check expiry
certbot certificates

# Renew certificates
certbot renew --dry-run  # Test first
certbot renew            # Actual renewal

# Configure for nginx
certbot --nginx -d escavador.nag4wa.org
```

### Service Management
```bash
# Enable service on boot
systemctl enable <service>

# Disable service
systemctl disable <service>

# Check if enabled
systemctl is-enabled <service>

# View service logs
journalctl -u <service> -f
```

### User Management
```bash
# List users
cat /etc/passwd | grep "/home"

# Check user's groups
groups <username>

# File ownership on VPS
# Web files: raguser:root
# System configs: root:root
```

## Output Standards

- No emojis in any output or code
- Never mention AI-generated or co-authored attributions unless user explicitly requests
- Use clear, concise language in all communications
- Provide file paths with line numbers for code references (e.g., `/etc/nginx/nginx.conf:42`)

## Version History

**Last Updated**: 2025-10-29
**Version**: 3.0.0 (VPS-Optimized)

**Changelog**:
- v3.0.0 (2025-10-29): Complete VPS optimization
  - Removed all macOS-specific content
  - Added VPS server management sections
  - Added emergency procedures
  - Added automated maintenance scripts
  - Focused on production server stability
- v2.1.0 (2025-10-20): Added Iterations UI optimization
- v2.0.0 (2025-01-16): Initial comprehensive global instructions

*This file provides universal defaults for Claude Code sessions on this VPS. Project-specific CLAUDE.md files override these settings.*
