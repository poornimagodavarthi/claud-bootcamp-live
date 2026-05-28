# Module 00 — Set up Claude Code on your laptop

> Before Module 01 you need a terminal where `claude --version` prints a version number. That's it. Follow the seven steps below and you will be done in ~15 minutes.

## What you'll build

A working install of Claude Code on your own laptop, plus one file `first-prompt.txt` at the root of your home directory that contains your very first prompt to Claude and the reply you got back. That file is what Module 01 will check.

## Before you start

You need:

- **A laptop** running macOS, Linux, or Windows 10/11. On Windows you must be inside **WSL2** with an Ubuntu (or similar) shell — Claude Code does not run in raw PowerShell or `cmd.exe`. If you don't have WSL2 yet, follow Microsoft's WSL2 install guide first and come back here.
- **An internet connection** that is not blocking `npmjs.com` or `anthropic.com` (a corporate proxy might).
- **A free or paid Anthropic account** with API access enabled. The free tier is enough for this whole course.
- **Node.js 20 or newer**. Check with `node --version`. If you don't have it, install from <https://nodejs.org> (the LTS download is fine).
- **About 15 minutes** of focused time.

You do NOT need any prior coding experience. You do NOT need Git installed yet (Module 05 will need it).

## Step-by-step

1. **Open a terminal.**
   - macOS: press `Cmd+Space`, type `Terminal`, press Enter.
   - Linux: open your usual terminal app.
   - Windows: open WSL2 (e.g. start menu → "Ubuntu").
2. **Confirm Node.js is installed.** Run:
   ```sh
   node --version
   ```
   You should see something like `v20.11.0` or higher. If you get `command not found`, install Node.js first.
3. **Install Claude Code globally.** Run:
   ```sh
   npm i -g @anthropic-ai/claude-code
   ```
   This downloads the `claude` command and puts it on your PATH. It takes about a minute on a normal connection.
4. **Check the install worked.** Run:
   ```sh
   claude --version
   ```
   You should see a version number, e.g. `claude-code/1.2.3`. If you see `command not found`, jump to the troubleshooting table.
5. **Log in once.** Run:
   ```sh
   claude
   ```
   The first time it runs, it will open your browser and ask you to authorize the CLI against your Anthropic account. Click "Authorize", then come back to the terminal. You should now see a `>` prompt waiting for input.
6. **Send your very first prompt.** At the `>` prompt, type:
   ```
   Reply with one sentence that explains what Claude Code is, written for an absolute beginner.
   ```
   Press Enter. Wait for the reply (usually 2–4 seconds).
7. **Capture the answer.** Copy the reply you got, open a new file at `~/first-prompt.txt`, and paste in both your prompt and the reply. Save the file. Type `/exit` to leave the Claude session.

## The prompt to paste

This is the literal prompt you will paste at step 6. Copy it verbatim:

```
Reply with one sentence that explains what Claude Code is, written for an absolute beginner.
```

## How to know it worked

Run these two commands in your terminal:

```sh
claude --version
test -s ~/first-prompt.txt && echo "first-prompt.txt is saved"
```

You should see a version line followed by `first-prompt.txt is saved`. If both print, you are ready for Module 01.

## If something went wrong

| Symptom | Likely cause | Fix |
|---|---|---|
| `command not found: node` | Node.js is not installed or not on PATH. | Install Node.js LTS from <https://nodejs.org>, then close and reopen your terminal. |
| `EACCES` or "permission denied" during `npm i -g` | npm wants to write to a system path. | Re-run with `sudo npm i -g @anthropic-ai/claude-code` on macOS/Linux, OR run `npm config set prefix ~/.npm-global` and add `~/.npm-global/bin` to your PATH, then retry without `sudo`. |
| `command not found: claude` after install | The install succeeded but your shell does not know about it. | Close and reopen the terminal. If still missing, run `npm bin -g` to see where npm installed the binary; add that directory to your PATH. |
| Browser does not open at step 5 | Headless terminal, SSH, or strict firewall. | Copy the URL the CLI prints to a different machine's browser, complete the auth there, and paste the returned token back into the terminal. |
| Claude says "rate limited" or "quota exceeded" | Free-tier daily cap hit. | Wait ~24 hours, OR upgrade to a paid plan. The whole beginner course only needs a few dozen prompts, so the free tier is normally enough. |
| Claude's first reply is way longer than one sentence | The model interpreted your prompt loosely. | That is fine for Module 00. You'll learn to constrain output in Module 03. Just paste whatever it gave you. |
| Windows: `command not found` even though I installed Node in Windows | You ran the install in PowerShell, not WSL2. | Open WSL2 (Ubuntu) and reinstall Node + Claude Code there. PowerShell installs are not supported by this course. |

## You did it!

If `~/first-prompt.txt` exists and `claude --version` prints a version, the setup phase is complete. Continue to [`Module 01 — Meet Claude Code`](../part-01/README.md) when you are ready.
