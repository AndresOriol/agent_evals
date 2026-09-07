/**
 * Exercises the ported modules and prints one JSON object of observations.
 *
 * The hidden tests run this with `node` from a scratch directory and assert on
 * the result, so the port is graded by what it does rather than by what its
 * source looks like. Anything that throws is reported rather than crashing the
 * driver, so one broken export cannot hide the state of the others.
 */

import { pathToFileURL } from 'node:url';
import * as path from 'node:path';
import * as fs from 'node:fs';

const dist = process.argv[2];
const out = {};

async function load(name) {
  return import(pathToFileURL(path.join(dist, name)).href);
}

function attempt(label, fn) {
  try {
    out[label] = fn();
  } catch (err) {
    out[label] = { __error: String(err && err.message ? err.message : err) };
  }
}

const storage = await load('storage.js');
const prompt = await load('prompt.js');
const runner = await load('runner.js');

// --- storage -----------------------------------------------------------------
attempt('new_session', () => {
  const id = storage.createSession('First task');
  const s = storage.getSession(id);
  return {
    title: s.title,
    messages: s.messages,
    status: s.status,
    has_stamps: Boolean(s.created_at) && Boolean(s.updated_at),
  };
});

attempt('persisted', () => {
  const id = storage.createSession('Persisted');
  const file = path.join('.ui_data', 'sessions.json');
  const raw = JSON.parse(fs.readFileSync(file, 'utf-8'));
  return { on_disk: Boolean(raw[id]), title: storage.getSession(id).title };
});

attempt('newest_first', () => {
  const older = storage.createSession('older');
  const newer = storage.createSession('newer');
  storage.updateSession(older, [{ role: 'user', content: 'hi' }]);
  const afterOlder = storage.getAllSessions()[0].id === older;
  storage.updateSession(newer, [{ role: 'user', content: 'hi' }]);
  const afterNewer = storage.getAllSessions()[0].id === newer;
  return { after_older: afterOlder, after_newer: afterNewer };
});

attempt('update_replaces', () => {
  const id = storage.createSession();
  storage.updateSession(id, [{ role: 'user', content: 'a' }], 'working');
  const working = storage.getSession(id).status;
  storage.updateSession(id, [], 'completed', 'Renamed');
  const after = storage.getSession(id);
  return { working, messages: after.messages, title: after.title };
});

attempt('unknown_update_is_noop', () => {
  const before = storage.getAllSessions().length;
  storage.updateSession('nope', [{ role: 'user', content: 'a' }]);
  return { unchanged: storage.getAllSessions().length === before };
});

attempt('delete_twice', () => {
  const id = storage.createSession();
  storage.deleteSession(id);
  storage.deleteSession(id);
  return { gone: storage.getSession(id) === null || storage.getSession(id) === undefined };
});

// Deliberately last among the storage checks: it leaves the store unreadable,
// and a port that throws here would take every check after it down too.
attempt('corrupt_store', () => {
  fs.mkdirSync('.ui_data', { recursive: true });
  fs.writeFileSync(path.join('.ui_data', 'sessions.json'), '{ not json', 'utf-8');
  return { sessions: storage.getAllSessions() };
});

// --- prompt ------------------------------------------------------------------
attempt('combine', () =>
  prompt.combine([
    { role: 'user', content: 'one' },
    { role: 'assistant', content: 'two' },
    { role: 'user', content: 'three' },
  ]),
);
attempt('label_unknown', () => prompt.labelFor('wizard'));
attempt('label_system', () => prompt.labelFor('system'));
attempt('combine_blank', () =>
  prompt.combine([
    { role: 'user', content: '   ' },
    { role: 'user', content: 'real' },
  ]),
);
attempt('title_short', () => prompt.titleFrom('Fix the parser'));
attempt('title_long', () =>
  prompt.titleFrom('the quick brown fox jumps over the lazy dog', 20),
);
attempt('title_empty', () => prompt.titleFrom(''));

// --- runner ------------------------------------------------------------------
attempt('build_command', () => runner.buildCommand('/work'));
attempt('build_command_empty', () => {
  runner.buildCommand('');
  return '__no_throw__';
});
attempt('reply_done', () =>
  runner.extractReply(
    '12:00 INFO routing\n12:01 INFO 200 OK\n\n=== DONE after 4 message(s) ===\n\nThe answer is 5.\n',
  ),
);
attempt('reply_stopped', () =>
  runner.extractReply(
    'log line\n=== STOPPED (step budget spent) ===\n\nWhat I got done.\n',
  ),
);
attempt('reply_no_marker', () => runner.extractReply('  no marker here  '));
attempt('exit_ok', () => runner.describeExit(0));
attempt('exit_stopped', () => runner.describeExit(1, true));
attempt('exit_crash', () => runner.describeExit(1));

process.stdout.write(JSON.stringify(out, null, 2));
