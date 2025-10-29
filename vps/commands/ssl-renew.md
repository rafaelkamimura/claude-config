# SSL Certificate Renewal

Manage SSL certificate renewal for Let's Encrypt certificates with safety checks.

## Execution Steps

### Step 1: Check Current Certificate Status

Use Bash tool with command:
```bash
echo "=== SSL CERTIFICATE STATUS ===" && echo "" && certbot certificates && echo "" && echo "=== CERTIFICATE EXPIRY DATES ===" && for cert in /etc/letsencrypt/live/*/cert.pem; do domain=$(dirname $cert | xargs basename) && expiry=$(openssl x509 -enddate -noout -in $cert | cut -d= -f2) && echo "Domain: $domain - Expires: $expiry"; done
```

Description: "Check current SSL certificate status and expiry dates"

### Step 2: Analyze Certificate Status

Review the output from Step 1:
- If certificates expire in less than 30 days: Recommend renewal
- If certificates expire in more than 30 days: Inform user renewal is not urgent
- If no certificates found: Inform user to set up certificates first

Output: "Certificate status check complete. See expiry dates above."

### Step 3: Renewal Decision

Use AskUserQuestion tool with the following question:

- **Question**: "How do you want to proceed with certificate renewal?"
- **Header**: "Action"
- **Options**:
  1. **Label**: "Test renewal (dry-run)", **Description**: "Simulate renewal without making changes"
  2. **Label**: "Force renewal now", **Description**: "Force renewal even if not expiring soon"
  3. **Label**: "Automatic renewal check", **Description**: "Let certbot decide if renewal is needed"
  4. **Label**: "Cancel", **Description**: "Exit without making changes"
- **multiSelect**: false

WAIT for user's response.

### Step 4: Execute Renewal Based on Selection

If user selected "Test renewal (dry-run)":

Use Bash tool with command:
```bash
echo "=== TESTING SSL RENEWAL ===" && certbot renew --dry-run && echo "" && echo "Test complete. No changes were made."
```

Description: "Test SSL certificate renewal process"

If user selected "Force renewal now":

Use Bash tool with command:
```bash
echo "=== FORCING SSL RENEWAL ===" && certbot renew --force-renewal && echo "" && echo "Forced renewal complete."
```

Description: "Force SSL certificate renewal"

If user selected "Automatic renewal check":

Use Bash tool with command:
```bash
echo "=== AUTOMATIC SSL RENEWAL ===" && certbot renew && echo "" && echo "Automatic renewal check complete."
```

Description: "Run automatic SSL certificate renewal"

If user selected "Cancel":

Output: "SSL renewal cancelled. No changes made."

Exit command.

### Step 5: Verify Renewal Success

If renewal was attempted (not cancelled or dry-run):

Use Bash tool with command:
```bash
echo "=== VERIFYING RENEWED CERTIFICATES ===" && echo "" && certbot certificates && echo "" && echo "=== NEW EXPIRY DATES ===" && for cert in /etc/letsencrypt/live/*/cert.pem; do domain=$(dirname $cert | xargs basename) && expiry=$(openssl x509 -enddate -noout -in $cert | cut -d= -f2) && echo "Domain: $domain - Expires: $expiry"; done
```

Description: "Verify renewed certificate status"

### Step 6: Test Nginx Configuration

Use Bash tool with command:
```bash
echo "=== TESTING NGINX CONFIGURATION ===" && nginx -t && echo "" && echo "Nginx configuration is valid."
```

Description: "Test Nginx configuration with new certificates"

### Step 7: Reload Nginx

If Nginx configuration test passed:

Use Bash tool with command:
```bash
echo "=== RELOADING NGINX ===" && systemctl reload nginx && systemctl status nginx --no-pager | head -10 && echo "" && echo "Nginx reloaded with new certificates."
```

Description: "Reload Nginx to apply new SSL certificates"

If Nginx configuration test failed:

Output: "CRITICAL: Nginx configuration test failed! Do not reload Nginx. Review the error output above and fix configuration issues."

Exit command.

### Step 8: Verify SSL Connection

Use Bash tool with command:
```bash
echo "=== VERIFYING SSL CONNECTION ===" && echo "" && for domain in escavador.nag4wa.org; do echo "Testing: $domain" && echo | openssl s_client -connect $domain:443 -servername $domain 2>/dev/null | openssl x509 -noout -dates 2>/dev/null && echo ""; done
```

Description: "Verify SSL connections are working"

### Step 9: Summary

Output: "SSL certificate renewal complete!"

Output summary:
- Certificate renewal status (success/failure)
- New expiry dates
- Nginx reload status
- Next recommended renewal date (60 days before expiry)

## Notes

- Let's Encrypt certificates are valid for 90 days
- Automatic renewal should happen at 60 days (30 days before expiry)
- Always test with --dry-run first if unsure
- Certbot automatically handles renewal hooks
- Nginx must be reloaded for new certificates to take effect
- Check /var/log/letsencrypt/letsencrypt.log for detailed renewal logs

## Troubleshooting

If renewal fails:
1. Check Nginx is running: `systemctl status nginx`
2. Check port 80 is accessible (certbot needs it for validation)
3. Check DNS records point to this server
4. Check firewall allows port 80: `ufw status | grep 80`
5. Review logs: `tail -50 /var/log/letsencrypt/letsencrypt.log`
