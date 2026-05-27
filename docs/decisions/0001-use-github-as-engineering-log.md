# Decision 0001: Use GitHub as the Engineering Log

Date: 2026-05-27

## Status

Accepted

## Context

The VANT project is almost purely mechanical. The repository does not need a software application structure, but it does need a reliable way to record progress, design rationale, build evidence, and test results.

## Decision

Use GitHub as the main progress log and engineering notebook:

- Markdown files for logs, decisions, test reports, and fabrication notes.
- Issues for active work items, questions, defects, and test tasks.
- Wiki pages for stable project knowledge.
- Repository folders for CAD, drawings, photos, references, and build evidence.

## Consequences

- The project remains easy to browse without specialized tools.
- Mechanical work can be reviewed chronologically.
- CAD files may need Git LFS later if they become large.
