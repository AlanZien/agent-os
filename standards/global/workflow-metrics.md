# Workflow Metrics Standard - AgentOS Tracker

**Version**: 2.0 | **Applies to**: All agent-os workflow executions

## Purpose

Track and analyze workflow execution metrics to identify bottlenecks, optimize processes, and measure implementation quality over time.

## Metrics Categories

### 1. Execution Metrics

| Metric | Description | Unit |
|--------|-------------|------|
| `spec_duration` | Total time from spec start to verification | minutes |
| `task_group_durations` | Time per task group | minutes |
| `test_execution_time` | Time to run all tests | seconds |
| `build_time` | Time to build production bundle | seconds |

### 2. Quality Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| `tests_passed_rate` | % of tests passing | ≥95% |
| `type_check_status` | TypeScript compilation | Pass |
| `lint_status` | ESLint check | Pass |
| `regressions_introduced` | New failing tests | 0 |

### 3. Complexity Metrics

| Metric | Description |
|--------|-------------|
| `track_used` | 🚀 FAST / ⚙️ STANDARD / 🏗️ COMPLEX |
| `complexity_points` | Total points calculated |
| `task_groups_count` | Number of task groups |
| `files_created` | New files in implementation |
| `files_modified` | Existing files modified |

## Collection Points

Metrics are collected at these workflow stages:

```
┌─────────────────────────────────────────────────────────────┐
│  WORKFLOW STAGE          │  METRICS COLLECTED              │
├─────────────────────────────────────────────────────────────┤
│  1. Spec Shaping         │  complexity_points, track_used  │
│  2. Task Creation        │  task_groups_count              │
│  3. Implementation       │  task_group_durations           │
│  4. Testing              │  tests_*, test_execution_time   │
│  5. Verification         │  type_check, lint, spec_duration│
└─────────────────────────────────────────────────────────────┘
```

## Metrics Report Format

The implementation-verifier includes a metrics section in the final verification report:

```markdown
## 7. Workflow Metrics

### Execution Summary
| Metric | Value |
|--------|-------|
| Track | ⚙️ STANDARD |
| Complexity Points | 15 |
| Total Duration | 45 min |
| Task Groups | 4 |

### Task Group Breakdown
| Task Group | Duration | Tests |
|------------|----------|-------|
| 1. Database Layer | 12 min | 8 |
| 2. API Routes | 10 min | 12 |
| 3. UI Components | 15 min | 6 |
| 4. Integration | 8 min | 4 |

### Quality Summary
| Check | Status | Details |
|-------|--------|---------|
| Tests | ✅ 30/30 | 100% passing |
| TypeScript | ✅ | No errors |
| ESLint | ✅ | No issues |
| Build | ✅ | Successful |

### Comparison to Estimates
| Metric | Estimated | Actual | Delta |
|--------|-----------|--------|-------|
| Duration | 50 min | 45 min | -10% |
| Tests | 25 | 30 | +5 |
```

## Metrics Log File

All spec metrics are appended to `agent-os/metrics/workflow-log.json`:

```json
{
  "specs": [
    {
      "spec_id": "2026-01-04-authentication",
      "date": "2026-01-04",
      "track": "COMPLEX",
      "complexity_points": 25,
      "duration_minutes": 120,
      "task_groups": 12,
      "tests": {
        "unit": 45,
        "e2e": 12,
        "passed": 57,
        "failed": 0
      },
      "quality": {
        "typescript": "pass",
        "eslint": "pass",
        "build": "pass"
      },
      "files": {
        "created": 24,
        "modified": 8
      }
    }
  ]
}
```

## Using Metrics

### View Historical Metrics

```bash
# Pretty print workflow log
npx tsx scripts/workflow-metrics.ts --view

# Export to CSV
npx tsx scripts/workflow-metrics.ts --export metrics.csv

# Calculate averages by track
npx tsx scripts/workflow-metrics.ts --summary
```

### Analyze Trends

The metrics log enables:
- **Velocity tracking**: Average duration per complexity point
- **Quality trends**: Test pass rate over time
- **Estimation accuracy**: Predicted vs actual duration
- **Bottleneck detection**: Which phases take longest

## Integration

### For Implementation-Verifier

Add metrics section to final verification report:

1. Read `planning/track.md` for complexity data
2. Count task groups from `tasks.md`
3. Extract test results from Vitest/Playwright output
4. Record TypeScript/ESLint check results
5. Write metrics section to report
6. Append to `agent-os/metrics/workflow-log.json`

### For Implementer

Track task group start/end times in implementation reports:

```markdown
## Implementation: Task Group 1

**Started:** 2026-01-04 10:00
**Completed:** 2026-01-04 10:12
**Duration:** 12 minutes
**Tests Written:** 8
```

---

**Token Count**: ~500 tokens | **Critical for**: Workflow optimization
