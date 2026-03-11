# Execution Plans

This directory contains execution plans that track progress and decisions for work in the repository.
Execution plans are lightweight artifacts that combine elements of project planning, progress tracking,
and decision logging in a format that is both human-readable and potentially usable by automated agents.

## Structure

- `active/` - Currently executing plans
- `completed/` - Finished or archived plans
- `templates/` - Templates for creating new plans

## Naming Convention

Files are named using the pattern: `{TYPE}-{DESCRIPTION}.md`

Where:
- `TYPE` is one of: FEAT (feature), BUG (bug fix), REFI (refactor), DOC (documentation), TEST, CHORE
- `DESCRIPTION` is a short, kebab-case description of the work

Example: `FEAT-user-authentication.md`

Each plan also includes an ID in the metadata: `{TYPE}-{YYYYMMDD}-{SEQUENCE}`

Example: `FEAT-20260312-001`

## Usage

1. To start a new piece of work:
   - Copy the template from `templates/EXECUTION-PLAN-TEMPLATE.md` to `active/` with an appropriate name
   - Fill in the metadata (ID, type, goal, etc.)
   - Begin logging progress and decisions as work proceeds

2. During work:
   - Update the Progress Log after completing meaningful accomplishments
   - Update the Decision Log immediately after making significant decisions
   - Keep the Associated Work section current with related PR numbers and commit hashes
   - Update the Updated timestamp regularly

3. When work is complete:
   - Move the plan from `active/` to `completed/` with a date prefix (e.g., `2026-03-12-FEAT-user-auth.md`)
   - Update the status to "Completed"
   - Fill in any final metrics or notes

## Agent-Friendly Design

These plans are designed to be:
- **Machine-readable**: Consistent structure, ISO timestamps, clear delimiters
- **Traceable**: Direct links to PRs, issues, and commits
- **Reasoning-transparent**: Decision logs capture the rationale behind choices
- **Progress-oriented**: Verb-object accomplishments in progress logs

## Maintenance

- Plans in `active/` should be updated at least daily during active work
- Stale plans (no updates for >3 days) should be reviewed for blockers or completion
- Completed plans are kept for historical reference and can be referenced in future work