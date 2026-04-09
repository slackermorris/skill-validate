---
title: Progress Update
description: Update execution plan with progress from daily notes and git status
tags: exec-plan, progress, daily-notes
---

## Progress Update

Reviews today's daily notes and git status to extract relevant insights and updates the specified execution plan with progress information.

### Steps

1. Read today's daily note from `~/Documents/Kwicherbelliaken/Daily/YYYY-MM-DD.md`
2. Extract:
   - Decisions made
   - Action items completed
   - Notes & connections relevant to the execution plan
   - Reflections on progress
3. Check git status to identify:
   - Files modified
   - Commits made today on this branch
   - Current branch status
4. Update the execution plan specified by title in `docs/exec-plans/active/` with:
   - Progress log entries for completed work
   - Updated associated work (PRs, commits, issues)
   - Updated checkpoints if applicable
   - Updated notes & blockers based on daily notes
5. Preserve existing metadata and goal sections

### Implementation Notes

- The command assumes daily notes use YAML frontmatter with date field
- Looks for sections: # Decisions, # Action Items, # Notes & Connections, # Reflection
- For git integration: uses `git log --since="yesterday"` to find recent commits, commits should be specific to this branch
- Updates only the Progress Log, Associated Work, Checkpoints, and Notes & Blockers sections
- Does not modify Metadata or Goal sections
