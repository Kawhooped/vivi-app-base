# Reality Regard

**Status:** Experimental specification  
**Parent project:** Device Studio / Reality Loom  
**Branch:** `experiment/reality-regard`

## Central experiment

Can a collection of agents build increasingly powerful models of reality by observing, describing, negating, recombining, and testing one another's models?

The ambition is to regard existence as a whole. The engineering discipline is to keep every claim distinguishable from evidence, inference, and imagination.

## Governing law

> Nothing gets promoted to reality merely because all the agents agree.

Consensus is a social fact about the agents. It is not, by itself, evidence about the world. Every model remains provisional and must expose what could prove it wrong.

## Agent roles

| Agent | Responsibility | Required output |
|---|---|---|
| REGARD | Gather observations; identify entities, relationships and conditions. | Observation records with source, time, scope and uncertainty. |
| SCHEMA | Construct a model of what may be happening. | Versioned model with claims, relations, assumptions and predictions. |
| NEGATION | Search for omissions, contradictions and alternative explanations. | Counterclaims, missing variables and discriminating tests. |
| RECOMBINATION | Construct new possible configurations from existing model parts. | Candidate models with lineage and explicit changes. |
| MONSTERS | Produce competing interpretations and hostile tests. | Adversarial scenarios, failure cases and rival explanations. |
| REALITY CHECK | Compare predictions with evidence and observed outcomes. | Test results, discrepancies and evidence links. |
| EVOLUTION | Preserve what worked, record failures and generate the next experiment. | Version decisions, retained components and next experiment. |

Agents are roles, not authorities. A role may be implemented by a model, a deterministic program, a human, or a combination.

## Epistemic labels

Every claim must carry one of these labels:

- **OBSERVED** — directly recorded evidence, with provenance.
- **INFERRED** — derived from one or more identified premises.
- **HYPOTHESIS** — a proposed explanation that could be tested.
- **IMAGINED** — a constructed possibility not yet supported as a description of the world.
- **UNKNOWN** — unresolved or insufficiently observed.

Labels attach to individual claims, not entire documents. A model may contain claims in several states. Transformations must preserve provenance and must not silently upgrade a claim's status.

## Core data objects

### Observation

- `id`: stable identifier
- `content`: what was observed, stated as narrowly as possible
- `source`: person, instrument, dataset or document
- `observed_at`: timestamp or interval
- `scope`: where and under what conditions it applies
- `method`: how it was obtained
- `limitations`: known measurement or sampling limits

### Claim

- `id`: stable identifier
- `statement`: one proposition
- `epistemic_status`: one of the five labels above
- `supports`: observation or claim IDs
- `challenges`: conflicting claim IDs
- `confidence`: optional calibrated estimate, never a substitute for evidence
- `created_by`: agent or human role
- `version`: claim revision

### Model

- `id` and `version`
- `claims`: claim IDs
- `entities` and `relationships`
- `assumptions`
- `predictions`: expected observations and conditions
- `known_gaps`
- `lineage`: parent model IDs and transformation
- `status`: exploratory, under-test, supported, contradicted or retired

### Experiment

- `question`: what uncertainty is being reduced?
- `prediction`: what should happen if the model is useful?
- `procedure`: repeatable test steps
- `success_criteria`: specified before the test
- `result`: observed outcome, including inconclusive outcomes
- `evidence`: linked observations and artifacts
- `decision`: retain, revise, reject or run again

## Iteration protocol

1. REGARD records observations without embedding explanations in the observation field.
2. SCHEMA creates a model whose claims link back to their support and assumptions.
3. NEGATION identifies contradictions, omissions and rival explanations.
4. RECOMBINATION creates alternatives while preserving model lineage.
5. MONSTERS attacks the alternatives with adversarial cases and edge conditions.
6. REALITY CHECK evaluates predictions against independently recorded outcomes.
7. EVOLUTION records what changed, what survived, what failed and what should be tested next.

Each cycle must produce inspectable artifacts. An agent's confident prose is not an experiment result.

## Independence and anti-consensus safeguards

- Agreement among agents is recorded as agreement, never counted as external validation.
- Where practical, competing agents receive the same evidence independently before seeing one another's conclusions.
- Reality Check should use evidence not generated solely by the model being evaluated.
- Predictions and success criteria are timestamped before outcomes are examined.
- Preserve failed, contradicted and inconclusive experiments.
- Track shared data, model families and prompt dependencies so apparent independence is not mistaken for independent confirmation.
- Record dissent and unresolved contradictions rather than averaging them away.
- No agent may silently rewrite source observations or erase provenance.

## First prototype: deliberately small

Build a local, inspectable cycle before adding autonomous complexity:

1. A human supplies a small set of observations.
2. REGARD structures them into entities, relationships and conditions.
3. SCHEMA produces one candidate model and explicit predictions.
4. NEGATION produces at least one rival explanation and identifies missing evidence.
5. MONSTERS generates a hostile test case.
6. A human or external dataset supplies the Reality Check result.
7. EVOLUTION compares the prediction with the result and writes the next experiment.

The first success criterion is not that the model sounds intelligent. It is that the cycle can preserve provenance, expose a meaningful disagreement, make a testable prediction, and update its model after an outcome.

## Evaluation

Measure the system by artifacts and outcomes:

- **Traceability:** can every factual claim be traced to its evidence or premises?
- **Calibration:** do confidence estimates correspond to observed accuracy over repeated trials?
- **Predictive performance:** do preregistered predictions outperform a simple baseline?
- **Error discovery:** do NEGATION and MONSTERS find consequential errors missed by SCHEMA?
- **Update quality:** does the model change appropriately after contradictory evidence?
- **Reproducibility:** can another run reconstruct the same inputs, versions and procedure?
- **Coverage:** which entities, relationships or conditions remain unobserved?

Do not use agent agreement, verbosity, novelty or confidence as standalone measures of truth.

## Open research questions

1. How can agents remain meaningfully independent while sharing useful discoveries?
2. How should uncertainty propagate when claims are recombined?
3. What counts as independent evidence for a given domain?
4. How can the system detect that its observation vocabulary excludes important phenomena?
5. Can it improve its own methods of observation and testing without making its evaluation circular?
6. Which parts of the process should be automated, and which require human or instrument-mediated judgment?

## Initial implementation boundary

This document defines the research protocol only. It does not authorize autonomous edits to the Android application, automatic deployment, or treating generated simulations as validated descriptions of the physical world. Implement the first cycle as a separate, testable module and preserve the existing Reality Loom behavior.
