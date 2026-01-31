"""
AI Use Case Prioritizer

Prioritizes AI use cases based on:
- Business value potential
- Technical feasibility
- Data readiness
- Strategic alignment
- Implementation complexity
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json


class ValueCategory(Enum):
    """Use case value categories"""
    COST_REDUCTION = "Cost Reduction"
    REVENUE_GROWTH = "Revenue Growth"
    RISK_MITIGATION = "Risk Mitigation"
    CUSTOMER_EXPERIENCE = "Customer Experience"
    OPERATIONAL_EFFICIENCY = "Operational Efficiency"
    COMPLIANCE = "Compliance"


class FeasibilityLevel(Enum):
    """Technical feasibility levels"""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class PriorityTier(Enum):
    """Use case priority tiers"""
    QUICK_WIN = "Quick Win"
    STRATEGIC = "Strategic"
    FOUNDATION = "Foundation Builder"
    FUTURE = "Future Opportunity"


@dataclass
class UseCase:
    """An AI use case"""
    id: str
    name: str
    description: str
    business_problem: str
    ai_approach: str
    value_category: ValueCategory
    estimated_value: str
    feasibility: FeasibilityLevel
    data_readiness: int  # 1-10
    complexity: int  # 1-10
    time_to_value: str
    dependencies: List[str]
    risks: List[str]
    success_metrics: List[str]
    priority_tier: PriorityTier = PriorityTier.FUTURE
    priority_score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "business_problem": self.business_problem,
            "ai_approach": self.ai_approach,
            "value_category": self.value_category.value,
            "estimated_value": self.estimated_value,
            "feasibility": self.feasibility.value,
            "data_readiness": self.data_readiness,
            "complexity": self.complexity,
            "time_to_value": self.time_to_value,
            "priority_tier": self.priority_tier.value,
            "priority_score": self.priority_score,
            "success_metrics": self.success_metrics
        }


@dataclass
class UseCasePortfolio:
    """Prioritized portfolio of AI use cases"""
    organization_name: str
    sector: str
    use_cases: List[UseCase]
    prioritization_criteria: Dict[str, float]
    tier_summary: Dict[str, List[str]]
    recommended_sequence: List[str]
    total_estimated_value: str
    generated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "organization_name": self.organization_name,
            "sector": self.sector,
            "use_cases": [uc.to_dict() for uc in self.use_cases],
            "tier_summary": self.tier_summary,
            "recommended_sequence": self.recommended_sequence,
            "total_estimated_value": self.total_estimated_value,
            "generated_at": self.generated_at.isoformat()
        }


class UseCasePrioritizer:
    """
    Prioritizes AI use cases using a value-feasibility framework.
    """

    # Sector-specific use case templates
    SECTOR_USE_CASES = {
        "financial_services": [
            {
                "name": "Fraud Detection Enhancement",
                "description": "ML-based real-time fraud detection for transactions",
                "business_problem": "High fraud losses and false positive rates",
                "ai_approach": "Supervised ML with anomaly detection",
                "value_category": ValueCategory.RISK_MITIGATION,
                "estimated_value": "$2-5M annually",
                "time_to_value": "6-9 months"
            },
            {
                "name": "Credit Risk Scoring",
                "description": "AI-enhanced credit risk assessment",
                "business_problem": "Suboptimal credit decisions and defaults",
                "ai_approach": "Gradient boosting with explainability",
                "value_category": ValueCategory.RISK_MITIGATION,
                "estimated_value": "$1-3M annually",
                "time_to_value": "9-12 months"
            },
            {
                "name": "Customer Churn Prediction",
                "description": "Predict and prevent customer attrition",
                "business_problem": "Customer churn impacting revenue",
                "ai_approach": "Classification with propensity modeling",
                "value_category": ValueCategory.REVENUE_GROWTH,
                "estimated_value": "$500K-2M annually",
                "time_to_value": "4-6 months"
            },
            {
                "name": "Intelligent Document Processing",
                "description": "Automate document extraction and processing",
                "business_problem": "Manual document processing costs",
                "ai_approach": "NLP and computer vision",
                "value_category": ValueCategory.OPERATIONAL_EFFICIENCY,
                "estimated_value": "$1-3M annually",
                "time_to_value": "6-9 months"
            }
        ],
        "healthcare": [
            {
                "name": "Clinical Decision Support",
                "description": "AI-assisted diagnosis and treatment recommendations",
                "business_problem": "Diagnostic accuracy and care variation",
                "ai_approach": "Deep learning on clinical data",
                "value_category": ValueCategory.CUSTOMER_EXPERIENCE,
                "estimated_value": "Quality improvement",
                "time_to_value": "12-18 months"
            },
            {
                "name": "Patient No-Show Prediction",
                "description": "Predict appointment no-shows for intervention",
                "business_problem": "Revenue loss from no-shows",
                "ai_approach": "Classification model",
                "value_category": ValueCategory.OPERATIONAL_EFFICIENCY,
                "estimated_value": "$500K-1M annually",
                "time_to_value": "3-6 months"
            },
            {
                "name": "Claims Denial Prediction",
                "description": "Predict and prevent claim denials",
                "business_problem": "Revenue cycle losses from denials",
                "ai_approach": "ML classification with NLP",
                "value_category": ValueCategory.REVENUE_GROWTH,
                "estimated_value": "$1-3M annually",
                "time_to_value": "6-9 months"
            }
        ],
        "manufacturing": [
            {
                "name": "Predictive Maintenance",
                "description": "Predict equipment failures before they occur",
                "business_problem": "Unplanned downtime and maintenance costs",
                "ai_approach": "Time series ML with sensor data",
                "value_category": ValueCategory.COST_REDUCTION,
                "estimated_value": "$1-5M annually",
                "time_to_value": "6-12 months"
            },
            {
                "name": "Quality Prediction",
                "description": "Predict and prevent quality defects",
                "business_problem": "Quality issues and waste",
                "ai_approach": "Computer vision and process ML",
                "value_category": ValueCategory.COST_REDUCTION,
                "estimated_value": "$500K-2M annually",
                "time_to_value": "6-9 months"
            },
            {
                "name": "Demand Forecasting",
                "description": "AI-enhanced demand forecasting",
                "business_problem": "Inventory costs and stockouts",
                "ai_approach": "Time series with external factors",
                "value_category": ValueCategory.OPERATIONAL_EFFICIENCY,
                "estimated_value": "$1-3M annually",
                "time_to_value": "4-6 months"
            }
        ],
        "retail": [
            {
                "name": "Personalization Engine",
                "description": "Personalized product recommendations",
                "business_problem": "Low conversion rates",
                "ai_approach": "Collaborative filtering and deep learning",
                "value_category": ValueCategory.REVENUE_GROWTH,
                "estimated_value": "5-15% revenue lift",
                "time_to_value": "6-9 months"
            },
            {
                "name": "Demand Forecasting",
                "description": "AI-powered demand forecasting",
                "business_problem": "Inventory inefficiency",
                "ai_approach": "Ensemble time series",
                "value_category": ValueCategory.COST_REDUCTION,
                "estimated_value": "$1-3M annually",
                "time_to_value": "4-6 months"
            },
            {
                "name": "Price Optimization",
                "description": "Dynamic pricing optimization",
                "business_problem": "Margin optimization",
                "ai_approach": "Reinforcement learning",
                "value_category": ValueCategory.REVENUE_GROWTH,
                "estimated_value": "2-5% margin improvement",
                "time_to_value": "9-12 months"
            }
        ],
        "general": [
            {
                "name": "Intelligent Process Automation",
                "description": "AI-enhanced RPA for complex processes",
                "business_problem": "Manual process costs and errors",
                "ai_approach": "ML + RPA integration",
                "value_category": ValueCategory.OPERATIONAL_EFFICIENCY,
                "estimated_value": "30-50% efficiency gain",
                "time_to_value": "4-6 months"
            },
            {
                "name": "Customer Service AI",
                "description": "AI-powered customer support",
                "business_problem": "Support costs and satisfaction",
                "ai_approach": "NLP chatbots and agent assist",
                "value_category": ValueCategory.CUSTOMER_EXPERIENCE,
                "estimated_value": "20-40% cost reduction",
                "time_to_value": "3-6 months"
            },
            {
                "name": "Predictive Analytics Dashboard",
                "description": "AI-powered business intelligence",
                "business_problem": "Reactive decision making",
                "ai_approach": "Automated ML with forecasting",
                "value_category": ValueCategory.OPERATIONAL_EFFICIENCY,
                "estimated_value": "Improved decisions",
                "time_to_value": "3-4 months"
            }
        ]
    }

    def __init__(self):
        # Default prioritization weights
        self.weights = {
            "business_value": 0.30,
            "feasibility": 0.25,
            "data_readiness": 0.20,
            "strategic_alignment": 0.15,
            "time_to_value": 0.10
        }

    def prioritize(
        self,
        organization_name: str,
        sector: str,
        assessment_result: Optional[Dict] = None,
        custom_use_cases: Optional[List[Dict]] = None,
        custom_weights: Optional[Dict[str, float]] = None
    ) -> UseCasePortfolio:
        """
        Prioritize AI use cases for an organization.

        Args:
            organization_name: Name of organization
            sector: Industry sector
            assessment_result: Optional assessment results for context
            custom_use_cases: Optional custom use cases to include
            custom_weights: Optional custom prioritization weights

        Returns:
            UseCasePortfolio with prioritized use cases
        """
        if custom_weights:
            self.weights = custom_weights

        # Get sector-specific use cases
        sector_templates = self.SECTOR_USE_CASES.get(sector, self.SECTOR_USE_CASES["general"])

        # Convert templates to UseCase objects
        use_cases = []
        for i, template in enumerate(sector_templates):
            uc = self._template_to_use_case(template, i, assessment_result)
            use_cases.append(uc)

        # Add custom use cases if provided
        if custom_use_cases:
            for i, custom in enumerate(custom_use_cases):
                uc = self._custom_to_use_case(custom, len(use_cases) + i)
                use_cases.append(uc)

        # Score and prioritize
        for uc in use_cases:
            uc.priority_score = self._calculate_priority_score(uc, assessment_result)
            uc.priority_tier = self._determine_tier(uc)

        # Sort by priority score
        use_cases.sort(key=lambda x: x.priority_score, reverse=True)

        # Create tier summary
        tier_summary = self._create_tier_summary(use_cases)

        # Recommended sequence
        sequence = self._determine_sequence(use_cases)

        # Total value (qualitative)
        total_value = self._estimate_total_value(use_cases)

        return UseCasePortfolio(
            organization_name=organization_name,
            sector=sector,
            use_cases=use_cases,
            prioritization_criteria=self.weights,
            tier_summary=tier_summary,
            recommended_sequence=sequence,
            total_estimated_value=total_value
        )

    def _template_to_use_case(
        self,
        template: Dict,
        index: int,
        assessment: Optional[Dict]
    ) -> UseCase:
        """Convert template to UseCase object"""
        # Estimate feasibility and data readiness based on assessment
        feasibility = FeasibilityLevel.MEDIUM
        data_readiness = 5
        complexity = 5

        if assessment:
            # Use assessment scores to inform estimates
            dim_scores = assessment.get("dimension_scores", {})
            data_score = self._get_dim_score(dim_scores, "data_maturity")
            tech_score = self._get_dim_score(dim_scores, "technology_infrastructure")

            if data_score >= 60 and tech_score >= 60:
                feasibility = FeasibilityLevel.HIGH
                data_readiness = 7
                complexity = 4
            elif data_score < 40 or tech_score < 40:
                feasibility = FeasibilityLevel.LOW
                data_readiness = 3
                complexity = 7

        return UseCase(
            id=f"uc_{index:03d}",
            name=template["name"],
            description=template["description"],
            business_problem=template["business_problem"],
            ai_approach=template["ai_approach"],
            value_category=template["value_category"],
            estimated_value=template["estimated_value"],
            feasibility=feasibility,
            data_readiness=data_readiness,
            complexity=complexity,
            time_to_value=template["time_to_value"],
            dependencies=[],
            risks=["Data availability", "Model accuracy", "User adoption"],
            success_metrics=["Model accuracy", "Business KPI improvement", "User adoption rate"]
        )

    def _custom_to_use_case(self, custom: Dict, index: int) -> UseCase:
        """Convert custom dict to UseCase"""
        return UseCase(
            id=f"custom_{index:03d}",
            name=custom.get("name", "Custom Use Case"),
            description=custom.get("description", ""),
            business_problem=custom.get("business_problem", ""),
            ai_approach=custom.get("ai_approach", "ML/AI"),
            value_category=ValueCategory[custom.get("value_category", "OPERATIONAL_EFFICIENCY")],
            estimated_value=custom.get("estimated_value", "TBD"),
            feasibility=FeasibilityLevel[custom.get("feasibility", "MEDIUM")],
            data_readiness=custom.get("data_readiness", 5),
            complexity=custom.get("complexity", 5),
            time_to_value=custom.get("time_to_value", "6-12 months"),
            dependencies=custom.get("dependencies", []),
            risks=custom.get("risks", []),
            success_metrics=custom.get("success_metrics", [])
        )

    def _get_dim_score(self, dim_scores: Dict, dim_name: str) -> float:
        """Get dimension score from assessment"""
        if dim_name in dim_scores:
            score_data = dim_scores[dim_name]
            return score_data.get("score", 50) if isinstance(score_data, dict) else 50
        return 50

    def _calculate_priority_score(
        self,
        use_case: UseCase,
        assessment: Optional[Dict]
    ) -> float:
        """Calculate priority score (0-100)"""
        # Business value score (based on value category and estimate)
        value_scores = {
            ValueCategory.REVENUE_GROWTH: 90,
            ValueCategory.COST_REDUCTION: 85,
            ValueCategory.RISK_MITIGATION: 80,
            ValueCategory.CUSTOMER_EXPERIENCE: 75,
            ValueCategory.OPERATIONAL_EFFICIENCY: 70,
            ValueCategory.COMPLIANCE: 65
        }
        value_score = value_scores.get(use_case.value_category, 50)

        # Feasibility score
        feasibility_scores = {
            FeasibilityLevel.HIGH: 90,
            FeasibilityLevel.MEDIUM: 60,
            FeasibilityLevel.LOW: 30
        }
        feasibility_score = feasibility_scores.get(use_case.feasibility, 50)

        # Data readiness score (1-10 to 0-100)
        data_score = use_case.data_readiness * 10

        # Complexity score (inverse - lower complexity = higher score)
        complexity_score = (10 - use_case.complexity) * 10

        # Time to value score (faster = higher)
        time_score = 50  # Default
        ttv = use_case.time_to_value.lower()
        if "3-4" in ttv or "3-6" in ttv:
            time_score = 90
        elif "4-6" in ttv or "6-9" in ttv:
            time_score = 70
        elif "9-12" in ttv or "6-12" in ttv:
            time_score = 50
        elif "12" in ttv:
            time_score = 30

        # Weighted score
        score = (
            value_score * self.weights["business_value"] +
            feasibility_score * self.weights["feasibility"] +
            data_score * self.weights["data_readiness"] +
            complexity_score * self.weights["strategic_alignment"] +
            time_score * self.weights["time_to_value"]
        )

        return round(score, 1)

    def _determine_tier(self, use_case: UseCase) -> PriorityTier:
        """Determine priority tier based on score and characteristics"""
        score = use_case.priority_score
        feasibility = use_case.feasibility
        complexity = use_case.complexity

        # Quick Win: High score, high feasibility, low complexity
        if score >= 70 and feasibility == FeasibilityLevel.HIGH and complexity <= 5:
            return PriorityTier.QUICK_WIN

        # Strategic: High score but more complex
        if score >= 60:
            return PriorityTier.STRATEGIC

        # Foundation Builder: Medium score, builds capabilities
        if score >= 45 and feasibility != FeasibilityLevel.LOW:
            return PriorityTier.FOUNDATION

        # Future: Everything else
        return PriorityTier.FUTURE

    def _create_tier_summary(self, use_cases: List[UseCase]) -> Dict[str, List[str]]:
        """Create summary by tier"""
        summary = {
            PriorityTier.QUICK_WIN.value: [],
            PriorityTier.STRATEGIC.value: [],
            PriorityTier.FOUNDATION.value: [],
            PriorityTier.FUTURE.value: []
        }

        for uc in use_cases:
            summary[uc.priority_tier.value].append(uc.name)

        return summary

    def _determine_sequence(self, use_cases: List[UseCase]) -> List[str]:
        """Determine recommended implementation sequence"""
        sequence = []

        # Quick wins first
        quick_wins = [uc for uc in use_cases if uc.priority_tier == PriorityTier.QUICK_WIN]
        sequence.extend([uc.name for uc in quick_wins[:2]])

        # Then strategic
        strategic = [uc for uc in use_cases if uc.priority_tier == PriorityTier.STRATEGIC]
        sequence.extend([uc.name for uc in strategic[:2]])

        # Foundation builders
        foundation = [uc for uc in use_cases if uc.priority_tier == PriorityTier.FOUNDATION]
        sequence.extend([uc.name for uc in foundation[:1]])

        return sequence

    def _estimate_total_value(self, use_cases: List[UseCase]) -> str:
        """Estimate total portfolio value"""
        # Qualitative estimate based on use cases
        high_value_count = len([uc for uc in use_cases if uc.priority_tier in [PriorityTier.QUICK_WIN, PriorityTier.STRATEGIC]])

        if high_value_count >= 4:
            return "$5M-$15M+ annually (at full implementation)"
        elif high_value_count >= 2:
            return "$2M-$8M annually (at full implementation)"
        else:
            return "$500K-$3M annually (at full implementation)"
