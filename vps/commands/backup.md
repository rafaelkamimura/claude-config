# VPS Backup Manager

Execute comprehensive VPS backups including databases, web files, and configurations.

## Execution Steps

### Step 1: Pre-Backup Checks

Use Bash tool with command:
```bash
echo "=== PRE-BACKUP CHECKS ===" && echo "" && echo "Current disk usage:" && df -h / && echo "" && echo "Creating backup directory..." && mkdir -p /backup && echo "Backup directory ready: /backup"
```

Description: "Verify disk space and prepare backup directory"

### Step 2: Database Backup Selection

Use AskUserQuestion tool with the following question:

- **Question**: "Which databases do you want to backup?"
- **Header**: "Database"
- **Options**:
  1. **Label**: "All Docker databases", **Description**: "Backup all databases from running Docker containers"
  2. **Label**: "Specific container", **Description**: "Backup database from a specific Docker container"
  3. **Label**: "Skip database backup", **Description**: "Don't backup databases"
- **multiSelect**: false

WAIT for user's response.

### Step 3: Execute Database Backup

If user selected "All Docker databases" or "Specific container":

Use Bash tool with command:
```bash
DATE=$(date +%Y%m%d_%H%M%S) && echo "=== DATABASE BACKUP ===" && docker ps --filter "ancestor=*postgres*" --filter "ancestor=*mysql*" --filter "ancestor=*mariadb*" --format "{{.Names}}" | while read container; do echo "Backing up $container..." && docker exec $container pg_dumpall -U postgres > /backup/db_${container}_${DATE}.sql 2>/dev/null || docker exec $container mysqldump -u root --all-databases > /backup/db_${container}_${DATE}.sql 2>/dev/null || echo "Failed to backup $container"; done && echo "Database backups complete"
```

Description: "Backup all databases from Docker containers"

If user wants specific container, ask for container name and backup that specific one.

### Step 4: Web Files Backup

Use Bash tool with command:
```bash
DATE=$(date +%Y%m%d_%H%M%S) && echo "=== WEB FILES BACKUP ===" && if [ -d /var/www/nag4wa ]; then tar -czf /backup/web_nag4wa_${DATE}.tar.gz /var/www/nag4wa && echo "Web files backed up: /backup/web_nag4wa_${DATE}.tar.gz" && ls -lh /backup/web_nag4wa_${DATE}.tar.gz; else echo "Web directory not found, skipping..."; fi
```

Description: "Backup web application files"

### Step 5: Nginx Configuration Backup

Use Bash tool with command:
```bash
DATE=$(date +%Y%m%d_%H%M%S) && echo "=== NGINX CONFIG BACKUP ===" && tar -czf /backup/nginx_config_${DATE}.tar.gz /etc/nginx/ && echo "Nginx config backed up: /backup/nginx_config_${DATE}.tar.gz" && ls -lh /backup/nginx_config_${DATE}.tar.gz
```

Description: "Backup Nginx configuration"

### Step 6: SSL Certificates Backup

Use Bash tool with command:
```bash
DATE=$(date +%Y%m%d_%H%M%S) && echo "=== SSL CERTIFICATES BACKUP ===" && if [ -d /etc/letsencrypt ]; then tar -czf /backup/ssl_certs_${DATE}.tar.gz /etc/letsencrypt && echo "SSL certificates backed up: /backup/ssl_certs_${DATE}.tar.gz" && ls -lh /backup/ssl_certs_${DATE}.tar.gz; else echo "No SSL certificates found, skipping..."; fi
```

Description: "Backup SSL certificates"

### Step 7: Docker Volumes Backup (Optional)

Use AskUserQuestion tool with the following question:

- **Question**: "Do you want to backup Docker volumes?"
- **Header**: "Volumes"
- **Options**:
  1. **Label**: "Yes, backup all volumes", **Description**: "Backup all Docker volumes"
  2. **Label**: "No, skip volumes", **Description**: "Skip Docker volume backup"
- **multiSelect**: false

WAIT for user's response.

If user selected "Yes, backup all volumes":

Use Bash tool with command:
```bash
DATE=$(date +%Y%m%d_%H%M%S) && echo "=== DOCKER VOLUMES BACKUP ===" && docker volume ls -q | while read volume; do echo "Backing up volume: $volume" && docker run --rm -v ${volume}:/data -v /backup:/backup alpine tar -czf /backup/volume_${volume}_${DATE}.tar.gz -C /data . && echo "Volume $volume backed up"; done && echo "Docker volumes backup complete"
```

Description: "Backup all Docker volumes"

### Step 8: Cleanup Old Backups

Use AskUserQuestion tool with the following question:

- **Question**: "Remove backups older than how many days?"
- **Header**: "Retention"
- **Options**:
  1. **Label**: "7 days", **Description**: "Keep last 7 days of backups"
  2. **Label**: "14 days", **Description**: "Keep last 14 days of backups"
  3. **Label**: "30 days", **Description**: "Keep last 30 days of backups"
  4. **Label**: "Don't delete old backups", **Description**: "Keep all backups"
- **multiSelect**: false

WAIT for user's response.

If user selected a retention period:

Use Bash tool with command (replace {days} with user's selection):
```bash
echo "=== CLEANING OLD BACKUPS ===" && find /backup -name "*.tar.gz" -mtime +{days} -delete && find /backup -name "*.sql" -mtime +{days} -delete && echo "Old backups removed (older than {days} days)"
```

Description: "Remove old backup files"

### Step 9: Backup Summary

Use Bash tool with command:
```bash
echo "=== BACKUP SUMMARY ===" && echo "" && echo "Backup location: /backup" && echo "" && echo "Recent backups:" && ls -lh /backup | tail -20 && echo "" && echo "Total backup size:" && du -sh /backup && echo "" && echo "Disk space after backup:" && df -h /
```

Description: "Show backup summary and disk usage"

Output: "Backup complete! All files saved to /backup directory."

## Notes

- Backups are stored in `/backup` directory
- Database backups are in SQL format
- Configuration and file backups are compressed tar.gz files
- Consider moving backups to external storage for disaster recovery
- Set up automated backups using cron for production systems
