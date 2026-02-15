---
id: TASK-5
title: Document Vast.ai serverless limitations
status: Done
assignee: []
created_date: '2026-02-15 16:28'
labels: []
dependencies: []
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Vast.ai serverless endpoints do NOT scale to zero. Autoscaler always keeps min 1 worker running per endpoint, even with cold_workers=0 and min_load=0. Custom templates also can't integrate pyworker for health signals. Destroying an instance causes autoscaler to immediately respawn. Only way to stop billing is deleting the endpoint entirely. Conclusion: RunPod is better for on-demand/low-traffic GPU workloads. Vast.ai only makes sense for sustained high-utilization workloads. Template hashes saved for recreation if needed: ComfyUI=497aea616c2479830c1af8c30244bda9, Whisper=3262085b2154d13164e4701005f1a22f.
<!-- SECTION:DESCRIPTION:END -->
