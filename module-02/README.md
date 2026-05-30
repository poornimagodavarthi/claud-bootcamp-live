# task — CLI Task Manager

A single-file, dependency-free task manager for your terminal. Tasks are stored
in a `tasks.json` file in the current working directory.

## Requirements

- Python 3.11+ (standard library only — nothing to install)

## Install

Make the script executable and put it on your `PATH`:

```sh
chmod +x task.py
ln -s "$(pwd)/task.py" /usr/local/bin/task
```

Or just run it directly with `python3 task.py <command>`.

## Commands

| Command | Description |
| --- | --- |
| `task add "<text>"` | Add a new task |
| `task list` | List all tasks (id, status, created_at, text) |
| `task done <id>` | Mark a task as done |
| `task delete <id>` | Delete a task |

### Examples

```sh
$ task add "Write the spec"
Added task #1: Write the spec

$ task list
ID  STATUS  CREATED_AT                 TEXT
1   todo    2026-05-30T13:42:29+00:00  Write the spec

$ task done 1
Marked #1 as done

$ task delete 99
No task with id 99      # exit code 1
```

## Exit codes

- `0` — success
- `1` — user error (e.g. unknown id, empty task text)
- `2` — internal error (e.g. corrupted/unreadable `tasks.json`)
