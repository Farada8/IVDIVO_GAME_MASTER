# ROOM917 RU Cast Lock Template Alignment Note

Date: 2026-08-22

Status: WORKING

The v1.0 cast-lock receipt template exists on branch `room917-ru-cast-engine-v2`. The validator additionally requires `hard_reject_flags` to be present and empty for every locked role. Before merge, the template must be read back using the branch-specific blob SHA and aligned so its role payload schema explicitly includes that field.

This note is not cast evidence and cannot authorize `LOCKED` or paid synthesis.
