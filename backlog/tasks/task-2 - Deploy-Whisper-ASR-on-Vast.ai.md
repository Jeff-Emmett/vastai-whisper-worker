---
id: TASK-2
title: Deploy Whisper ASR on Vast.ai
status: Done
assignee: []
created_date: '2026-02-15 07:55'
updated_date: '2026-02-15 16:28'
labels: []
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Deploy faster-whisper server on Vast.ai using fedirz/faster-whisper-server:latest-cuda image. Endpoint ID: 12196, Workergroup: 17040. Working on Titan V at $0.07/hr. Note: Custom templates don't support pyworker auto-scaling - runs as managed instance. Server must be started manually via SSH.
<!-- SECTION:DESCRIPTION:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
2026-02-15: Endpoint destroyed. Vast.ai serverless does NOT scale to zero — always keeps at least 1 worker running per endpoint ($0.07-0.12/hr idle). Not viable for on-demand/low-traffic use. Use RunPod serverless instead.
<!-- SECTION:NOTES:END -->
