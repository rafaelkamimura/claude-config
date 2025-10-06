# Task Initialization Command

Intelligent task initialization system with context loading, prompt optimization, and memory management.

## Purpose
Streamline task initialization by:
- Loading all relevant project context
- Optimizing task prompts for clarity and completeness
- Preventing regressions through context awareness
- Maintaining task history and memory checkpoints

## Workflow

### Phase 1: Context Loading
1. **Load Project Documentation**
   - Read project CLAUDE.md if exists: `cat CLAUDE.md 2>/dev/null || echo "No project CLAUDE.md found"`
   - Read global CLAUDE.md if exists: `cat /Users/nagawa/CLAUDE.md 2>/dev/null || echo "No global CLAUDE.md found"`
   - Read local CLAUDE.md if exists: `cat /Users/nagawa/.claude/CLAUDE.md 2>/dev/null || echo "No local CLAUDE.md found"`
   - Read README.md if exists: `cat README.md 2>/dev/null || echo "No README.md found"`
   - List documentation files: `find . -maxdepth 2 -name "*.md" -not -path "./.git/*" -not -path "./node_modules/*" | head -20`

2. **Check MCP Memory Availability**
   - Attempt to list MCP resources to check for memory tools
   - Note: Memory functionality will be used if available, otherwise proceed without it

3. **Gather Project Structure**
   - Identify project type: `ls -la | head -20`
   - Check for package.json, go.mod, requirements.txt, Cargo.toml, etc.
   - Identify test framework and build tools

### Phase 2: Prompt Collection
1. **Present Context Summary**
   - Show loaded documentation summary
   - Display project type and key technologies
   - List available MCP tools and resources

2. **STOP** → "Context loaded. Please provide your task/prompt:"
   - Wait for user to provide their task description

### Phase 3: Prompt Optimization
1. **Analyze Original Prompt** using parallel Task agents:
   - **backend-architect**: Analyze architectural implications
   - **test-automator**: Identify testing requirements
   - **code-reviewer**: Check for completeness and clarity
   - **security-auditor**: Identify security considerations

2. **Generate Optimized Prompt**
   Create enhanced prompt including:
   - Clear success criteria
   - Regression prevention checks
   - Testing requirements
   - Security considerations
   - Performance implications
   - Architecture alignment
   - Project-specific conventions from CLAUDE.md

3. **Present Optimization**
   ```markdown
   ## Original Prompt
   [user's original prompt]
   
   ## Optimized Prompt
   [enhanced prompt with all considerations]
   
   ### Success Criteria
   - [specific measurable outcomes]
   
   ### Regression Prevention
   - [checks to ensure no breaking changes]
   
   ### Testing Requirements
   - [unit, integration, e2e test requirements]
   ```

4. **STOP** → "Approve optimized prompt? (y/yes/ok to proceed, n to revise):"
   - If n: Ask for specific changes and re-optimize
   - If y/yes/ok: Proceed to Phase 4

### Phase 4: Task Tracking
1. **Create Task History Directory**
   ```bash
   mkdir -p .claude/task-history
   ```

2. **Save Task Record**
   Create `.claude/task-history/[timestamp]-[task-slug].md`:
   ```markdown
   # Task: [Task Title]
   **Date:** [ISO timestamp]
   **Project:** [current directory]
   **Status:** Started
   
   ## Original Prompt
   [original user prompt]
   
   ## Optimized Prompt
   [optimized prompt]
   
   ## Context
   - Project Type: [detected type]
   - Key Technologies: [list]
   - MCP Tools Available: [list]
   
   ## Success Criteria
   [from optimization]
   
   ## Regression Checks
   [from optimization]
   
   ## Testing Requirements
   [from optimization]
   ```

3. **Update .gitignore**
   ```bash
   grep -q "^.claude/task-history/" .gitignore || echo ".claude/task-history/" >> .gitignore
   ```

### Phase 5: Memory Checkpoint (if available)
1. **Check for MCP Memory Tools**
   - If memory tools available (create_entities, add_observations, etc.)
   
2. **Create Task Entity**
   ```json
   {
     "name": "task_[timestamp]",
     "entityType": "task",
     "observations": [
       "Project: [project name]",
       "Objective: [task summary]",
       "Date: [ISO timestamp]",
       "Technologies: [list]"
     ]
   }
   ```

3. **Create Project Entity** (if not exists)
   ```json
   {
     "name": "project_[project_name]",
     "entityType": "project",
     "observations": [
       "Path: [full path]",
       "Type: [project type]",
       "Last task: [timestamp]"
     ]
   }
   ```

4. **Create Relation**
   ```json
   {
     "from": "task_[timestamp]",
     "to": "project_[project_name]",
     "relationType": "belongs_to"
   }
   ```

### Phase 6: Execution
1. **Initialize Todo List**
   Use TodoWrite to create initial task breakdown based on optimized prompt

2. **Display Execution Plan**
   ```markdown
   ## Ready to Execute
   
   Task initialized with:
   - [X] Context loaded from [N] sources
   - [X] Prompt optimized with [N] considerations
   - [X] Task history saved to .claude/task-history/
   - [X] Memory checkpoint created (if available)
   - [X] Todo list initialized
   
   Starting execution with optimized prompt...
   ```

3. **Begin Implementation**
   - Execute the optimized prompt
   - Use specialized agents as needed
   - Track progress with TodoWrite
   - Run validation checks from success criteria

## Error Handling

### Missing Documentation
- Continue with available context
- Note missing files in task history
- Suggest creating CLAUDE.md if not present

### MCP Memory Unavailable
- Log as "Memory checkpoint skipped - MCP not available"
- Continue with file-based history only

### Prompt Rejection Loop
- After 3 rejections, offer to proceed with original prompt
- Save rejection reasons in task history

### Project Detection Failure
- Ask user to specify project type
- Update task history with manual specification

## Command Shortcuts
- `/task-init` - Start full workflow
- Context is always loaded fresh to ensure accuracy
- Previous task history can be reviewed in .claude/task-history/

## Best Practices
1. Always check for existing CLAUDE.md files
2. Respect project-specific conventions
3. Include regression prevention in every task
4. Create comprehensive test requirements
5. Document task history for future reference
6. Use memory checkpoints for cross-session continuity

## Notes
- Task history is local to each project
- Memory entities persist globally across projects
- Optimized prompts improve task success rate
- Regression checks prevent breaking changes