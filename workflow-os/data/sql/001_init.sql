PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS workspaces (
    workspace_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    root_path TEXT NOT NULL UNIQUE,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS skills (
    skill_id TEXT PRIMARY KEY,
    folder_name TEXT NOT NULL UNIQUE,
    recommended_slug TEXT NOT NULL,
    display_name TEXT NOT NULL,
    description TEXT NOT NULL,
    skill_path TEXT NOT NULL,
    ui_metadata_path TEXT,
    managed_output_root TEXT,
    output_mode TEXT NOT NULL,
    resource_dirs_json TEXT NOT NULL,
    notes_json TEXT NOT NULL,
    enabled INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tools (
    tool_id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    category TEXT NOT NULL,
    local_path TEXT,
    remote_capable INTEGER NOT NULL DEFAULT 0,
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS repositories (
    repo_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    source_url TEXT,
    license TEXT,
    local_path TEXT,
    status TEXT NOT NULL DEFAULT 'candidate',
    notes TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tasks (
    task_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    brief TEXT,
    status TEXT NOT NULL,
    priority TEXT,
    source TEXT,
    goal_lock_path TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS runs (
    run_id TEXT PRIMARY KEY,
    task_id TEXT,
    workspace_id TEXT,
    router_agent TEXT,
    executor_agent TEXT,
    reviewer_agent TEXT,
    status TEXT NOT NULL,
    summary TEXT,
    started_at TEXT,
    finished_at TEXT,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE SET NULL,
    FOREIGN KEY (workspace_id) REFERENCES workspaces(workspace_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS artifacts (
    artifact_id TEXT PRIMARY KEY,
    run_id TEXT,
    skill_id TEXT,
    artifact_type TEXT NOT NULL,
    relative_path TEXT,
    absolute_path TEXT,
    sensitivity TEXT NOT NULL DEFAULT 'normal',
    created_at TEXT NOT NULL,
    FOREIGN KEY (run_id) REFERENCES runs(run_id) ON DELETE SET NULL,
    FOREIGN KEY (skill_id) REFERENCES skills(skill_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS decisions (
    decision_id TEXT PRIMARY KEY,
    task_id TEXT,
    run_id TEXT,
    decision_type TEXT NOT NULL,
    summary TEXT NOT NULL,
    rationale TEXT,
    human_approved INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE SET NULL,
    FOREIGN KEY (run_id) REFERENCES runs(run_id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS memories (
    memory_id TEXT PRIMARY KEY,
    topic TEXT NOT NULL,
    summary TEXT NOT NULL,
    source_path TEXT,
    tags TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id TEXT,
    task_id TEXT,
    actor TEXT,
    event_type TEXT NOT NULL,
    message TEXT NOT NULL,
    payload_json TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (run_id) REFERENCES runs(run_id) ON DELETE SET NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id) ON DELETE SET NULL
);

CREATE VIRTUAL TABLE IF NOT EXISTS skill_fts USING fts5(
    display_name,
    description,
    notes,
    content='skills',
    content_rowid='rowid'
);

CREATE VIRTUAL TABLE IF NOT EXISTS repository_fts USING fts5(
    name,
    source_url,
    notes,
    content='repositories',
    content_rowid='rowid'
);

CREATE VIRTUAL TABLE IF NOT EXISTS task_fts USING fts5(
    title,
    brief,
    content='tasks',
    content_rowid='rowid'
);

CREATE VIRTUAL TABLE IF NOT EXISTS decision_fts USING fts5(
    summary,
    rationale,
    content='decisions',
    content_rowid='rowid'
);

CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
    topic,
    summary,
    tags,
    content='memories',
    content_rowid='rowid'
);

CREATE TRIGGER IF NOT EXISTS skills_ai AFTER INSERT ON skills BEGIN
    INSERT INTO skill_fts(rowid, display_name, description, notes)
    VALUES (new.rowid, new.display_name, new.description, new.notes_json);
END;

CREATE TRIGGER IF NOT EXISTS skills_ad AFTER DELETE ON skills BEGIN
    INSERT INTO skill_fts(skill_fts, rowid, display_name, description, notes)
    VALUES ('delete', old.rowid, old.display_name, old.description, old.notes_json);
END;

CREATE TRIGGER IF NOT EXISTS skills_au AFTER UPDATE ON skills BEGIN
    INSERT INTO skill_fts(skill_fts, rowid, display_name, description, notes)
    VALUES ('delete', old.rowid, old.display_name, old.description, old.notes_json);
    INSERT INTO skill_fts(rowid, display_name, description, notes)
    VALUES (new.rowid, new.display_name, new.description, new.notes_json);
END;

CREATE TRIGGER IF NOT EXISTS repositories_ai AFTER INSERT ON repositories BEGIN
    INSERT INTO repository_fts(rowid, name, source_url, notes)
    VALUES (new.rowid, new.name, COALESCE(new.source_url, ''), COALESCE(new.notes, ''));
END;

CREATE TRIGGER IF NOT EXISTS repositories_ad AFTER DELETE ON repositories BEGIN
    INSERT INTO repository_fts(repository_fts, rowid, name, source_url, notes)
    VALUES ('delete', old.rowid, old.name, COALESCE(old.source_url, ''), COALESCE(old.notes, ''));
END;

CREATE TRIGGER IF NOT EXISTS repositories_au AFTER UPDATE ON repositories BEGIN
    INSERT INTO repository_fts(repository_fts, rowid, name, source_url, notes)
    VALUES ('delete', old.rowid, old.name, COALESCE(old.source_url, ''), COALESCE(old.notes, ''));
    INSERT INTO repository_fts(rowid, name, source_url, notes)
    VALUES (new.rowid, new.name, COALESCE(new.source_url, ''), COALESCE(new.notes, ''));
END;

CREATE TRIGGER IF NOT EXISTS tasks_ai AFTER INSERT ON tasks BEGIN
    INSERT INTO task_fts(rowid, title, brief)
    VALUES (new.rowid, new.title, COALESCE(new.brief, ''));
END;

CREATE TRIGGER IF NOT EXISTS tasks_ad AFTER DELETE ON tasks BEGIN
    INSERT INTO task_fts(task_fts, rowid, title, brief)
    VALUES ('delete', old.rowid, old.title, COALESCE(old.brief, ''));
END;

CREATE TRIGGER IF NOT EXISTS tasks_au AFTER UPDATE ON tasks BEGIN
    INSERT INTO task_fts(task_fts, rowid, title, brief)
    VALUES ('delete', old.rowid, old.title, COALESCE(old.brief, ''));
    INSERT INTO task_fts(rowid, title, brief)
    VALUES (new.rowid, new.title, COALESCE(new.brief, ''));
END;

CREATE TRIGGER IF NOT EXISTS decisions_ai AFTER INSERT ON decisions BEGIN
    INSERT INTO decision_fts(rowid, summary, rationale)
    VALUES (new.rowid, new.summary, COALESCE(new.rationale, ''));
END;

CREATE TRIGGER IF NOT EXISTS decisions_ad AFTER DELETE ON decisions BEGIN
    INSERT INTO decision_fts(decision_fts, rowid, summary, rationale)
    VALUES ('delete', old.rowid, old.summary, COALESCE(old.rationale, ''));
END;

CREATE TRIGGER IF NOT EXISTS decisions_au AFTER UPDATE ON decisions BEGIN
    INSERT INTO decision_fts(decision_fts, rowid, summary, rationale)
    VALUES ('delete', old.rowid, old.summary, COALESCE(old.rationale, ''));
    INSERT INTO decision_fts(rowid, summary, rationale)
    VALUES (new.rowid, new.summary, COALESCE(new.rationale, ''));
END;

CREATE TRIGGER IF NOT EXISTS memories_ai AFTER INSERT ON memories BEGIN
    INSERT INTO memory_fts(rowid, topic, summary, tags)
    VALUES (new.rowid, new.topic, new.summary, COALESCE(new.tags, ''));
END;

CREATE TRIGGER IF NOT EXISTS memories_ad AFTER DELETE ON memories BEGIN
    INSERT INTO memory_fts(memory_fts, rowid, topic, summary, tags)
    VALUES ('delete', old.rowid, old.topic, old.summary, COALESCE(old.tags, ''));
END;

CREATE TRIGGER IF NOT EXISTS memories_au AFTER UPDATE ON memories BEGIN
    INSERT INTO memory_fts(memory_fts, rowid, topic, summary, tags)
    VALUES ('delete', old.rowid, old.topic, old.summary, COALESCE(old.tags, ''));
    INSERT INTO memory_fts(rowid, topic, summary, tags)
    VALUES (new.rowid, new.topic, new.summary, COALESCE(new.tags, ''));
END;

CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_runs_status ON runs(status);
CREATE INDEX IF NOT EXISTS idx_artifacts_run_id ON artifacts(run_id);
CREATE INDEX IF NOT EXISTS idx_decisions_task_id ON decisions(task_id);
CREATE INDEX IF NOT EXISTS idx_events_run_id ON events(run_id);
