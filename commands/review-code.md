# Pre-Commit Code Review

AI-powered code review that checks for anti-patterns, suggests refactoring, and ensures code quality before commits.

## Purpose
- Perform comprehensive code review
- Detect anti-patterns and code smells
- Suggest refactoring opportunities
- Verify naming conventions and style
- Generate review checklist

## Workflow

### Phase 1: Review Scope
1. **STOP** → "Select review scope:"
   ```
   1. Changed files only - Review uncommitted changes
   2. Staged files - Review staged changes
   3. Last commit - Review previous commit
   4. Custom files - Specify files to review
   5. Full codebase - Complete review (slow)
   
   Choose scope (1-5):
   ```

2. **Review Focus**
   - STOP → "Review priorities? (all/security/performance/style/architecture):"
   - STOP → "Strictness level? (lenient/standard/strict):"
   - STOP → "Include refactoring suggestions? (y/n):"

### Phase 2: File Analysis
1. **Gather Changed Files**
   ```bash
   # Get changed files
   git diff --name-only HEAD
   git diff --staged --name-only
   ```

2. **Categorize by Type**
   ```javascript
   const fileCategories = {
     source: ['*.js', '*.ts', '*.py', '*.go'],
     tests: ['*.test.*', '*.spec.*'],
     config: ['*.json', '*.yml', '*.toml'],
     docs: ['*.md', '*.rst'],
     styles: ['*.css', '*.scss']
   };
   ```

### Phase 3: Agent-Based Review
Deploy specialized agents for different aspects:

1. **Code Quality Review**
   - **code-reviewer**: General code quality
   - **backend-architect**: Architecture patterns
   - **security-auditor**: Security issues
   - **performance-engineer**: Performance concerns
   - **test-automator**: Test coverage

2. **Agent Prompts**
   ```
   Review this code for:
   1. Code smells and anti-patterns
   2. SOLID principle violations
   3. Naming consistency
   4. Error handling
   5. Performance issues
   6. Security vulnerabilities
   7. Test coverage gaps
   ```

### Phase 4: Code Quality Checks

#### Clean Code Principles
```javascript
// ❌ Bad: Unclear naming
function calc(x, y) {
  return x * 0.1 + y;
}

// ✅ Good: Clear intent
function calculateTotalWithTax(price, tax) {
  const TAX_RATE = 0.1;
  return price * TAX_RATE + tax;
}
```

#### Single Responsibility
```javascript
// ❌ Bad: Multiple responsibilities
class UserService {
  getUser(id) { /* ... */ }
  sendEmail(user) { /* ... */ }
  validatePassword(password) { /* ... */ }
  logActivity(action) { /* ... */ }
}

// ✅ Good: Single responsibility
class UserService {
  getUser(id) { /* ... */ }
}
class EmailService {
  sendEmail(user) { /* ... */ }
}
```

#### DRY (Don't Repeat Yourself)
```javascript
// ❌ Bad: Duplicated logic
function calculateUserDiscount(user) {
  if (user.purchases > 10) return 0.2;
  if (user.purchases > 5) return 0.1;
  return 0;
}

function calculateProductDiscount(product) {
  if (product.sales > 10) return 0.2;
  if (product.sales > 5) return 0.1;
  return 0;
}

// ✅ Good: Reusable function
function calculateDiscount(count) {
  if (count > 10) return 0.2;
  if (count > 5) return 0.1;
  return 0;
}
```

### Phase 5: Anti-Pattern Detection

#### Code Smells
```yaml
code_smells:
  - Long Method: > 50 lines
  - Large Class: > 500 lines
  - Long Parameter List: > 4 parameters
  - Duplicate Code: Similar blocks
  - Dead Code: Unused variables/functions
  - Magic Numbers: Hardcoded values
  - God Object: Class doing everything
```

#### Common Anti-Patterns
```javascript
// ❌ Callback Hell
getData(function(a) {
  getMoreData(a, function(b) {
    getMoreData(b, function(c) {
      console.log(c);
    });
  });
});

// ✅ Use async/await
const a = await getData();
const b = await getMoreData(a);
const c = await getMoreData(b);
console.log(c);
```

### Phase 6: Security Review

#### Common Vulnerabilities
```javascript
// ❌ SQL Injection
const query = `SELECT * FROM users WHERE id = ${userId}`;

// ✅ Parameterized query
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [userId]);

// ❌ XSS
element.innerHTML = userInput;

// ✅ Safe text content
element.textContent = userInput;
```

#### Authentication Issues
```javascript
// ❌ Weak password validation
if (password.length > 5) { /* ... */ }

// ✅ Strong validation
const strongPassword = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
if (!strongPassword.test(password)) {
  throw new Error('Password must be at least 8 characters with uppercase, lowercase, number, and special character');
}
```

### Phase 7: Performance Review

#### Performance Issues
```javascript
// ❌ N+1 Query Problem
const users = await getUsers();
for (const user of users) {
  user.posts = await getPosts(user.id);  // N queries
}

// ✅ Batch loading
const users = await getUsers();
const userIds = users.map(u => u.id);
const allPosts = await getPostsByUserIds(userIds);  // 1 query
```

#### Memory Leaks
```javascript
// ❌ Event listener leak
element.addEventListener('click', handler);
// Never removed

// ✅ Proper cleanup
element.addEventListener('click', handler);
// On cleanup:
element.removeEventListener('click', handler);
```

### Phase 8: Style and Convention

#### Naming Conventions
```javascript
// ❌ Inconsistent naming
const user_name = 'John';
const lastName = 'Doe';
const AGE = 30;

// ✅ Consistent naming
const firstName = 'John';
const lastName = 'Doe';
const age = 30;
```

#### Code Formatting
```javascript
// ❌ Inconsistent formatting
function foo(){
if(x==1){return true}
else{
return false}}

// ✅ Proper formatting
function isValid(value) {
  if (value === 1) {
    return true;
  }
  return false;
}
```

### Phase 9: Review Report Generation

```markdown
# Code Review Report

## Summary
- **Files Reviewed**: 12
- **Issues Found**: 23
- **Critical**: 2
- **Warnings**: 8
- **Suggestions**: 13

## Critical Issues

### 1. SQL Injection Vulnerability
**File**: src/api/users.js:45
**Issue**: Direct string concatenation in SQL query
```javascript
const query = `SELECT * FROM users WHERE email = '${email}'`;
```
**Fix**:
```javascript
const query = 'SELECT * FROM users WHERE email = ?';
db.query(query, [email]);
```

### 2. Exposed API Key
**File**: src/config.js:12
**Issue**: Hardcoded API key in source
```javascript
const API_KEY = 'sk-1234567890abcdef';
```
**Fix**: Move to environment variable

## Code Quality Issues

### Long Method
**File**: src/services/payment.js:78-145
**Issue**: Method processPayment has 67 lines
**Suggestion**: Extract to smaller functions:
- validatePaymentData()
- calculateFees()
- processTransaction()
- sendConfirmation()

### Duplicate Code
**Files**: src/utils/validate.js, src/helpers/check.js
**Issue**: Similar validation logic in 3 places
**Suggestion**: Create shared validation module

## Performance Concerns

### N+1 Query
**File**: src/controllers/posts.js:34
**Issue**: Loading comments in loop
**Impact**: 50+ database queries for single page
**Fix**: Use JOIN or batch loading

## Style Guide Violations

### Naming Convention
- Variable `XMLHttpRequest` should be `xmlHttpRequest`
- Function `Getuser` should be `getUser`
- Constant `api_key` should be `API_KEY`

## Test Coverage

### Missing Tests
- PaymentService.processRefund() - 0% coverage
- UserController.deleteAccount() - 0% coverage
- EmailService.sendBulk() - 45% coverage

## Refactoring Opportunities

### 1. Extract Method
```javascript
// Current: 45-line validation block
// Suggested: extractValidation() method
```

### 2. Replace Magic Numbers
```javascript
// Current: if (retries > 3)
// Suggested: const MAX_RETRIES = 3;
```

## Security Checklist
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] SQL injection protection
- [ ] XSS prevention
- [ ] CSRF tokens used
- [ ] Authentication required
- [ ] Authorization checked
- [ ] Rate limiting implemented

## Approval Checklist
- [ ] Code follows style guide
- [ ] Tests are passing
- [ ] Documentation updated
- [ ] No console.logs
- [ ] Error handling complete
- [ ] Performance acceptable
- [ ] Security reviewed
- [ ] Accessibility considered
```

### Phase 10: Auto-Fix Suggestions

1. **Safe Auto-Fixes**
   ```bash
   # Format code
   prettier --write .
   
   # Fix linting issues
   eslint --fix .
   
   # Remove unused imports
   ```

2. **Refactoring Suggestions**
   ```javascript
   // Extract constant
   - if (age > 18)
   + const ADULT_AGE = 18;
   + if (age > ADULT_AGE)
   
   // Use optional chaining
   - if (user && user.profile && user.profile.name)
   + if (user?.profile?.name)
   ```

## Review Metrics

### Code Complexity
```yaml
cyclomatic_complexity:
  low: < 5
  medium: 5-10
  high: > 10
  
cognitive_complexity:
  simple: < 10
  moderate: 10-20
  complex: > 20
```

### Maintainability Index
```
MI = 171 - 5.2 * ln(V) - 0.23 * C - 16.2 * ln(L)
Where:
  V = Halstead Volume
  C = Cyclomatic Complexity
  L = Lines of Code
```

## Integration

### With `/commit`
- Runs automatically before commit
- Blocks commit on critical issues
- Adds review status to commit message

### With `/test-suite`
- Suggests tests for uncovered code
- Validates test quality

### With `/tech-debt`
- Tracks code quality over time
- Identifies areas needing refactoring

## Configuration

### .claude/review-config.json
```json
{
  "rules": {
    "maxLineLength": 100,
    "maxFileLength": 500,
    "maxFunctionLength": 50,
    "maxComplexity": 10
  },
  "ignore": [
    "node_modules/**",
    "dist/**",
    "*.min.js"
  ],
  "autoFix": {
    "formatting": true,
    "imports": true,
    "naming": false
  },
  "severity": {
    "security": "error",
    "performance": "warning",
    "style": "info"
  }
}
```

## Best Practices

1. **Review Early and Often**
   - Review before commit
   - Small, focused reviews
   - Regular refactoring

2. **Focus on Important Issues**
   - Security first
   - Then correctness
   - Then performance
   - Finally style

3. **Constructive Feedback**
   - Explain why
   - Provide examples
   - Suggest solutions

## Notes
- Uses multiple specialized agents
- Integrates with linting tools
- Can auto-fix simple issues
- Generates actionable reports
- Never ignores security issues