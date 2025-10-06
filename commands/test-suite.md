# Test Suite Runner

Automated testing orchestrator that intelligently runs tests based on changed files, generates coverage reports, and can create missing tests.

## Purpose
- Run appropriate tests based on file changes
- Generate coverage reports with visual diffs
- Auto-fix simple test failures
- Create missing tests using specialized agents
- Ensure quality before commits

## Workflow

### Phase 1: Test Discovery
1. **Detect Test Framework**
   ```bash
   # Check for test frameworks
   framework=""
   [ -f "package.json" ] && grep -q "jest\|mocha\|vitest\|cypress" package.json && framework="js"
   [ -f "pytest.ini" ] || [ -f "setup.cfg" ] && framework="python"
   [ -f "go.mod" ] && framework="go"
   [ -f "Cargo.toml" ] && framework="rust"
   ```

2. **Find Test Files**
   ```bash
   # Locate test files
   find . -name "*.test.*" -o -name "*.spec.*" -o -name "*_test.*" | head -20
   ```

3. **Analyze Changed Files**
   ```bash
   # Get modified files since last commit
   git diff --name-only HEAD
   git diff --staged --name-only
   ```

### Phase 2: Test Strategy Selection
1. **STOP** → "Select test scope:"
   ```
   1. Changed files only - Test files related to modifications
   2. Unit tests - Fast, isolated component tests
   3. Integration tests - Component interaction tests
   4. E2E tests - Full user workflow tests
   5. Full suite - All available tests
   6. Custom pattern - Specify test pattern
   
   Choose scope (1-6):
   ```

2. **Test Options**
   - STOP → "Enable coverage report? (y/n):"
   - STOP → "Auto-fix simple failures? (y/n):"
   - STOP → "Create missing tests? (y/n):"
   - STOP → "Fail on coverage decrease? (y/n):"

### Phase 3: Test Execution
1. **Run Tests by Framework**
   
   **JavaScript/TypeScript:**
   ```bash
   # Jest
   npm test -- --coverage --watchAll=false
   
   # Vitest
   npm run test -- --coverage --run
   
   # Mocha
   npm test -- --reporter spec
   
   # Cypress (E2E)
   npx cypress run
   ```
   
   **Python:**
   ```bash
   # Pytest
   pytest --cov=. --cov-report=html --cov-report=term
   
   # Unittest
   python -m unittest discover
   ```
   
   **Go:**
   ```bash
   go test -v -cover ./...
   go test -race -coverprofile=coverage.out ./...
   ```
   
   **Rust:**
   ```bash
   cargo test --all
   cargo tarpaulin --out Html
   ```

2. **Capture Test Results**
   - Parse test output
   - Extract failed tests
   - Calculate coverage metrics
   - Identify flaky tests

### Phase 4: Intelligent Test Analysis
1. **Deploy Analysis Agents**
   
   **For Failed Tests:**
   - **debugger**: Analyze failure reasons
   - **test-automator**: Suggest fixes
   
   **For Missing Tests:**
   - **test-automator**: Generate test cases
   - **backend-architect**: Validate test logic
   
   **For Coverage Gaps:**
   - **code-reviewer**: Identify critical uncovered code
   - **test-automator**: Create coverage tests

2. **Auto-Fix Attempts**
   Common fixes:
   - Update snapshots
   - Fix import paths
   - Update mocked data
   - Adjust timeouts
   - Fix async handling

### Phase 5: Test Generation
If missing tests detected:

1. **Analyze Untested Code**
   ```javascript
   // Example: Function without tests
   function calculateDiscount(price, percentage) {
     if (percentage < 0 || percentage > 100) {
       throw new Error('Invalid percentage');
     }
     return price * (1 - percentage / 100);
   }
   ```

2. **Generate Test Cases**
   ```javascript
   // Generated test
   describe('calculateDiscount', () => {
     test('applies correct discount', () => {
       expect(calculateDiscount(100, 20)).toBe(80);
     });
     
     test('handles zero discount', () => {
       expect(calculateDiscount(100, 0)).toBe(100);
     });
     
     test('throws on invalid percentage', () => {
       expect(() => calculateDiscount(100, -10)).toThrow();
       expect(() => calculateDiscount(100, 110)).toThrow();
     });
   });
   ```

3. **Review Generated Tests**
   - STOP → "Review generated tests. Accept? (y/n/edit):"

### Phase 6: Coverage Report
1. **Generate Visual Report**
   ```markdown
   ## Test Coverage Report
   
   ### Summary
   - **Statements**: 85.2% (1247/1463)
   - **Branches**: 78.4% (421/537)
   - **Functions**: 91.3% (189/207)
   - **Lines**: 86.1% (1198/1391)
   
   ### Coverage Change
   📈 +2.3% from previous run
   
   ### Uncovered Files
   | File | Coverage | Missing Lines |
   |------|----------|---------------|
   | auth.service.ts | 67% | 45-52, 78-81 |
   | payment.processor.ts | 72% | 123-145 |
   
   ### Critical Gaps
   - Authentication error handling (auth.service.ts:45-52)
   - Payment retry logic (payment.processor.ts:123-145)
   ```

2. **Coverage Diff**
   ```diff
   File: src/services/user.service.ts
   - Coverage: 78% → 85% (+7%)
   + Lines covered: 45-67 (new)
   - Uncovered: 89-92 (error handling)
   ```

### Phase 7: Quality Gates
1. **Check Test Results**
   ```yaml
   quality_gates:
     tests_passing: true
     coverage_threshold: 80%
     no_console_logs: true
     no_skip_tests: true
     performance_benchmarks: pass
   ```

2. **Generate Report**
   ```markdown
   ## Test Suite Results
   
   ✅ **Passed**: 156/162 tests
   ❌ **Failed**: 6 tests
   ⏭️ **Skipped**: 3 tests
   
   ### Failed Tests
   1. UserService › should handle invalid email
      - Expected: ValidationError
      - Received: undefined
   
   ### Recommendations
   - Fix authentication tests before commit
   - Add tests for new payment module
   - Remove skipped tests or fix them
   ```

3. **Decision Point**
   - STOP → "Tests failed. Options: (fix/ignore/debug):"
   - If fix: Auto-fix or manual intervention
   - If debug: Launch `/debug-assistant`
   - If ignore: Document reason

## Test Patterns

### Unit Test Detection
```javascript
// Matches: *.test.js, *.spec.ts, *.unit.js
const unitTestPattern = /\.(test|spec|unit)\.(js|ts|jsx|tsx)$/;
```

### Integration Test Detection
```javascript
// Matches: *.integration.js, *.int.test.js
const integrationPattern = /\.(integration|int\.test)\.(js|ts)$/;
```

### E2E Test Detection
```javascript
// Matches: *.e2e.js, cypress/*, playwright/*
const e2ePattern = /\.(e2e|cy)\.(js|ts)$|cypress|playwright/;
```

## Smart Test Selection

### Changed File Mapping
```javascript
// Map source files to their tests
const testMapping = {
  'src/services/user.service.ts': [
    'tests/unit/user.service.test.ts',
    'tests/integration/user.api.test.ts'
  ],
  'src/api/auth.controller.ts': [
    'tests/unit/auth.controller.test.ts',
    'tests/e2e/auth.e2e.ts'
  ]
};
```

### Dependency Analysis
- Detect which files import changed modules
- Run tests for dependent components
- Skip unrelated test suites

## Auto-Fix Strategies

### Snapshot Updates
```bash
# Jest
npm test -- -u

# Vitest
npm test -- --update
```

### Async Timeouts
```javascript
// Increase timeout for slow tests
jest.setTimeout(10000);
```

### Mock Updates
```javascript
// Update mocked responses
jest.mock('./api', () => ({
  fetchUser: jest.fn(() => Promise.resolve(updatedMockData))
}));
```

## Integration Points

### With `/commit`
- Runs automatically before commit
- Blocks commit on test failure (configurable)
- Includes test results in commit message

### With `/review-code`
- Suggests tests for new code
- Reviews test quality
- Identifies test anti-patterns

### With `/security-scan`
- Runs security tests
- Validates input sanitization
- Tests authentication/authorization

## Error Handling

### Test Timeout
- Kill long-running tests
- Report timeout location
- Suggest timeout increase

### Missing Dependencies
- Detect missing test packages
- Offer to install them
- Update package.json

### Flaky Tests
- Track intermittent failures
- Retry flaky tests (configurable)
- Report flakiness patterns

## Configuration

### .claude/test-config.json
```json
{
  "framework": "jest",
  "coverage": {
    "threshold": 80,
    "failOnDecrease": true
  },
  "autoFix": {
    "snapshots": true,
    "imports": true,
    "timeouts": false
  },
  "testPattern": "**/*.test.ts",
  "excludePattern": "**/node_modules/**",
  "parallel": true,
  "maxWorkers": 4
}
```

## Best Practices

1. **Test Pyramid**
   - Many unit tests (fast)
   - Some integration tests (moderate)
   - Few E2E tests (slow)

2. **Coverage Goals**
   - Aim for 80%+ coverage
   - Focus on critical paths
   - Don't chase 100%

3. **Test Quality**
   - Descriptive test names
   - Single assertion per test
   - Independent test cases

4. **Performance**
   - Run tests in parallel
   - Use test doubles
   - Minimize I/O operations

## Notes
- Integrates with all major test frameworks
- Supports multiple languages
- Can generate tests using AI
- Never commits failing tests
- Maintains test history for trend analysis