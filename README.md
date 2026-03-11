# Skill Validate

This repository contains validation utilities and examples.

## Execution Plans

This project uses execution plans to track progress and decisions for work. Execution plans are lightweight artifacts that combine elements of project planning, progress tracking, and decision logging.

### Location
Execution plans are stored in the `docs/exec-plans/` directory:
- `active/` - Currently executing plans
- `completed/` - Finished or archived plans  
- `templates/` - Templates for creating new plans

### Usage
See `docs/exec-plans/INDEX.md` for detailed information on how to use execution plans in this repository.

### Quick Reference
- To start work: Copy template from `templates/EXECUTION-PLAN-TEMPLATE.md` to `active/`
- During work: Update Progress Log and Decision Log regularly
- When complete: Move plan to `completed/` with date prefix

This approach helps maintain transparency in work progress while creating artifacts that could potentially be used by automated agents in the future.