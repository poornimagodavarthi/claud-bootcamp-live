import { Command } from "commander";
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { resolve } from "node:path";

type Task = {
  id: number;
  status: "open" | "done";
  created_at: string;
  text: string;
};

const DB = resolve(process.cwd(), "tasks.json");

function load(): Task[] {
  if (!existsSync(DB)) return [];
  try {
    return JSON.parse(readFileSync(DB, "utf-8")) as Task[];
  } catch {
    process.stderr.write("error: tasks.json is corrupt\n");
    process.exit(2);
  }
}

function save(rows: Task[]): void {
  writeFileSync(DB, JSON.stringify(rows, null, 2), "utf-8");
}

function nextId(rows: Task[]): number {
  return rows.reduce((m, r) => Math.max(m, r.id), 0) + 1;
}

const program = new Command();
program.name("task").description("CLI Task Manager");

program
  .command("add <text>")
  .description("add a task")
  .action((text: string) => {
    if (!text.trim()) {
      process.stderr.write("error: text must not be empty\n");
      process.exit(1);
    }
    const rows = load();
    const row: Task = {
      id: nextId(rows),
      status: "open",
      created_at: new Date().toISOString(),
      text: text.trim(),
    };
    rows.push(row);
    save(rows);
    console.log(`Added task #${row.id}: ${row.text}`);
  });

program
  .command("list")
  .option("--status <status>", "filter by status (open|done)")
  .action((opts: { status?: "open" | "done" }) => {
    let rows = load();
    if (opts.status) rows = rows.filter((r) => r.status === opts.status);
    if (rows.length === 0) return console.log("(no tasks)");
    console.log("id  status  created_at                 text");
    for (const r of rows) {
      console.log(
        `${String(r.id).padStart(2)}  ${r.status.padEnd(6)}  ${r.created_at.padEnd(25)}  ${r.text}`,
      );
    }
  });

program
  .command("done <id>")
  .action((idStr: string) => {
    const id = Number(idStr);
    const rows = load();
    const row = rows.find((r) => r.id === id);
    if (!row) {
      process.stderr.write(`No task with id ${id}\n`);
      process.exit(1);
    }
    row.status = "done";
    save(rows);
    console.log(`Marked #${id} as done`);
  });

program
  .command("delete <id>")
  .action((idStr: string) => {
    const id = Number(idStr);
    const rows = load();
    const next = rows.filter((r) => r.id !== id);
    if (next.length === rows.length) {
      process.stderr.write(`No task with id ${id}\n`);
      process.exit(1);
    }
    save(next);
    console.log(`Deleted #${id}`);
  });

program.parseAsync(process.argv).catch((err) => {
  process.stderr.write(`internal error: ${err}\n`);
  process.exit(2);
});
