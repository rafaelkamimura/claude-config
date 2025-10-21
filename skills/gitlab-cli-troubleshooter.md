# GitLab CLI Troubleshooter

Comprehensive troubleshooting and configuration skill for GitLab CLI (`glab`) integration issues, with focus on custom GitLab instances and shell function setup.

## Purpose

Diagnose and fix common `glab` configuration problems including authentication issues, project detection failures, `-R` flag incompatibilities, and shell function conflicts. Automatically sets up smart project-aware shell functions.

## When to Use This Skill

Use this skill when experiencing:
- `glab mr list` returning 404 errors
- `-R` flag not recognizing project paths
- "command not found" errors for custom glab aliases
- Authentication or permission issues
- Project auto-detection failures
- Shell function/alias conflicts

## Prerequisites

Before running this skill, ensure:
1. `glab` CLI is installed (`glab version` works)
2. GitLab instance is accessible
3. You have a Personal Access Token (PAT)
4. `jq` is installed for JSON processing
5. You're using zsh or bash shell

## Execution Steps

### Step 1: Verify glab Installation and Version

Use Bash tool with command:
```bash
glab version && glab auth status
```
Description: "Check glab installation and authentication status"

Expected output should show:
- Version (1.70+)
- Logged in status
- API/GraphQL endpoints
- Protocol configuration

If not installed:
- macOS: `brew install glab`
- Linux: See https://gitlab.com/gitlab-org/cli/-/releases

### Step 2: Test GitLab API Access

Use Bash tool with command:
```bash
glab api projects --paginate 2>&1 | head -50
```
Description: "Test GitLab API access and list accessible projects"

**Success indicators:**
- Returns JSON array of projects
- No authentication errors
- Shows projects you have access to

**If fails:**
- Re-run authentication: `glab auth login --hostname YOUR_GITLAB_HOST`
- Check PAT has `api` scope
- Verify network connectivity

### Step 3: Identify Project Path and ID

Use Bash tool with command:
```bash
cd "$(git rev-parse --show-toplevel)" && \
git remote get-url origin && \
echo "" && \
glab api projects --paginate | jq -r '.[] | select(.name | contains("YOUR_PROJECT_NAME")) | {id, path_with_namespace, ssh_url_to_repo}'
```
Description: "Extract git remote URL and find matching GitLab project"

Replace `YOUR_PROJECT_NAME` with actual project name (e.g., "sisjur-backend").

**Note the following:**
- `id`: Numeric project ID (e.g., 46)
- `path_with_namespace`: Full path (e.g., "novacap/sisjur-backend")
- Git remote URL format (ssh://, git@, https://)

### Step 4: Test Direct API Access (Workaround)

The `-R` flag often fails on custom GitLab instances. Test direct API access:

Use Bash tool with command:
```bash
PROJECT_ID=46  # Replace with your project ID from Step 3
glab api "projects/${PROJECT_ID}/merge_requests" | jq -r '.[] | "\(.iid)\t\(.title)\t\(.state)"' | head -5
```
Description: "Test direct API access to merge requests"

**If this works but `glab mr list -R` doesn't:**
- Your instance doesn't support `-R` properly
- Proceed with shell function workaround (Step 5)

**If this also fails (404):**
- Check project ID is correct
- Verify PAT has access to this project
- Check project visibility settings

### Step 5: Diagnose Shell Function Conflicts

Use Bash tool with command:
```bash
type gli glv gln 2>&1
alias | grep "^gl"
```
Description: "Check for existing glab aliases and functions"

**Common conflicts:**
- Existing `glp` alias (common git log alias)
- Functions defined but not loading (wrong shell file)
- Duplicate definitions in multiple rc files

### Step 6: Create Smart GitLab Functions

Use Bash tool with command:
```bash
cat << 'FUNCTION_TEST' > /tmp/glab_functions_test.zsh
# Test function extraction
_test_extract_path() {
    local git_url="ssh://git@git.example.com:2424/owner/repo.git"
    git_url="${git_url%.git}"

    if [[ "$git_url" =~ "ssh://" ]]; then
        project_path="${git_url##*/}"
        parent_path="${git_url%/*}"
        project_path="${parent_path##*/}/${project_path}"
        echo "Extracted: $project_path"
    fi
}
_test_extract_path
FUNCTION_TEST

zsh /tmp/glab_functions_test.zsh
```
Description: "Test project path extraction logic"

Expected: "Extracted: owner/repo"

### Step 7: Check Syntax of User's .zshrc

Use Bash tool with command:
```bash
zsh -n ~/.zshrc 2>&1 || echo "Syntax errors found above"
```
Description: "Validate .zshrc syntax for errors"

**If syntax errors found:**
1. Note the line number
2. Use Read tool to examine that section
3. Common issues:
   - Unclosed functions (missing `}`)
   - Orphaned code fragments
   - Duplicate function definitions

### Step 8: Install Smart glab Functions

Output the following plan to user:

```markdown
## GitLab CLI Smart Functions Installation

I'll add smart glab functions to your `~/.zshrc` that:
- Auto-detect project ID from git remote
- Cache project IDs for 60 minutes (performance)
- Work around `-R` flag issues
- Provide formatted output

### Functions to add:
- `gli` - List merge requests
- `glv <id>` - View MR details
- `gln <id> "message"` - Add note to MR
- `glapi <endpoint>` - Direct API access

### Installation steps:
1. Backup current .zshrc
2. Add helper function `_glab_get_project_id()`
3. Add user-facing functions
4. Handle conflicts (rename `glp` to `glpipe`)
5. Validate syntax
6. Test in new shell

Proceed? (y/n)
```

WAIT for user confirmation.

### Step 9: Backup and Install Functions

If user confirms, use Write tool to append to `~/.zshrc`:

```zsh
# GitLab CLI (glab) - Smart project detection
# Automatically detects GitLab project ID from git remote URL
_glab_get_project_id() {
    local git_url=$(git remote get-url origin 2>/dev/null)
    if [[ -z "$git_url" ]]; then
        echo "Error: Not in a git repository" >&2
        return 1
    fi

    # Remove .git suffix
    git_url="${git_url%.git}"

    # Extract project path based on URL format
    local project_path=""

    if [[ "$git_url" =~ "ssh://" ]]; then
        # ssh://git@host:port/path/project -> path/project
        project_path="${git_url##*/}"
        local parent_path="${git_url%/*}"
        project_path="${parent_path##*/}/${project_path}"
    elif [[ "$git_url" =~ "git@" ]]; then
        # git@host:path/project -> path/project
        project_path="${git_url##*:}"
    elif [[ "$git_url" =~ "https://" || "$git_url" =~ "http://" ]]; then
        # https://host/path/project -> path/project
        project_path="${git_url##*/}"
        local parent_path="${git_url%/*}"
        project_path="${parent_path##*/}/${project_path}"
    fi

    if [[ -z "$project_path" ]]; then
        echo "Error: Could not extract project path from git remote" >&2
        return 1
    fi

    # Query GitLab API to get project ID (cached for performance)
    local cache_file="/tmp/glab_project_id_${project_path//\//_}"
    if [[ -f "$cache_file" ]] && [[ $(find "$cache_file" -mmin -60 2>/dev/null) ]]; then
        cat "$cache_file"
        return 0
    fi

    local project_id=$(glab api projects --paginate 2>/dev/null | jq -r ".[] | select(.path_with_namespace == \"$project_path\") | .id" | head -1)

    if [[ -n "$project_id" ]]; then
        echo "$project_id" > "$cache_file"
        echo "$project_id"
        return 0
    else
        echo "Error: Could not find project ID for $project_path" >&2
        return 1
    fi
}

# Smart glab functions using API directly (workaround for -R flag issues)
gli() {
    local project_id=$(_glab_get_project_id)
    [[ $? -eq 0 ]] && glab api "projects/${project_id}/merge_requests" "$@" | jq -r '.[] | "\(.iid)\t\(.title)\t\(.source_branch)\t\(.state)"'
}

glv() {
    local project_id=$(_glab_get_project_id)
    local mr_id="$1"
    [[ $? -eq 0 && -n "$mr_id" ]] && glab api "projects/${project_id}/merge_requests/${mr_id}"
}

gln() {
    local project_id=$(_glab_get_project_id)
    local mr_id="$1"
    shift
    [[ $? -eq 0 && -n "$mr_id" ]] && glab api "projects/${project_id}/merge_requests/${mr_id}/notes" -f body="$*"
}

glapi() {
    local project_id=$(_glab_get_project_id)
    [[ $? -eq 0 ]] && glab api "projects/${project_id}$1" "${@:2}"
}
```

**Important:** Handle existing conflicts:
- If `glp` alias exists, rename new function to `glpipe`
- Remove any duplicate glab function blocks
- Clean up orphaned code fragments

### Step 10: Validate Installation

Use Bash tool with command:
```bash
# Test in a fresh shell
zsh -c 'source ~/.zshrc && cd ~/path/to/git/repo && type gli && gli' 2>&1 | head -10
```
Description: "Test glab functions in fresh shell"

**Success indicators:**
- `type gli` shows function definition
- `gli` returns formatted MR list
- No error messages

### Step 11: Performance Verification

Use Bash tool with command:
```bash
time zsh -c 'source ~/.zshrc && cd ~/path/to/git/repo && gli > /dev/null'
```
Description: "Measure glab function performance"

**Expected:**
- First run: 2-5 seconds (API call)
- Subsequent runs (within 60min): < 0.5 seconds (cached)

## Common Issues and Solutions

### Issue 1: "404 Not Found" with `-R` flag

**Symptom:**
```bash
glab mr list -R novacap/sisjur-backend
ERROR: 404 Not Found
```

**Root Cause:**
Custom GitLab instances with non-standard configurations don't support `-R` flag properly.

**Solution:**
Use direct API access instead (functions from Step 9).

**Test:**
```bash
glab api projects/46/merge_requests  # Works
glab mr list -R novacap/sisjur-backend  # Fails
```

### Issue 2: Function not found after sourcing .zshrc

**Symptom:**
```bash
source ~/.zshrc
gli
zsh: command not found: gli
```

**Root Causes:**
1. Alias conflicts (existing `gli` alias blocks function)
2. Syntax errors preventing function definition
3. Wrong shell (bash vs zsh)

**Solutions:**
```bash
# Check for conflicts
alias | grep gli
type gli

# Remove conflicting alias
unalias gli 2>/dev/null

# Verify syntax
zsh -n ~/.zshrc

# Open new shell instead of sourcing
exec zsh
```

### Issue 3: "parse error near `})`"

**Symptom:**
```bash
source ~/.zshrc
/Users/user/.zshrc:217: parse error near `}'
```

**Root Cause:**
Duplicate or incomplete function definitions.

**Solution:**
1. Read .zshrc around line 217
2. Look for:
   - Orphaned `}` without opening `{`
   - Function body without declaration (`function_name()`)
   - Duplicate glab function blocks
3. Remove duplicates and fragments

### Issue 4: Slow performance (every call takes 3+ seconds)

**Symptom:**
Each `gli` call takes multiple seconds.

**Root Cause:**
Cache not working or being cleared.

**Solutions:**
```bash
# Check cache
ls -lah /tmp/glab_project_id_*

# Verify cache is readable
cat /tmp/glab_project_id_novacap_sisjur-backend

# Manual cache creation
echo "46" > /tmp/glab_project_id_novacap_sisjur-backend

# Check find command works
find /tmp/glab_project_id_novacap_sisjur-backend -mmin -60
```

### Issue 5: PAT authentication failures

**Symptom:**
```bash
glab api projects
ERROR: 401 Unauthorized
```

**Root Cause:**
PAT missing or lacks required scopes.

**Required Scopes:**
- `api` (full API access) - **REQUIRED**
- `read_api` (optional, redundant with `api`)
- `read_user` (optional, for user info)

**Solution:**
1. Go to GitLab → Settings → Access Tokens
2. Create new PAT with `api` scope
3. Re-authenticate:
   ```bash
   glab auth login --hostname git.v2solucoes.tec.br
   ```
4. Test:
   ```bash
   glab auth status
   glab api projects | jq '.[0].name'
   ```

### Issue 6: Project ID not found

**Symptom:**
```bash
gli
Error: Could not find project ID for novacap/sisjur-backend
```

**Root Causes:**
1. Project doesn't exist in accessible projects
2. PAT lacks permissions
3. Project path extracted incorrectly

**Solutions:**
```bash
# List all accessible projects
glab api projects --paginate | jq -r '.[] | .path_with_namespace' | grep sisjur

# Check path extraction
git remote get-url origin

# Manual override (temporary)
export GLAB_PROJECT_ID=46
gli() { glab api "projects/${GLAB_PROJECT_ID}/merge_requests" | jq -r '.[] | "\(.iid)\t\(.title)\t\(.state)"'; }
```

## Testing Checklist

After installation, verify:

- [ ] `glab version` shows version 1.70+
- [ ] `glab auth status` shows logged in
- [ ] `glab api projects` returns project list
- [ ] `type gli` shows function definition
- [ ] `gli` returns formatted MR list (in git repo)
- [ ] Second `gli` call is faster (cache working)
- [ ] `glv 212` shows MR #212 details
- [ ] `gln 212 "test"` adds comment to MR #212
- [ ] Functions work in new terminal window
- [ ] No conflicts with existing aliases
- [ ] `.zshrc` has no syntax errors

## Advanced Customization

### Add More glab Functions

```zsh
# List issues
glissue() {
    local project_id=$(_glab_get_project_id)
    [[ $? -eq 0 ]] && glab api "projects/${project_id}/issues" "$@" | jq -r '.[] | "\(.iid)\t\(.title)\t\(.state)"'
}

# List pipelines
glpipe() {
    local project_id=$(_glab_get_project_id)
    [[ $? -eq 0 ]] && glab api "projects/${project_id}/pipelines" "$@" | jq -r '.[] | "\(.id)\t\(.status)\t\(.ref)"'
}

# Merge MR
glmerge() {
    local project_id=$(_glab_get_project_id)
    local mr_id="$1"
    [[ $? -eq 0 && -n "$mr_id" ]] && glab api -X PUT "projects/${project_id}/merge_requests/${mr_id}/merge"
}
```

### Custom Output Formatting

```zsh
# Colored output with status
gli() {
    local project_id=$(_glab_get_project_id)
    [[ $? -eq 0 ]] && glab api "projects/${project_id}/merge_requests" "$@" | \
        jq -r '.[] | "\(.iid)\t\(.title)\t\(.state)"' | \
        while IFS=$'\t' read -r iid title state; do
            case "$state" in
                opened) echo -e "\033[32m${iid}\033[0m\t${title}" ;;
                merged) echo -e "\033[34m${iid}\033[0m\t${title}" ;;
                closed) echo -e "\033[31m${iid}\033[0m\t${title}" ;;
            esac
        done
}
```

### Multi-Host Support

```zsh
# Support multiple GitLab instances
_glab_get_project_id() {
    # ... (existing code) ...

    # Detect host from git URL
    local gitlab_host=""
    if [[ "$git_url" =~ "git.company1.com" ]]; then
        export GITLAB_HOST="https://git.company1.com"
    elif [[ "$git_url" =~ "git.company2.com" ]]; then
        export GITLAB_HOST="https://git.company2.com"
    fi

    # Rest of function...
}
```

## Troubleshooting Commands Reference

```bash
# Authentication
glab auth status
glab auth login --hostname YOUR_HOST

# List projects
glab api projects --paginate | jq -r '.[] | {id, path: .path_with_namespace}'

# Test MR access
glab api projects/PROJECT_ID/merge_requests | jq '.[0]'

# Check cache
ls -lah /tmp/glab_project_id_*
cat /tmp/glab_project_id_NAMESPACE_REPO

# Validate .zshrc
zsh -n ~/.zshrc

# Test function
zsh -c 'source ~/.zshrc && type gli'

# Clear cache
rm /tmp/glab_project_id_*

# Debug project path extraction
git remote get-url origin
```

## Support

For additional help:
1. Check `glab` documentation: https://gitlab.com/gitlab-org/cli
2. Verify GitLab API works: `curl -H "PRIVATE-TOKEN: $TOKEN" https://gitlab.com/api/v4/projects`
3. Review `.zshrc` for conflicts: `grep -n "glab\|gli" ~/.zshrc`

## Notes

- Functions use direct GitLab API (bypasses buggy `-R` flag)
- Project IDs are cached for 60 minutes in `/tmp`
- Requires `jq` for JSON processing
- Works with custom ports and SSH URLs
- Compatible with zsh and bash (with minor modifications)

---

**Created**: 2025-10-21
**Based on**: Real-world troubleshooting of custom GitLab instances
