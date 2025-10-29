# Server Health Check

Comprehensive VPS health check with system resources, services, and security status.

## Execution Steps

### Step 1: System Resources Check

Use Bash tool with command:
```bash
echo "=== SYSTEM HEALTH REPORT ===" && echo "" && echo "=== UPTIME & LOAD ===" && uptime && echo "" && echo "=== CPU INFO ===" && lscpu | grep -E "^CPU\(s\)|Model name|Thread" && echo "" && echo "=== MEMORY ===" && free -h && echo "" && echo "=== SWAP ===" && swapon -s && echo "" && echo "=== DISK USAGE ===" && df -h / && echo "" && echo "=== DISK I/O (Top 5 Processes) ===" && ps aux --sort=-%cpu | head -6
```

Description: "Collect system resource metrics"

### Step 2: Service Status Check

Use Bash tool with command:
```bash
echo "=== SERVICE STATUS ===" && systemctl is-active nginx docker ssh && echo "" && echo "=== NGINX STATUS ===" && systemctl status nginx --no-pager | head -10 && echo "" && echo "=== DOCKER STATUS ===" && systemctl status docker --no-pager | head -10 && echo "" && echo "=== DOCKER CONTAINERS ===" && docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

Description: "Check status of critical services"

### Step 3: Network Status Check

Use Bash tool with command:
```bash
echo "=== NETWORK STATUS ===" && echo "" && echo "=== LISTENING PORTS ===" && ss -tuln | grep LISTEN && echo "" && echo "=== ACTIVE CONNECTIONS ===" && ss -s && echo "" && echo "=== NETWORK INTERFACES ===" && ip -br addr
```

Description: "Check network configuration and connections"

### Step 4: Security Status Check

Use Bash tool with command:
```bash
echo "=== SECURITY STATUS ===" && echo "" && echo "=== FIREWALL STATUS ===" && ufw status || echo "Firewall not enabled" && echo "" && echo "=== RECENT LOGIN ATTEMPTS ===" && last -5 && echo "" && echo "=== FAILED LOGIN ATTEMPTS ===" && lastb -5 2>/dev/null || echo "No failed login attempts" && echo "" && echo "=== SSL CERTIFICATES ===" && certbot certificates 2>/dev/null || echo "Certbot not configured"
```

Description: "Check security configuration and recent access"

### Step 5: Recent Errors Check

Use Bash tool with command:
```bash
echo "=== RECENT ERRORS ===" && echo "" && echo "=== NGINX ERRORS (Last 10) ===" && tail -10 /var/log/nginx/error.log 2>/dev/null || echo "No Nginx errors found" && echo "" && echo "=== SYSTEM ERRORS (Last 10) ===" && journalctl -p err -n 10 --no-pager || echo "No recent system errors" && echo "" && echo "=== DOCKER ERRORS ===" && journalctl -u docker -p err -n 10 --no-pager || echo "No Docker errors"
```

Description: "Check for recent errors in logs"

### Step 6: Summary and Recommendations

Output a summary based on the health check results:

- If load average > CPU count: Warn about high CPU usage
- If memory available < 1GB: Warn about low memory
- If disk usage > 80%: Warn about disk space
- If any critical service is inactive: Alert about service failure
- If firewall is disabled: Recommend enabling it
- If swap usage > 50%: Investigate memory pressure

Output: "Health check complete. Review the output above for any issues requiring attention."
