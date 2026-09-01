# Mitacs Globalink GRI 2027 Research Statement & Resume Narrative

**Applicant:** Kuldeep Gheghate  
**Institution:** Pimpri Chinchwad College of Engineering (PCCOE), Pune, India  
**Target Program:** Mitacs Globalink Research Internship (GRI) 2027 (Project 52752 / Complex Network Analytics)  

---

## 1. Resume Bullet Points

```text
Generalized K-Core Decomposition for Dynamic & Complex Networks | Python, NetworkX, NumPy, Streamlit
• Architected a high-performance graph analytics engine implementing Batagelj-Zaversnik's linear-time O(V+E) core decomposition algorithm from scratch with 100% test-verified parity against NetworkX.
• Engineered a localized dynamic incremental k-core maintenance algorithm, pruning redundant graph-wide recomputations to achieve up to 15x execution speedups across continuous edge mutation streams.
• Formulated and implemented generalized strength-based weighted core decomposition and multiplex joint core peeling algorithms across heterogeneous multi-relational network topologies.
• Built an interactive Streamlit research dashboard for live parameter exploration, real-time dynamic edge mutations, sub-network filtering, and empirical benchmark visualizations.
```

---

## 2. Mitacs Globalink Statement of Interest (Research Narrative)

**Applicant Profile & Research Background:**
As a third-year Computer Engineering undergraduate at PCCOE Pune with a published paper in IEEE ICISC-2026 on cryptographic verification and distributed systems, my research interests center on high-performance graph analytics, complex networks, and scalable discrete algorithms.

**Motivation & Technical Depth:**
In developing the **Generalized K-Core Analyzer (GKCA)**, I tackled the algorithmic limitations of static graph decomposition when applied to modern evolving networks. Core decomposition is essential for identifying dense graph nuclei, yet real-world networks undergo continuous topology mutations and possess multi-modal relationships.

Key technical milestones achieved in this project:
1. **Algorithmic Mastery & Linear Complexity:** Implemented Batagelj-Zaversnik's $\mathcal{O}(V + E)$ bin-sorting algorithm using positional index arrays (`vert`, `pos`, `deg`, `bin`), achieving optimal asymptotic time and space bounds.
2. **Incremental Dynamic Graph Processing:** Designed localized graph traversal algorithms that isolate candidate vertex sets affected by edge additions/deletions, cutting execution latency from global recomputation to localized subgraph traversal.
3. **Complex Network Generalizations:** Extended classical degree metrics to continuous node strength in weighted graphs and multi-layered joint degree vectors in multiplex topologies.
4. **Empirical Rigor & Open Science:** Authored an automated 24-test verification suite and built a full Streamlit dashboard to make theoretical insights accessible to evaluators.

**Alignment with Mitacs Host Lab:**
My hands-on experience in implementing advanced graph algorithms from scratch, designing dynamic incremental data structures, and conducting rigorous benchmarking directly aligns with the research goals of host Canadian institutions focusing on large-scale network science, algorithmic optimization, and computational graph theory.
