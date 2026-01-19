#!/usr/bin/env node
/**
 * sync-to-tracker.js
 *
 * Synchronizes agent-os spec data to AgentOS-Tracker via REST API.
 * Called automatically after each workflow step (/write-spec, /create-tasks, etc.)
 *
 * Usage: node sync-to-tracker.js <spec-path> [--type=project|feature|tasks|tests]
 *
 * Environment variables required:
 *   TRACKER_API_URL - Base URL of the tracker (e.g., http://localhost:3000)
 *   AGENT_OS_API_KEY - API key for authentication
 */

require('dotenv').config();
const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

// Configuration
const TRACKER_API_URL = process.env.TRACKER_API_URL || 'http://localhost:3000';
const AGENT_OS_API_KEY = process.env.AGENT_OS_API_KEY;

// Validate required env vars
if (!AGENT_OS_API_KEY) {
  console.error('❌ Missing AGENT_OS_API_KEY environment variable');
  console.error('💡 Add AGENT_OS_API_KEY to your .env file');
  process.exit(1);
}

/**
 * Make HTTP request to Tracker API
 */
function trackerRequest(endpoint, method, body = null) {
  return new Promise((resolve, reject) => {
    const url = new URL(endpoint, TRACKER_API_URL);
    const isHttps = url.protocol === 'https:';
    const httpModule = isHttps ? https : http;

    const options = {
      hostname: url.hostname,
      port: url.port || (isHttps ? 443 : 80),
      path: url.pathname,
      method: method,
      headers: {
        Authorization: `Bearer ${AGENT_OS_API_KEY}`,
        'Content-Type': 'application/json',
      },
    };

    const req = httpModule.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => (data += chunk));
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve({ success: true, data: parsed, status: res.statusCode });
          } else {
            resolve({ success: false, error: parsed, status: res.statusCode });
          }
        } catch (e) {
          reject(new Error(`Failed to parse response: ${data}`));
        }
      });
    });

    req.on('error', reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

/**
 * Extract spec metadata from raw-idea.md or spec.md
 */
function extractSpecMetadata(specPath) {
  const specName = path.basename(specPath);
  let title = specName;
  let description = '';

  // Try to read spec.md for title/description
  const specFile = path.join(specPath, 'spec.md');
  if (fs.existsSync(specFile)) {
    const content = fs.readFileSync(specFile, 'utf-8');

    // Extract title from first # heading
    const titleMatch = content.match(/^#\s+(.+)$/m);
    if (titleMatch) {
      title = titleMatch[1].trim();
    }

    // Extract description from Overview section or first paragraph
    const overviewMatch = content.match(/##\s*Overview\s*\n+([\s\S]*?)(?=\n##|$)/i);
    if (overviewMatch) {
      description = overviewMatch[1].trim().split('\n')[0];
    }
  }

  // Fallback to raw-idea.md
  if (!description) {
    const rawIdeaFile = path.join(specPath, 'raw-idea.md');
    if (fs.existsSync(rawIdeaFile)) {
      const content = fs.readFileSync(rawIdeaFile, 'utf-8');
      description = content.split('\n').find((line) => line.trim().length > 0) || '';
    }
  }

  return { title, description, externalId: specName };
}

/**
 * Parse tasks.md to extract tasks
 */
function parseTasks(specPath) {
  const tasksFile = path.join(specPath, 'tasks.md');
  if (!fs.existsSync(tasksFile)) {
    return [];
  }

  const content = fs.readFileSync(tasksFile, 'utf-8');
  const tasks = [];
  const lines = content.split('\n');
  let currentGroup = null;
  let order = 0;

  for (const line of lines) {
    // Detect task group headers
    if (line.match(/^###\s+/) || line.match(/^####\s*Task Group/)) {
      currentGroup = line
        .replace(/^#+\s*/, '')
        .replace(/Task Group \d+:\s*/, '')
        .trim();
    }

    // Detect tasks: "- [ ] 1.1 Task description" or "- [x] 1.1 Task description"
    const taskMatch = line.match(/^(\s*)- \[([ x])\]\s*(\d+(?:\.\d+)?)\s+(.+)$/);
    if (taskMatch) {
      const [, indent, checked, taskId, description] = taskMatch;
      order++;
      tasks.push({
        external_id: taskId,
        title: description.trim(),
        description: `Task ${taskId} from ${currentGroup || 'Ungrouped'}`,
        status: checked === 'x' ? 'done' : 'todo',
        priority: 'medium',
        story_points: 1,
        order: order,
        group: currentGroup,
      });
    }
  }

  return tasks;
}

/**
 * Parse test-plan.md to extract tests
 */
function parseTests(specPath) {
  const testPlanFile = path.join(specPath, 'test-plan.md');
  if (!fs.existsSync(testPlanFile)) {
    return [];
  }

  const content = fs.readFileSync(testPlanFile, 'utf-8');
  const tests = [];
  const lines = content.split('\n');
  let currentSection = null;
  let order = 0;

  for (const line of lines) {
    // Detect test sections
    if (line.match(/^##\s+/)) {
      currentSection = line.replace(/^##\s*/, '').trim();
    }

    // Detect test cases: "- [ ] TEST-001: Description" or similar patterns
    const testMatch = line.match(/^-\s*\[([ x])\]\s*(TEST-\d+|TC-\d+|\d+\.\d+):\s*(.+)$/i);
    if (testMatch) {
      const [, checked, testId, description] = testMatch;
      order++;
      tests.push({
        external_id: testId,
        title: description.trim(),
        description: `Test from ${currentSection || 'General'}`,
        status: checked === 'x' ? 'passed' : 'pending',
        test_type: currentSection?.toLowerCase().includes('unit')
          ? 'unit'
          : currentSection?.toLowerCase().includes('e2e')
            ? 'e2e'
            : currentSection?.toLowerCase().includes('integration')
              ? 'integration'
              : 'manual',
      });
    }
  }

  return tests;
}

/**
 * Sync project (creates or updates based on external_id)
 */
async function syncProject(specPath, projectId = null) {
  const metadata = extractSpecMetadata(specPath);

  console.log(`📁 Syncing project: ${metadata.title}`);

  const result = await trackerRequest('/api/agent-os/projects', 'POST', {
    external_id: metadata.externalId,
    name: metadata.title,
    description: metadata.description,
  });

  if (result.success) {
    console.log(`   ✅ Project synced (${result.status === 201 ? 'created' : 'updated'})`);
    return result.data.data?.id || result.data.id;
  } else {
    console.error(`   ❌ Failed to sync project:`, result.error);
    return null;
  }
}

/**
 * Sync feature (the spec itself is a feature within a project)
 */
async function syncFeature(specPath, projectId) {
  if (!projectId) {
    console.error('   ⚠️  Cannot sync feature without project ID');
    return null;
  }

  const metadata = extractSpecMetadata(specPath);

  // Determine phase based on what files exist
  let phase = 'raw-idea';
  if (fs.existsSync(path.join(specPath, 'spec.md'))) {
    phase = 'spec';
  }
  if (fs.existsSync(path.join(specPath, 'tasks.md'))) {
    phase = 'development';
  }
  if (fs.existsSync(path.join(specPath, 'test-plan.md'))) {
    phase = 'testing';
  }

  console.log(`📋 Syncing feature: ${metadata.title} (phase: ${phase})`);

  const result = await trackerRequest('/api/agent-os/features', 'POST', {
    external_id: metadata.externalId,
    project_id: projectId,
    title: metadata.title,
    description: metadata.description,
    phase: phase,
  });

  if (result.success) {
    console.log(`   ✅ Feature synced (${result.status === 201 ? 'created' : 'updated'})`);
    return result.data.data?.id || result.data.id;
  } else {
    console.error(`   ❌ Failed to sync feature:`, result.error);
    return null;
  }
}

/**
 * Sync tasks from tasks.md
 */
async function syncTasks(specPath, sprintId = null) {
  const tasks = parseTasks(specPath);

  if (tasks.length === 0) {
    console.log('📝 No tasks found in tasks.md');
    return;
  }

  console.log(`📝 Syncing ${tasks.length} tasks...`);

  let synced = 0;
  let failed = 0;

  for (const task of tasks) {
    const payload = {
      external_id: `${path.basename(specPath)}-${task.external_id}`,
      title: task.title,
      description: task.description,
      status: task.status,
      priority: task.priority,
      story_points: task.story_points,
      order: task.order,
    };

    if (sprintId) {
      payload.sprint_id = sprintId;
    }

    const result = await trackerRequest('/api/agent-os/tasks', 'POST', payload);

    if (result.success) {
      synced++;
    } else {
      failed++;
      console.error(`   ❌ Task ${task.external_id}: ${result.error?.message || 'Unknown error'}`);
    }
  }

  console.log(
    `   ✅ Tasks synced: ${synced}/${tasks.length}${failed > 0 ? ` (${failed} failed)` : ''}`
  );
}

/**
 * Sync tests from test-plan.md
 */
async function syncTests(specPath, featureId = null) {
  const tests = parseTests(specPath);

  if (tests.length === 0) {
    console.log('🧪 No tests found in test-plan.md');
    return;
  }

  console.log(`🧪 Syncing ${tests.length} tests...`);

  let synced = 0;
  let failed = 0;

  for (const test of tests) {
    const payload = {
      external_id: `${path.basename(specPath)}-${test.external_id}`,
      title: test.title,
      description: test.description,
      status: test.status,
      test_type: test.test_type,
    };

    if (featureId) {
      payload.feature_id = featureId;
    }

    const result = await trackerRequest('/api/agent-os/tests', 'POST', payload);

    if (result.success) {
      synced++;
    } else {
      failed++;
      console.error(`   ❌ Test ${test.external_id}: ${result.error?.message || 'Unknown error'}`);
    }
  }

  console.log(
    `   ✅ Tests synced: ${synced}/${tests.length}${failed > 0 ? ` (${failed} failed)` : ''}`
  );
}

/**
 * Full sync - project, feature, tasks, and tests
 */
async function fullSync(specPath) {
  console.log('\n🔄 Syncing to AgentOS-Tracker...\n');
  console.log(`   Spec: ${path.basename(specPath)}`);
  console.log(`   Tracker: ${TRACKER_API_URL}\n`);

  // 1. Sync project
  const projectId = await syncProject(specPath);

  // 2. Sync feature
  const featureId = await syncFeature(specPath, projectId);

  // 3. Sync tasks (if tasks.md exists)
  if (fs.existsSync(path.join(specPath, 'tasks.md'))) {
    await syncTasks(specPath);
  }

  // 4. Sync tests (if test-plan.md exists)
  if (fs.existsSync(path.join(specPath, 'test-plan.md'))) {
    await syncTests(specPath, featureId);
  }

  console.log('\n✨ Tracker sync complete!\n');
}

/**
 * Main entry point
 */
async function main() {
  const args = process.argv.slice(2);
  const specPath = args.find((arg) => !arg.startsWith('--'));
  const typeArg = args.find((arg) => arg.startsWith('--type='));
  const syncType = typeArg ? typeArg.split('=')[1] : 'all';

  if (!specPath) {
    console.error(
      'Usage: node sync-to-tracker.js <spec-path> [--type=all|project|feature|tasks|tests]'
    );
    console.error('Example: node sync-to-tracker.js agent-os/specs/2026-01-19-my-feature');
    process.exit(1);
  }

  if (!fs.existsSync(specPath)) {
    console.error(`❌ Spec path does not exist: ${specPath}`);
    process.exit(1);
  }

  try {
    switch (syncType) {
      case 'project':
        await syncProject(specPath);
        break;
      case 'feature':
        const projectId = await syncProject(specPath);
        await syncFeature(specPath, projectId);
        break;
      case 'tasks':
        await syncTasks(specPath);
        break;
      case 'tests':
        await syncTests(specPath);
        break;
      case 'all':
      default:
        await fullSync(specPath);
    }
  } catch (error) {
    console.error('❌ Sync failed:', error.message);
    // Don't fail the workflow if sync fails
    process.exit(0);
  }
}

main();
