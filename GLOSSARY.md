# Glossary

The shared, single-source-of-truth glossary for the Claude Code 101 beginner course. Every term defined here is referenced by at least one beginner slide deck under [slides/beginner/](slides/beginner/README.md), and every term that appears on any deck's "Glossary card" is defined here byte-identically. The structural validator (`scripts/validate.sh` check V8) enforces both directions: no drift, no orphans, no duplicates.

Format for every entry: `- **Term**: One-line definition.` (single line, period at the end). Group by first letter under H2 headings, alphabetised within each group.

## A

- **Accept**: Choosing to keep a change Claude proposed.

## C

- **CLAUDE.md**: A short Markdown file at the root of your project that tells Claude Code your house rules.
- **Capstone**: The final hands-on project at the end of Module 08.
- **Claude Code**: The command-line tool from Anthropic that lets you talk to the Claude AI model from your terminal.
- **CLI**: Command-line interface — a program you control by typing commands instead of clicking buttons.
- **Constraint**: A limit you put on Claude's reply, such as a word count or a list of words it must avoid.
- **Conversation**: A sequence of prompts and replies in the same Claude Code session.

## D

- **Diff**: The set of lines Claude proposes to add and remove from a file.

## G

- **git restore**: A Git command that undoes uncommitted changes to a file.

## H

- **Hunk**: One contiguous chunk of changed lines inside a larger diff.

## P

- **Permission**: A yes/no setting that lets a tool read, write, or run things on your machine.
- **Persistence**: Saving data to a file so it survives between program runs.
- **PII**: Personally identifiable information — names, addresses, phone numbers, account numbers, and similar private data.
- **Project context**: Information about your project (often in CLAUDE.md) that you give Claude so its answers fit your codebase.
- **Prompt**: The text you send to Claude. One message in the conversation.

## R

- **Reject**: Choosing not to keep a change Claude proposed.
- **Reversible edit**: A change you can undo with one command.
- **Role prompt**: A prompt that tells Claude what role to play, for example "Act as a careful junior tester.".

## S

- **Secret**: Sensitive data like a password or API key that must never be pasted into a prompt.
- **Subcommand**: A second word after the main command, such as `add` in `notes.py add`.

## T

- **Terminal**: The text window where you type commands and read their output.
