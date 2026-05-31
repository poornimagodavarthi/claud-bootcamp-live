# Iteration Notes — task.py diff summary

Comparison: `module-02/python/task.py` (older) vs `module-02/task.py` (current)

## module-02/python/task.py (older)

- No shebang line
- Uses private-prefixed helpers: `_load()`, `_save()`, `_next_id()`
- Task status is `"open"` (not `"done"`)
- `cmd_list` supports a `--status open|done` filter flag
- Error handling is inline (direct `print` + `sys.exit(2)`) — no `UserError` class
- No `ensure_ascii=False` or trailing newline on save
- Parser uses `fn=` attribute (not `func=`)
- `raise SystemExit(main())` at the end

## module-02/task.py (current)

- Has `#!/usr/bin/env python3` shebang
- Named helpers: `load_tasks()`, `save_tasks()`, `next_id()`, `find_task()`
- Task status uses `"todo"` / `"done"`
- No `--status` filter on `list`
- Dedicated `UserError` exception class — clean separation of user vs internal errors
- Named exit code constants: `EXIT_OK`, `EXIT_USER_ERROR`, `EXIT_INTERNAL_ERROR`
- `save_tasks` uses `ensure_ascii=False` + trailing `"\n"`
- `build_parser()` extracted as its own function
- `sys.exit(main())` at the end

## Bottom line

The current version is more robust (better error handling, cleaner structure), while the `python/` version has one extra feature — the `--status` filter on `task list`.
