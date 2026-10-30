# Device Studio

An Android home for a growing collection of interactive devices: focused tools that construct models, simulate systems, generate stories and support decisions.

## First device family

- **Story Device** — prompt → interpret → build → simulate → continue. Builds worlds, characters and events while tracking rules, conflicts and consequences.
- **City Simulator** — models residents, housing, jobs, transit, healthcare, education, environment and public resources.
- **World Builder** — reusable entity, property, relationship, rule, state and event models.
- **Decision Lab** — compares proposals, challenges assumptions and records predictions and outcomes.

## Shared device architecture

Every device follows a common contract:

1. **Purpose** — what job does this device perform?
2. **Inputs** — prompts, structured data, observations or user controls.
3. **Model** — entities, properties, relationships, rules, environment and state.
4. **Operations** — build, transform, simulate, compare or decide.
5. **Outputs** — useful results with assumptions and uncertainty visible.
6. **Memory** — save state, history, experiments and versioned changes.

The Android app is the device launcher and interaction shell. Device logic should remain modular so individual tools can evolve without redesigning the whole application.

## Principles

- Complexity inside, simplicity outside.
- Evidence over confidence.
- Separate observations, inferences and unknowns.
- Preserve experiment history and working versions.
- No model is treated as reality; validate predictions against outcomes.

## Build

Open the project in Android Studio and run the app configuration. The project uses Kotlin, Jetpack Compose, Material 3, Hilt and Room.

## Reality Loom

Reality Loom is the modular simulation engine and first interactive physical-world device.

- Browser prototype: [open the Reality Loom source](docs/reality-loom/index.html)
- Module catalog and adapter contract: [docs/reality-loom/MODULES.md](docs/reality-loom/MODULES.md)
- Android launcher: Reality Loom is available as a device entry and is hosted in a WebView using the bundled asset at `app/src/main/assets/reality-loom/index.html`.

The current prototype includes 3D space, Rapier rigid-body physics, gravity, collisions, a fixed-step clock, pause/resume, single-step, time scaling, entity inspection and local save/restore. Additional domains remain separate modules until their adapters and tests are ready.
