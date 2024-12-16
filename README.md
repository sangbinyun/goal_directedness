# **Goal-Directedness with LangGraph**

This repository contains a **goal-directed agent system** built with LangGraph, designed to implement a **problem decomposition strategy** inspired by cognitive science.

---

## **Project Structure**

The project is organized as follows:

```plaintext
goal_directedness/
│
├── metrics/                    # Metrics evaluation (details not provided)
├── states/                     # State management for LLM agents
│
├── evaluator.py                # Evaluation utilities
├── naive.py                    # Benchmark LLM for single-step reasoning
├── problem_decomposition.py    # LangGraph-based problem decomposition agent system
├── prompt.py                   # Prompts used in the agent system
├── run_problem_decomposition.py # Script to run the problem decomposition agent
├── utils.py                    # Utility functions (e.g., LLM loading)
├── main_evaluation.ipynb       # Main evaluation notebook
│
└── test/                       # Placeholder for tests (if any)
```

---

## **Setup Instructions**
### Install Dependencies
This project uses Poetry for dependency management. To set up the environment, run:

```bash
poetry install
```

## **Key Files**
- problem_decomposition.py:
Contains the LangGraph-based problem decomposition agent system.

- prompt.py
Stores the prompts used within the agent system.

- naive.py
A single-step LLM benchmark for performance comparison.

- run_problem_decomposition.py
A standalone script for testing the problem decomposition system without additional dependencies.

---

## How to Run
### 1. Main Evaluation
To execute the entire evaluation pipeline, run the main_evaluation.ipynb notebook. It integrates:

- Problem decomposition agent
- Single-step LLM benchmark
- Evaluation metrics

### 2. Run Problem Decomposition Only
To test only the problem decomposition agent, execute the following script:

*notes: currently working on minor problems occured while running the following code..

```bash
poetry run python goal_directedness/run_problem_decomposition.py
```

If you are not using poetry, run:
```bash
python goal_directedness/run_problem_decomposition.py
```
