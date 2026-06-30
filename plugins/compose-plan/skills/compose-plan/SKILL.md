---
name: compose-plan
description: Skill for generating structured development plans for geophysics, AI, and scientific computing projects
type: skill
---

# Skill: compose-plan

## Purpose

The `compose_plan` skill is responsible for generating a structured development plan before writing any code. It is primarily used for projects related to:

- Geophysics
- Ground Penetrating Radar (GPR)
- Seismic data processing
- AI / Machine Learning in geophysics
- Scientific computing
- Data processing workflows
- Visualization pipelines
- General scientific programming tasks

The goal of this skill is to convert a user's request into a complete development plan that will later be executed to generate code. This skill does not immediately generate final production code. Instead it produces a clear architecture and TODO execution plan.

## Core Philosophy

Before writing code, always perform structured planning. Every project should define:

1. Problem definition
2. Algorithmic approach
3. Directory structure
4. Script structure
5. Data flow
6. Required modules
7. Execution plan
8. Testing examples

## Project Type Identification

Before generating the plan, classify the request into one of the following categories:

1. GPR Data Processing
2. Seismic Data Processing
3. Machine Learning Model Training
4. Machine Learning Inference Pipeline
5. Scientific Visualization
6. Data Conversion or Preprocessing
7. Numerical Simulation
8. Utility Script
9. Multi-stage Workflow Pipeline

If the task belongs to geophysics, prioritize scientific workflows. The project type should influence algorithm design, directory structure, script modules, and required libraries.

## Expected Output Sections

1. Problem Description
2. Objective
3. Proposed Solution
4. Mathematical Model (if applicable)
5. Algorithm Overview
6. Directory Structure
7. Script Descriptions
8. Code Architecture
9. Data Flow
10. Required Libraries
11. Scalability Planning
12. Implementation Phases
13. TODO Execution Plan

## Project Directory Structure

```
project_root/
├── README.md
├── compose_plan.md
├── scripts/
│   ├── main_script.py
│   ├── processing.py
│   ├── utilities.py
│   ├── model.py
│   └── visualization.py
├── examples/
│   ├── example_usage.py
│   ├── demo_run.py
│   └── sample_input/
├── data/
│   ├── raw/
│   └── processed/
├── results/
│   ├── figures/
│   └── outputs/
└── docs/
    └── algorithm_description.md
```

## Directory Rules

### scripts/
Contains all main code implementations: data processing scripts, ML training pipelines, inversion algorithms, geophysical modeling scripts. No example or demo code should be stored here.

### examples/
Contains example usage scripts: running the main algorithm, demonstration scripts, small reproducible workflows, tutorials. These scripts show users how to run the main code.

### data/
Optional folder for input datasets with `raw/` and `processed/` subfolders.

### results/
Stores outputs: plots, processed data, model outputs, inversion results.

### docs/
Contains documentation: algorithm explanations, mathematical formulations, references.

## Code Architecture Rules

All generated projects should follow a modular architecture. Avoid monolithic scripts.

Typical module structure:
```
scripts/
├── main_script.py
├── data_loader.py
├── processing.py
├── algorithm.py
├── model.py
├── visualization.py
└── utils.py
```

The main script should:
1. Parse user inputs
2. Load data
3. Call processing functions
4. Execute algorithms
5. Save outputs
6. Generate plots

## Algorithm Planning

Each plan must describe the algorithm in clear steps.

### GPR Processing Algorithms
- Background removal
- Time zero correction
- Gain correction
- Migration
- Noise filtering

### Seismic Processing Algorithms
- Waveform filtering
- Spectral analysis
- Travel time analysis
- Inversion workflows

### Machine Learning Algorithms
- CNN training
- Dataset preparation
- Model evaluation
- Prediction pipelines

## Code Style Guidelines

Generated code should follow these principles: modular, readable, reusable, documented, scientific-friendly.

Prefer: Python, NumPy, SciPy, Matplotlib, PyTorch, Pandas when relevant.

Functions should:
- Perform a single task
- Have clear inputs and outputs
- Include docstrings

## Scalability Planning

The planning system should evaluate whether the project requires scalable execution. Check for:

- Large datasets
- GPU training
- HPC execution
- Batch processing
- Parallel workflows

If needed, include: parallel data loading, GPU acceleration, batch processing, checkpoint saving, resume capability, logging.

## Implementation Phases

Complex projects should be implemented in stages:

- **Phase 1**: Project structure setup
- **Phase 2**: Core algorithm implementation
- **Phase 3**: Data pipeline integration
- **Phase 4**: Visualization and output generation
- **Phase 5**: Example scripts and testing
- **Phase 6**: Documentation

Each phase should correspond to tasks in the TODO list.

## Mathematical Model Section

If the project involves a scientific algorithm, include:

- Mathematical formulation
- Equations used
- Parameter definitions
- Assumptions

Example — Background removal in GPR:

Mean trace subtraction: `B(t) = (1/N) Σ A_i(t)`

Corrected trace: `A_i_corrected(t) = A_i(t) - B(t)`

## When to Use

Use this skill whenever:
- Planning a new coding project
- Designing geophysical workflows
- Implementing ML pipelines
- Creating scientific tools
- Organizing complex code generation tasks

## Critical Instruction

This skill must never generate full code implementations. It only produces the structured development plan. Code generation will be executed later using separate coding steps.
