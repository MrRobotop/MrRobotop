<!--
  Profile README for github.com/MrRobotop
  The block between the STATS markers is rewritten every day by .github/workflows/refresh-stats.yml.
  Everything else is yours to edit.
-->

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-dark.svg">
  <img alt="Rishabh Patil. AI engineer and researcher, co-founder and CEO of Valuren." src="assets/banner-light.svg" width="100%">
</picture>

<p align="center">
  <a href="https://www.linkedin.com/in/rishabh-ashok-patil/"><img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge"></a>
  <a href="https://huggingface.co/rishhh"><img alt="Hugging Face" src="https://img.shields.io/badge/Hugging_Face-FFD21E?style=for-the-badge&logo=huggingface&logoColor=black"></a>
  <a href="https://orcid.org/0009-0007-0868-9673"><img alt="ORCID" src="https://img.shields.io/badge/ORCID-A6CE39?style=for-the-badge&logo=orcid&logoColor=white"></a>
  <a href="https://www.rishabhpatil.com"><img alt="Website" src="https://img.shields.io/badge/rishabhpatil.com-24292f?style=for-the-badge"></a>
  <a href="mailto:rishabh.a.patil@outlook.com"><img alt="Email" src="https://img.shields.io/badge/Email-2a78d6?style=for-the-badge"></a>
</p>

I build AI systems that have to be right: evaluation for LLM agents, evidence-based claim verification, safe planning in learned latent spaces, and machine learning for markets. As co-founder and CEO of [Valuren](https://www.linkedin.com/company/valuren/), I give fashion and luxury brands digital product passports: verified authenticity, ownership history and royalties on resale. Based in London.

<!-- STATS:START -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/stats-dark.svg">
  <img alt="Live stats: 2,792 Hugging Face downloads (309 in the last 30 days), 28 models, 71 GitHub stars across 69 public repos, 491 PyPI downloads, 4 preprints. Updated 9 Oct 2026." src="assets/stats-light.svg" width="100%">
</picture>

<details>
<summary>Stats as a table</summary>

| Metric | Value |
| :-- | :-- |
| Hugging Face downloads, all time | 2,792 (VeriSci models 2,129 · SchemaSage models 403 · Datasets 260) |
| Hugging Face downloads, last 30 days | 309 |
| Models, datasets, Spaces | 28, 1, 2 |
| GitHub stars | 71 across 69 public repos |
| PyPI downloads, excluding mirrors | 491 (toploss 223 · clap-family 268) |
| Preprints | 4 (2026, on Zenodo) |

Updated 9 Oct 2026; refreshed daily by GitHub Actions.

</details>
<!-- STATS:END -->

## LLM systems

### VeriSci: scientific claim verification

<a href="https://huggingface.co/spaces/rishhh/verisci-claim-space"><picture><source media="(prefers-color-scheme: dark)" srcset="https://huggingface.co/datasets/huggingface/badges/resolve/main/open-in-hf-spaces-sm-dark.svg"><img alt="Try the live demo on Hugging Face Spaces" src="https://huggingface.co/datasets/huggingface/badges/resolve/main/open-in-hf-spaces-sm.svg"></picture></a>
<a href="https://huggingface.co/rishhh/verisci-claim-verifier-retrieval-adapted-seed123"><img alt="VeriSci model downloads, updated daily" src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2FMrRobotop%2FMrRobotop%2FHEAD%2Fassets%2Fdata%2Fbadge-verisci.json"></a>

Paste a scientific claim and VeriSci answers SUPPORTS, REFUTES or NOT ENOUGH INFO, with the sentences that justify the label. The Hub holds the retriever, the release verifier and the seeded ablations of evidence selection behind it.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/verisci-dark.svg">
  <img alt="VeriSci pipeline: claim, retrieve with BM25 and a fine-tuned e5 retriever, select evidence sentences, verify with a calibrated DeBERTa model, return a label with evidence. Retriever Recall@5 0.867. Verifier accuracy 0.905, macro-F1 0.874, calibration error 0.024. End to end on SciFact validation: 0.691 accuracy, 0.653 macro-F1." src="assets/verisci-light.svg" width="100%">
</picture>

### SchemaSage-SQL: safe text-to-SQL

<a href="https://huggingface.co/rishhh/schemasage-sql-qwen3-4b-clean-balanced-200"><picture><source media="(prefers-color-scheme: dark)" srcset="https://huggingface.co/datasets/huggingface/badges/resolve/main/model-on-hf-sm-dark.svg"><img alt="Model on Hugging Face" src="https://huggingface.co/datasets/huggingface/badges/resolve/main/model-on-hf-sm.svg"></picture></a>
<a href="https://huggingface.co/datasets/rishhh/schemasage-sql-clean-text2sql"><picture><source media="(prefers-color-scheme: dark)" srcset="https://huggingface.co/datasets/huggingface/badges/resolve/main/dataset-on-hf-sm-dark.svg"><img alt="Dataset on Hugging Face" src="https://huggingface.co/datasets/huggingface/badges/resolve/main/dataset-on-hf-sm.svg"></picture></a>
<a href="https://huggingface.co/rishhh/schemasage-sql-qwen3-4b-clean-balanced-200"><img alt="SchemaSage model downloads, updated daily" src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2FMrRobotop%2FMrRobotop%2FHEAD%2Fassets%2Fdata%2Fbadge-schemasage.json"></a>
<a href="https://huggingface.co/datasets/rishhh/schemasage-sql-clean-text2sql"><img alt="SchemaSage dataset downloads, updated daily" src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2FMrRobotop%2FMrRobotop%2FHEAD%2Fassets%2Fdata%2Fbadge-schemasage-data.json"></a>
<a href="https://github.com/MrRobotop/schemasage-sql"><img alt="Code on GitHub" src="https://img.shields.io/badge/code-schemasage--sql-24292f?style=flat-square&logo=github&logoColor=white"></a>

QLoRA adapters on Qwen3-4B that turn questions into read-only SQL grounded in the schema you pass in, with a safety layer that refuses destructive requests. A larger 8,192-row run scored higher on exact match and execution accuracy but missed one blocked refusal, so the smaller adapter shipped.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/schemasage-dark.svg">
  <img alt="SchemaSage-SQL release baseline on 64 cleaned held-out examples: 100% SQL parse validity, 98.3% schema adherence, 0% unsafe queries, 100% correct refusals. QLoRA on Qwen3-4B-Instruct-2507, trained on 111,444 cleaned examples, 10,862 of them refusals." src="assets/schemasage-light.svg" width="100%">
</picture>

### Evaluation and agent tooling

**[ariadne-eval](https://github.com/MrRobotop/ariadne-eval)** &nbsp;<img alt="Tests, live status" src="https://img.shields.io/github/actions/workflow/status/MrRobotop/ariadne-eval/tests.yml?style=flat-square&label=tests"> <img alt="285 tests" src="https://img.shields.io/badge/tests-285-2a78d6?style=flat-square"> <img alt="mypy strict" src="https://img.shields.io/badge/mypy-strict-2a78d6?style=flat-square"><br>
Trajectory-level tracing and scoring for multi-step, tool-using agents, so behaviour regressions show up before production.

**[evalforge](https://github.com/MrRobotop/evalforge)** &nbsp;<img alt="Tests, live status" src="https://img.shields.io/github/actions/workflow/status/MrRobotop/evalforge/tests.yml?style=flat-square&label=tests"> <img alt="538 tests" src="https://img.shields.io/badge/tests-538-2a78d6?style=flat-square"><br>
LLM evaluation for text-to-SQL and code: bootstrapped confidence intervals, calibrated LLM-as-judge, cost and latency Pareto fronts, and a CI gate that comments on every pull request.

**[financeMCPSuite](https://github.com/MrRobotop/financeMCPSuite)** and **[ml-intern-mcp-toolkit](https://github.com/MrRobotop/ml-intern-mcp-toolkit)** &nbsp;<img alt="CI, live status" src="https://img.shields.io/github/actions/workflow/status/MrRobotop/ml-intern-mcp-toolkit/ci.yml?style=flat-square&label=CI"> <img alt="Model Context Protocol" src="https://img.shields.io/badge/MCP-servers-24292f?style=flat-square&logo=modelcontextprotocol&logoColor=white"><br>
MCP servers: strategy, P&L and risk data for Claude; full-text arXiv reading and an experiment tracker for an autonomous ML agent.

## Research that ships

Each library pairs installable code with a first-author preprint.

### toploss

<a href="https://pypi.org/project/toploss/"><img alt="PyPI version" src="https://img.shields.io/pypi/v/toploss?style=flat-square&label=PyPI&color=2a78d6"></a>
<a href="https://github.com/MrRobotop/toploss/actions/workflows/ci.yaml"><img alt="CI, live status" src="https://img.shields.io/github/actions/workflow/status/MrRobotop/toploss/ci.yaml?style=flat-square&label=CI"></a>
<a href="https://doi.org/10.5281/zenodo.20497841"><img alt="DOI 10.5281/zenodo.20497841" src="https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20497841-2a78d6?style=flat-square"></a>

Five optimiser-free PyTorch regularisers that rebuild SAM, cautious weight decay, AdEMAMix and other recent optimiser ideas as loss penalties, so plain SGD or Adam gets their effect.

<img alt="SASP results: test cross-entropy over 120 epochs against the baseline, and Hessian trace at convergence, baseline about 171 against about 100 with SASP." src="assets/toploss-sasp.png" width="100%">

<sub>SASP, three seeds on CPU: Hessian trace at convergence down 41% (170.8 to 100.0) and test cross-entropy down 18%, at +15% wall-clock against +107% for SAM.</sub>

### clap-family

<a href="https://pypi.org/project/clap-family/"><img alt="PyPI version" src="https://img.shields.io/pypi/v/clap-family?style=flat-square&label=PyPI&color=2a78d6"></a>
<a href="https://github.com/MrRobotop/clap-family"><img alt="Checks, live status" src="https://img.shields.io/github/check-runs/MrRobotop/clap-family/HEAD?style=flat-square&label=checks"></a>
<img alt="72 tests" src="https://img.shields.io/badge/tests-72-2a78d6?style=flat-square">
<a href="https://doi.org/10.5281/zenodo.20467271"><img alt="DOI 10.5281/zenodo.20467271" src="https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20467271-2a78d6?style=flat-square"></a>

Conservative Lapse-Action Planning: reach the best safe region of a latent space, then stay there. Differentiable PyTorch adapters and seven planner variants.

<p align="center"><img alt="CLAP planning in a two-dimensional latent field: the trajectory reaches the safe target region and dwells there, avoiding a high-value reward trap and an unsafe out-of-distribution zone." src="assets/clap-planning.png" width="64%"></p>

<sub>In a 2-D latent field the planner reaches the safe target and dwells there (dwell 0.75), with zero time in the reward trap or the out-of-distribution zone.</sub>

### micro-world-model

<a href="https://github.com/MrRobotop/micro-world-model"><img alt="PyTorch" src="https://img.shields.io/badge/PyTorch-H--JEPA-24292f?style=flat-square&logo=pytorch&logoColor=white"></a>
<a href="https://doi.org/10.5281/zenodo.20480620"><img alt="DOI 10.5281/zenodo.20480620" src="https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20480620-2a78d6?style=flat-square"></a>

Hierarchical JEPA world model that plans in a 256-dimensional latent space with no reconstruction, no reward and no EMA target. Trained on about 49,000 sequences for 300 epochs.

## Quant systems

| Project | What it does | Built with |
| :-- | :-- | :-- |
| [**hft-market-data-processor**](https://github.com/MrRobotop/hft-market-data-processor) | Rust market-data engine with lock-free queues, benchmarked at 4M+ ticks per second with sub-microsecond latency | <img alt="Rust" src="https://img.shields.io/badge/Rust-24292f?style=flat-square&logo=rust&logoColor=white"> |
| [**statistical-arb-timesfm**](https://github.com/MrRobotop/statistical-arb-timesfm) | Pairs trading with Kalman-filter hedge ratios and TimesFM 2.5 forecasts, served through FastAPI to a React dashboard | <img alt="Python" src="https://img.shields.io/badge/Python-24292f?style=flat-square&logo=python&logoColor=white"> <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-24292f?style=flat-square&logo=fastapi&logoColor=white"> |
| [**timesfm-risk-engine**](https://github.com/MrRobotop/timesfm-risk-engine) | Value-at-Risk and stress testing on TimesFM 2.5 | <img alt="Python" src="https://img.shields.io/badge/Python-24292f?style=flat-square&logo=python&logoColor=white"> |

## Selected papers

- **Topological Loss Engineering:** Embedding Optimizer-Side Geometric Constraints Directly Into the Objective Function. Zenodo, 2026. [doi:10.5281/zenodo.20497841](https://doi.org/10.5281/zenodo.20497841)
- **Conservative Lapse-Action Planning:** A Variational Access-and-Dwell Framework for Safe Latent Trajectory Optimization. Zenodo, 2026. [doi:10.5281/zenodo.20467271](https://doi.org/10.5281/zenodo.20467271)
- **Micro-World Models:** Energy-Based Hierarchical Joint-Embedding Predictive Architectures for Continuous Kinematic Planning. Zenodo, 2026. [doi:10.5281/zenodo.20480620](https://doi.org/10.5281/zenodo.20480620)
- **Accelerated Machine Learning with Dependent Types.** MSc dissertation, University of St Andrews, 2025, supervised by Dr Edwin Brady. [Summary](https://www.rishabhpatil.com/research/ml-dependent-types)

Full list on [ORCID](https://orcid.org/0009-0007-0868-9673).

## Toolbox

<img alt="Python" src="https://img.shields.io/badge/Python-24292f?style=flat-square&logo=python&logoColor=white"> <img alt="PyTorch" src="https://img.shields.io/badge/PyTorch-24292f?style=flat-square&logo=pytorch&logoColor=white"> <img alt="Hugging Face Transformers and PEFT" src="https://img.shields.io/badge/Transformers_%C2%B7_PEFT-24292f?style=flat-square&logo=huggingface&logoColor=white"> <img alt="Model Context Protocol" src="https://img.shields.io/badge/MCP-24292f?style=flat-square&logo=modelcontextprotocol&logoColor=white"> <img alt="Pydantic" src="https://img.shields.io/badge/Pydantic-24292f?style=flat-square&logo=pydantic&logoColor=white"> <img alt="Gradio" src="https://img.shields.io/badge/Gradio-24292f?style=flat-square&logo=gradio&logoColor=white"> <img alt="FastAPI" src="https://img.shields.io/badge/FastAPI-24292f?style=flat-square&logo=fastapi&logoColor=white"> <img alt="Rust" src="https://img.shields.io/badge/Rust-24292f?style=flat-square&logo=rust&logoColor=white"> <img alt="C++" src="https://img.shields.io/badge/C%2B%2B-24292f?style=flat-square&logo=cplusplus&logoColor=white"> <img alt="Polars" src="https://img.shields.io/badge/Polars-24292f?style=flat-square&logo=polars&logoColor=white"> <img alt="Apache Kafka" src="https://img.shields.io/badge/Kafka-24292f?style=flat-square&logo=apachekafka&logoColor=white"> <img alt="Docker" src="https://img.shields.io/badge/Docker-24292f?style=flat-square&logo=docker&logoColor=white"> <img alt="GitHub Actions" src="https://img.shields.io/badge/GitHub_Actions-24292f?style=flat-square&logo=githubactions&logoColor=white">

## Background

MSc Artificial Intelligence, University of St Andrews. BSc Artificial Intelligence, VU Amsterdam. Before Valuren I co-founded RelAIable, an AI consultancy in Amsterdam, as Chief AI Officer.

Happy to talk about digital product passports, LLM evaluation or world models: [rishabh.a.patil@outlook.com](mailto:rishabh.a.patil@outlook.com)

<sub>Badges are live. The stats card refreshes daily through GitHub Actions.</sub>
