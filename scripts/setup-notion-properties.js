#!/usr/bin/env node
require('dotenv').config();
const https = require('https');

// Load from environment variables
const NOTION_TOKEN = process.env.NOTION_TOKEN;
const NOTION_VERSION = '2025-09-03';
const PROJECTS_DB_ID = process.env.NOTION_PROJECTS_DB_ID;
const TASKS_DB_ID = process.env.NOTION_TASKS_DB_ID;

// Validate required env vars
if (!NOTION_TOKEN || !PROJECTS_DB_ID || !TASKS_DB_ID) {
  console.error('❌ Missing required environment variables:');
  if (!NOTION_TOKEN) console.error('   - NOTION_TOKEN');
  if (!PROJECTS_DB_ID) console.error('   - NOTION_PROJECTS_DB_ID');
  if (!TASKS_DB_ID) console.error('   - NOTION_TASKS_DB_ID');
  console.error('\n💡 Copy .env.example to .env and fill in your Notion credentials');
  process.exit(1);
}

function notionRequest(path, method, body = null) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.notion.com',
      path: path,
      method: method,
      headers: {
        'Authorization': `Bearer ${NOTION_TOKEN}`,
        'Notion-Version': NOTION_VERSION,
        'Content-Type': 'application/json'
      }
    };
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(new Error(`Failed to parse: ${data}`));
        }
      });
    });
    req.on('error', reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

async function main() {
  console.log('🔧 Setup Notion properties for Agent-OS workflow...\n');

  try {
    // Get current Projects DB schema
    const projectsDb = await notionRequest(`/v1/data_sources/${PROJECTS_DB_ID}`, 'GET');
    const currentProjectProps = projectsDb.properties || {};

    console.log('📊 Projects Database:');

    // Add missing properties
    const newProjectProps = { ...currentProjectProps };

    if (!currentProjectProps['Current Agent']) {
      newProjectProps['Current Agent'] = {
        rich_text: {}
      };
      console.log('  ➕ Adding "Current Agent" (text)');
    } else {
      console.log('  ✅ "Current Agent" already exists');
    }

    if (!currentProjectProps['Spec Path']) {
      newProjectProps['Spec Path'] = {
        rich_text: {}
      };
      console.log('  ➕ Adding "Spec Path" (text)');
    } else {
      console.log('  ✅ "Spec Path" already exists');
    }

    // Update Projects DB
    await notionRequest(`/v1/data_sources/${PROJECTS_DB_ID}`, 'PATCH', {
      properties: newProjectProps
    });

    console.log('\n✅ Tasks Database:');

    // Get current Tasks DB schema
    const tasksDb = await notionRequest(`/v1/data_sources/${TASKS_DB_ID}`, 'GET');
    const currentTaskProps = tasksDb.properties || {};

    const newTaskProps = { ...currentTaskProps };

    if (!currentTaskProps['Task ID']) {
      newTaskProps['Task ID'] = {
        rich_text: {}
      };
      console.log('  ➕ Adding "Task ID" (text)');
    } else {
      console.log('  ✅ "Task ID" already exists');
    }

    if (!currentTaskProps['Task Group']) {
      newTaskProps['Task Group'] = {
        rich_text: {}
      };
      console.log('  ➕ Adding "Task Group" (text)');
    } else {
      console.log('  ✅ "Task Group" already exists');
    }

    // Check if Project relation exists (might be named "🎯 Projects")
    const hasProjectRelation = currentTaskProps['Project'] || currentTaskProps['🎯 Projects'];
    if (!hasProjectRelation) {
      newTaskProps['Project'] = {
        relation: {
          database_id: PROJECTS_DB_ID
        }
      };
      console.log('  ➕ Adding "Project" (relation to Projects)');
    } else {
      console.log('  ✅ "Project" relation exists');
      if (currentTaskProps['🎯 Projects']) {
        console.log('     ℹ️  Note: Found "🎯 Projects" - consider renaming to "Project" for consistency');
      }
    }

    // Update Tasks DB
    await notionRequest(`/v1/data_sources/${TASKS_DB_ID}`, 'PATCH', {
      properties: newTaskProps
    });

    console.log('\n✨ Notion properties setup complete!');
    console.log('\n💡 Recommendations:');
    if (currentTaskProps['🎯 Projects'] && !currentTaskProps['Project']) {
      console.log('   - Rename "🎯 Projects" to "Project" in Notion UI for consistency');
    }
    console.log('   - Your Agent-OS workflow is now ready to use!');

  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

main();
