---
id: TASK-4
title: Improve Whisper server auto-start reliability
status: To Do
assignee: []
created_date: '2026-02-15 07:55'
labels: []
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Current issue: Vast.ai overrides Docker CMD with its own launch wrapper, so the whisper server must be started manually via SSH after each worker creation. Explore solutions: 1) Better onstart.sh that survives Vast.ai's process management, 2) Supervisor/systemd inside container, 3) Wait for Vast.ai to support custom template auto-scaling. Currently works as managed instance, not true serverless.
<!-- SECTION:DESCRIPTION:END -->
