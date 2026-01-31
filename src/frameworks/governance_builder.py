"""
AI Governance Framework Builder

Generates customized AI Governance frameworks including:
- Governance structure and decision rights
- AI lifecycle management
- Risk management framework
- Compliance requirements
- Model governance
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class GovernanceMaturity(Enum):
    """AI Governance maturity levels"""
    NONE = "No Governance"
    INFORMAL = "Informal"
    DEVELOPING = "Developing"
    ESTABLISHED = "Established"
    ADVANCED = "Advanced"


class RiskCategory(Enum):
    """AI Risk categories"""
    MODEL_RISK = "Model Risk"
    DATA_RISK = "Data Risk"
    OPERATIONAL_RISK = "Operational Risk"
    ETHICAL_RISK = "Ethical Risk"
    REGULATORY_RISK = "Regulatory Risk"
    REPUTATIONAL_RISK = "Reputational Risk"


@dataclass
class GovernanceBody:
    """A governance body or committee"""
    name: str
    purpose: str
    responsibilities: List[str]
    members: List[str]
    meeting_frequency: str
    decision_authority: List[str]


@dataclass
class Policy:
    """An AI policy"""
    name: str
    purpose: str
    scope: str
    key_requirements: List[str]
    owner: str
    review_frequency: str


@dataclass
class GovernanceFramework:
    """Complete AI Governance Framework"""
    organization_name: str
    current_maturity: GovernanceMaturity
    target_maturity: GovernanceMaturity
    governance_bodies: List[GovernanceBody]
    policies: List[Policy]
    lifecycle_stages: List[Dict[str, Any]]
    risk_framework: Dict[str, Any]
    compliance_requirements: List[Dict[str, str]]
    model_governance: Dict[str, Any]
    third_party_governance: Dict[str, Any]
    implementation_roadmap: List[Dict[str, Any]]
    generated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "organization_name": self.organization_name,
            "current_maturity": self.current_maturity.value,
            "target_maturity": self.target_maturity.value,
            "governance_bodies": [
                {
                    "name": gb.name,
                    "purpose": gb.purpose,
                    "responsibilities": gb.responsibilities,
                    "members": gb.members,
                    "meeting_frequency": gb.meeting_frequency,
                    "decision_authority": gb.decision_authority
                }
                for gb in self.governance_bodies
            ],
            "policies": [
                {
                    "name": p.name,
                    "purpose": p.purpose,
                    "scope": p.scope,
                    "key_requirements": p.key_requirements,
                    "owner": p.owner
                }
                for p in self.policies
            ],
            "lifecycle_stages": self.lifecycle_stages,
            "risk_framework": self.risk_framework,
            "compliance_requirements": self.compliance_requirements,
            "model_governance": self.model_governance,
            "third_party_governance": self.third_party_governance,
            "implementation_roadmap": self.implementation_roadmap,
            "generated_at": self.generated_at.isoformat()
        }


class GovernanceFrameworkBuilder:
    """
    Builds customized AI Governance frameworks.
    """

    def build_framework(
        self,
        organization_name: str,
        assessment_result: Dict[str, Any],
        sector: str = "general",
        regulatory_requirements: Optional[List[str]] = None
    ) -> GovernanceFramework:
        """
        Build a complete AI Governance Framework.

        Args:
            organization_name: Name of organization
            assessment_result: Assessment results
            sector: Industry sector
            regulatory_requirements: Specific regulations to address

        Returns:
            GovernanceFramework
        """
        # Determine current and target maturity
        governance_score = self._get_governance_score(assessment_result)
        current_maturity = self._score_to_maturity(governance_score)
        target_maturity = self._determine_target(current_maturity)

        # Build governance bodies
        bodies = self._build_governance_bodies(current_maturity, sector)

        # Build policies
        policies = self._build_policies(sector, regulatory_requirements)

        # Define lifecycle stages
        lifecycle = self._define_lifecycle_stages()

        # Build risk framework
        risk_framework = self._build_risk_framework(sector)

        # Compliance requirements
        compliance = self._define_compliance_requirements(sector, regulatory_requirements)

        # Model governance
        model_gov = self._build_model_governance()

        # Third-party governance
        third_party = self._build_third_party_governance()

        # Implementation roadmap
        roadmap = self._build_implementation_roadmap(current_maturity)

        return GovernanceFramework(
            organization_name=organization_name,
            current_maturity=current_maturity,
            target_maturity=target_maturity,
            governance_bodies=bodies,
            policies=policies,
            lifecycle_stages=lifecycle,
            risk_framework=risk_framework,
            compliance_requirements=compliance,
            model_governance=model_gov,
            third_party_governance=third_party,
            implementation_roadmap=roadmap
        )

    def _get_governance_score(self, assessment: Dict) -> float:
        """Extract governance score from assessment"""
        dim_scores = assessment.get("dimension_scores", {})
        if "governance_compliance" in dim_scores:
            score_data = dim_scores["governance_compliance"]
            return score_data.get("score", 50) if isinstance(score_data, dict) else 50
        return 50

    def _score_to_maturity(self, score: float) -> GovernanceMaturity:
        """Convert score to maturity level"""
        if score >= 80:
            return GovernanceMaturity.ADVANCED
        elif score >= 60:
            return GovernanceMaturity.ESTABLISHED
        elif score >= 40:
            return GovernanceMaturity.DEVELOPING
        elif score >= 20:
            return GovernanceMaturity.INFORMAL
        return GovernanceMaturity.NONE

    def _determine_target(self, current: GovernanceMaturity) -> GovernanceMaturity:
        """Determine target maturity"""
        progression = {
            GovernanceMaturity.NONE: GovernanceMaturity.DEVELOPING,
            GovernanceMaturity.INFORMAL: GovernanceMaturity.DEVELOPING,
            GovernanceMaturity.DEVELOPING: GovernanceMaturity.ESTABLISHED,
            GovernanceMaturity.ESTABLISHED: GovernanceMaturity.ADVANCED,
            GovernanceMaturity.ADVANCED: GovernanceMaturity.ADVANCED
        }
        return progression.get(current, GovernanceMaturity.DEVELOPING)

    def _build_governance_bodies(
        self,
        maturity: GovernanceMaturity,
        sector: str
    ) -> List[GovernanceBody]:
        """Build governance body recommendations"""
        bodies = []

        # AI Steering Committee
        bodies.append(GovernanceBody(
            name="AI Steering Committee",
            purpose="Provide strategic oversight and direction for AI initiatives",
            responsibilities=[
                "Approve AI strategy and major investments",
                "Monitor AI portfolio performance",
                "Resolve escalated issues",
                "Champion AI adoption across organization"
            ],
            members=["CEO/COO (Sponsor)", "CTO/CIO", "CDO", "Business Unit Leaders", "CISO", "General Counsel"],
            meeting_frequency="Monthly",
            decision_authority=["AI strategy approval", "Investment >$500K", "High-risk AI deployment"]
        ))

        # AI Ethics Board
        bodies.append(GovernanceBody(
            name="AI Ethics Board",
            purpose="Ensure ethical AI development and deployment",
            responsibilities=[
                "Review high-risk AI applications",
                "Develop and maintain AI ethics policy",
                "Investigate ethical concerns",
                "Provide ethics guidance to teams"
            ],
            members=["Chief Ethics Officer", "Legal Representative", "HR Representative", "External Advisor", "Business Representatives"],
            meeting_frequency="Bi-weekly",
            decision_authority=["Ethics approval for AI projects", "Policy exceptions", "Investigation outcomes"]
        ))

        # AI Center of Excellence
        bodies.append(GovernanceBody(
            name="AI Center of Excellence (CoE)",
            purpose="Provide technical leadership and enable AI capabilities",
            responsibilities=[
                "Maintain AI platform and tools",
                "Develop and enforce standards",
                "Support project teams",
                "Build organizational AI capabilities"
            ],
            members=["AI/ML Lead", "Data Science Leads", "ML Engineers", "Data Engineers", "AI Product Managers"],
            meeting_frequency="Weekly",
            decision_authority=["Technical standards", "Tool selection", "Architecture decisions"]
        ))

        # Model Risk Committee (for regulated industries)
        if sector in ["financial_services", "healthcare"]:
            bodies.append(GovernanceBody(
                name="Model Risk Committee",
                purpose="Oversee model risk management",
                responsibilities=[
                    "Review and approve model deployments",
                    "Monitor model performance",
                    "Ensure regulatory compliance",
                    "Manage model inventory"
                ],
                members=["Chief Risk Officer", "Model Risk Manager", "Compliance Officer", "Business Model Owners"],
                meeting_frequency="Weekly",
                decision_authority=["Model deployment approval", "Model retirement", "Risk acceptance"]
            ))

        return bodies

    def _build_policies(
        self,
        sector: str,
        regulatory_requirements: Optional[List[str]]
    ) -> List[Policy]:
        """Build policy recommendations"""
        policies = []

        # AI Acceptable Use Policy
        policies.append(Policy(
            name="AI Acceptable Use Policy",
            purpose="Define appropriate use of AI within the organization",
            scope="All employees and contractors using or developing AI",
            key_requirements=[
                "AI must be used for legitimate business purposes",
                "Human oversight required for high-impact decisions",
                "Data used in AI must comply with privacy policies",
                "AI outputs must be verified before critical decisions",
                "Prohibited uses clearly defined"
            ],
            owner="Chief AI Officer / CTO",
            review_frequency="Annual"
        ))

        # AI Ethics Policy
        policies.append(Policy(
            name="AI Ethics Policy",
            purpose="Ensure AI is developed and used ethically",
            scope="All AI systems and applications",
            key_requirements=[
                "Fairness assessment for all AI models",
                "Bias testing before deployment",
                "Transparency in AI decision-making",
                "Human appeal process for AI decisions",
                "Regular ethics reviews"
            ],
            owner="Chief Ethics Officer",
            review_frequency="Annual"
        ))

        # AI Data Governance Policy
        policies.append(Policy(
            name="AI Data Governance Policy",
            purpose="Govern data used in AI systems",
            scope="All data used for AI training, testing, and inference",
            key_requirements=[
                "Data quality standards for AI",
                "Data lineage documentation",
                "Consent and privacy compliance",
                "Data retention and deletion",
                "Synthetic data guidelines"
            ],
            owner="Chief Data Officer",
            review_frequency="Annual"
        ))

        # Model Risk Management Policy
        policies.append(Policy(
            name="Model Risk Management Policy",
            purpose="Manage risks associated with AI/ML models",
            scope="All production AI/ML models",
            key_requirements=[
                "Model validation before deployment",
                "Ongoing performance monitoring",
                "Model documentation requirements",
                "Change management process",
                "Model retirement criteria"
            ],
            owner="Chief Risk Officer",
            review_frequency="Annual"
        ))

        # Third-Party AI Policy
        policies.append(Policy(
            name="Third-Party AI Policy",
            purpose="Govern use of external AI services and vendors",
            scope="All third-party AI tools, APIs, and services",
            key_requirements=[
                "Vendor due diligence requirements",
                "Contract requirements for AI services",
                "Data handling requirements",
                "Performance monitoring",
                "Exit strategy requirements"
            ],
            owner="Procurement / Vendor Management",
            review_frequency="Annual"
        ))

        return policies

    def _define_lifecycle_stages(self) -> List[Dict[str, Any]]:
        """Define AI lifecycle governance stages"""
        return [
            {
                "stage": "Ideation & Intake",
                "governance_activities": [
                    "Use case submission",
                    "Initial risk assessment",
                    "Business case review",
                    "Prioritization"
                ],
                "approvals_required": ["Business sponsor", "AI CoE review"],
                "artifacts": ["Use case brief", "Initial risk assessment"]
            },
            {
                "stage": "Design & Development",
                "governance_activities": [
                    "Technical design review",
                    "Data assessment",
                    "Ethics review (if required)",
                    "Security review"
                ],
                "approvals_required": ["Technical lead", "Ethics board (high-risk)"],
                "artifacts": ["Design document", "Data lineage", "Ethics assessment"]
            },
            {
                "stage": "Testing & Validation",
                "governance_activities": [
                    "Model validation",
                    "Bias testing",
                    "Performance testing",
                    "User acceptance"
                ],
                "approvals_required": ["Model Risk (regulated)", "Business owner"],
                "artifacts": ["Validation report", "Test results", "UAT sign-off"]
            },
            {
                "stage": "Deployment",
                "governance_activities": [
                    "Deployment readiness review",
                    "Monitoring setup verification",
                    "Rollback plan review",
                    "Go-live approval"
                ],
                "approvals_required": ["Deployment board", "Business owner", "Operations"],
                "artifacts": ["Deployment checklist", "Monitoring plan", "Rollback plan"]
            },
            {
                "stage": "Operations & Monitoring",
                "governance_activities": [
                    "Performance monitoring",
                    "Drift detection",
                    "Incident management",
                    "Periodic reviews"
                ],
                "approvals_required": ["N/A (continuous)"],
                "artifacts": ["Monitoring dashboards", "Incident reports", "Review reports"]
            },
            {
                "stage": "Retirement",
                "governance_activities": [
                    "Retirement assessment",
                    "Data handling",
                    "Stakeholder communication",
                    "Archive documentation"
                ],
                "approvals_required": ["Business owner", "AI CoE"],
                "artifacts": ["Retirement plan", "Archive records"]
            }
        ]

    def _build_risk_framework(self, sector: str) -> Dict[str, Any]:
        """Build AI risk management framework"""
        return {
            "risk_categories": [
                {
                    "category": RiskCategory.MODEL_RISK.value,
                    "description": "Risks from model errors, bias, or degradation",
                    "examples": ["Inaccurate predictions", "Biased outcomes", "Model drift"],
                    "controls": ["Model validation", "Ongoing monitoring", "Retraining triggers"]
                },
                {
                    "category": RiskCategory.DATA_RISK.value,
                    "description": "Risks related to data quality, privacy, and security",
                    "examples": ["Poor data quality", "Privacy violations", "Data breaches"],
                    "controls": ["Data quality checks", "Privacy controls", "Access management"]
                },
                {
                    "category": RiskCategory.OPERATIONAL_RISK.value,
                    "description": "Risks from AI system failures or misuse",
                    "examples": ["System outages", "Incorrect usage", "Integration failures"],
                    "controls": ["SLAs and monitoring", "User training", "Testing"]
                },
                {
                    "category": RiskCategory.ETHICAL_RISK.value,
                    "description": "Risks from unethical AI behavior or outcomes",
                    "examples": ["Discrimination", "Lack of transparency", "Privacy erosion"],
                    "controls": ["Ethics reviews", "Bias testing", "Explainability requirements"]
                },
                {
                    "category": RiskCategory.REGULATORY_RISK.value,
                    "description": "Risks from non-compliance with regulations",
                    "examples": ["Regulatory fines", "License revocation", "Legal action"],
                    "controls": ["Compliance assessments", "Audit trails", "Documentation"]
                },
                {
                    "category": RiskCategory.REPUTATIONAL_RISK.value,
                    "description": "Risks to organization's reputation from AI",
                    "examples": ["Public AI failures", "Negative press", "Customer backlash"],
                    "controls": ["Quality assurance", "Communication plans", "Incident response"]
                }
            ],
            "risk_assessment_process": {
                "frequency": "Per project + annual portfolio review",
                "methodology": "Likelihood x Impact matrix",
                "risk_levels": ["Low", "Medium", "High", "Critical"],
                "escalation_thresholds": {
                    "Critical": "AI Steering Committee",
                    "High": "AI Ethics Board",
                    "Medium": "AI CoE",
                    "Low": "Project team"
                }
            },
            "risk_appetite": "The organization accepts moderate AI risk where potential benefits significantly outweigh risks and appropriate controls are in place. High-risk AI applications require explicit steering committee approval."
        }

    def _define_compliance_requirements(
        self,
        sector: str,
        regulatory_requirements: Optional[List[str]]
    ) -> List[Dict[str, str]]:
        """Define compliance requirements"""
        requirements = []

        # Common requirements
        requirements.extend([
            {
                "regulation": "GDPR",
                "applicability": "EU personal data processing",
                "ai_requirements": "Right to explanation, data minimization, purpose limitation, automated decision-making restrictions",
                "compliance_activities": "Privacy impact assessments, consent management, data subject rights handling"
            },
            {
                "regulation": "CCPA/CPRA",
                "applicability": "California consumer data",
                "ai_requirements": "Transparency about automated decision-making, opt-out rights",
                "compliance_activities": "Privacy notices, consumer request handling"
            }
        ])

        # Sector-specific requirements
        if sector == "financial_services":
            requirements.extend([
                {
                    "regulation": "SR 11-7 (Federal Reserve)",
                    "applicability": "Bank models",
                    "ai_requirements": "Model risk management, validation, documentation",
                    "compliance_activities": "Model inventory, independent validation, MRM program"
                },
                {
                    "regulation": "Fair Lending Laws (ECOA, FHA)",
                    "applicability": "Credit decisions",
                    "ai_requirements": "Non-discrimination, adverse action notices",
                    "compliance_activities": "Fair lending testing, disparate impact analysis"
                }
            ])
        elif sector == "healthcare":
            requirements.extend([
                {
                    "regulation": "HIPAA",
                    "applicability": "Protected health information",
                    "ai_requirements": "PHI protection in AI systems",
                    "compliance_activities": "Security assessments, BAAs, access controls"
                },
                {
                    "regulation": "FDA (SaMD)",
                    "applicability": "Clinical decision support AI",
                    "ai_requirements": "510(k) or De Novo for certain AI devices",
                    "compliance_activities": "Regulatory classification, premarket submission if required"
                }
            ])

        # EU AI Act (emerging)
        requirements.append({
            "regulation": "EU AI Act",
            "applicability": "AI systems in EU market",
            "ai_requirements": "Risk classification, high-risk AI requirements, prohibited practices",
            "compliance_activities": "Risk assessment, conformity assessment, registration"
        })

        return requirements

    def _build_model_governance(self) -> Dict[str, Any]:
        """Build model governance framework"""
        return {
            "model_inventory": {
                "purpose": "Maintain comprehensive inventory of all AI/ML models",
                "required_information": [
                    "Model ID and name",
                    "Business purpose",
                    "Model type and algorithm",
                    "Training data sources",
                    "Owner and developer",
                    "Risk tier",
                    "Deployment status",
                    "Performance metrics"
                ],
                "update_frequency": "Continuous with quarterly review"
            },
            "model_tiering": {
                "Tier 1 (Critical)": {
                    "criteria": "High business impact, regulatory scrutiny, or customer-facing decisions",
                    "validation": "Independent validation required",
                    "monitoring": "Real-time with automated alerts",
                    "review_frequency": "Quarterly"
                },
                "Tier 2 (Significant)": {
                    "criteria": "Moderate business impact or internal decisions",
                    "validation": "Peer validation required",
                    "monitoring": "Daily metrics review",
                    "review_frequency": "Semi-annual"
                },
                "Tier 3 (Standard)": {
                    "criteria": "Low business impact, supportive role",
                    "validation": "Self-validation acceptable",
                    "monitoring": "Weekly metrics review",
                    "review_frequency": "Annual"
                }
            },
            "validation_requirements": {
                "conceptual_soundness": "Review of model design and assumptions",
                "data_quality": "Assessment of training and input data",
                "performance_testing": "Accuracy, precision, recall, AUC as appropriate",
                "bias_testing": "Fairness metrics across protected classes",
                "stability_testing": "Sensitivity analysis, stress testing"
            },
            "monitoring_requirements": {
                "performance_metrics": "Model accuracy, precision, recall tracked over time",
                "data_drift": "Input data distribution changes monitored",
                "concept_drift": "Relationship between inputs and outputs monitored",
                "business_metrics": "Business KPIs tied to model performance"
            }
        }

    def _build_third_party_governance(self) -> Dict[str, Any]:
        """Build third-party AI governance framework"""
        return {
            "due_diligence_requirements": [
                "AI/ML capabilities assessment",
                "Data handling practices",
                "Security certifications (SOC2, ISO 27001)",
                "Model documentation availability",
                "Bias and fairness practices",
                "Regulatory compliance status"
            ],
            "contract_requirements": [
                "Data ownership and usage rights",
                "Model transparency provisions",
                "Performance SLAs",
                "Audit rights",
                "Incident notification",
                "Liability provisions",
                "Exit and data return provisions"
            ],
            "ongoing_monitoring": [
                "Performance against SLAs",
                "Security and compliance updates",
                "Model updates and changes",
                "Incident tracking",
                "Annual reassessment"
            ],
            "risk_considerations": [
                "Vendor lock-in",
                "Data privacy in external processing",
                "Model explainability limitations",
                "Business continuity",
                "Regulatory compliance"
            ]
        }

    def _build_implementation_roadmap(
        self,
        current_maturity: GovernanceMaturity
    ) -> List[Dict[str, Any]]:
        """Build governance implementation roadmap"""
        roadmap = []

        # Phase 1: Foundation (0-3 months)
        roadmap.append({
            "phase": "Phase 1: Foundation",
            "duration": "0-3 months",
            "objectives": [
                "Establish basic governance structure",
                "Draft core policies",
                "Create model inventory"
            ],
            "key_activities": [
                "Form AI Steering Committee",
                "Appoint AI governance lead",
                "Draft AI Acceptable Use Policy",
                "Begin model inventory",
                "Identify high-risk AI applications"
            ],
            "success_criteria": [
                "Steering Committee operational",
                "Core policy approved",
                "High-risk models identified"
            ]
        })

        # Phase 2: Build (3-6 months)
        roadmap.append({
            "phase": "Phase 2: Build",
            "duration": "3-6 months",
            "objectives": [
                "Implement governance processes",
                "Establish ethics review",
                "Deploy monitoring basics"
            ],
            "key_activities": [
                "Launch AI Ethics Board",
                "Implement intake process",
                "Deploy model monitoring",
                "Train governance roles",
                "Complete model inventory"
            ],
            "success_criteria": [
                "Ethics Board operational",
                "All new AI through intake",
                "Monitoring in place for Tier 1"
            ]
        })

        # Phase 3: Mature (6-12 months)
        roadmap.append({
            "phase": "Phase 3: Mature",
            "duration": "6-12 months",
            "objectives": [
                "Full governance operationalization",
                "Automation and tooling",
                "Continuous improvement"
            ],
            "key_activities": [
                "Automate governance workflows",
                "Implement governance tooling",
                "Conduct first governance audit",
                "Refine policies based on learnings",
                "Expand training programs"
            ],
            "success_criteria": [
                "All AI under governance",
                "Automated compliance checks",
                "Successful audit completion"
            ]
        })

        return roadmap
