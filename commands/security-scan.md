# Security Scanner

Comprehensive security analysis tool that performs SAST/DAST scanning, dependency checks, secret detection, and license compliance verification.

## Purpose
- Run static and dynamic security analysis
- Check dependencies for vulnerabilities
- Detect hardcoded secrets and credentials
- Verify license compliance
- Generate security reports for merge requests

## Workflow

### Phase 1: Scan Type Selection
1. **STOP** → "Select security scan type:"
   ```
   1. Quick scan - Fast checks for critical issues
   2. Full scan - Comprehensive security analysis
   3. Secrets only - API keys, passwords, tokens
   4. Dependencies only - Vulnerable packages
   5. License check - Compliance verification
   6. Custom scan - Select specific checks
   
   Choose type (1-6):
   ```

2. **Scan Options**
   - STOP → "Include SAST analysis? (y/n):"
   - STOP → "Check container images? (y/n):"
   - STOP → "Scan infrastructure code? (y/n):"
   - STOP → "Generate SBOM? (y/n):"

### Phase 2: Environment Detection
1. **Identify Technologies**
   ```bash
   # Detect languages and frameworks
   languages=""
   [ -f "package.json" ] && languages="$languages javascript"
   [ -f "requirements.txt" ] && languages="$languages python"
   [ -f "go.mod" ] && languages="$languages go"
   [ -f "Cargo.toml" ] && languages="$languages rust"
   [ -f "pom.xml" ] && languages="$languages java"
   [ -f "Gemfile" ] && languages="$languages ruby"
   [ -f "composer.json" ] && languages="$languages php"
   ```

2. **Check for Security Tools**
   ```bash
   # Check existing security configurations
   [ -f ".semgrep.yml" ] && echo "Semgrep configured"
   [ -f ".snyk" ] && echo "Snyk configured"
   [ -f ".gitleaks.toml" ] && echo "Gitleaks configured"
   ```

### Phase 3: SAST Analysis
1. **Run Semgrep Scan**
   Use mcp__semgrep tools:
   ```python
   # Prepare files for scanning
   code_files = []
   for file in changed_files:
       content = read_file(file)
       code_files.append({
           "filename": file,
           "content": content
       })
   
   # Run security scan
   results = semgrep_scan(code_files, config="auto")
   ```

2. **Common Vulnerability Patterns**
   - SQL Injection
   - XSS vulnerabilities
   - Command injection
   - Path traversal
   - Insecure deserialization
   - Authentication bypass
   - Cryptographic weaknesses

3. **Framework-Specific Checks**
   ```yaml
   # React/Vue XSS
   - pattern: dangerouslySetInnerHTML={{...}}
     severity: HIGH
   
   # Express.js
   - pattern: app.use(cors())  # without options
     severity: MEDIUM
   
   # Django
   - pattern: DEBUG = True  # in production
     severity: CRITICAL
   ```

### Phase 4: Secret Detection
1. **Scan for Secrets**
   ```bash
   # Common secret patterns
   patterns:
     - AWS: AKIA[0-9A-Z]{16}
     - GitHub: ghp_[0-9a-zA-Z]{36}
     - Generic API: api[_-]?key[_-]?=[\'\"][0-9a-zA-Z]{32,}
     - Private Key: -----BEGIN (RSA|DSA|EC|PGP) PRIVATE KEY
     - Password: password\s*=\s*[\'\"][^\'\"]+[\'\"]
   ```

2. **Check Files**
   ```bash
   # High-risk files
   .env
   .env.local
   config.json
   settings.py
   application.properties
   docker-compose.yml
   ```

3. **Secret Remediation**
   ```markdown
   ## Detected Secrets
   
   ⚠️ **Critical**: AWS Access Key found
   - File: src/config.js:45
   - Pattern: AKIAIOSFODNN7EXAMPLE
   - Action: Move to environment variable
   
   Suggested fix:
   ```javascript
   // Instead of:
   const AWS_KEY = "AKIAIOSFODNN7EXAMPLE";
   
   // Use:
   const AWS_KEY = process.env.AWS_ACCESS_KEY_ID;
   ```

### Phase 5: Dependency Scanning
1. **Check Package Vulnerabilities**
   
   **JavaScript/Node.js:**
   ```bash
   npm audit --json
   npx snyk test
   ```
   
   **Python:**
   ```bash
   pip-audit
   safety check
   ```
   
   **Go:**
   ```bash
   go list -m all | nancy sleuth
   govulncheck ./...
   ```
   
   **Java:**
   ```bash
   mvn dependency-check:check
   ```

2. **Vulnerability Report**
   ```markdown
   ## Dependency Vulnerabilities
   
   ### Critical (2)
   | Package | Version | Vulnerability | Fix |
   |---------|---------|---------------|-----|
   | lodash | 4.17.19 | Prototype Pollution | Update to 4.17.21 |
   | axios | 0.21.0 | SSRF | Update to 0.21.2 |
   
   ### High (3)
   | Package | Version | CVE | CVSS |
   |---------|---------|-----|------|
   | express | 4.17.0 | CVE-2022-24999 | 7.5 |
   ```

3. **Auto-Fix Dependencies**
   ```bash
   # Auto-update safe dependencies
   npm audit fix
   
   # Force updates (with caution)
   npm audit fix --force
   ```

### Phase 6: License Compliance
1. **Scan Licenses**
   ```bash
   # Extract all licenses
   license-checker --json > licenses.json
   ```

2. **Check Compliance**
   ```yaml
   allowed_licenses:
     - MIT
     - Apache-2.0
     - BSD-3-Clause
     - ISC
   
   restricted_licenses:
     - GPL-3.0
     - AGPL-3.0
   
   forbidden_licenses:
     - Commercial
     - Proprietary
   ```

3. **License Report**
   ```markdown
   ## License Compliance
   
   ### Summary
   - Total packages: 847
   - Compliant: 832
   - Warnings: 12
   - Violations: 3
   
   ### Violations
   | Package | License | Risk |
   |---------|---------|------|
   | some-lib | GPL-3.0 | Copyleft requirement |
   | other-pkg | Unknown | Legal risk |
   ```

### Phase 7: Container Security
1. **Scan Docker Images**
   ```bash
   # Scan with Trivy
   trivy image myapp:latest
   
   # Scan Dockerfile
   hadolint Dockerfile
   ```

2. **Check Base Images**
   ```dockerfile
   # Vulnerable base image
   FROM node:14-alpine  # CVE-2023-xxxxx
   
   # Suggested fix
   FROM node:20-alpine
   ```

3. **Runtime Security**
   ```yaml
   # Security best practices
   - Don't run as root
   - Use minimal base images
   - Remove unnecessary packages
   - Scan at build time
   - Sign images
   ```

### Phase 8: Infrastructure as Code
1. **Scan Terraform/CloudFormation**
   ```bash
   # Terraform
   tfsec .
   checkov -d .
   
   # CloudFormation
   cfn-lint template.yaml
   ```

2. **Common IaC Issues**
   ```yaml
   issues:
     - S3 bucket public access
     - Unencrypted databases
     - Open security groups
     - Missing logging
     - Weak IAM policies
   ```

### Phase 9: Security Report Generation
1. **Aggregate Results**
   ```markdown
   # Security Scan Report
   
   ## Executive Summary
   - **Critical Issues**: 2
   - **High Issues**: 5
   - **Medium Issues**: 12
   - **Low Issues**: 23
   
   ## Critical Findings
   
   ### 1. Hardcoded AWS Credentials
   **File**: src/config.js:45
   **Risk**: Account compromise
   **Remediation**: Use AWS Secrets Manager
   
   ### 2. SQL Injection Vulnerability
   **File**: api/users.js:78
   **Risk**: Data breach
   **Remediation**: Use parameterized queries
   
   ## Dependency Vulnerabilities
   [Table of vulnerable packages]
   
   ## Secret Detection
   [List of detected secrets]
   
   ## License Compliance
   [Compliance status]
   
   ## Recommendations
   1. Implement secret management system
   2. Update vulnerable dependencies
   3. Add security headers
   4. Enable rate limiting
   5. Implement CSP
   
   ## Compliance Status
   - OWASP Top 10: ⚠️ Partial
   - PCI DSS: ❌ Non-compliant
   - GDPR: ⚠️ Review needed
   ```

2. **Generate SARIF Output**
   ```json
   {
     "version": "2.1.0",
     "runs": [{
       "tool": {
         "driver": {
           "name": "SecurityScanner",
           "version": "1.0.0"
         }
       },
       "results": [...]
     }]
   }
   ```

### Phase 10: Remediation
1. **Auto-Fix Options**
   - STOP → "Auto-fix available issues? (y/n):"
   
   **Safe Auto-Fixes:**
   - Update dependencies
   - Add security headers
   - Fix permission issues
   - Remove debug code

2. **Manual Fix Guidance**
   ```markdown
   ## Manual Fixes Required
   
   ### High Priority
   1. **Replace hardcoded secrets**
      - Move to .env file
      - Use secret management service
      - Rotate compromised credentials
   
   2. **Fix SQL injection**
      ```javascript
      // Vulnerable
      db.query(`SELECT * FROM users WHERE id = ${userId}`);
      
      // Fixed
      db.query('SELECT * FROM users WHERE id = ?', [userId]);
      ```
   ```

## Integration with Workflow

### With `/commit`
- Run before committing sensitive changes
- Block commits with critical issues
- Add security status to commit message

### With `/mr-draft`
- Include security report in MR
- Highlight security improvements
- Document remaining risks

### With `/deploy`
- Final security check before deployment
- Verify production configurations
- Check for debug flags

## Security Policies

### Severity Levels
```yaml
critical:
  - Hardcoded secrets
  - Remote code execution
  - SQL injection
  - Authentication bypass

high:
  - XSS vulnerabilities
  - Path traversal
  - Insecure deserialization
  - Outdated crypto

medium:
  - Missing security headers
  - Verbose error messages
  - Weak password policy
  - Missing rate limiting

low:
  - Code quality issues
  - Missing best practices
  - Documentation gaps
```

### Blocking Rules
```yaml
block_on:
  - critical_vulnerabilities: true
  - high_vulnerabilities: count > 5
  - secrets_detected: true
  - license_violations: true
```

## Configuration

### .claude/security-config.json
```json
{
  "scanners": {
    "semgrep": true,
    "gitleaks": true,
    "trivy": true,
    "snyk": false
  },
  "thresholds": {
    "critical": 0,
    "high": 5,
    "medium": 20
  },
  "autoFix": {
    "dependencies": true,
    "headers": true,
    "permissions": false
  },
  "ignorePaths": [
    "node_modules/",
    "test/",
    ".git/"
  ]
}
```

## Best Practices

1. **Shift Left Security**
   - Scan early in development
   - Fix issues before PR
   - Educate developers

2. **Defense in Depth**
   - Multiple scanning tools
   - Different scan types
   - Regular updates

3. **Risk Management**
   - Prioritize critical issues
   - Track security debt
   - Document exceptions

4. **Continuous Monitoring**
   - Scan on every commit
   - Monitor dependencies
   - Track CVE databases

## Notes
- Integrates with Semgrep MCP
- Supports all major languages
- Can generate SBOM
- Never ignores critical issues
- Maintains security baseline