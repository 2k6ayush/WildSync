# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

Project overview
- Name: WildSync
- Purpose: AI-powered forest management system that helps forest departments analyze ecosystem data and make data-driven conservation decisions. Users upload forest data (tree counts, animal populations, soil quality, location details, past calamities) and receive actionable insights via interactive heat maps and AI-generated recommendations for resource allocation and wildlife protection.

Current repository state
- This repository currently contains documentation (README.md) and no implementation code, build system, tests, or CI configuration.
- There are no defined commands for building, linting, or testing at this time.

What Warp should know right now
- Source layout and architecture are not established yet. Once code is added, update this file to include:
  - How to build the project (language/toolchain and exact commands)
  - How to run all tests and a single test
  - How to run linters/formatters
  - Any services or databases required for local development

Where to look for commands (once code is added)
- Depending on the chosen stack, commands will typically live in:
  - JavaScript/TypeScript: package.json scripts
  - Python: pyproject.toml (poetry/pdm), setup.cfg, or Makefile, plus requirements files
  - .NET: .sln/.csproj with dotnet CLI
  - Java/Kotlin: Maven (pom.xml) or Gradle (build.gradle/gradle.kts)
  - Go: go.mod with Makefile or task runner
  - Docker: Dockerfile and docker-compose.yml for local orchestration
- Also check CI definitions (e.g., .github/workflows/*.yml) for authoritative build/test steps.

Files of note
- README.md: High-level description of the project’s goals and intended capabilities.

Action for maintainers
- After scaffolding the initial codebase and toolchain, add the concrete commands under a Commands section, and include a brief architecture overview that explains major components (data ingestion, storage, analysis/ML, mapping/visualization, API/UI) and their interactions.
