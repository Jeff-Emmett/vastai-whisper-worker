---
id: TASK-3
title: Push Docker image to container registry
status: To Do
assignee: []
created_date: '2026-02-15 07:55'
labels: []
dependencies: []
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Image built on Netcup (5.4GB) but push to ghcr.io failed (missing write:packages scope) and Docker Hub failed (no auth). Currently using public fedirz/faster-whisper-server image instead, so custom image push is low priority. If needed later: run 'gh auth refresh --scopes write:packages' then 'docker push ghcr.io/jeff-emmett/vastai-whisper-worker:latest'.
<!-- SECTION:DESCRIPTION:END -->
