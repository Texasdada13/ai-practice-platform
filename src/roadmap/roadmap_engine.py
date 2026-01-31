"""
AI Roadmap Engine

Generates multi-year AI implementation roadmaps based on:
- Assessment results
- Strategic priorities
- Resource constraints
- Risk tolerance
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json


class RoadmapHorizon(Enum):
    """Roadmap time horizons"""
    SHORT = "12 months"
    MEDIUM = "18 months"
    LONG = "24 months"
    EXTENDED = "36 months"


class InitiativeCategory(Enum):
    """Categories of AI initiatives"""
    FOUNDATION = "Foundation"
    CAPABILITY = "Capability Building"
    USE_CASE = "Use Case Delivery"
    OPTIMIZATION = "Optimization"
    INNOVATION = "Innovation"


class InitiativeStatus(Enum):
    """Initiative status"""
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    ON_HOLD = "On Hold"
    AT_RISK = "At Risk"


@dataclass
class Milestone:
    """A roadmap milestone"""
    name: str
    description: str
    target_date: str
    category: InitiativeCategory
    dependencies: List[str]
    success_criteria: List[str]
    owner: str
    status: InitiativeStatus = InitiativeStatus.NOT_STARTED


@dataclass
class Initiative:
    """A roadmap initiative"""
    id: str
    name: str
    description: str
    category: InitiativeCategory
    phase: int
    start_month: int
    duration_months: int
    effort_level: str  # Low, Medium, High
    investment_range: str
    dependencies: List[str]
    deliverables: List[str]
    success_metrics: List[str]
    risks: List[str]
    resources_required: Dict[str, Any]
    status: InitiativeStatus = InitiativeStatus.NOT_STARTED


@dataclass
class RoadmapPhase:
    """A phase in the roadmap"""
    phase_number: int
    name: str
    duration_months: int
    start_month: int
    objectives: List[str]
    initiatives: List[Initiative]
    milestones: List[Milestone]
    investment_range: str
    key_outcomes: List[str]
    risks: List[str]
    success_criteria: List[str]


@dataclass
class AIRoadmap:
    """Complete AI Implementation Roadmap"""
    organization_name: str
    horizon: RoadmapHorizon
    current_maturity: str
    target_maturity: str
    phases: List[RoadmapPhase]
    total_investment_range: str
    critical_path: List[str]
    key_dependencies: List[Dict[str, str]]
    risk_summary: List[Dict[str, str]]
    resource_plan: Dict[str, Any]
    governance_milestones: List[Milestone]
    generated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "organization_name": self.organization_name,
            "horizon": self.horizon.value,
            "current_maturity": self.current_maturity,
            "target_maturity": self.target_maturity,
            "phases": [
                {
                    "phase_number": p.phase_number,
                    "name": p.name,
                    "duration_months": p.duration_months,
                    "start_month": p.start_month,
                    "objectives": p.objectives,
                    "initiatives": [
                        {
                            "id": i.id,
                            "name": i.name,
                            "description": i.description,
                            "category": i.category.value,
                            "start_month": i.start_month,
                            "duration_months": i.duration_months,
                            "deliverables": i.deliverables
                        }
                        for i in p.initiatives
                    ],
                    "milestones": [
                        {
                            "name": m.name,
                            "target_date": m.target_date,
                            "success_criteria": m.success_criteria
                        }
                        for m in p.milestones
                    ],
                    "investment_range": p.investment_range,
                    "key_outcomes": p.key_outcomes
                }
                for p in self.phases
            ],
            "total_investment_range": self.total_investment_range,
            "critical_path": self.critical_path,
            "resource_plan": self.resource_plan,
            "generated_at": self.generated_at.isoformat()
        }

    def to_gantt_data(self) -> List[Dict[str, Any]]:
        """Export data for Gantt chart visualization"""
        tasks = []
        for phase in self.phases:
            # Add phase as parent task
            tasks.append({
                "id": f"phase_{phase.phase_number}",
                "name": phase.name,
                "start": phase.start_month,
                "duration": phase.duration_months,
                "type": "phase",
                "progress": 0
            })
            # Add initiatives as child tasks
            for init in phase.initiatives:
                tasks.append({
                    "id": init.id,
                    "name": init.name,
                    "start": init.start_month,
                    "duration": init.duration_months,
                    "type": "initiative",
                    "category": init.category.value,
                    "parent": f"phase_{phase.phase_number}",
                    "progress": 0
                })
        return tasks


class AIRoadmapEngine:
    """
    Generates AI Implementation Roadmaps.

    Creates phased roadmaps based on assessment results,
    considering dependencies, resources, and risk tolerance.
    """

    # Initiative templates by category
    INITIATIVE_TEMPLATES = {
        InitiativeCategory.FOUNDATION: [
            {
                "id": "found_001",
                "name": "AI Governance Framework",
                "description": "Establish AI governance structure, policies, and processes",
                "duration_months": 3,
                "effort_level": "Medium",
                "investment_range": "$100K-$200K",
                "deliverables": ["Governance charter", "AI policies", "Review process"],
                "success_metrics": ["Policies approved", "Governance body operational"]
            },
            {
                "id": "found_002",
                "name": "Data Foundation for AI",
                "description": "Assess and improve data quality, establish data governance for AI",
                "duration_months": 6,
                "effort_level": "High",
                "investment_range": "$200K-$500K",
                "deliverables": ["Data quality baseline", "Data catalog", "Governance framework"],
                "success_metrics": ["Data quality score improved 20%", "Catalog coverage 80%"]
            },
            {
                "id": "found_003",
                "name": "AI Strategy & Roadmap",
                "description": "Develop comprehensive AI strategy aligned with business objectives",
                "duration_months": 2,
                "effort_level": "Medium",
                "investment_range": "$50K-$150K",
                "deliverables": ["AI strategy document", "Use case portfolio", "Investment plan"],
                "success_metrics": ["Strategy approved", "Budget allocated"]
            }
        ],
        InitiativeCategory.CAPABILITY: [
            {
                "id": "cap_001",
                "name": "AI/ML Platform Implementation",
                "description": "Deploy enterprise AI/ML platform with MLOps capabilities",
                "duration_months": 6,
                "effort_level": "High",
                "investment_range": "$300K-$800K",
                "deliverables": ["ML platform", "CI/CD pipelines", "Model registry"],
                "success_metrics": ["Platform operational", "First model deployed"]
            },
            {
                "id": "cap_002",
                "name": "AI Talent Acquisition & Development",
                "description": "Build AI team and develop organization-wide AI literacy",
                "duration_months": 12,
                "effort_level": "High",
                "investment_range": "$500K-$1.5M",
                "deliverables": ["AI team hired", "Training programs", "CoE established"],
                "success_metrics": ["Team of 5-10", "50% leadership trained"]
            },
            {
                "id": "cap_003",
                "name": "Data Engineering Modernization",
                "description": "Build modern data pipelines and feature store for AI",
                "duration_months": 6,
                "effort_level": "High",
                "investment_range": "$200K-$600K",
                "deliverables": ["Data pipelines", "Feature store", "Real-time capabilities"],
                "success_metrics": ["Pipelines operational", "Features available in <24hrs"]
            }
        ],
        InitiativeCategory.USE_CASE: [
            {
                "id": "uc_001",
                "name": "AI Pilot Program",
                "description": "Execute initial AI pilots to demonstrate value",
                "duration_months": 4,
                "effort_level": "Medium",
                "investment_range": "$100K-$300K",
                "deliverables": ["2-3 pilots completed", "Business value documented", "Lessons learned"],
                "success_metrics": ["Pilots successful", "Measurable ROI"]
            },
            {
                "id": "uc_002",
                "name": "Production AI Scaling",
                "description": "Scale successful pilots to production deployment",
                "duration_months": 6,
                "effort_level": "High",
                "investment_range": "$300K-$800K",
                "deliverables": ["Production deployments", "Monitoring in place", "Support model"],
                "success_metrics": ["3+ models in production", "SLAs met"]
            }
        ],
        InitiativeCategory.OPTIMIZATION: [
            {
                "id": "opt_001",
                "name": "AI Operations Optimization",
                "description": "Optimize AI operations for efficiency and reliability",
                "duration_months": 4,
                "effort_level": "Medium",
                "investment_range": "$100K-$250K",
                "deliverables": ["Automated retraining", "Performance optimization", "Cost optimization"],
                "success_metrics": ["50% faster deployment", "20% cost reduction"]
            }
        ],
        InitiativeCategory.INNOVATION: [
            {
                "id": "inn_001",
                "name": "Advanced AI Exploration",
                "description": "Explore advanced AI capabilities (GenAI, autonomous systems)",
                "duration_months": 6,
                "effort_level": "Medium",
                "investment_range": "$150K-$400K",
                "deliverables": ["Innovation pilots", "Technology assessment", "Recommendations"],
                "success_metrics": ["New capabilities identified", "Innovation pipeline"]
            }
        ]
    }

    def __init__(self):
        pass

    def generate_roadmap(
        self,
        organization_name: str,
        assessment_result: Dict[str, Any],
        horizon: RoadmapHorizon = RoadmapHorizon.MEDIUM,
        priorities: Optional[List[str]] = None,
        constraints: Optional[Dict[str, Any]] = None
    ) -> AIRoadmap:
        """
        Generate an AI implementation roadmap.

        Args:
            organization_name: Name of organization
            assessment_result: Assessment results
            horizon: Time horizon for roadmap
            priorities: Optional priority areas
            constraints: Optional constraints (budget, timeline, etc.)

        Returns:
            AIRoadmap
        """
        maturity_level = assessment_result.get("maturity_level", "Exploring")
        overall_score = assessment_result.get("overall_score", 0)
        dimension_scores = assessment_result.get("dimension_scores", {})

        # Determine target maturity
        target_maturity = self._determine_target_maturity(maturity_level, horizon)

        # Generate phases based on maturity
        phases = self._generate_phases(maturity_level, horizon, dimension_scores, constraints)

        # Calculate total investment
        total_investment = self._calculate_total_investment(phases)

        # Identify critical path
        critical_path = self._identify_critical_path(phases)

        # Key dependencies
        dependencies = self._identify_dependencies(phases)

        # Risk summary
        risks = self._summarize_risks(phases, maturity_level)

        # Resource plan
        resource_plan = self._build_resource_plan(phases, maturity_level)

        # Governance milestones
        gov_milestones = self._create_governance_milestones(phases)

        return AIRoadmap(
            organization_name=organization_name,
            horizon=horizon,
            current_maturity=maturity_level,
            target_maturity=target_maturity,
            phases=phases,
            total_investment_range=total_investment,
            critical_path=critical_path,
            key_dependencies=dependencies,
            risk_summary=risks,
            resource_plan=resource_plan,
            governance_milestones=gov_milestones
        )

    def _determine_target_maturity(self, current: str, horizon: RoadmapHorizon) -> str:
        """Determine realistic target maturity based on horizon"""
        maturity_progression = ["Exploring", "Experimenting", "Scaling", "Optimizing"]

        try:
            current_idx = maturity_progression.index(current)
        except ValueError:
            current_idx = 0

        # How many levels can we advance based on horizon
        advancement = {
            RoadmapHorizon.SHORT: 1,
            RoadmapHorizon.MEDIUM: 1,
            RoadmapHorizon.LONG: 2,
            RoadmapHorizon.EXTENDED: 2
        }

        target_idx = min(current_idx + advancement[horizon], len(maturity_progression) - 1)
        return maturity_progression[target_idx]

    def _generate_phases(
        self,
        maturity: str,
        horizon: RoadmapHorizon,
        dimension_scores: Dict,
        constraints: Optional[Dict]
    ) -> List[RoadmapPhase]:
        """Generate roadmap phases based on maturity level"""
        phases = []
        current_month = 0

        # Determine number of phases based on horizon
        num_phases = {
            RoadmapHorizon.SHORT: 3,
            RoadmapHorizon.MEDIUM: 4,
            RoadmapHorizon.LONG: 4,
            RoadmapHorizon.EXTENDED: 5
        }[horizon]

        # Phase durations vary by horizon
        total_months = int(horizon.value.split()[0])

        # Generate phases based on maturity
        if maturity in ["Exploring", "Experimenting"]:
            phases = self._generate_early_maturity_phases(total_months, dimension_scores)
        else:
            phases = self._generate_advanced_maturity_phases(total_months, dimension_scores)

        return phases

    def _generate_early_maturity_phases(
        self,
        total_months: int,
        dimension_scores: Dict
    ) -> List[RoadmapPhase]:
        """Generate phases for Exploring/Experimenting maturity"""
        phases = []

        # Phase 1: Foundation (0-6 months)
        phase1_initiatives = [
            Initiative(
                id="found_001", name="AI Governance Framework",
                description="Establish AI governance structure and policies",
                category=InitiativeCategory.FOUNDATION,
                phase=1, start_month=0, duration_months=3,
                effort_level="Medium", investment_range="$100K-$200K",
                dependencies=[], deliverables=["Governance charter", "AI policies"],
                success_metrics=["Policies approved"], risks=["Executive alignment"],
                resources_required={"FTEs": 2, "External": "Consulting support"}
            ),
            Initiative(
                id="found_002", name="Data Foundation Assessment",
                description="Assess data readiness and establish improvement plan",
                category=InitiativeCategory.FOUNDATION,
                phase=1, start_month=1, duration_months=4,
                effort_level="High", investment_range="$150K-$350K",
                dependencies=[], deliverables=["Data quality baseline", "Improvement plan"],
                success_metrics=["Assessment complete"], risks=["Data access"],
                resources_required={"FTEs": 3, "External": "Data consultants"}
            ),
            Initiative(
                id="found_003", name="AI Strategy Development",
                description="Develop AI strategy and use case portfolio",
                category=InitiativeCategory.FOUNDATION,
                phase=1, start_month=0, duration_months=2,
                effort_level="Medium", investment_range="$50K-$100K",
                dependencies=[], deliverables=["AI strategy", "Use case portfolio"],
                success_metrics=["Strategy approved"], risks=["Stakeholder alignment"],
                resources_required={"FTEs": 1, "External": "Strategy consulting"}
            )
        ]

        phase1_milestones = [
            Milestone(
                name="AI Governance Approved", description="AI governance framework approved by leadership",
                target_date="Month 3", category=InitiativeCategory.FOUNDATION,
                dependencies=[], success_criteria=["Charter signed", "Policies approved"],
                owner="AI Lead"
            ),
            Milestone(
                name="AI Strategy Approved", description="AI strategy and roadmap approved",
                target_date="Month 2", category=InitiativeCategory.FOUNDATION,
                dependencies=[], success_criteria=["Executive sign-off", "Budget allocated"],
                owner="AI Lead"
            )
        ]

        phases.append(RoadmapPhase(
            phase_number=1, name="Foundation",
            duration_months=6, start_month=0,
            objectives=[
                "Establish AI governance and policies",
                "Assess and plan data improvements",
                "Develop AI strategy and use case portfolio",
                "Secure executive sponsorship and budget"
            ],
            initiatives=phase1_initiatives,
            milestones=phase1_milestones,
            investment_range="$300K-$650K",
            key_outcomes=["Governance operational", "Strategy approved", "Data baseline established"],
            risks=["Executive alignment", "Data access challenges"],
            success_criteria=["Governance in place", "Strategy approved", "Pilots selected"]
        ))

        # Phase 2: Build (6-12 months)
        phase2_initiatives = [
            Initiative(
                id="cap_001", name="AI/ML Platform Setup",
                description="Deploy initial AI/ML platform capabilities",
                category=InitiativeCategory.CAPABILITY,
                phase=2, start_month=6, duration_months=5,
                effort_level="High", investment_range="$300K-$600K",
                dependencies=["found_002"], deliverables=["ML platform", "Dev environment"],
                success_metrics=["Platform operational"], risks=["Technical complexity"],
                resources_required={"FTEs": 4, "External": "Platform vendor"}
            ),
            Initiative(
                id="uc_001", name="AI Pilot Execution",
                description="Execute 2-3 AI pilots to demonstrate value",
                category=InitiativeCategory.USE_CASE,
                phase=2, start_month=7, duration_months=4,
                effort_level="Medium", investment_range="$150K-$350K",
                dependencies=["found_001", "found_003"], deliverables=["Pilot results", "Lessons learned"],
                success_metrics=["Pilots completed", "Value demonstrated"], risks=["Data quality", "Scope creep"],
                resources_required={"FTEs": 3, "External": "ML consultants"}
            ),
            Initiative(
                id="cap_002", name="AI Team Building",
                description="Hire core AI team and launch training programs",
                category=InitiativeCategory.CAPABILITY,
                phase=2, start_month=6, duration_months=6,
                effort_level="High", investment_range="$400K-$800K",
                dependencies=[], deliverables=["Core team hired", "Training launched"],
                success_metrics=["Team of 5+", "Training programs live"], risks=["Talent availability"],
                resources_required={"FTEs": 5, "External": "Recruiting support"}
            )
        ]

        phase2_milestones = [
            Milestone(
                name="ML Platform Operational", description="AI/ML platform deployed and operational",
                target_date="Month 10", category=InitiativeCategory.CAPABILITY,
                dependencies=["Data foundation"], success_criteria=["Platform live", "First model deployed"],
                owner="Platform Lead"
            ),
            Milestone(
                name="Pilots Completed", description="Initial AI pilots completed with results",
                target_date="Month 11", category=InitiativeCategory.USE_CASE,
                dependencies=["Governance"], success_criteria=["2+ pilots done", "ROI documented"],
                owner="AI Lead"
            )
        ]

        phases.append(RoadmapPhase(
            phase_number=2, name="Build",
            duration_months=6, start_month=6,
            objectives=[
                "Deploy AI/ML platform",
                "Execute initial AI pilots",
                "Build core AI team",
                "Launch AI training programs"
            ],
            initiatives=phase2_initiatives,
            milestones=phase2_milestones,
            investment_range="$850K-$1.75M",
            key_outcomes=["Platform operational", "Pilots demonstrating value", "Team in place"],
            risks=["Talent acquisition", "Technical complexity"],
            success_criteria=["Platform live", "2+ successful pilots", "Core team hired"]
        ))

        # Phase 3: Scale (12-18 months)
        phase3_initiatives = [
            Initiative(
                id="uc_002", name="Production AI Deployment",
                description="Scale successful pilots to production",
                category=InitiativeCategory.USE_CASE,
                phase=3, start_month=12, duration_months=5,
                effort_level="High", investment_range="$300K-$600K",
                dependencies=["uc_001", "cap_001"], deliverables=["Production deployments", "Monitoring"],
                success_metrics=["3+ in production", "SLAs met"], risks=["Operations readiness"],
                resources_required={"FTEs": 4, "External": "MLOps support"}
            ),
            Initiative(
                id="cap_003", name="MLOps Implementation",
                description="Implement MLOps for automated model lifecycle",
                category=InitiativeCategory.CAPABILITY,
                phase=3, start_month=12, duration_months=4,
                effort_level="Medium", investment_range="$150K-$300K",
                dependencies=["cap_001"], deliverables=["CI/CD for ML", "Monitoring", "Automation"],
                success_metrics=["Automated deployment", "Model monitoring"], risks=["Process change"],
                resources_required={"FTEs": 2, "External": "MLOps consultants"}
            )
        ]

        phase3_milestones = [
            Milestone(
                name="Production AI Live", description="Multiple AI use cases in production",
                target_date="Month 17", category=InitiativeCategory.USE_CASE,
                dependencies=["Platform", "Pilots"], success_criteria=["3+ models live", "Value tracking"],
                owner="AI Lead"
            )
        ]

        phases.append(RoadmapPhase(
            phase_number=3, name="Scale",
            duration_months=6, start_month=12,
            objectives=[
                "Scale AI pilots to production",
                "Implement MLOps practices",
                "Expand AI use case portfolio",
                "Achieve measurable ROI"
            ],
            initiatives=phase3_initiatives,
            milestones=phase3_milestones,
            investment_range="$450K-$900K",
            key_outcomes=["Multiple AI in production", "MLOps operational", "ROI demonstrated"],
            risks=["Operations scaling", "Change management"],
            success_criteria=["3+ production AI", "Automated operations", "$500K+ value"]
        ))

        return phases

    def _generate_advanced_maturity_phases(
        self,
        total_months: int,
        dimension_scores: Dict
    ) -> List[RoadmapPhase]:
        """Generate phases for Scaling/Optimizing maturity"""
        # Advanced organizations focus on optimization and innovation
        phases = []

        # Phase 1: Optimize (0-6 months)
        phase1_initiatives = [
            Initiative(
                id="opt_001", name="AI Operations Excellence",
                description="Optimize AI operations for efficiency and scale",
                category=InitiativeCategory.OPTIMIZATION,
                phase=1, start_month=0, duration_months=4,
                effort_level="Medium", investment_range="$150K-$300K",
                dependencies=[], deliverables=["Optimized pipelines", "Cost reduction"],
                success_metrics=["30% faster deployment", "20% cost reduction"],
                risks=["Process disruption"], resources_required={"FTEs": 2}
            ),
            Initiative(
                id="opt_002", name="AI Governance Maturation",
                description="Advance AI governance to industry-leading practices",
                category=InitiativeCategory.FOUNDATION,
                phase=1, start_month=0, duration_months=3,
                effort_level="Medium", investment_range="$100K-$200K",
                dependencies=[], deliverables=["Enhanced policies", "Automated compliance"],
                success_metrics=["Governance score 90+"], risks=["Cultural change"],
                resources_required={"FTEs": 1}
            )
        ]

        phases.append(RoadmapPhase(
            phase_number=1, name="Optimize",
            duration_months=6, start_month=0,
            objectives=["Optimize AI operations", "Mature governance", "Reduce costs"],
            initiatives=phase1_initiatives,
            milestones=[],
            investment_range="$250K-$500K",
            key_outcomes=["Optimized operations", "Mature governance"],
            risks=["Change fatigue"],
            success_criteria=["Efficiency gains", "Governance maturity"]
        ))

        # Phase 2: Innovate (6-12 months)
        phase2_initiatives = [
            Initiative(
                id="inn_001", name="Advanced AI Exploration",
                description="Explore and pilot advanced AI (GenAI, etc.)",
                category=InitiativeCategory.INNOVATION,
                phase=2, start_month=6, duration_months=5,
                effort_level="Medium", investment_range="$200K-$400K",
                dependencies=[], deliverables=["Innovation pilots", "Capability roadmap"],
                success_metrics=["New capabilities proven"], risks=["Technology risk"],
                resources_required={"FTEs": 3}
            ),
            Initiative(
                id="inn_002", name="AI Product Development",
                description="Develop AI-enabled products or services",
                category=InitiativeCategory.INNOVATION,
                phase=2, start_month=7, duration_months=6,
                effort_level="High", investment_range="$400K-$800K",
                dependencies=["inn_001"], deliverables=["AI products", "Market testing"],
                success_metrics=["Product launched", "Revenue generation"],
                risks=["Market acceptance"], resources_required={"FTEs": 5}
            )
        ]

        phases.append(RoadmapPhase(
            phase_number=2, name="Innovate",
            duration_months=6, start_month=6,
            objectives=["Explore advanced AI", "Develop AI products", "Drive innovation"],
            initiatives=phase2_initiatives,
            milestones=[],
            investment_range="$600K-$1.2M",
            key_outcomes=["Innovation pipeline", "AI products"],
            risks=["Technology risk", "Market risk"],
            success_criteria=["Advanced capabilities", "Product revenue"]
        ))

        return phases

    def _calculate_total_investment(self, phases: List[RoadmapPhase]) -> str:
        """Calculate total investment across all phases"""
        # Parse investment ranges and sum
        min_total = 0
        max_total = 0

        for phase in phases:
            try:
                range_str = phase.investment_range.replace("$", "").replace(",", "")
                parts = range_str.split("-")
                min_val = self._parse_investment(parts[0])
                max_val = self._parse_investment(parts[1]) if len(parts) > 1 else min_val
                min_total += min_val
                max_total += max_val
            except:
                pass

        return f"${min_total/1000000:.1f}M-${max_total/1000000:.1f}M"

    def _parse_investment(self, val_str: str) -> int:
        """Parse investment string to integer"""
        val_str = val_str.strip().upper()
        multiplier = 1
        if "M" in val_str:
            multiplier = 1000000
            val_str = val_str.replace("M", "")
        elif "K" in val_str:
            multiplier = 1000
            val_str = val_str.replace("K", "")
        try:
            return int(float(val_str) * multiplier)
        except:
            return 0

    def _identify_critical_path(self, phases: List[RoadmapPhase]) -> List[str]:
        """Identify critical path through roadmap"""
        critical = []
        for phase in phases:
            # Highest effort initiatives on critical path
            for init in sorted(phase.initiatives, key=lambda x: x.duration_months, reverse=True)[:2]:
                critical.append(init.name)
        return critical

    def _identify_dependencies(self, phases: List[RoadmapPhase]) -> List[Dict[str, str]]:
        """Identify key dependencies"""
        dependencies = []
        for phase in phases:
            for init in phase.initiatives:
                if init.dependencies:
                    dependencies.append({
                        "initiative": init.name,
                        "depends_on": ", ".join(init.dependencies),
                        "impact": "Blocking" if len(init.dependencies) > 1 else "Sequential"
                    })
        return dependencies

    def _summarize_risks(self, phases: List[RoadmapPhase], maturity: str) -> List[Dict[str, str]]:
        """Summarize key risks"""
        risks = [
            {
                "risk": "Talent acquisition challenges",
                "likelihood": "High" if maturity in ["Exploring", "Experimenting"] else "Medium",
                "impact": "High",
                "mitigation": "Early hiring, competitive offers, upskilling"
            },
            {
                "risk": "Data quality issues",
                "likelihood": "High",
                "impact": "High",
                "mitigation": "Data foundation investment, quality monitoring"
            },
            {
                "risk": "Executive sponsorship changes",
                "likelihood": "Medium",
                "impact": "Critical",
                "mitigation": "Multiple sponsors, regular value communication"
            },
            {
                "risk": "Technology choices obsolescence",
                "likelihood": "Medium",
                "impact": "Medium",
                "mitigation": "Cloud-native, vendor diversification"
            }
        ]
        return risks

    def _build_resource_plan(self, phases: List[RoadmapPhase], maturity: str) -> Dict[str, Any]:
        """Build resource plan"""
        return {
            "team_growth": {
                "Phase 1": "2-4 FTEs + consulting",
                "Phase 2": "5-8 FTEs",
                "Phase 3": "8-12 FTEs"
            },
            "key_roles": [
                "AI/ML Lead",
                "Data Scientists (2-4)",
                "ML Engineers (2-4)",
                "Data Engineers (2-3)",
                "AI Product Manager",
                "MLOps Engineer"
            ],
            "external_support": [
                "Strategy consulting (Phase 1)",
                "Platform implementation (Phase 2)",
                "MLOps setup (Phase 2-3)"
            ],
            "training_investment": "$50K-$100K annually"
        }

    def _create_governance_milestones(self, phases: List[RoadmapPhase]) -> List[Milestone]:
        """Create governance-specific milestones"""
        return [
            Milestone(
                name="Quarterly AI Review 1",
                description="First quarterly AI portfolio review",
                target_date="Month 3",
                category=InitiativeCategory.FOUNDATION,
                dependencies=[],
                success_criteria=["All initiatives reviewed", "Issues addressed"],
                owner="AI Steering Committee"
            ),
            Milestone(
                name="Annual AI Strategy Review",
                description="Annual review and update of AI strategy",
                target_date="Month 12",
                category=InitiativeCategory.FOUNDATION,
                dependencies=[],
                success_criteria=["Strategy updated", "Year 2 plan approved"],
                owner="AI Steering Committee"
            )
        ]
