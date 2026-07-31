# Operations Use Case Selection

> Practical decision support for selecting feasible, valuable analytics and AI use cases in operations and supply chain management.

This repository is part of Frank Kienle's Data2Value work: turning operations knowledge, analytics methods, and AI possibilities into assets that managers and teams can actually use.

The core question is simple, but often ignored:

**Which analytics or AI use cases are worth doing next — and which ones only look good in a slide deck?**

Many organizations do not fail because they have no ideas. They fail because they choose use cases without checking business value, data readiness, operational feasibility, adoption risk, and the decision process the use case is supposed to improve.

This repository helps structure that selection conversation.

---

## Who this is for

This material is useful for:

- operations and supply chain managers who need to prioritize analytics and AI ideas,
- analytics translators who connect business questions with technical teams,
- data science and BI teams who need better business framing before building models,
- lecturers, coaches, and facilitators teaching practical analytics use-case selection,
- teams preparing for AI-agent readiness in operations.

It is deliberately practical. The goal is not to collect AI buzzwords. The goal is to identify use cases that can survive contact with operational reality.

---

## Business problem

Analytics and AI initiatives often start with the wrong question:

> Which model or tool should we use?

A better starting point is:

> Which operational decision, process, or bottleneck should we improve — and is this use case feasible enough to justify investment?

Use-case selection should balance at least five dimensions:

1. **Business value** — cost, service, risk, quality, speed, sustainability, or resilience impact.
2. **Decision relevance** — whether the output changes a real management or operational decision.
3. **Data readiness** — availability, quality, granularity, ownership, and update frequency.
4. **Implementation feasibility** — process integration, systems, skills, governance, and change effort.
5. **Adoption risk** — whether people will trust, use, and maintain the solution.

For AI agents, this becomes even more important. A chatbot can advise. An agent changes workflows. That means the use case must be selected with stronger attention to risk, control points, accountability, and integration.

---

## What is inside this repository

The repository contains 25 operations and supply-chain analytics case briefs. The public `index.html` consolidates every brief into one searchable Blue Trust page, while the original interactive slide versions remain available as supporting material. The cases are organized around four operational domains:

| Domain | Focus | Example questions |
|---|---|---|
| SOURCE | Supplier and procurement analytics | Which suppliers create risk? Where do quality or capacity issues appear first? |
| MAKE | Manufacturing and production analytics | Which production constraints matter? Where can predictive maintenance or quality analytics help? |
| PLAN | Planning and inventory analytics | Where do forecasts, inventories, S&OP, and segmentation decisions need better support? |
| DELIVER | Fulfillment and logistics analytics | Where can customer service, network design, transportation, and routing decisions improve? |

Main folders:

- `index.html` — generated one-page case library with search, domain navigation, and expandable full briefs.
- `presentations/` — interactive HTML presentations by domain and use case.
- `assets/` — CSS, JavaScript, fonts, and presentation styling.
- `scripts/build_one_page.py` — rebuilds `index.html` from the 25 presentation sources.
- `videos/video-manifest.json` — placeholder configuration for YouTube integration.

---

## Use-case map

### SOURCE — supplier analytics

- Supplier Performance Metrics
- Supplier Risk Analysis
- Supplier Capacity Planning
- Compliance / Document Tracking
- Raw Materials Quality Analytics

### MAKE — manufacturing analytics

- Manufacturing Cost Analysis
- Production Scheduling
- Batch Size Optimization
- Predictive Maintenance
- AI for Quality Assurance
- Digital Twin
- Overall Equipment Effectiveness

### PLAN — planning analytics

- Demand Forecasting
- Inventory Optimization
- Multi-Echelon Inventory Optimization
- Vendor Managed Inventory
- Supply Chain Segmentation
- Sales & Operations Planning
- Supply Chain Risk Analysis

### DELIVER — delivery analytics

- Customer Satisfaction Analysis
- Order Fulfillment Analytics
- Supply Chain Network Design
- Transportation Cost Analysis
- Delivery Time Prediction
- Delivery Route Optimization

---

## How to use this material

### For managers and business teams

Use the repository as a structured discussion tool:

1. Search or browse the use-case domains on the one-page library.
2. Select 3-5 candidate use cases relevant to your operation.
3. Discuss value, feasibility, data readiness, and adoption risk.
4. Prioritize one small pilot before scaling the topic.
5. Define the decision the analytics or AI system should improve.

A useful rule:

> If nobody can name the decision that changes, the use case is not ready.

### For analytics translators

Use the cases as workshop prompts:

- What is the operational pain point?
- Who owns the decision?
- Which data is needed?
- What would a useful output look like?
- What would make users ignore the result?
- Is this a dashboard, prediction, optimization model, workflow automation, or future AI-agent candidate?

### For data science teams

Use the material before model building:

- separate business questions from model questions,
- identify data and process dependencies early,
- check whether the use case needs prediction, optimization, simulation, classification, monitoring, or simple reporting,
- avoid building technically interesting solutions for low-value decisions.

---

## Reproducibility and local setup

This repository is a static HTML learning platform. No backend setup is required for basic use. To regenerate the consolidated library after editing a presentation source, install Beautiful Soup and run the builder:

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/build_one_page.py
```

Recommended local preview:

```bash
cd operations_use_case_selection
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000
```

You can also open `index.html` directly in a browser, but using a small local web server is usually more reliable for loading assets and future embedded video configuration.

No private datasets are required. The material is educational and conceptual.

---

## Related content and next step

- AI in Operations: https://kienlef.github.io/ai-agents-in-operations/
- Operations Intelligence Map: https://kienlef.github.io/operations-intelligence-map/
- Twenty-seven decision owners and agent boundaries: https://kienlef.github.io/operations-use-cases/
- One-page analytical case library: https://kienlef.github.io/operations_use_case_selection/index.html
- YouTube channel until a specific playlist is curated: https://www.youtube.com/@frankkienle7312
- GitHub repository: https://github.com/kienlef/operations_use_case_selection
- Professional profile: https://linkedin.com/in/frankkienle

Recommended path: use the relationship map to understand the operating system, check the decision owner and agent boundary, then inspect the analytical brief on the one-page library.

---

## Why this matters for AI-agent readiness

AI agents in operations should not start with tool excitement. They should start with use-case discipline.

A good first agentic use case is usually not the most glamorous one. It is a workflow where:

- the decision process is repeated often,
- the data sources are known,
- the risk is bounded,
- human review points are clear,
- the business owner can explain the value,
- failure modes are visible and manageable.

This repository can therefore be used as a bridge from classic analytics use-case selection to more advanced AI-agent prioritization.

---

## Disclaimer and confidentiality note

This repository is a personal educational/knowledge project by Frank Kienle. It is not affiliated with, endorsed by, or representative of any employer. Code, examples, and datasets are for learning and demonstration purposes. No employer-confidential data or internal business logic is included.

Users should adapt the ideas to their own context and validate assumptions, data quality, risks, and governance requirements before applying them in real operations.

---

## License note

Content © Frank Kienle. Educational use is encouraged with attribution.

Before reusing substantial parts of the material in commercial training, products, or public derivative works, please check the repository license and contact Frank Kienle if the intended use is unclear.
