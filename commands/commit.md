# Smart Git Commit Command

Intelligent git commit system that stages only task-related changes and generates meaningful commit messages without AI tool references.

## Purpose
- Stage only files related to the current task
- Generate professional commit messages
- Exclude any mention of AI/agent tools
- Maintain clean git history

## Workflow

### Phase 1: Task Context Discovery
1. **Check for Task History**
   ```bash
   # Find most recent task file
   task_file=$(ls -t .claude/task-history/*.md 2>/dev/null | head -1)
   ```
   - If no task history found: STOP → "No task history found. Use /task-init first or specify files manually."

2. **Extract Task Information**
   - Parse task file for:
     - Task title/objective
     - Files mentioned in optimized prompt
     - Success criteria
     - Technologies involved

### Phase 2: Git Status Analysis
1. **Check Repository Status**
   ```bash
   git status --porcelain
   ```
   
2. **Categorize Changes**
   - Modified files (M)
   - Added files (A, ??)
   - Deleted files (D)
   - Renamed files (R)

3. **Identify Task-Related Files**
   Using task context, identify files that:
   - Match file patterns from task description
   - Are in directories mentioned in task
   - Match technology/framework patterns from task
   - Were created/modified after task start time

### Phase 3: Selective Staging
1. **Present Changes for Review**
   ```markdown
   ## Task: [Task Title]
   
   ### Definitely Related (will stage):
   - file1.js (modified) - implements feature X
   - file2.test.js (added) - tests for feature X
   
   ### Possibly Related (confirm):
   - config.json (modified) - may contain task settings
   - README.md (modified) - may document task changes
   
   ### Unrelated (will skip):
   - .env (modified) - local environment changes
   - debug.log (added) - temporary debug file
   ```

2. **STOP** → "Review staging plan. Adjust? (y to modify, n to proceed):"
   - If y: Allow user to specify which files to include/exclude
   - If n: Proceed with staging

3. **Stage Selected Files**
   ```bash
   # Stage only task-related files
   git add [selected files]
   ```

### Phase 4: Commit Message Generation
1. **Analyze Changes for Message**
   Use Task agents to analyze staged changes:
   - What functionality was added/modified/fixed
   - What problem was solved
   - What improvement was made

2. **Generate Commit Message**
   Format:
   ```
   [type]: [concise description]

   [optional body with details]
   
   [optional footer with references]
   ```
   
   Types:
   - `feat`: New feature
   - `fix`: Bug fix
   - `docs`: Documentation only
   - `style`: Formatting, missing semicolons, etc.
   - `refactor`: Code change that neither fixes a bug nor adds a feature
   - `perf`: Performance improvement
   - `test`: Adding missing tests
   - `chore`: Changes to build process or auxiliary tools

3. **Clean Message**
   Remove any references to:
   - Claude, ChatGPT, Copilot, or any AI
   - Agents, automation, or AI-assistance
   - Generated code or automated changes
   - Task-init or command system

4. **Present Commit Message**
   ```markdown
   ## Proposed Commit Message:
   ```
   [generated message]
   ```
   ```

5. **STOP** → "Use this commit message? (y/yes to commit, n to edit, abort to cancel):"
   - If n: STOP → "Enter your commit message:"
   - If abort: Unstage files and exit
   - If y/yes: Proceed to commit

### Phase 5: Commit Execution
1. **Create Commit**
   ```bash
   git commit -m "[final message]"
   ```

2. **Update Task History**
   Append to task file:
   ```markdown
   ## Commits
   - [commit hash]: [commit message] ([timestamp])
   ```

3. **Show Result**
   ```bash
   git log --oneline -1
   git status
   ```

## Smart Detection Rules

### File Pattern Matching
Automatically detect task-related files based on:

1. **Direct Mentions**
   - Files explicitly mentioned in task description
   - Files in paths specified in task

2. **Technology Patterns**
   - React task → *.jsx, *.tsx, components/
   - API task → controllers/, routes/, *.api.*
   - Database task → migrations/, models/, *.sql
   - Testing task → *.test.*, *.spec.*, __tests__/
   - Documentation task → *.md, docs/

3. **Temporal Correlation**
   - Files modified after task start time
   - Files in same directory as other task files

4. **Dependency Chain**
   - Files that import/require task files
   - Files imported by task files
   - Config files affecting task files

### Exclusion Rules
Always exclude:
- `.env`, `.env.local`, `.env.*`
- `*.log`, `*.tmp`, `*.cache`
- `.DS_Store`, `Thumbs.db`
- `node_modules/`, `vendor/`, `target/`
- Build outputs unless specifically part of task
- Personal IDE settings (`.vscode/settings.json`, `.idea/`)

## Error Handling

### No Git Repository
- Check if in git repository
- Suggest `git init` if appropriate
- Exit gracefully

### No Changes to Commit
- Show current status
- Suggest checking task completion
- Exit gracefully

### Merge Conflicts
- Detect merge conflict markers
- Warn user to resolve conflicts first
- Provide guidance on conflict resolution

### Task File Issues
- If no task history: Offer to proceed with manual file selection
- If corrupt task file: Use fallback to git status only
- If multiple active tasks: Ask which task to commit for

## Command Options

### Basic Usage
```
/commit
```
Runs full smart commit workflow

### Manual Override
If no task context or user wants manual control:
1. STOP → "No task context. Enter files to stage (space-separated) or 'all' for git add -A:"
2. STOP → "Enter commit message:"
3. Proceed with standard commit

## Integration with /task-init

### Task Continuity
- Reads task context from `.claude/task-history/`
- Uses task success criteria to validate changes
- Links commits back to original task

### Workflow Connection
```
/task-init → [work on task] → /commit → [repeat as needed]
```

## Best Practices

1. **One Task, One Commit**
   - Keep commits focused on single task
   - Use multiple commits for complex tasks
   - Each commit should be independently valid

2. **Message Quality**
   - First line: 50 chars or less
   - Use imperative mood ("add" not "added")
   - Explain what and why, not how

3. **Clean History**
   - No WIP commits
   - No debugging artifacts
   - No commented code

## Notes
- Commit messages never mention AI assistance
- Task history helps maintain commit context
- Smart staging prevents accidental commits
- Works with any git workflow (feature branches, trunk-based, etc.)