# SDLC Automation Demo OpenSpec Context

This repository uses OpenSpec-style change artifacts for the story-to-PR flow.

Lineage:

- Project: `https://github.com/Fission-AI/OpenSpec`
- Site: `https://openspec.pro`

Live OpenHands Automations create change folders under:

```text
openspec/changes/github-issue-<issue-number>-<short-slug>/
```

Each change folder should include:

- `proposal.md`
- `design.md`
- `tasks.md`
- `specs/<capability>/spec.md`

The timed customer demo does not install or invoke the OpenSpec CLI inside the
label-triggered automation. The automation writes these artifacts directly so
the run remains deterministic, avoids package-install variance, and fits the
Rajistics/OpenHands automation timeout. Operators can run OpenSpec CLI setup or
archive commands outside the live automation when the CLI is already available.
