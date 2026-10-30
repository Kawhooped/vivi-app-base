# Device Core Specification

Version: 0.1

## Purpose
Provide a stable shared contract for a family of small interactive devices. A device is a focused system that receives inputs, constructs or updates a model, performs operations and returns inspectable outputs.

## Device contract
Each device declares:
- id and name
- purpose
- input schema
- model schema
- operations
- output schema
- persistence requirements
- validation tests
- version

## Model structure
A model may contain:
1. subject
2. entities
3. properties
4. relationships
5. rules
6. environment
7. current state
8. events
9. time
10. outcomes

Models may be verbal, visual, mathematical, spatial, computational or multimodal. A model can contain smaller models and connect to other models.

## Common operation cycle
Receive → Interpret → Represent → Operate → Evaluate → Record.

## Epistemic labels
Every claim that matters should be identifiable as:
- observed
- inferred
- assumed
- unknown

A coherent model is not automatically accurate. Predictions should be compared with observations, and model revisions should record what evidence motivated the change.

## Device registry
- story-device: prompt interpretation, world construction, story simulation and continuation.
- city-simulator: urban systems, population, resources, policy changes and simulated outcomes.
- world-builder: reusable environment and entity construction.
- decision-lab: independent proposals, critique, decision records and outcome evaluation.

## Architecture constraints
- Keep device logic modular.
- Keep shared schemas stable and versioned.
- Keep user-facing controls simple.
- Preserve prior working versions.
- Do not silently overwrite model history.
- A device must state its limitations and avoid presenting toy simulations as real-world forecasts.

## Roadmap
1. Establish launcher and registry.
2. Implement Story Device as first interactive device.
3. Integrate City Simulator as a reusable model-driven device.
4. Add persistence and experiment history.
5. Add agent roles and decision evaluation after the single-device loop is reliable.
