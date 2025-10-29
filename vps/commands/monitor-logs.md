# Log Monitor

Real-time log monitoring for VPS services with filtering and search capabilities.

## Execution Steps

### Step 1: Select Log Source

Use AskUserQuestion tool with the following question:

- **Question**: "Which logs do you want to monitor?"
- **Header**: "Log Source"
- **Options**:
  1. **Label**: "All critical logs", **Description**: "Monitor Nginx, Docker, and system logs simultaneously"
  2. **Label**: "Nginx access log", **Description**: "Monitor HTTP/HTTPS access requests"
  3. **Label**: "Nginx error log", **Description**: "Monitor Nginx errors and warnings"
  4. **Label**: "Docker container logs", **Description**: "Monitor specific Docker container"
  5. **Label**: "System logs (journalctl)", **Description**: "Monitor system-wide logs"
  6. **Label**: "Authentication logs", **Description**: "Monitor login attempts and auth events"
- **multiSelect**: false

WAIT for user's response.

### Step 2: Apply Filters (Optional)

Use AskUserQuestion tool with the following question:

- **Question**: "Do you want to filter the logs?"
- **Header**: "Filters"
- **Options**:
  1. **Label**: "No filter (show all)", **Description**: "Display all log entries"
  2. **Label**: "Errors only", **Description**: "Show only error messages"
  3. **Label**: "Custom filter", **Description**: "Enter custom grep pattern"
- **multiSelect**: false

WAIT for user's response.

If user selected "Custom filter":

Output: "Enter your grep pattern (e.g., '404', 'error', 'failed'):"

WAIT for user's next message with the filter pattern.

### Step 3: Execute Log Monitoring

Based on user's selection in Step 1:

**If "All critical logs" selected:**

Use Bash tool with command (adjust based on filter selection):
```bash
echo "=== MONITORING ALL CRITICAL LOGS ===" && echo "Press Ctrl+C to stop" && echo "" && (tail -f /var/log/nginx/error.log & tail -f /var/log/nginx/access.log & journalctl -f -u docker & journalctl -f -p err)
```

Description: "Monitor all critical system logs in real-time"

**If "Nginx access log" selected:**

For no filter:
```bash
echo "=== NGINX ACCESS LOG ===" && echo "Press Ctrl+C to stop" && echo "" && tail -f /var/log/nginx/access.log
```

For errors only:
```bash
echo "=== NGINX ACCESS LOG (Errors Only) ===" && echo "Press Ctrl+C to stop" && echo "" && tail -f /var/log/nginx/access.log | grep -E " (4[0-9]{2}|5[0-9]{2}) "
```

For custom filter (replace {pattern} with user's pattern):
```bash
echo "=== NGINX ACCESS LOG (Filtered) ===" && echo "Press Ctrl+C to stop" && echo "" && tail -f /var/log/nginx/access.log | grep "{pattern}"
```

Description: "Monitor Nginx access log"

**If "Nginx error log" selected:**

For no filter:
```bash
echo "=== NGINX ERROR LOG ===" && echo "Press Ctrl+C to stop" && echo "" && tail -f /var/log/nginx/error.log
```

For errors only:
```bash
echo "=== NGINX ERROR LOG (Errors Only) ===" && echo "Press Ctrl+C to stop" && echo "" && tail -f /var/log/nginx/error.log | grep -E "\[error\]|\[crit\]|\[alert\]|\[emerg\]"
```

For custom filter (replace {pattern} with user's pattern):
```bash
echo "=== NGINX ERROR LOG (Filtered) ===" && echo "Press Ctrl+C to stop" && echo "" && tail -f /var/log/nginx/error.log | grep "{pattern}"
```

Description: "Monitor Nginx error log"

**If "Docker container logs" selected:**

First, show available containers:

Use Bash tool with command:
```bash
echo "=== AVAILABLE DOCKER CONTAINERS ===" && docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Image}}"
```

Description: "List running Docker containers"

Output: "Enter the container name you want to monitor:"

WAIT for user's next message with container name.

Then use Bash tool with command (replace {container} with user's input):
```bash
echo "=== MONITORING CONTAINER: {container} ===" && echo "Press Ctrl+C to stop" && echo "" && docker logs -f {container}
```

Description: "Monitor Docker container logs"

**If "System logs (journalctl)" selected:**

For no filter:
```bash
echo "=== SYSTEM LOGS ===" && echo "Press Ctrl+C to stop" && echo "" && journalctl -f
```

For errors only:
```bash
echo "=== SYSTEM LOGS (Errors Only) ===" && echo "Press Ctrl+C to stop" && echo "" && journalctl -f -p err
```

For custom filter (replace {pattern} with user's pattern):
```bash
echo "=== SYSTEM LOGS (Filtered) ===" && echo "Press Ctrl+C to stop" && echo "" && journalctl -f | grep "{pattern}"
```

Description: "Monitor system logs via journalctl"

**If "Authentication logs" selected:**

For no filter:
```bash
echo "=== AUTHENTICATION LOGS ===" && echo "Press Ctrl+C to stop" && echo "" && tail -f /var/log/auth.log
```

For errors only (failed attempts):
```bash
echo "=== AUTHENTICATION LOGS (Failed Attempts) ===" && echo "Press Ctrl+C to stop" && echo "" && tail -f /var/log/auth.log | grep -E "Failed password|authentication failure|Invalid user"
```

For custom filter (replace {pattern} with user's pattern):
```bash
echo "=== AUTHENTICATION LOGS (Filtered) ===" && echo "Press Ctrl+C to stop" && echo "" && tail -f /var/log/auth.log | grep "{pattern}"
```

Description: "Monitor authentication and login logs"

### Step 4: Monitoring Active

Output: "Log monitoring active. Press Ctrl+C to stop."

Output: "Note: In Claude Code, use the interrupt button or close the terminal to stop monitoring."

## Quick Log Analysis Commands

After stopping monitoring, offer these analysis options:

### Recent Errors Summary
```bash
echo "=== RECENT ERRORS SUMMARY ===" && echo "" && echo "Nginx errors:" && tail -20 /var/log/nginx/error.log | grep -c error && echo "" && echo "System errors:" && journalctl -p err --since "1 hour ago" --no-pager | wc -l && echo "" && echo "Failed logins:" && grep "Failed password" /var/log/auth.log | tail -10
```

### Traffic Summary (Last Hour)
```bash
echo "=== TRAFFIC SUMMARY (Last Hour) ===" && echo "" && echo "Total requests:" && journalctl -u nginx --since "1 hour ago" --no-pager | grep -c "GET\|POST" && echo "" && echo "Status codes:" && tail -1000 /var/log/nginx/access.log | awk '{print $9}' | sort | uniq -c | sort -rn
```

### Top IPs (Last 1000 requests)
```bash
echo "=== TOP IP ADDRESSES ===" && tail -1000 /var/log/nginx/access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head -10
```

## Notes

- Logs are monitored in real-time (tail -f)
- Use Ctrl+C or interrupt button to stop monitoring
- Multiple log sources can't be monitored simultaneously in same session
- For permanent monitoring, consider using `screen` or `tmux`
- Log files can be large - filters help reduce noise
- Some logs require root access

## Common Filter Patterns

- **HTTP errors**: `" (4[0-9]{2}|5[0-9]{2}) "`
- **Failed logins**: `"Failed password|authentication failure"`
- **Docker errors**: `"error|Error|ERROR"`
- **SSL issues**: `"SSL|TLS|certificate"`
- **Slow requests**: `"upstream timed out|timeout"`
- **Specific IP**: `"192.168.1.100"`
