---
id: TASK-4
title: Improve Whisper server auto-start reliability
status: Done
assignee: []
created_date: '2026-02-15 07:55'
updated_date: '2026-02-15 16:28'
labels: []
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Current issue: Vast.ai overrides Docker CMD with its own launch wrapper, so the whisper server must be started manually via SSH after each worker creation. Explore solutions: 1) Better onstart.sh that survives Vast.ai's process management, 2) Supervisor/systemd inside container, 3) Wait for Vast.ai to support custom template auto-scaling. Currently works as managed instance, not true serverless.
<!-- SECTION:DESCRIPTION:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
2026-02-15: Moot — Vast.ai endpoints destroyed. Platform limitation: custom templates cannot scale to zero and autoscaler always respawns workers. Whisper stays on RunPod serverless.
<!-- SECTION:NOTES:END -->
