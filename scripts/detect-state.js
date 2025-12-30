#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function parseTasks(tasksContent) {
  const tasks = [];
  const lines = tasksContent.split('\n');
  let currentGroup = null;

  for (const line of lines) {
    // Detect task group headers
    if (line.startsWith('###') && !line.includes('Task Group')) {
      currentGroup = line.replace(/^###\s*/, '').trim();
    }

    // Detect task group with "Task Group X:" pattern
    if (line.match(/####\s*Task Group \d+:/)) {
      currentGroup = line.replace(/^####\s*/, '').trim();
    }

    // Detect tasks (e.g., "- [ ] 1.1 Create model")
    const taskMatch = line.match(/^(\s*)- \[([ x])\]\s*(\d+\.\d+)\s+(.+)$/);
    if (taskMatch) {
      const [, indent, checked, taskId, description] = taskMatch;
      tasks.push({
        id: taskId,
        description: description.trim(),
        completed: checked === 'x',
        group: currentGroup || 'Ungrouped',
        indent: indent.length
      });
    }
  }

  return tasks;
}

function detectState(specPath) {
  const state = {
    specPath: specPath,
    specName: path.basename(specPath),
    nextAgent: null,
    nextTask: null,
    projectStatus: null,
    summary: ''
  };

  // Check which files exist
  const hasRawIdea = fs.existsSync(path.join(specPath, 'raw-idea.md'));
  const hasRequirements = fs.existsSync(path.join(specPath, 'planning', 'requirements.md'));
  const hasSpec = fs.existsSync(path.join(specPath, 'spec.md'));
  const hasTasks = fs.existsSync(path.join(specPath, 'tasks.md'));

  // Determine next agent
  if (!hasRawIdea) {
    state.nextAgent = 'spec-initializer';
    state.projectStatus = 'Not Started';
    state.summary = 'Need to initialize spec folder';
  } else if (!hasRequirements) {
    state.nextAgent = 'spec-shaper';
    state.projectStatus = 'Planning';
    state.summary = 'Need to gather requirements';
  } else if (!hasSpec) {
    state.nextAgent = 'spec-writer';
    state.projectStatus = 'Planning';
    state.summary = 'Need to write specification';
  } else if (!hasTasks) {
    state.nextAgent = 'tasks-list-creator';
    state.projectStatus = 'Planning';
    state.summary = 'Need to create tasks list';
  } else {
    // Parse tasks to find next incomplete task
    const tasksContent = fs.readFileSync(path.join(specPath, 'tasks.md'), 'utf-8');
    const tasks = parseTasks(tasksContent);

    const incompleteTasks = tasks.filter(t => !t.completed);

    if (incompleteTasks.length === 0) {
      state.nextAgent = 'complete';
      state.projectStatus = 'Done';
      state.summary = 'All tasks completed!';
    } else {
      state.nextAgent = 'implementer';
      state.nextTask = incompleteTasks[0];
      state.projectStatus = 'In Progress';
      state.summary = `Next task: ${state.nextTask.id} - ${state.nextTask.description}`;
    }
  }

  return state;
}

function main() {
  const specPath = process.argv[2];

  if (!specPath) {
    console.error('Usage: node detect-state.js <spec-path>');
    console.error('Example: node detect-state.js agent-os/specs/2025-12-28-project-bootstrap');
    process.exit(1);
  }

  if (!fs.existsSync(specPath)) {
    console.error(`Error: Spec path does not exist: ${specPath}`);
    process.exit(1);
  }

  const state = detectState(specPath);

  // Output as JSON for easy parsing by shell script
  console.log(JSON.stringify(state, null, 2));
}

main();
