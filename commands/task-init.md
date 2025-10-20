# Task Initialization Command

Intelligent task initialization system with context loading, prompt optimization, and memory management.

## Purpose
Streamline task initialization by:
- Loading all relevant project context
- Optimizing task prompts for clarity and completeness
- Preventing regressions through context awareness
- Maintaining task history and memory checkpoints

## Execution Steps

### Step 1: Load Project Context

Use Read tool to load these files (if they don't exist, continue without them):
1. Read `./CLAUDE.md` (project-specific instructions)
2. Read `/Users/nagawa/CLAUDE.md` (global instructions)
3. Read `/Users/nagawa/.claude/CLAUDE.md` (local instructions)
4. Read `./README.md` (project overview)

Use Glob tool to find additional documentation:
- Pattern: `*.md`
- Limit to 20 results

Use Bash tool to identify project type:
- Command: `ls -la | head -20`
- Description: "List files to identify project type"
- Look for: package.json, go.mod, requirements.txt, Cargo.toml, pyproject.toml

### Step 2: Present Context and Get Task

Output a context summary showing:
- Project type detected (if any)
- Documentation files found
- Key technologies identified

Then output: "Context loaded. Please provide your task/prompt:"

WAIT for user's next message containing their task description.

### Step 3: Analyze Task with Specialized Agents

CRITICAL: Use Task tool to launch ALL 4 agents IN PARALLEL (send a single message with 4 Task tool invocations):

1. Task tool call:
   - subagent_type: "backend-architect"
   - prompt: "Analyze the architectural implications and requirements for this task: [insert user's task here]. Identify architecture patterns, dependencies, and structural considerations."

2. Task tool call:
   - subagent_type: "test-automator"
   - prompt: "Identify comprehensive testing requirements for this task: [insert user's task here]. Specify what unit tests, integration tests, and E2E tests are needed."

3. Task tool call:
   - subagent_type: "code-reviewer"
   - prompt: "Review this task description for completeness and clarity: [insert user's task here]. Identify what additional details or considerations should be included."

4. Task tool call:
   - subagent_type: "security-auditor"
   - prompt: "Identify security considerations and requirements for this task: [insert user's task here]. Specify what security measures, validations, or checks are needed."

Wait for all 4 agents to complete before proceeding.

### Step 4: Generate and Present Optimized Prompt

Based on all agent responses, create an enhanced prompt that includes:
- Clear objective from original task
- Architecture considerations from backend-architect
- Testing requirements from test-automator
- Clarity improvements from code-reviewer
- Security requirements from security-auditor

Format and output as:
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

### Security Considerations
- [security measures needed]
```

Then output: "Review the optimized prompt above. Approve? (Reply 'yes' to proceed, 'no' to revise):"

WAIT for user approval.

### Step 5: Create Task History

If user approves (responds with yes/y/ok):

1. Use Bash tool:
   - Command: `mkdir -p .claude/task-history`
   - Description: "Create task history directory"

2. Use Write tool to create file at `.claude/task-history/[timestamp]-[slug].md` with content:
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

   ## Success Criteria
   [from optimization]

   ## Regression Checks
   [from optimization]

   ## Testing Requirements
   [from optimization]
   ```

3. Use Bash tool:
   - Command: `grep -q "^.claude/task-history/" .gitignore || echo ".claude/task-history/" >> .gitignore`
   - Description: "Add task history to gitignore"

### Step 6: Initialize Todo List

Use TodoWrite tool to create initial task breakdown based on the optimized prompt.
Break the task into 3-7 concrete, actionable steps with:
- content: Imperative form (e.g., "Implement user authentication")
- activeForm: Present continuous (e.g., "Implementing user authentication")
- status: "pending" for all items initially

### Step 7: Display Execution Summary

Output:
```markdown
## Task Initialized Successfully

- Context loaded from [N] sources
- Prompt optimized with agent analysis
- Task history saved to .claude/task-history/[filename]
- Todo list initialized with [N] items

Starting execution with optimized prompt...
```

### Step 8: Begin Implementation

Execute the optimized prompt by:
1. Mark the first todo item as "in_progress" using TodoWrite
2. Use appropriate specialized agents as needed (via Task tool)
3. Update todo status as you complete each item using TodoWrite
4. Run validation checks from success criteria
5. Follow the testing requirements specified
6. Apply security considerations identified

## Error Handling

If documentation files don't exist:
- Continue with available context
- Note missing files when presenting context summary
- Suggest creating CLAUDE.md if not present

If user rejects optimized prompt 3 times:
- Offer to proceed with original prompt
- Ask what specific concerns they have

If agents fail to respond:
- Proceed with partial optimization
- Note which agent failed in optimized prompt

If no git repository exists:
- Skip gitignore update
- Skip task history creation (or create without git integration)
- Continue with in-memory tracking only

## Notes

- Task history is saved locally to each project
- Optimized prompts improve task success rate by including all considerations upfront
- Always use TodoWrite to track progress through implementation
- Context is loaded fresh each time to ensure accuracy