# SOFTWARE REQUIREMENTS SPECIFICATION (SRS)
## Generalized K-Core Decomposition for Dynamic and Complex Networks
### A Research-Oriented Graph Analytics Project

---

### Document Control

| Field | Value |
|---|---|
| **Prepared by** | Kuldeep Gheghate |
| **Institution** | Pimpri Chinchwad College of Engineering (PCCOE), Pune, India |
| **Programme** | B.E. Computer Engineering (Third Year, Class of 2027) |
| **Prepared for** | Mitacs Globalink Research Internship (GRI) 2027 – Project 52752 application support; also usable as a standalone GitHub / resume research project |
| **Document Type** | Software Requirements Specification (IEEE 830 / 29148 inspired) |
| **Version** | 1.0 |
| **Date** | August 29, 2026 |
| **Status** | Draft for guided, phase-by-phase implementation (build tool: Antigravity) |

---

### Revision History

| Version | Date | Author | Description |
|---|---|---|---|
| 1.0 | 29 Aug 2026 | Kuldeep Gheghate | Initial SRS created to drive phase-by-phase build of the Generalized K-Core project. |

---

### Purpose of This Document

This Software Requirements Specification (SRS) defines, without any implementation code, everything that must exist for the **"Generalized K-Core Decomposition for Dynamic and Complex Networks"** project to be considered complete: its functional and non-functional requirements, architecture, data model, technology stack, directory structure, installation requirements, phased build plan, and testing/acceptance criteria. It is written so that an AI build agent (such as Antigravity) or any developer can implement the project step by step, phase by phase, directly from this specification.

No source code is included anywhere in this document by design — only requirements, structure, configuration, and installation instructions. Implementation is intentionally left to the build phase that follows this SRS.

---

## Table of Contents

- [1. Introduction](#1-introduction)
  - [1.1 Purpose](#11-purpose)
  - [1.2 Scope](#12-scope)
  - [1.3 Definitions, Acronyms, and Abbreviations](#13-definitions-acronyms-and-abbreviations)
  - [1.4 References](#14-references)
  - [1.5 Document Overview](#15-document-overview)
- [2. Overall Description](#2-overall-description)
  - [2.1 Product Perspective](#21-product-perspective)
  - [2.2 Product Functions (Summary)](#22-product-functions-summary)
  - [2.3 User Classes and Characteristics](#23-user-classes-and-characteristics)
  - [2.4 Operating Environment](#24-operating-environment)
  - [2.5 Design and Implementation Constraints](#25-design-and-implementation-constraints)
  - [2.6 Assumptions and Dependencies](#26-assumptions-and-dependencies)
- [3. System Features (Functional Requirements)](#3-system-features-functional-requirements)
  - [FR-1: Graph Construction and Loading Module](#fr-1-graph-construction-and-loading-module)
  - [FR-2: Static K-Core Decomposition – Basic (Naive) Algorithm](#fr-2-static-k-core-decomposition--basic-naive-algorithm)
  - [FR-3: Efficient Core-Number Computation (Batagelj-Zaversnik)](#fr-3-efficient-core-number-computation-batagelj-zaversnik)
  - [FR-4: Baseline Validation Against NetworkX](#fr-4-baseline-validation-against-networkx)
  - [FR-5: Dynamic Graph Update Module](#fr-5-dynamic-graph-update-module)
  - [FR-6: Full Recomputation Baseline](#fr-6-full-recomputation-baseline)
  - [FR-7: Incremental K-Core Maintenance Module](#fr-7-incremental-k-core-maintenance-module)
  - [FR-8: Weighted K-Core Module](#fr-8-weighted-k-core-module)
  - [FR-9: Multi-Relational (Multiplex) K-Core Module](#fr-9-multi-relational-multiplex-k-core-module)
  - [FR-10: Experimentation and Benchmarking Module](#fr-10-experimentation-and-benchmarking-module)
  - [FR-11: Static Visualization Module (Matplotlib)](#fr-11-static-visualization-module-matplotlib)
  - [FR-12: Interactive Streamlit Dashboard Module](#fr-12-interactive-streamlit-dashboard-module)
  - [FR-13: Documentation and Reporting Module](#fr-13-documentation-and-reporting-module)
  - [FR-14: Version Control and GitHub Publishing Module](#fr-14-version-control-and-github-publishing-module)
- [4. External Interface Requirements](#4-external-interface-requirements)
  - [4.1 User Interface – Streamlit Dashboard](#41-user-interface--streamlit-dashboard)
  - [4.2 Hardware Interfaces](#42-hardware-interfaces)
  - [4.3 Software Interfaces](#43-software-interfaces)
  - [4.4 Communication Interfaces](#44-communication-interfaces)
- [5. Non-Functional Requirements](#5-non-functional-requirements)
  - [5.1 Performance Requirements](#51-performance-requirements)
  - [5.2 Reliability and Correctness](#52-reliability-and-correctness)
  - [5.3 Usability](#53-usability)
  - [5.4 Maintainability and Extensibility](#54-maintainability-and-extensibility)
  - [5.5 Portability](#55-portability)
  - [5.6 Security and Data Handling](#56-security-and-data-handling)
- [6. System Architecture](#6-system-architecture)
  - [6.1 High-Level Architecture](#61-high-level-architecture)
  - [6.2 Module Decomposition](#62-module-decomposition)
  - [6.3 Data Flow Description](#63-data-flow-description)
- [7. Data Requirements](#7-data-requirements)
  - [7.1 Input Data Formats](#71-input-data-formats)
  - [7.2 Internal Data Structures](#72-internal-data-structures)
  - [7.3 Output Data](#73-output-data)
- [8. Technology Stack and Installation Requirements](#8-technology-stack-and-installation-requirements)
  - [8.1 Core Technology Stack](#81-core-technology-stack)
  - [8.2 Prerequisite Software Installation](#82-prerequisite-software-installation)
  - [8.3 Project Environment Setup](#83-project-environment-setup)
  - [8.4 Library Installation Commands](#84-library-installation-commands)
  - [8.5 Freezing and Recording Dependencies](#85-freezing-and-recording-dependencies)
  - [8.6 Verifying the Environment](#86-verifying-the-environment)
- [9. Project Directory Structure](#9-project-directory-structure)
  - [9.1 Directory Responsibilities](#91-directory-responsibilities)
- [10. Development Roadmap (Implementation Phases)](#10-development-roadmap-implementation-phases)
  - [10.1 Sequencing Rule](#101-sequencing-rule)
  - [10.2 Explicit Exclusions During Early Phases](#102-explicit-exclusions-during-early-phases)
  - [10.3 Phase Summary](#103-phase-summary)
- [11. Testing Requirements](#11-testing-requirements)
  - [11.1 Unit Testing](#111-unit-testing)
  - [11.2 Integration Testing](#112-integration-testing)
  - [11.3 Performance Testing](#113-performance-testing)
  - [11.4 Acceptance Criteria (Project-Level)](#114-acceptance-criteria-project-level)
- [12. Final Deliverables](#12-final-deliverables)
- [13. Appendices](#13-appendices)
  - [Appendix A – Requirements Traceability Matrix](#appendix-a--requirements-traceability-matrix)
  - [Appendix B – Glossary Recap](#appendix-b--glossary-recap)
  - [Appendix C – References Recap](#appendix-c--references-recap)
  - [Appendix D – Explicit Non-Goals](#appendix-d--explicit-non-goals)

---

## 1. Introduction

### 1.1 Purpose
This document specifies the requirements for a research-grade software system that performs Generalized K-Core Decomposition on static, dynamic, weighted, and multi-relational (multiplex) graphs, benchmarks the performance of multiple algorithmic variants, and presents the results through an interactive dashboard. The system is intended to:
- Demonstrate a graduate-level understanding of graph algorithms built on the author's existing Data Structures and Algorithms (DSA) foundation.
- Produce a defensible, well-documented GitHub research artifact.
- Support a Mitacs Globalink Research Internship (GRI) 2027 application (Project reference 52752) as well as a resume-ready research project entry.

### 1.2 Scope
The system, referred to throughout this document as the **Generalized K-Core Analyzer (GKCA)**, shall:
- Load and construct graphs from files or synthetic generators.
- Compute k-core decomposition and core numbers for a static, unweighted, single-relation graph, first with a naive/basic algorithm and then with an efficient $\mathcal{O}(m)$ algorithm (Batagelj-Zaversnik).
- Support dynamic updates (edge insertion/deletion) and maintain k-core information incrementally, without a full recomputation, and compare this against full recomputation.
- Extend the decomposition to weighted graphs (weighted degree / strength-based cores).
- Extend the decomposition to multi-relational / multiplex graphs (multiple edge/relationship types).
- Run controlled experiments comparing static vs dynamic, naive vs efficient, unweighted vs weighted, and single-relation vs multi-relation variants, and record runtime, memory, and core-distribution metrics.
- Visualize graphs, core distributions, and benchmark results using Matplotlib, and provide an interactive Streamlit dashboard for exploration.
- Be organized, version-controlled, documented, and published as a clean public GitHub repository with a technical report, suitable for a Mitacs statement of interest and a resume bullet list.

**Out of Scope (Explicitly Excluded):** Distributed computing frameworks (e.g., Apache Spark), GPU/CUDA implementations, deep learning, graph neural networks, large-language-model components, production-grade Neo4j deployments, and million-node-scale datasets. These may be listed only as "possible future work."

### 1.3 Definitions, Acronyms, and Abbreviations

| Term | Definition |
|---|---|
| **K-Core** | A maximal connected subgraph in which every node has degree at least $k$ within that subgraph. |
| **Core Number / Coreness** | The largest $k$ for which a node belongs to the $k$-core; a per-node integer label produced by core decomposition. |
| **Degeneracy** | The maximum $k$ for which a non-empty $k$-core exists in the graph; equals the maximum core number. |
| **K-Shell** | The set of nodes whose core number is exactly $k$ (i.e., the nodes in the $k$-core but not the $(k+1)$-core). |
| **Batagelj-Zaversnik (BZ) Algorithm** | An $\mathcal{O}(m)$ (linear in edges) algorithm for computing exact core numbers of every node, used as the efficient baseline. |
| **Incremental / Dynamic Core Maintenance** | Updating core numbers only for the subset of nodes actually affected by an edge insertion or deletion, instead of recomputing the whole graph. |
| **Weighted K-Core** | A generalization of k-core where node "degree" is replaced by weighted degree (strength), and membership is governed by a weight threshold. |
| **Multi-Relational / Multiplex Graph** | A graph containing more than one type of edge/relationship between nodes (e.g., 'follows' vs 'collaborates'), each forming its own layer. |
| **Adjacency List** | A per-node list of neighboring nodes; the core in-memory graph representation used throughout the project. |
| **NetworkX** | The Python graph library used as the reference implementation and validation baseline (`core_number()`, `k_core()`). |
| **SRS** | Software Requirements Specification (this document). |
| **GKCA** | Generalized K-Core Analyzer — the short name used for this system throughout the document. |
| **Antigravity** | The AI build/coding agent that will consume this SRS, phase by phase, to implement the project. |

### 1.4 References
- NetworkX official documentation — `core_number()`, `k_core()`, and related algorithms ([networkx.org](https://networkx.org)).
- Batagelj, V. and Zaversnik, M., "An O(m) Algorithm for Cores Decomposition of Networks."
- Mitacs Globalink Research Internship (GRI) 2027 — official program page and eligibility requirements ([mitacs.ca](https://www.mitacs.ca)).
- Kuldeep Gheghate et al., paper accepted at the 10th International Conference on Inventive Systems and Control (ICISC-2026), on AI- and blockchain-based certificate verification (used as prior research credibility in the Mitacs narrative).
- Streamlit official documentation ([streamlit.io](https://streamlit.io)).
- Pandas, NumPy, and Matplotlib official documentation.

### 1.5 Document Overview
- **Section 2** provides the overall product description, user classes, operating environment, and constraints.
- **Section 3** defines the detailed functional requirements across all modules.
- **Section 4** specifies external interfaces, including the interactive dashboard layout.
- **Section 5** details non-functional requirements such as performance, reliability, and maintainability.
- **Section 6** describes the system architecture, layers, and data flow.
- **Section 7** outlines data requirements and internal structures.
- **Section 8** specifies the technology stack and complete setup instructions.
- **Section 9** establishes the repository directory structure.
- **Section 10** defines the phased implementation roadmap.
- **Section 11** details testing requirements and project acceptance criteria.
- **Section 12** summarizes the final deliverables.
- **Section 13** includes appendices covering requirements traceability, glossaries, references, and non-goals.

---

## 2. Overall Description

### 2.1 Product Perspective
GKCA is a new, standalone, locally-run research tool. It is not a plug-in to an existing system and has no dependency on any proprietary platform. It is composed of a Python algorithm/analysis layer and a Streamlit-based presentation layer, backed by flat files (edge lists, GraphML, CSV results) rather than a database. Neo4j and other graph databases are explicitly deferred to "optional later" status and are not part of the core deliverable.

### 2.2 Product Functions (Summary)
- **Graph construction:** Load and generate graphs from files or synthetic generators (Data layer).
- **Static decomposition:** Compute static k-core decomposition via naive and efficient $\mathcal{O}(m)$ algorithms (Core Algorithms).
- **Dynamic maintenance:** Handle edge insertion/deletion with full-recompute and incremental-maintenance modes (Dynamic).
- **Weighted decomposition:** Compute strength-based weighted cores (Weighted).
- **Multi-relational decomposition:** Compute multi-layer/multiplex cores (Multi-Relational).
- **Benchmarking & metrics:** Run comparative experiments and log metrics (Experiments).
- **Visualization:** Generate static charts via Matplotlib and provide an interactive Streamlit dashboard (Visualization).
- **Delivery:** Version control, documentation, technical reporting, and GitHub publication (Delivery).

### 2.3 User Classes and Characteristics

| User Class | Description | Technical Level |
|---|---|---|
| **Primary Developer / Researcher** | Kuldeep Gheghate — builds, tests, and documents the system; must be able to explain every design decision (data structures, complexity, why an edge insertion affects certain nodes). | Intermediate; strong in C++/DSA fundamentals, learning Python graph libraries and research methodology through this project. |
| **Evaluator / Reviewer** | A Mitacs professor, resume reviewer, or GitHub visitor who inspects the repository, README, report, and dashboard to judge technical depth. | Advanced (domain expert) — the system must therefore be defensible, not just functional. |
| **Dashboard End User** | Anyone exploring the tool interactively (including the developer during demos) to adjust $k$, filter by relationship type, and view live core statistics. | Non-specialist to intermediate; UI must be self-explanatory. |

### 2.4 Operating Environment
- **Operating System:** Windows 10/11 (primary), with cross-platform compatibility for Linux/macOS as a design goal since all chosen libraries are cross-platform.
- **Runtime:** Python 3.11 or 3.12 (64-bit).
- **Editor / IDE:** Visual Studio Code with the Python and Jupyter extensions.
- **Version Control:** Git (local) and GitHub (remote, public repository).
- **Dashboard Runtime:** Streamlit, served locally via `streamlit run` and viewed in any modern web browser (Chrome, Edge, Firefox).

### 2.5 Design and Implementation Constraints
- No distributed computing, GPU/CUDA, Apache Spark, deep learning, LLMs, or graph neural networks may be used to satisfy any requirement in this document.
- No production graph database (e.g., Neo4j) is required; it remains an optional, clearly-labeled future extension.
- Dataset scale is bounded to synthetic/medium real-world networks (indicatively hundreds to a few tens of thousands of nodes) — explicitly not massive/million-node datasets.
- Every algorithmic module must be implemented and understood by the author (not copied wholesale from an existing repository); NetworkX's built-in implementations are used strictly as a validation baseline, not as the submitted implementation.
- The project must remain explainable end-to-end: for every file in the repository, the author must be able to justify the data structure, complexity, and design choice if asked by a reviewer.

### 2.6 Assumptions and Dependencies
- The developer has administrative rights on the development machine to install Python, Git, and VS Code.
- Internet access is available for package installation (`pip`) and GitHub operations.
- NetworkX's `core_number()` and `k_core()` implementations remain available and stable across the Python/NetworkX versions used, for use as a validation baseline.
- A small number of real-world edge-list datasets (e.g., a citation, social, or collaboration network) are obtainable from public sources (e.g., SNAP, KONECT) for the "real-world dataset" phase.

---

## 3. System Features (Functional Requirements)

Each functional requirement (FR) below corresponds to one module of the system, maps directly to one or more files in the project directory structure (Section 9), and aligns with specific phases of the build roadmap (Section 10). Priority follows the MoSCoW standard: **Must have (M)**, **Should have (S)**, **Could have (C)**.

### FR-1: Graph Construction and Loading Module

| Field | Detail |
|---|---|
| **Priority** | Must have (M) |
| **Description** | Provides the foundation for every other module: creation of graphs from scratch, from files, or from generators, using an adjacency-list-based representation. |
| **Inputs** | Manually specified node/edge lists; CSV/edge-list files; GraphML files; synthetic graph generator parameters (node count, edge probability, degree distribution). |
| **Processing / Behaviour** | Validate input; construct an in-memory graph object; compute basic descriptive statistics (node count, edge count, average degree, density, connected components). |
| **Outputs** | An in-memory graph object; a printed/logged summary of graph statistics. |

### FR-2: Static K-Core Decomposition – Basic (Naive) Algorithm

| Field | Detail |
|---|---|
| **Priority** | Must have (M) |
| **Description** | Implements the conceptual, naive k-core algorithm: repeatedly remove nodes with degree less than $k$ until no such nodes remain, for a chosen $k$. |
| **Inputs** | A static graph; an integer $k$. |
| **Processing / Behaviour** | Iteratively scan node degrees, queue and remove nodes below the threshold, update neighbor degrees, and repeat until stable, exactly mirroring the DSA-style pseudocode: `Graph -> Degree calculation -> Queue nodes with degree < k -> Remove node -> Update neighbors -> Continue`. |
| **Outputs** | The k-core subgraph for the given $k$; the list of removed nodes and the order of removal (for later explanation/demonstration). |

### FR-3: Efficient Core-Number Computation (Batagelj-Zaversnik)

| Field | Detail |
|---|---|
| **Priority** | Must have (M) |
| **Description** | Implements the linear-time $\mathcal{O}(m)$ algorithm that computes the core number of every node in a single pass, rather than repeating naive removal for every $k$. |
| **Inputs** | A static graph. |
| **Processing / Behaviour** | Bucket-sort nodes by degree; repeatedly extract the minimum-degree node, assign its core number, decrement neighbor degrees, and re-bucket, following the standard BZ procedure. |
| **Outputs** | A dictionary/table mapping every node to its core number; the graph's degeneracy (maximum core number). |

### FR-4: Baseline Validation Against NetworkX

| Field | Detail |
|---|---|
| **Priority** | Must have (M) |
| **Description** | Cross-checks the author's own FR-2/FR-3 implementations against NetworkX's `core_number()` and `k_core()` to prove correctness. |
| **Inputs** | A static graph; the author's computed core numbers. |
| **Processing / Behaviour** | Run NetworkX's reference implementation on the same graph; compare node-by-node core numbers and report any mismatches. |
| **Outputs** | A pass/fail validation report per test graph, stored for the testing section (Section 11). |

### FR-5: Dynamic Graph Update Module

| Field | Detail |
|---|---|
| **Priority** | Must have (M) |
| **Description** | Supports adding and removing edges (and optionally nodes) on an existing graph after initial construction, simulating an evolving network. |
| **Inputs** | An existing graph; an edge (or node) to add or remove. |
| **Processing / Behaviour** | Apply the mutation to the in-memory graph; identify the set of nodes whose neighborhood changed as a result. |
| **Outputs** | The updated graph; the set of "affected" nodes to be passed to the maintenance module. |

### FR-6: Full Recomputation Baseline

| Field | Detail |
|---|---|
| **Priority** | Must have (M) |
| **Description** | Recomputes core numbers for the entire graph from scratch after every dynamic update, used as the correctness and performance baseline for incremental maintenance. |
| **Inputs** | The updated graph (from FR-5). |
| **Processing / Behaviour** | Re-run FR-3 (efficient static algorithm) on the whole graph after each update. |
| **Outputs** | Updated core numbers for all nodes; a recorded runtime for comparison against the incremental approach. |

### FR-7: Incremental K-Core Maintenance Module

| Field | Detail |
|---|---|
| **Priority** | Must have (M) |
| **Description** | The core research contribution: updates only the nodes whose core number can actually change after an edge insertion/deletion, instead of recomputing the whole graph. |
| **Inputs** | The updated graph; the set of affected nodes (from FR-5); prior core numbers. |
| **Processing / Behaviour** | Apply an incremental core-maintenance procedure that propagates changes outward only as far as necessary from the modified edge, stopping once no further core numbers change. |
| **Outputs** | Updated core numbers for the affected subset of nodes; a recorded runtime for comparison against full recomputation; a correctness check against FR-6's result on the same update. |

### FR-8: Weighted K-Core Module

| Field | Detail |
|---|---|
| **Priority** | Should have (S) |
| **Description** | Generalizes core decomposition to weighted graphs, where edges carry numeric weights (e.g., interaction strength). |
| **Inputs** | A graph with edge weights; a weighted-degree (strength) threshold or weighted-$k$ value. |
| **Processing / Behaviour** | Compute weighted degree (sum of incident edge weights) per node; iteratively remove nodes below the weighted threshold, updating neighbor weighted degrees, analogous to FR-2 but weight-aware. |
| **Outputs** | Weighted core numbers / weighted k-core subgraph; comparison against the unweighted result on the same graph. |

### FR-9: Multi-Relational (Multiplex) K-Core Module

| Field | Detail |
|---|---|
| **Priority** | Should have (S) |
| **Description** | Generalizes core decomposition to graphs with multiple relationship types (layers), e.g., 'follows' vs 'collaborates' edges between the same node set. |
| **Inputs** | A multi-relational graph (edges tagged by relationship type); a relationship filter (e.g., 'All', or a specific type); an integer $k$. |
| **Processing / Behaviour** | Either compute per-layer core decomposition and combine according to a clearly defined rule (e.g., union/intersection of layer-wise cores), or compute a combined-degree core across selected relationship types, per the design chosen in Phase 10. |
| **Outputs** | Core numbers under the selected relationship filter; comparison against single-relation results. |

### FR-10: Experimentation and Benchmarking Module

| Field | Detail |
|---|---|
| **Priority** | Must have (M) |
| **Description** | Runs controlled, repeatable experiments across all variants and records quantitative results. |
| **Inputs** | A set of test graphs (synthetic, of varying size/density, plus at least one real-world dataset); a list of experiment types to run. |
| **Processing / Behaviour** | Execute static vs dynamic, naive vs efficient, unweighted vs weighted, and single- vs multi-relation comparisons; time each run; record memory usage where feasible; repeat runs for statistical stability. |
| **Outputs** | Structured result tables (CSV, via Pandas) containing graph size, algorithm variant, runtime, and core-distribution statistics; ready for plotting. |

### FR-11: Static Visualization Module (Matplotlib)

| Field | Detail |
|---|---|
| **Priority** | Must have (M) |
| **Description** | Produces publication-quality static charts from experiment results and graph structure. |
| **Inputs** | Result tables from FR-10; graph objects and core-number dictionaries. |
| **Processing / Behaviour** | Generate: (a) core-number distribution histograms/bar charts, (b) runtime comparison charts (full recompute vs incremental), (c) a small-graph node-link visualization colored by core number. |
| **Outputs** | PNG/SVG chart files saved under the results directory, referenced by the technical report and README. |

### FR-12: Interactive Streamlit Dashboard Module

| Field | Detail |
|---|---|
| **Priority** | Must have (M) |
| **Description** | Provides an interactive, browser-based dashboard for exploring the graph, adjusting $k$, filtering by relationship type, mutating the graph, and viewing live statistics. |
| **Inputs** | A loaded graph (default demo graph plus optional file upload); user interactions from dashboard controls. |
| **Processing / Behaviour** | Render summary metrics (node/edge counts, maximum core); accept a $k$ value via slider/input; accept a relationship-type filter via dropdown; provide 'Add Edge' / 'Remove Edge' actions that trigger FR-5 through FR-7; render the graph visualization and core-distribution chart; display full-recompute vs incremental timing for the most recent update. |
| **Outputs** | A running local web application (`streamlit run dashboard/app.py`) matching the layout specified in Section 4.1. |

### FR-13: Documentation and Reporting Module

| Field | Detail |
|---|---|
| **Priority** | Must have (M) |
| **Description** | Produces the written artifacts that make the project explainable and presentable. |
| **Inputs** | All results, charts, and design decisions from the modules above. |
| **Processing / Behaviour** | Author a technical report covering problem statement, motivation, methodology, experiments, results, limitations, and future work; author a README with setup instructions, screenshots, and usage examples. |
| **Outputs** | A technical report (Markdown/PDF/Word) and a polished `README.md`. |

### FR-14: Version Control and GitHub Publishing Module

| Field | Detail |
|---|---|
| **Priority** | Must have (M) |
| **Description** | Ensures the project is tracked in Git from day one and published as a clean, public, well-organized GitHub repository. |
| **Inputs** | The full local project directory. |
| **Processing / Behaviour** | Initialize Git at project start; commit incrementally per phase/feature; maintain a `.gitignore`; push to a public GitHub repository once the structure and first working modules exist; tag releases at major milestones (e.g., after Phase 8, Phase 11, Phase 14). |
| **Outputs** | A public GitHub repository named `generalized-kcore-analysis` containing full history, README, LICENSE, and results. |

---

## 4. External Interface Requirements

### 4.1 User Interface – Streamlit Dashboard
The dashboard is the single primary user interface for GKCA. It must contain, at minimum, the following elements, laid out as a single-page application:

```text
GENERALIZED K-CORE ANALYZER
----------------------------------------
Nodes: <live count>        Edges: <live count>
Maximum Core: <live value>

K:  [ slider / numeric input ]
Relationship:  [ dropdown: All | <type 1> | <type 2> | ... ]

[ Add Edge ]   [ Remove Edge ]

GRAPH VISUALIZATION  (node-link diagram, nodes colored by core number)

Core Distribution  (bar chart of node count per core number)

Full Recompute: <seconds>        Incremental: <seconds>
```

#### Dashboard Element Requirements

| Element | Type | Requirement |
|---|---|---|
| **Summary metrics** | Text / metric widgets | Must always reflect the current in-memory graph state, updating immediately after any edge add/remove or file upload. |
| **K control** | Slider or numeric input | Range must span 1 to the current maximum core; changing it must instantly re-filter the displayed core subgraph. |
| **Relationship filter** | Dropdown | Must list 'All' plus every distinct relationship type present in the loaded multi-relational graph (FR-9). |
| **Add Edge / Remove Edge** | Buttons + input fields for node pair (and optional weight/type) | Must trigger FR-5 through FR-7 and refresh all dependent visuals and timing figures. |
| **Graph visualization** | Matplotlib figure embedded in Streamlit | Must color nodes by core number and remain legible for graphs up to a few hundred nodes; larger graphs may be sampled or summarized instead of rendered node-by-node. |
| **Core distribution chart** | Bar chart | Must show the number of nodes at each core number, recomputed after every change. |
| **Timing display** | Text metrics | Must show the most recent full-recomputation time and incremental-maintenance time side by side, in seconds, to at least 2 decimal places. |

### 4.2 Hardware Interfaces
- Standard laptop/desktop hardware; no specialized hardware (GPU, cluster) required.
- **Minimum recommended:** 4-core CPU, 8 GB RAM, 5 GB free disk space for the environment, datasets, and results.

### 4.3 Software Interfaces

| Interface | Requirement |
|---|---|
| **Operating System** | Windows 10/11 (primary target); Linux/macOS supported as the stack is cross-platform. |
| **Python Runtime** | CPython 3.11 or 3.12 (64-bit), managed via a project-local virtual environment (`.venv`). |
| **Package Manager** | `pip`, using a pinned `requirements.txt`. |
| **Editor** | Visual Studio Code with Python and Jupyter extensions. |
| **Version Control** | Git (local) integrated with a public GitHub remote repository. |
| **Browser** | Any modern browser (Chrome, Edge, Firefox) to view the Streamlit dashboard, served at `localhost`. |

### 4.4 Communication Interfaces
No network services are required for the core system to run — it is entirely local. The only network interactions are:
1. `pip` package downloads during setup.
2. Git/GitHub HTTPS or SSH operations for version control and publishing.
3. Optional downloading of public real-world datasets (e.g., from SNAP or KONECT) during Phase 6.

---

## 5. Non-Functional Requirements

### 5.1 Performance Requirements

| ID | Requirement |
|---|---|
| **NFR-1** | For a synthetic graph of about 5,000 nodes and 18,000–20,000 edges, full k-core recomputation should complete in well under 1 second on the target hardware (indicative target: $\le 1.0\text{ s}$), and incremental maintenance after a single edge update should be measurably faster than full recomputation (indicative target: $\le 0.2\text{ s}$), consistent with the incremental-vs-recompute comparison shown on the dashboard. |
| **NFR-2** | The efficient static algorithm (FR-3) must be empirically verified to scale near-linearly with the number of edges, consistent with its $\mathcal{O}(m)$ design, across at least three graph sizes in the benchmarking suite. |
| **NFR-3** | The Streamlit dashboard must reflect a slider/dropdown change or an edge add/remove action within a perceptibly interactive time (indicative target: $\le 1\text{–}2\text{ seconds}$) for graphs within the project's stated scale. |

### 5.2 Reliability and Correctness
- Every custom algorithm (FR-2, FR-3, FR-7, FR-8, FR-9) must be validated against NetworkX's reference implementation (FR-4) wherever an equivalent reference exists, and must produce identical core numbers on all test graphs before being considered complete.
- The incremental maintenance module (FR-7) must always agree with the full-recomputation module (FR-6) on the resulting core numbers after the same sequence of updates.
- The system must handle malformed or empty input graphs gracefully (clear error messages, no silent incorrect results).

### 5.3 Usability
- The dashboard must be usable by someone without a graph-theory background: every numeric field must be labeled, and the core concept ($k$, relationship filter) must be explained via short in-app captions or tooltips.
- The README must let a new reader clone the repository and get the dashboard running within about 10–15 minutes by following documented steps only.

### 5.4 Maintainability and Extensibility
- Each algorithmic variant (basic, efficient, dynamic, weighted, multi-relational) must live in its own clearly named module, so a new variant can be added without modifying unrelated modules.
- All experiment configurations (graph sizes, densities, repetitions) must be defined as data/config rather than hard-coded inline, to support re-running experiments with different parameters.

### 5.5 Portability
- The system must run on any machine with Python 3.11+ and the packages in `requirements.txt`, with no OS-specific code paths beyond documented Windows-vs-Unix setup command differences.

### 5.6 Security and Data Handling
- No credentials, tokens, or personal data are processed by the system; only public or synthetic graph data is used.
- Any GitHub access tokens used for publishing must never be committed to the repository (enforced via `.gitignore` and environment variables, not hard-coded).

---

## 6. System Architecture

### 6.1 High-Level Architecture
GKCA follows a four-layer architecture:
1. **Data Layer:** Loads and represents graphs (adjacency lists via NetworkX `Graph`/`MultiGraph` objects), independent of any algorithm.
2. **Algorithm Layer:** The static (basic + efficient), dynamic/incremental, weighted, and multi-relational k-core engines; pure functions/classes operating on the Data Layer's graph objects.
3. **Experimentation Layer:** Orchestrates the Algorithm Layer across many configurations, times executions, and records results via Pandas.
4. **Presentation Layer:** Matplotlib static charts and the Streamlit interactive dashboard, both consuming only the outputs of the layers below; the Presentation Layer must never contain algorithmic logic itself.

This layering directly maps onto the `src/`, `experiments/`, and `dashboard/` directories defined in Section 9, and enforces the constraint from Section 2.5 that every module remains individually explainable.

### 6.2 Module Decomposition

| Layer | Module (conceptual) | Responsible Requirement(s) |
|---|---|---|
| **Data** | Graph Loader | FR-1 |
| **Algorithm** | Basic K-Core Engine | FR-2 |
| **Algorithm** | Efficient K-Core Engine (BZ) | FR-3, FR-4 |
| **Algorithm** | Dynamic Update Engine | FR-5, FR-6 |
| **Algorithm** | Incremental Maintenance Engine | FR-7 |
| **Algorithm** | Weighted K-Core Engine | FR-8 |
| **Algorithm** | Multi-Relational K-Core Engine | FR-9 |
| **Experimentation** | Benchmark Runner + Metrics | FR-10 |
| **Presentation** | Static Charting | FR-11 |
| **Presentation** | Streamlit Dashboard | FR-12 |
| **Delivery** | Report / README Authoring | FR-13 |
| **Delivery** | Git / GitHub Publishing | FR-14 |

### 6.3 Data Flow Description
A typical end-to-end flow:
1. **Graph Loader** constructs or loads a graph from raw/processed sources or synthetic generators.
2. The appropriate **Algorithm Layer engine** computes core numbers for the requested mode (static, dynamic, weighted, or multi-relational).
3. For dynamic mode, the **Dynamic Update Engine** applies a mutation and hands the affected-node set to the **Incremental Maintenance Engine**, whose result is cross-checked against the **Full Recomputation baseline**.
4. The **Experimentation Layer** repeats this across configurations and writes structured result tables (CSV).
5. The **Presentation Layer** reads only those result tables and graph/core-number objects to render static charts and the live dashboard — it performs no computation of its own.

---

## 7. Data Requirements

### 7.1 Input Data Formats

| Format | Used For | Notes |
|---|---|---|
| **Edge list (CSV / TSV)** | Custom and real-world datasets | Columns: `source`, `target`, optional `weight`, optional `relationship_type`. |
| **GraphML (`.graphml`)** | Interchange with NetworkX / other tools | Preserves node/edge attributes natively. |
| **Synthetic generator parameters** | Controlled experiments (Erdős-Rényi, Barabási-Albert, etc., via NetworkX generators) | Parameters (node count, edge probability / attachment count, seed) stored as experiment config, not as data files. |

### 7.2 Internal Data Structures
- **Graph representation:** Adjacency-list based (NetworkX `Graph` for single-relation, `MultiGraph` or a layered dict-of-graphs for multi-relational data).
- **Degree table:** `node -> integer degree` (and, for weighted graphs, `node -> float weighted degree`).
- **Core-number table:** `node -> integer core number` (the primary output of every algorithm variant).
- **Affected-node set:** A set of node identifiers produced by the Dynamic Update Engine and consumed by the Incremental Maintenance Engine.
- **Benchmark record:** One row per experiment run, containing graph size, edge count, variant name, runtime (seconds), and summary core statistics (e.g., degeneracy, mean core number).

### 7.3 Output Data
- **Result tables:** CSV files under `results/tables/`, produced by the Experimentation Layer.
- **Charts:** PNG/SVG files under `results/graphs/`, produced by the Static Charting module.
- **Logs:** Plain-text or CSV run logs sufficient to reproduce any reported figure in the technical report.

---

## 8. Technology Stack and Installation Requirements

This section lists every tool and library required for the project, why it is required, and the exact installation command/action. No project source code is included here — only setup and installation instructions, per the project's "install only what you need, when you need it" philosophy.

### 8.1 Core Technology Stack

| Category | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.11 / 3.12 (64-bit) | Primary implementation language for all algorithms and tooling. |
| **Graph processing** | NetworkX | Graph construction, adjacency-list representation, and reference k-core implementations (`core_number()`, `k_core()`) used for validation. |
| **Numerical computing** | NumPy | Efficient numerical operations, array-based bookkeeping in algorithms and experiments. |
| **Data analysis** | Pandas | Structuring, storing, and analyzing benchmark results as tables (CSV). |
| **Visualization (static)** | Matplotlib | Core-distribution histograms, runtime comparison charts, small-graph node-link plots. |
| **Visualization (interactive)** | Streamlit | The interactive dashboard described in Section 4.1. |
| **Version control** | Git | Local commit history from day one of the project. |
| **Hosting** | GitHub | Public repository hosting, portfolio/resume visibility, and Mitacs-facing artifact. |
| **Editor** | Visual Studio Code | Primary development environment, with Python and Jupyter extensions. |
| **Optional (later, not for MVP)** | igraph | A potential faster/alternative graph backend for large-graph performance comparisons. |
| **Optional (later, not for MVP)** | Neo4j | A potential graph-database backend, only if the project is extended beyond its current scope. |

### 8.2 Prerequisite Software Installation

#### 8.2.1 Python
- Download the official installer from [python.org](https://www.python.org) (Windows) and run it.
- During installation, enable the **"Add python.exe to PATH"** option before clicking **"Install Now."**
- Verify installation in a terminal:
  ```powershell
  python --version
  pip --version
  ```
  Expected output resembles `Python 3.12.x` and `pip 24.x.x` (exact patch versions do not matter).

#### 8.2.2 Visual Studio Code
- Download and install VS Code from the official site ([code.visualstudio.com](https://code.visualstudio.com)).
- During installation, enable **"Add to PATH"** and **"Add Open with Code action."**
- After installation, install two extensions from the Extensions panel: **Python** (Microsoft) and **Jupyter** (Microsoft).

#### 8.2.3 Git
- Download and install Git for Windows from the official site ([git-scm.com](https://git-scm.com)), using default installation settings.
- Verify installation:
  ```powershell
  git --version
  ```

### 8.3 Project Environment Setup

#### 8.3.1 Create the Project Folder
Create a folder named `Generalized-K-Core-Analysis` in a convenient location (e.g., `Documents`), and open that folder in VS Code (`File -> Open Folder`).

#### 8.3.2 Create and Activate a Virtual Environment
```powershell
python -m venv .venv
```
On Windows PowerShell, activate it with:
```powershell
.venv\Scripts\Activate.ps1
```
On macOS/Linux, activate it with:
```bash
source .venv/bin/activate
```
A successful activation shows `(.venv)` at the start of the terminal prompt. If PowerShell blocks the activation script with an execution-policy error, that specific error message should be resolved individually rather than by broadly disabling security settings.

#### 8.3.3 Select the Interpreter in VS Code
- Open the Command Palette (`Ctrl+Shift+P`), run **"Python: Select Interpreter,"** and choose the interpreter located at `.venv\Scripts\python.exe` (Windows) or `.venv/bin/python` (macOS/Linux).

### 8.4 Library Installation Commands
Install libraries in stages, matching the phase in which they first become necessary (see Section 10), rather than installing everything at once.

#### 8.4.1 Stage 1 – Core Libraries (required from Phase 1 onward)
```powershell
pip install networkx pandas numpy matplotlib
```

#### 8.4.2 Stage 2 – Dashboard Library (required starting at the visualization/dashboard phase)
```powershell
pip install streamlit
```
*Streamlit is deliberately installed later so that the developer first understands the underlying algorithms before building the interactive layer on top of them.*

#### 8.4.3 Stage 3 – Optional / Future Extensions (not required for the core deliverable)
```powershell
pip install python-igraph   # optional, faster backend for large-graph experiments
# Neo4j: install the Neo4j Desktop application separately from neo4j.com if this
# optional extension is ever pursued; not required for the base project.
```

### 8.5 Freezing and Recording Dependencies
Once the core libraries for a given stage are installed and verified, the exact versions must be captured in a `requirements.txt` file at the project root, so the environment is fully reproducible:
```powershell
pip freeze > requirements.txt
```
`requirements.txt` must be committed to Git and kept up to date every time a new dependency stage is added (Stage 2 after the dashboard phase, Stage 3 only if the optional extensions are actually adopted).

### 8.6 Verifying the Environment
A minimal setup-verification script (conceptually named `test_setup.py`, content left to the build phase) must import `networkx`, `numpy`, `pandas`, and `matplotlib`, print their version numbers, and print a success message. Running it successfully is the exit criterion for Phase 1 in Section 10.

---

## 9. Project Directory Structure

The repository must follow this structure. It is intentionally explicit and modular so that the layering from Section 6 is visible directly in the file tree — this structure itself is treated as a technical deliverable, since it demonstrates software-engineering discipline to a reviewer.

```text
generalized-kcore-analysis/
|
|-- data/
|   |-- raw/                 # untouched source datasets (synthetic + real-world)
|   `-- processed/           # cleaned / converted edge lists ready for use
|
|-- src/
|   |-- graph_loader.py      # FR-1: loading & constructing graphs
|   |-- kcore_basic.py       # FR-2: naive static k-core
|   |-- kcore_efficient.py   # FR-3/FR-4: Batagelj-Zaversnik + NetworkX validation
|   |-- dynamic_kcore.py     # FR-5/FR-6/FR-7: updates, recompute, incremental maintenance
|   |-- weighted_kcore.py    # FR-8: weighted core decomposition
|   |-- multilayer_kcore.py  # FR-9: multi-relational / multiplex core decomposition
|   `-- metrics.py           # shared metrics/statistics helpers used across modules
|
|-- experiments/
|   |-- static_experiment.py     # FR-10: naive vs efficient benchmarking
|   |-- dynamic_experiment.py    # FR-10: full recompute vs incremental benchmarking
|   |-- weighted_experiment.py   # FR-10: weighted vs unweighted benchmarking
|   `-- multilayer_experiment.py # FR-10: single- vs multi-relation benchmarking
|
|-- dashboard/
|   `-- app.py                # FR-12: Streamlit dashboard entry point
|
|-- results/
|   |-- graphs/               # FR-11: exported PNG/SVG charts
|   `-- tables/                # FR-10: exported CSV result tables
|
|-- tests/                    # Section 11: unit/integration/validation tests
|
|-- requirements.txt          # Section 8.5: pinned dependency list
|-- README.md                 # FR-13: setup, usage, screenshots
`-- LICENSE
```

### 9.1 Directory Responsibilities

| Directory / File | Responsibility |
|---|---|
| `data/` | All input datasets, separated into raw (untouched) and processed (cleaned/converted) forms. |
| `src/` | All algorithm-layer and data-layer modules; the reusable "library" part of the project. |
| `experiments/` | Scripts that call into `src/` to run and record benchmark experiments; no dashboard or plotting logic lives here beyond writing result tables. |
| `dashboard/` | The Streamlit application only; imports from `src/`, contains no algorithm logic of its own. |
| `results/` | All generated artifacts (charts, tables) that back the technical report and README screenshots. |
| `tests/` | Automated tests validating correctness (see Section 11). |
| `requirements.txt` | Reproducible dependency pinning, updated per Section 8.5. |
| `README.md` | Project overview, setup instructions, usage guide, and screenshots — the first thing any reviewer reads. |
| `LICENSE` | An open-source license (e.g., MIT) so the repository is clearly reusable/citable. |

---

## 10. Development Roadmap (Implementation Phases)

The project must be built strictly phase by phase. A phase is not considered complete until its exit criterion is met; the next phase must not begin until the developer confirms completion (e.g., by stating "Phase N completed" to the build agent). This mirrors the guided, incremental approach already agreed for this project.

### 10.1 Sequencing Rule
The dependency order **Static K-Core $\rightarrow$ Dynamic K-Core $\rightarrow$ Weighted K-Core $\rightarrow$ Multi-Relational K-Core $\rightarrow$ Performance Evaluation** must be respected: each later phase's algorithms are built on top of the validated correctness of the earlier ones (in particular, FR-6/FR-7 depend on FR-3, and FR-8/FR-9 are natural generalizations of FR-2/FR-3).

### 10.2 Explicit Exclusions During Early Phases
During Phase 1 specifically, the following must not yet be done, to keep the environment minimal and understood: writing any k-core code, installing Neo4j/CUDA/PyTorch/TensorFlow/LLM libraries, downloading large/random datasets, building the Streamlit dashboard, copying a k-core implementation from another repository, or writing the final README.

### 10.3 Phase Summary

| Phase | Name | Key Activities | Exit Criterion |
|---|---|---|---|
| **1** | Environment Setup | Install Python, VS Code, Git; create project folder, virtual environment, Stage-1 libraries; verify with a setup-check script. | Setup-check script runs successfully and prints correct library versions. |
| **2** | Graph Fundamentals | Learn/revise nodes, edges, degree, adjacency lists, traversal, and complexity; build small example graphs. | Developer can explain graph representations and construct a small graph confidently. |
| **3** | Static K-Core from Scratch | Manually solve small k-core examples by hand; implement the naive algorithm (FR-2). | Naive algorithm produces correct k-cores on hand-verified small examples. |
| **4** | Core Numbers & Efficient Implementation | Implement the Batagelj-Zaversnik algorithm (FR-3); validate against NetworkX (FR-4). | Efficient algorithm's output exactly matches NetworkX's `core_number()` on all test graphs. |
| **5** | Experiments (Static) | Generate synthetic graphs of varying size/density; benchmark naive vs efficient (FR-10, FR-11). | Runtime comparison chart clearly shows the efficient algorithm scaling better than the naive one. |
| **6** | Real-World Dataset | Obtain and load a real-world network (e.g., from SNAP/KONECT); run static decomposition on it. | Core statistics for the real-world dataset are computed and documented. |
| **7** | Dynamic Graphs | Implement edge insertion/deletion (FR-5) and study how core numbers change. | Developer can demonstrate, with an example, exactly which nodes change core number after one edge update. |
| **8** | Incremental K-Core | Implement full-recompute baseline (FR-6) and incremental maintenance (FR-7); validate they agree. | Incremental result matches full-recompute result on every test case, and is measurably faster. |
| **9** | Weighted Graphs | Extend to weighted degree / strength-based cores (FR-8). | Weighted core results differ sensibly from unweighted results on a graph with varied edge weights, and are documented. |
| **10** | Multi-Relational Graphs | Extend to multiple relationship types (FR-9), with a clearly defined combination rule. | Core results are shown to change meaningfully when the relationship filter changes. |
| **11** | Comparative Experiments | Run the full experiment suite: static vs dynamic, naive vs efficient, unweighted vs weighted, single- vs multi-relation (FR-10). | All four comparison result tables and charts exist and are internally consistent. |
| **12** | Visualization | Build all Matplotlib charts (FR-11) and the Streamlit dashboard (FR-12), including Add/Remove Edge actions and live timing. | Dashboard matches the layout in Section 4.1 and runs via `streamlit run dashboard/app.py` without errors. |
| **13** | Research Report | Write the technical report: problem, motivation, methodology, experiments, results, limitations, future work (FR-13). | Report references every chart/table in `results/` and is internally consistent with the code. |
| **14** | GitHub Publishing | Clean the repository, finalize README with screenshots, add LICENSE, push full history (FR-14). | Public GitHub repository is browsable end-to-end by a stranger and matches Section 9's structure. |
| **15** | Resume & Mitacs Application | Convert the completed project into resume bullet points and a Mitacs statement-of-interest narrative. | Resume bullets and narrative reference only features that are actually implemented and demonstrable. |

---

## 11. Testing Requirements

### 11.1 Unit Testing
- Each algorithm module (`kcore_basic`, `kcore_efficient`, `dynamic_kcore`, `weighted_kcore`, `multilayer_kcore`) must have unit tests covering: an empty graph, a single node, a small hand-verifiable graph, and a disconnected graph.
- `kcore_efficient` results must be unit-tested against NetworkX's `core_number()` for equality on every test graph (FR-4).
- `dynamic_kcore`'s incremental results must be unit-tested against its own full-recomputation results for equality after every simulated update (FR-6 vs FR-7).

### 11.2 Integration Testing
- **End-to-end test:** Load a graph via `graph_loader` $\rightarrow$ run efficient static decomposition $\rightarrow$ apply a dynamic update $\rightarrow$ run incremental maintenance $\rightarrow$ confirm the experiment runner can record all of the above into a result table without error.
- **Dashboard integration test:** Launch the Streamlit app, perform an Add Edge action, and confirm the summary metrics, core distribution chart, and timing display all update consistently.

### 11.3 Performance Testing
- Benchmark the efficient static algorithm on at least three graph sizes and confirm runtime grows consistently with edge count, not worse than expected for an $\mathcal{O}(m)$ algorithm.
- Benchmark incremental maintenance vs full recomputation on the same sequence of updates and confirm incremental maintenance is consistently faster once graphs are non-trivially large.

### 11.4 Acceptance Criteria (Project-Level)

| # | Acceptance Criterion |
|---|---|
| **1** | All Must-have (M) functional requirements in Section 3 are implemented and pass their associated tests. |
| **2** | The efficient algorithm and the incremental-maintenance algorithm are validated as correct against their respective baselines on every test graph. |
| **3** | The Streamlit dashboard matches the layout and behaviour specified in Section 4.1 and runs without errors from a fresh clone plus documented setup steps. |
| **4** | The GitHub repository matches the structure in Section 9, includes a complete commit history from Phase 1 onward, and includes README, LICENSE, and a technical report. |
| **5** | The technical report and README together allow a reviewer to understand the motivation, method, and results without reading the source code. |

---

## 12. Final Deliverables

- A public GitHub repository, `generalized-kcore-analysis`, matching Section 9's structure, with full commit history from Phase 1.
- A working Streamlit dashboard (FR-12), runnable locally via a single documented command (`streamlit run dashboard/app.py`).
- A complete set of benchmark result tables (CSV) and charts (PNG/SVG) under `results/`.
- A written technical report covering problem statement, motivation, methodology, experiments, results, limitations, and future work.
- A polished `README.md` with setup instructions, usage guide, and screenshots.
- A resume-ready project entry:

> **Generalized K-Core Decomposition for Dynamic and Complex Graphs**  
> *Python | NetworkX | NumPy | Pandas | Streamlit*  
> - Implemented k-core decomposition and node coreness analysis for static network structures using adjacency-list-based graph processing.  
> - Extended the analysis to dynamic edge insertions/deletions, evaluating incremental core updates against full recomputation.  
> - Developed experimental variants for weighted and multi-relational graphs and analyzed changes in core membership under different graph conditions.  
> - Benchmarked algorithm performance across synthetic and real-world networks using execution time, graph size, and core-distribution metrics.  
> - Built an interactive Streamlit dashboard to visualize k-core structure, dynamic updates, and core-number distributions.  

- A Mitacs GRI 2027 (Project 52752) statement-of-interest narrative connecting the applicant's DSA foundation, this project, and prior research experience (the IEEE ICISC-2026 paper).

---

## 13. Appendices

### Appendix A – Requirements Traceability Matrix

| Requirement | Module | Implemented in Phase(s) |
|---|---|---|
| **FR-1** | Graph Construction and Loading | 1, 2 |
| **FR-2** | Static K-Core – Naive | 3 |
| **FR-3 / FR-4** | Efficient K-Core + Validation | 4 |
| **FR-5 / FR-6** | Dynamic Update + Full Recompute | 7, 8 |
| **FR-7** | Incremental Maintenance | 8 |
| **FR-8** | Weighted K-Core | 9 |
| **FR-9** | Multi-Relational K-Core | 10 |
| **FR-10** | Experimentation / Benchmarking | 5, 11 |
| **FR-11** | Static Visualization | 5, 12 |
| **FR-12** | Streamlit Dashboard | 12 |
| **FR-13** | Documentation and Reporting | 13 |
| **FR-14** | Git / GitHub Publishing | 1, 14 |

### Appendix B – Glossary Recap
See [Section 1.3](#13-definitions-acronyms-and-abbreviations) for the full glossary of terms (K-Core, Core Number, Degeneracy, K-Shell, Batagelj-Zaversnik Algorithm, Incremental/Dynamic Core Maintenance, Weighted K-Core, Multi-Relational Graph, Adjacency List, NetworkX, SRS, GKCA, Antigravity).

### Appendix C – References Recap
- NetworkX official documentation ([networkx.org](https://networkx.org)).
- Batagelj, V. and Zaversnik, M., "An O(m) Algorithm for Cores Decomposition of Networks."
- Mitacs Globalink Research Internship (GRI) 2027 official program page ([mitacs.ca](https://www.mitacs.ca)).
- Proceedings of the 10th International Conference on Inventive Systems and Control (ICISC-2026).
- Streamlit, Pandas, NumPy, and Matplotlib official documentation.

### Appendix D – Explicit Non-Goals
Restated for emphasis: this project explicitly excludes distributed computing (e.g., Apache Spark), GPU/CUDA implementations, deep learning, graph neural networks, LLM components, production-grade Neo4j architecture, and massive/million-node datasets. Any of these may be mentioned only under "future work" in the technical report, never as implemented requirements.

---
*End of SRS Document*
