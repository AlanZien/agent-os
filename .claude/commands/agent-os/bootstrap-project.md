---
name: bootstrap-project
description: Automatically initialize project structure based on tech stack choices
subagent_type: project-bootstrapper
---

Initialize your project structure automatically based on the technology choices defined in `agent-os/product/tech-stack.md`.

**What this does:**
- Reads your tech stack decisions from `/plan-product`
- Runs appropriate project initialization commands (Expo, Vite, etc.)
- Installs all chosen dependencies
- Creates initial configuration files
- Sets up folder structure
- Makes initial git commit

**When to use:**
Run this AFTER `/plan-product` and BEFORE `/shape-spec` to automatically set up your project foundation.

**Requirements:**
- `agent-os/product/tech-stack.md` must exist (created by `/plan-product`)
- Node.js and npm must be installed
- Git must be initialized

**Example workflow:**
```
/plan-product           # Define mission, roadmap, tech stack
/bootstrap-project      # ← YOU ARE HERE - Auto-create project structure
/shape-spec            # Start defining your first feature
/write-spec
/plan-tests
/create-tasks
/implement-tasks
```

**What gets created:**
For an Expo + Supabase + Zustand stack:
```
mobile/               # Created by create-expo-app
├── app/              # Expo Router structure
├── components/
├── services/
│   └── supabase.ts   # Auto-configured
├── stores/           # Zustand stores
├── app.json
└── package.json      # With all dependencies

backend/              # If backend chosen
├── main.py
├── models/
├── routes/
└── requirements.txt

supabase/             # If Supabase chosen
├── migrations/
└── seed.sql
```

**Time saved:** 30-60 minutes vs manual setup

**Note:** This command is optional. You can still bootstrap manually if you prefer more control over the initial setup.
