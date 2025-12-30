#!/bin/bash

# Resume Agent-OS workflow from current state

SPEC_PATH="$1"

if [ -z "$SPEC_PATH" ]; then
  echo "Usage: ./resume-workflow.sh <spec-path>"
  echo "Example: ./resume-workflow.sh agent-os/specs/2025-12-28-project-bootstrap"
  exit 1
fi

if [ ! -d "$SPEC_PATH" ]; then
  echo "Error: Spec path does not exist: $SPEC_PATH"
  exit 1
fi

echo "🔍 Detecting current workflow state..."
echo ""

# Detect state using Node.js script
STATE_JSON=$(node scripts/detect-state.js "$SPEC_PATH")

# Parse JSON using Node.js (more reliable than bash)
NEXT_AGENT=$(echo "$STATE_JSON" | node -e "console.log(JSON.parse(require('fs').readFileSync(0, 'utf-8')).nextAgent)")
PROJECT_STATUS=$(echo "$STATE_JSON" | node -e "console.log(JSON.parse(require('fs').readFileSync(0, 'utf-8')).projectStatus)")
SUMMARY=$(echo "$STATE_JSON" | node -e "console.log(JSON.parse(require('fs').readFileSync(0, 'utf-8')).summary)")
SPEC_NAME=$(echo "$STATE_JSON" | node -e "console.log(JSON.parse(require('fs').readFileSync(0, 'utf-8')).specName)")

echo "📊 Current State:"
echo "   Spec: $SPEC_NAME"
echo "   Status: $PROJECT_STATUS"
echo "   Summary: $SUMMARY"
echo ""

# Determine next action
case $NEXT_AGENT in
  "spec-initializer")
    echo "▶️  Next: Run spec-initializer to initialize spec folder"
    echo ""
    echo "To continue, you need to manually launch the spec-initializer agent"
    echo "or use the Agent-OS orchestrator."
    ;;

  "spec-shaper")
    echo "▶️  Next: Run spec-shaper to gather requirements"
    echo ""
    echo "To continue, you need to manually launch the spec-shaper agent"
    echo "or use the Agent-OS orchestrator."
    ;;

  "spec-writer")
    echo "▶️  Next: Run spec-writer to create specification"
    echo ""
    echo "To continue, you need to manually launch the spec-writer agent"
    echo "or use the Agent-OS orchestrator."
    ;;

  "tasks-list-creator")
    echo "▶️  Next: Run tasks-list-creator to create tasks list"
    echo ""
    echo "To continue, you need to manually launch the tasks-list-creator agent"
    echo "or use the Agent-OS orchestrator."
    ;;

  "implementer")
    NEXT_TASK_ID=$(echo "$STATE_JSON" | node -e "const data = JSON.parse(require('fs').readFileSync(0, 'utf-8')); console.log(data.nextTask ? data.nextTask.id : '')")
    NEXT_TASK_DESC=$(echo "$STATE_JSON" | node -e "const data = JSON.parse(require('fs').readFileSync(0, 'utf-8')); console.log(data.nextTask ? data.nextTask.description : '')")

    echo "▶️  Next: Run implementer for task $NEXT_TASK_ID"
    echo "   Description: $NEXT_TASK_DESC"
    echo ""
    echo "To continue, you need to manually launch the implementer agent"
    echo "with instructions to implement task $NEXT_TASK_ID."
    ;;

  "complete")
    echo "✅ Workflow complete! All tasks are done."
    echo ""
    echo "You may want to:"
    echo "  - Run verification tests"
    echo "  - Commit your changes to Git"
    echo "  - Close the spec in Notion"
    ;;

  *)
    echo "❌ Unknown agent: $NEXT_AGENT"
    exit 1
    ;;
esac

echo ""
echo "💡 Tip: Check Notion for visual progress tracking"
