# Docker Cleanup

Safe Docker cleanup with confirmation and space recovery reporting.

## Execution Steps

### Step 1: Analyze Current Docker Usage

Use Bash tool with command:
```bash
echo "=== DOCKER DISK USAGE ANALYSIS ===" && echo "" && echo "=== CURRENT DISK USAGE ===" && df -h / && echo "" && echo "=== DOCKER SYSTEM INFO ===" && docker system df && echo "" && echo "=== CONTAINERS ===" && docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Size}}" && echo "" && echo "=== IMAGES ===" && docker images --format "table {{.Repository}}:{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}" && echo "" && echo "=== VOLUMES ===" && docker volume ls
```

Description: "Analyze Docker disk usage and resources"

### Step 2: Identify Cleanup Candidates

Use Bash tool with command:
```bash
echo "=== CLEANUP CANDIDATES ===" && echo "" && echo "Stopped containers:" && docker ps -a --filter "status=exited" --format "table {{.Names}}\t{{.Status}}\t{{.Size}}" && echo "" && echo "Dangling images (untagged):" && docker images -f "dangling=true" --format "table {{.Repository}}:{{.Tag}}\t{{.Size}}" && echo "" && echo "Unused volumes:" && docker volume ls -qf "dangling=true" | wc -l && echo "volume(s)"
```

Description: "Identify resources that can be cleaned up"

### Step 3: Select Cleanup Scope

Use AskUserQuestion tool with the following question:

- **Question**: "What do you want to clean up?"
- **Header**: "Cleanup Type"
- **Options**:
  1. **Label**: "Quick cleanup (safe)", **Description**: "Remove stopped containers and dangling images only"
  2. **Label**: "Standard cleanup", **Description**: "Remove stopped containers, unused images, and unused networks"
  3. **Label**: "Aggressive cleanup", **Description**: "Remove ALL unused resources (containers, images, volumes, networks)"
  4. **Label**: "Custom selection", **Description**: "Choose specific resources to clean"
  5. **Label**: "Cancel", **Description**: "Exit without cleaning"
- **multiSelect**: false

WAIT for user's response.

### Step 4: Execute Cleanup Based on Selection

**If "Quick cleanup (safe)" selected:**

Use AskUserQuestion tool to confirm:
- **Question**: "This will remove stopped containers and dangling images. Continue?"
- **Header**: "Confirm"
- **Options**:
  1. **Label**: "Yes, proceed", **Description**: "Execute cleanup"
  2. **Label**: "No, cancel", **Description**: "Cancel operation"
- **multiSelect**: false

WAIT for user confirmation.

If confirmed, use Bash tool with command:
```bash
echo "=== QUICK CLEANUP ===" && echo "" && echo "Removing stopped containers..." && docker container prune -f && echo "" && echo "Removing dangling images..." && docker image prune -f && echo "" && echo "Cleanup complete."
```

Description: "Execute quick Docker cleanup"

**If "Standard cleanup" selected:**

Use AskUserQuestion tool to confirm:
- **Question**: "This will remove stopped containers, unused images, and unused networks. Continue?"
- **Header**: "Confirm"
- **Options**:
  1. **Label**: "Yes, proceed", **Description**: "Execute cleanup"
  2. **Label**: "No, cancel", **Description**: "Cancel operation"
- **multiSelect**: false

WAIT for user confirmation.

If confirmed, use Bash tool with command:
```bash
echo "=== STANDARD CLEANUP ===" && echo "" && echo "Removing stopped containers..." && docker container prune -f && echo "" && echo "Removing unused images..." && docker image prune -a -f && echo "" && echo "Removing unused networks..." && docker network prune -f && echo "" && echo "Cleanup complete."
```

Description: "Execute standard Docker cleanup"

**If "Aggressive cleanup" selected:**

Output: "WARNING: This will remove ALL unused Docker resources including volumes with data!"

Use AskUserQuestion tool to confirm:
- **Question**: "Are you absolutely sure? This may delete important data in unused volumes!"
- **Header**: "Confirm"
- **Options**:
  1. **Label**: "Yes, I'm sure", **Description**: "Execute aggressive cleanup (DANGEROUS)"
  2. **Label**: "No, cancel", **Description**: "Cancel operation"
- **multiSelect**: false

WAIT for user confirmation.

If confirmed, use Bash tool with command:
```bash
echo "=== AGGRESSIVE CLEANUP ===" && echo "" && echo "Removing all unused resources..." && docker system prune -a -f --volumes && echo "" && echo "Aggressive cleanup complete."
```

Description: "Execute aggressive Docker cleanup (removes volumes)"

**If "Custom selection" selected:**

Use AskUserQuestion tool with the following question:
- **Question**: "Select resources to clean up:"
- **Header**: "Resources"
- **Options**:
  1. **Label**: "Stopped containers", **Description**: "Remove containers that are not running"
  2. **Label**: "Dangling images", **Description**: "Remove untagged images"
  3. **Label**: "Unused images", **Description**: "Remove all images not used by containers"
  4. **Label**: "Unused volumes", **Description**: "Remove volumes not used by containers"
  5. **Label**: "Unused networks", **Description**: "Remove networks not used by containers"
- **multiSelect**: true

WAIT for user selection.

Execute cleanup for each selected resource type using appropriate docker prune commands.

**If "Cancel" selected:**

Output: "Docker cleanup cancelled. No changes made."

Exit command.

### Step 5: Verify Space Recovered

Use Bash tool with command:
```bash
echo "=== SPACE RECOVERY REPORT ===" && echo "" && echo "=== NEW DISK USAGE ===" && df -h / && echo "" && echo "=== NEW DOCKER USAGE ===" && docker system df && echo "" && echo "Cleanup complete! Review space recovered above."
```

Description: "Show disk space recovered after cleanup"

### Step 6: Cleanup Summary

Output summary including:
- Containers removed (count)
- Images removed (count and size)
- Volumes removed (count if applicable)
- Networks removed (count)
- Total space recovered

Output: "Docker cleanup complete!"

## Safety Notes

- **Stopped containers**: Safe to remove if not needed for restart
- **Dangling images**: Safe to remove (untagged intermediate images)
- **Unused images**: Check if you need them for quick container creation
- **Unused volumes**: DANGEROUS - May contain important data! Always backup first!
- **Unused networks**: Safe to remove, Docker recreates default networks

## Recommendations

**Daily cleanup**:
```bash
docker container prune -f
docker image prune -f
```

**Weekly cleanup**:
```bash
docker system prune -f
```

**Monthly cleanup** (with caution):
```bash
docker system prune -a -f
# Note: Only prune volumes if you're sure they're not needed
# docker volume prune -f
```

## Troubleshooting

If cleanup fails:
1. Check if containers are running: `docker ps`
2. Stop running containers if safe: `docker stop <container>`
3. Check for volume mounts: `docker volume inspect <volume>`
4. Review Docker daemon logs: `journalctl -u docker -n 50`

## Related Commands

- View detailed container sizes: `docker ps -as`
- Find large images: `docker images --format "{{.Size}}\t{{.Repository}}:{{.Tag}}" | sort -h`
- Check volume usage: `docker system df -v`
- Inspect specific resource: `docker inspect <id>`
