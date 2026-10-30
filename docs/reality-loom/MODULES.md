# Reality Loom module catalog

Status key: **Active** means used in the browser prototype; **Candidate** means evaluated for a later adapter; **Research** means not yet selected.

## Core contract

A module is an independently versioned capability. It declares:
- stable module ID and semantic version
- capability tags and supported dimensions (2D/3D/time)
- entity components read and written
- lifecycle hooks: initialize, step, snapshot, restore, dispose
- dependencies, license, performance profile and validation suite
- deterministic/reproducible behavior declaration

The host owns entity identity, simulation time, persistence, event routing and observability. Modules own their specialized calculations. Modules must not silently mutate data outside their declared write set.

## First integration set

| Domain | Candidate | Role | License / notes | Status |
|---|---|---|---|---|
| 3D rendering | [Three.js](https://threejs.org/) | Scene, camera, geometry, materials | MIT | Active |
| Rigid-body physics | [Rapier](https://rapier.rs/) | Gravity, collision, joints, rigid bodies | Apache-2.0 | Active |
| 2D game systems | [Phaser](https://phaser.io/) | 2D scenes, input, animation, arcade physics | MIT | Candidate |
| 3D game engine | [Godot](https://godotengine.org/) | Full scene/game runtime; separate process/export or native app | MIT | Candidate |
| Agent-based modeling | [NetLogo](https://ccl.northwestern.edu/netlogo/) | Population and social-model references; assess runtime integration separately | GPL-2.0 | Candidate |
| Web 3D alternative | [Babylon.js](https://www.babylonjs.com/) | Alternative renderer/engine, not a second renderer in the same scene | Apache-2.0 | Candidate |
| Scientific computing | [Python / SciPy](https://scipy.org/) | Offline analysis, parameter fitting, scientific models | BSD-3-Clause | Research |
| Fluid simulation | [WebGPU samples](https://webgpu.github.io/webgpu-samples/) | GPU compute experiments | Per-project license review | Research |
| Graph/network models | [Graphology](https://graphology.github.io/) | Networks, centrality, graph algorithms | MIT | Candidate |
| Spatial indexing | [RBush](https://github.com/mourner/rbush) | 2D spatial queries | MIT | Candidate |

Licenses above are project-level starting points, not legal advice. Re-check the exact package, version, transitive dependencies, asset licenses and redistribution terms before shipping.

## Adapter interface (TypeScript sketch)

```ts
export interface SimulationModule {
  id: string;
  version: string;
  capabilities: string[];
  requires: string[];
  reads: string[];
  writes: string[];
  initialize(context: SimulationContext): Promise<void> | void;
  step(context: SimulationContext, dt: number): void;
  snapshot(): unknown;
  restore(snapshot: unknown): void;
  dispose(): void;
}
```

## Integration rules

1. One authoritative physics solver per interacting rigid-body world.
2. Fixed simulation timestep; rendering may run at a different frame rate.
3. Stable IDs and explicit units (meters, seconds, kilograms) at module boundaries.
4. Snapshot module state with world state; record module versions.
5. Use adapters rather than allowing modules to depend directly on each other's internals.
6. Run contract tests, deterministic replay tests where supported, and performance budgets before activation.
7. Treat toy models as exploratory simulations, never as validated real-world forecasts.

## Roadmap

- [x] Three.js scene and camera
- [x] Rapier rigid bodies, gravity and collision
- [x] Fixed-step clock, pause, single-step and time scaling
- [x] Entity inspection and local save/restore
- [x] Initial module registry
- [ ] Automated unit and browser tests
- [ ] Android WebView host integration
- [ ] Versioned experiment snapshots and replay
- [ ] Add one candidate module at a time after adapter tests
