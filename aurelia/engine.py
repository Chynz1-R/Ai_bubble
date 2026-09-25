from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Analysis:
    problem: str
    research_question: str
    evidence_status: list[str]
    known: list[str]
    hypotheses: list[str]
    recommended_pilot: list[str]
    estimated_benefit: list[str]
    uncertainty: list[str]
    human_approval_required: list[str]

    def render(self) -> str:
        sections = [
            ("Problem", [self.problem]),
            ("Research question", [self.research_question]),
            ("Evidence status", self.evidence_status),
            ("Known", self.known),
            ("Hypotheses", self.hypotheses),
            ("Recommended pilot", self.recommended_pilot),
            ("Estimated benefit", self.estimated_benefit),
            ("Uncertainty", self.uncertainty),
            ("Human approval required", self.human_approval_required),
        ]
        lines: list[str] = []
        for title, items in sections:
            lines.append(f"{title}:")
            for item in items:
                lines.append(f"- {item}")
            lines.append("")
        return "\n".join(lines).strip()


DOMAIN_PROFILES = (
    (
        ("flood", "coastal", "storm surge"),
        {
            "question": "Which mix of wetland restoration, selective barriers, and infrastructure elevation most reduces flood losses in the target region?",
            "known": [
                "Flood resilience work should compare protection gains against ecological and financial tradeoffs.",
                "High-impact infrastructure choices should be tested before large-scale rollout.",
            ],
            "hypotheses": [
                "Restored wetlands may reduce wave energy and downstream damage.",
                "Selective barriers may outperform continuous walls on cost per protected area.",
                "Elevating critical facilities may reduce long-term service disruption.",
            ],
            "pilot": [
                "Select one vulnerable coastal zone and define baseline flood-loss metrics.",
                "Test a limited wetland restoration segment with low-cost level sensors.",
                "Compare targeted barrier placement and elevation plans against a no-change baseline.",
            ],
            "benefit": [
                "Could reduce flood damage while preserving more ecosystem value than a single hard-infrastructure strategy.",
            ],
            "uncertainty": [
                "Results depend on storm intensity, sediment movement, local maintenance capacity, and land-use constraints.",
                "This output is a planning hypothesis, not site-specific engineering advice.",
            ],
            "approval": [
                "Environmental review",
                "Infrastructure and emergency-management review",
                "Community and budget approval",
            ],
        },
    ),
    (
        ("food", "crop", "hunger", "nutrition"),
        {
            "question": "Which combination of crops, irrigation, storage, and distribution can increase nutrition per liter of water in the target region?",
            "known": [
                "Food shortages usually involve interacting production, storage, logistics, and affordability constraints.",
                "Interventions should be evaluated against nutrition, water use, cost, and local adoption barriers.",
            ],
            "hypotheses": [
                "Improved storage may recover more food than expanding planted area alone.",
                "Crop mixes with lower water demand may improve nutrition resilience.",
                "Distribution changes may unlock gains even when yields remain flat.",
            ],
            "pilot": [
                "Run a small regional comparison of current practice versus improved storage and irrigation scheduling.",
                "Measure nutrition delivered, water use, spoilage, and farmer adoption over one growing cycle.",
            ],
            "benefit": [
                "Could improve food availability and resource efficiency without assuming a single cause of shortages.",
            ],
            "uncertainty": [
                "Local soil, market access, rainfall, and policy constraints may dominate the outcome.",
            ],
            "approval": [
                "Agronomy review",
                "Local farmer and community review",
                "Budget and procurement approval",
            ],
        },
    ),
    (
        ("cyber", "fraud", "misinformation", "impersonation"),
        {
            "question": "Which detection signals and human-review checkpoints most improve response quality while minimizing false positives?",
            "known": [
                "Defense systems must balance sensitivity with the cost of false alarms.",
                "Security interventions should preserve auditability and human escalation paths.",
            ],
            "hypotheses": [
                "Combining behavioral signals with provenance checks may detect abuse more reliably than either alone.",
                "Tiered escalation may reduce analyst load without automating irreversible actions.",
            ],
            "pilot": [
                "Evaluate detection rules on a labeled historical sample.",
                "Track precision, recall, and review time before broader deployment.",
            ],
            "benefit": [
                "Could improve detection quality while keeping high-impact decisions under human control.",
            ],
            "uncertainty": [
                "Adversaries adapt quickly, so measured performance may decay after deployment.",
            ],
            "approval": [
                "Security review",
                "Privacy and legal review",
                "Operational approval for escalation procedures",
            ],
        },
    ),
)


class AURELIAEngine:
    def analyze(self, problem: str) -> Analysis:
        cleaned_problem = " ".join(problem.split()).strip()
        if not cleaned_problem:
            raise ValueError("problem text is required")

        domain = self._domain_profile(cleaned_problem, cleaned_problem.lower())
        return Analysis(
            problem=cleaned_problem,
            research_question=domain["question"],
            evidence_status=[
                "No live literature, sensor feeds, or public records were retrieved by this local CLI run.",
                "Any empirical or numerical claim must be verified with cited sources before action.",
            ],
            known=domain["known"],
            hypotheses=domain["hypotheses"],
            recommended_pilot=domain["pilot"],
            estimated_benefit=domain["benefit"],
            uncertainty=domain["uncertainty"],
            human_approval_required=domain["approval"],
        )

    def _domain_profile(self, original_problem: str, normalized_problem: str) -> dict[str, list[str] | str]:
        for keywords, profile in DOMAIN_PROFILES:
            if any(self._matches_keyword(normalized_problem, word) for word in keywords):
                return profile

        formatted_problem = original_problem.rstrip("?.! ")
        return {
            "question": f"Which measurable interventions could address this problem most effectively: {formatted_problem}?",
            "known": [
                "The problem statement identifies a real-world issue that needs evidence before action.",
                "High-impact recommendations should be framed as testable proposals instead of certainties.",
            ],
            "hypotheses": [
                "A limited pilot may reveal whether the proposed intervention outperforms current practice.",
                "The main bottleneck may differ from first impressions and should be measured explicitly.",
            ],
            "pilot": [
                "Define success metrics, baseline conditions, and a small controlled test before scaling.",
                "Collect evidence on cost, risk, and benefit with domain experts in the loop.",
            ],
            "benefit": [
                "Could turn a vague problem into a safer, testable decision process.",
            ],
            "uncertainty": [
                "No domain-specific evidence was attached to the prompt.",
                "Further source review is required before any operational recommendation.",
            ],
            "approval": [
                "Relevant domain expert review",
                "Stakeholder review",
                "Formal authorization before irreversible action",
            ],
        }

    @staticmethod
    def _matches_keyword(problem: str, keyword: str) -> bool:
        return re.search(rf"\b{re.escape(keyword)}\b", problem) is not None
