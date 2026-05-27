# VANT

VANT stands for **Vehiculo Aereo No Tripulado**.

This repository is for logging the design, fabrication, assembly, testing, and iteration of an unmanned aerial vehicle project. It is intentionally mechanical-first: the main value here is traceable progress, design decisions, build evidence, and test records.

## Project Goals

- Keep a clear chronological record of work completed.
- Track mechanical design decisions and their rationale.
- Store CAD exports, drawings, photos, calculations, and test notes in predictable places.
- Make it easy to resume the project after time away.
- Keep GitHub issues and wiki pages useful as an engineering notebook.

## Repository Layout

```text
.
|-- PROJECT_LOG.md              Main chronological progress log
|-- BOM.md                      Bill of materials and sourcing notes
|-- docs/
|   |-- decisions/              Design decision records
|   |-- design/                 Mechanical design notes and calculations
|   |-- fabrication/            Manufacturing and assembly notes
|   |-- safety/                 Risk, handling, and test safety notes
|   |-- testing/                Ground, structural, and flight test records
|   `-- templates/              Reusable log and report templates
|-- cad/                        Native CAD files and exported geometry
|-- drawings/                   2D drawings, PDFs, DXF files
|-- media/                      Photos, sketches, screenshots, videos
|-- references/                 Datasheets, external references, standards notes
|-- wiki/                       GitHub Wiki seed pages
`-- .github/ISSUE_TEMPLATE/     GitHub issue templates for progress tracking
```

## Suggested Workflow

1. Add a short entry to `PROJECT_LOG.md` whenever work is done.
2. Open GitHub issues for tasks, questions, tests, and build problems.
3. Create a decision record in `docs/decisions/` when a design choice matters.
4. Store supporting evidence in `media/`, `drawings/`, `cad/`, or `docs/testing/`.
5. Summarize stable knowledge in the `wiki/` pages.

## Status

Project initialized on 2026-05-27.

## License

No license has been selected yet. Treat all project files as private/all rights reserved until a license is added.
