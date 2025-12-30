#!/bin/bash

# verify-tests.sh - Compare planned tests from test-plan.md vs implemented tests
# Usage: ./scripts/verify-tests.sh agent-os/specs/[spec-name]

set -e

SPEC_PATH="$1"

if [ -z "$SPEC_PATH" ]; then
  echo "Usage: ./scripts/verify-tests.sh <spec-path>"
  echo "Example: ./scripts/verify-tests.sh agent-os/specs/2024-01-15_user-authentication"
  exit 1
fi

TEST_PLAN="$SPEC_PATH/test-plan.md"

if [ ! -f "$TEST_PLAN" ]; then
  echo "❌ Error: test-plan.md not found at $TEST_PLAN"
  echo "Run /plan-tests first to create a test plan."
  exit 1
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 Test Coverage Verification"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📁 Spec: $SPEC_PATH"
echo ""

# Count planned tests by priority
CRITICAL_PLANNED=$(grep -c "^\*\*Priority:\*\* Critical" "$TEST_PLAN" || echo "0")
HIGH_PLANNED=$(grep -c "^\*\*Priority:\*\* High" "$TEST_PLAN" || echo "0")
MEDIUM_PLANNED=$(grep -c "^\*\*Priority:\*\* Medium" "$TEST_PLAN" || echo "0")
LOW_PLANNED=$(grep -c "^\*\*Priority:\*\* Low" "$TEST_PLAN" || echo "0")
TOTAL_PLANNED=$((CRITICAL_PLANNED + HIGH_PLANNED + MEDIUM_PLANNED + LOW_PLANNED))

echo "📋 Tests Planned (from test-plan.md):"
echo "   • Critical: $CRITICAL_PLANNED"
echo "   • High:     $HIGH_PLANNED"
echo "   • Medium:   $MEDIUM_PLANNED"
echo "   • Low:      $LOW_PLANNED"
echo "   • Total:    $TOTAL_PLANNED"
echo ""

# Extract test function names from test-plan.md
# Format: #### 1. test_function_name
PLANNED_TESTS=$(grep "^#### [0-9]\+\. test_" "$TEST_PLAN" | sed 's/^#### [0-9]\+\. \(test_[^ ]*\).*/\1/' || echo "")

if [ -z "$PLANNED_TESTS" ]; then
  echo "⚠️  Warning: No test function names found in test-plan.md"
  echo "   Expected format: #### 1. test_function_name"
  exit 0
fi

# Count implemented tests (backend + frontend)
# Backend: pytest --collect-only
# Frontend: npm test -- --listTests (if package.json exists)

echo "🔍 Scanning for Implemented Tests..."
echo ""

BACKEND_TESTS=0
FRONTEND_TESTS=0
IMPLEMENTED_TESTS=""

# Check backend tests (Python/pytest)
if [ -d "backend" ]; then
  cd backend
  if command -v pytest &> /dev/null; then
    BACKEND_OUTPUT=$(pytest --collect-only -q 2>/dev/null || echo "")
    BACKEND_TESTS=$(echo "$BACKEND_OUTPUT" | grep -c "test_" || echo "0")
    IMPLEMENTED_TESTS="$IMPLEMENTED_TESTS
$BACKEND_OUTPUT"
  fi
  cd ..
fi

# Check frontend tests (JavaScript/Jest)
if [ -d "mobile" ] && [ -f "mobile/package.json" ]; then
  cd mobile
  if [ -f "package.json" ] && grep -q '"test"' package.json; then
    FRONTEND_OUTPUT=$(npm test -- --listTests 2>/dev/null || echo "")
    FRONTEND_TESTS=$(echo "$FRONTEND_OUTPUT" | grep -c "\.test\." || echo "0")
    IMPLEMENTED_TESTS="$IMPLEMENTED_TESTS
$FRONTEND_OUTPUT"
  fi
  cd ..
fi

TOTAL_IMPLEMENTED=$((BACKEND_TESTS + FRONTEND_TESTS))

echo "✅ Tests Implemented:"
echo "   • Backend:  $BACKEND_TESTS tests"
echo "   • Frontend: $FRONTEND_TESTS tests"
echo "   • Total:    $TOTAL_IMPLEMENTED tests"
echo ""

# Compare planned vs implemented
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📈 Coverage Analysis"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ "$TOTAL_IMPLEMENTED" -eq "$TOTAL_PLANNED" ]; then
  echo "✅ PERFECT! All planned tests are implemented"
  echo "   Planned: $TOTAL_PLANNED | Implemented: $TOTAL_IMPLEMENTED"
elif [ "$TOTAL_IMPLEMENTED" -gt "$TOTAL_PLANNED" ]; then
  EXTRA=$((TOTAL_IMPLEMENTED - TOTAL_PLANNED))
  echo "⚠️  More tests implemented than planned"
  echo "   Planned: $TOTAL_PLANNED | Implemented: $TOTAL_IMPLEMENTED (+$EXTRA extra)"
  echo "   This is OK if additional edge cases were covered!"
elif [ "$TOTAL_IMPLEMENTED" -lt "$TOTAL_PLANNED" ]; then
  MISSING=$((TOTAL_PLANNED - TOTAL_IMPLEMENTED))
  echo "❌ Missing tests!"
  echo "   Planned: $TOTAL_PLANNED | Implemented: $TOTAL_IMPLEMENTED (-$MISSING missing)"
  echo ""
  echo "🔍 Missing Tests:"

  # Find which tests are missing
  while IFS= read -r planned_test; do
    if ! echo "$IMPLEMENTED_TESTS" | grep -q "$planned_test"; then
      PRIORITY=$(grep -A 1 "#### [0-9]\+\. $planned_test" "$TEST_PLAN" | grep "Priority:" | sed 's/.*Priority:\*\* \([^ ]*\).*/\1/')
      echo "   ❌ $planned_test (Priority: $PRIORITY)"
    fi
  done <<< "$PLANNED_TESTS"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Coverage percentage
if [ "$TOTAL_PLANNED" -gt 0 ]; then
  COVERAGE=$((TOTAL_IMPLEMENTED * 100 / TOTAL_PLANNED))
  echo "📊 Coverage: $COVERAGE%"

  if [ "$COVERAGE" -ge 100 ]; then
    echo "   Status: ✅ Excellent"
  elif [ "$COVERAGE" -ge 80 ]; then
    echo "   Status: ✅ Good"
  elif [ "$COVERAGE" -ge 60 ]; then
    echo "   Status: ⚠️  Fair (need more tests)"
  else
    echo "   Status: ❌ Poor (many tests missing)"
  fi
else
  echo "⚠️  No tests planned in test-plan.md"
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Exit code based on coverage
if [ "$TOTAL_IMPLEMENTED" -ge "$TOTAL_PLANNED" ]; then
  exit 0
else
  exit 1
fi
