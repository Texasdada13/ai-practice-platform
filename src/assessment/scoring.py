"""
AI Readiness Scoring Engine

Calculates dimension scores, overall readiness score, and maturity level
based on assessment responses.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum
import logging

from .questions import CORE_QUESTIONS, get_questions_for_sector, DIMENSION_WEIGHTS

logger = logging.getLogger(__name__)


class MaturityLevel(Enum):
    """AI Maturity levels based on readiness score."""
    EXPLORING = "Exploring"
    EXPERIMENTING = "Experimenting"
    SCALING = "Scaling"
    OPTIMIZING = "Optimizing"

    @property
    def description(self) -> str:
        return {
            MaturityLevel.EXPLORING: "Early awareness stage with limited AI activity. Organization is learning about AI possibilities.",
            MaturityLevel.EXPERIMENTING: "Pilots and proofs-of-concept underway. Building foundational capabilities and testing use cases.",
            MaturityLevel.SCALING: "Production AI deployments expanding. Established practices and growing organizational capability.",
            MaturityLevel.OPTIMIZING: "AI-driven organization with continuous improvement. AI embedded in strategy and operations."
        }[self]

    @property
    def color(self) -> str:
        return {
            MaturityLevel.EXPLORING: "#dc3545",      # Red
            MaturityLevel.EXPERIMENTING: "#fd7e14",  # Orange
            MaturityLevel.SCALING: "#28a745",        # Green
            MaturityLevel.OPTIMIZING: "#17a2b8"      # Blue/Teal
        }[self]

    @property
    def icon(self) -> str:
        return {
            MaturityLevel.EXPLORING: "🔍",
            MaturityLevel.EXPERIMENTING: "🧪",
            MaturityLevel.SCALING: "📈",
            MaturityLevel.OPTIMIZING: "🚀"
        }[self]

    @property
    def score_range(self) -> tuple:
        return {
            MaturityLevel.EXPLORING: (0, 25),
            MaturityLevel.EXPERIMENTING: (26, 50),
            MaturityLevel.SCALING: (51, 75),
            MaturityLevel.OPTIMIZING: (76, 100)
        }[self]


@dataclass
class DimensionScore:
    """Score for a single assessment dimension."""
    dimension_id: str
    dimension_name: str
    score: float  # 0-100
    question_count: int
    question_scores: Dict[str, int]  # question_id -> raw score (1-5)
    strengths: List[str]
    improvements: List[str]
    weight: float


@dataclass
class AssessmentResult:
    """Complete assessment result."""
    assessment_id: str
    organization_name: str
    sector: str
    overall_score: float  # 0-100
    maturity_level: MaturityLevel
    grade: str
    dimension_scores: Dict[str, DimensionScore]
    top_strengths: List[str]
    top_improvements: List[str]
    recommendations: List[str]
    benchmark_comparison: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "assessment_id": self.assessment_id,
            "organization_name": self.organization_name,
            "sector": self.sector,
            "overall_score": self.overall_score,
            "maturity_level": self.maturity_level.value,
            "maturity_description": self.maturity_level.description,
            "maturity_color": self.maturity_level.color,
            "grade": self.grade,
            "dimension_scores": {
                dim_id: {
                    "name": ds.dimension_name,
                    "score": ds.score,
                    "question_count": ds.question_count,
                    "weight": ds.weight,
                    "strengths": ds.strengths,
                    "improvements": ds.improvements
                }
                for dim_id, ds in self.dimension_scores.items()
            },
            "top_strengths": self.top_strengths,
            "top_improvements": self.top_improvements,
            "recommendations": self.recommendations,
            "benchmark_comparison": self.benchmark_comparison
        }


class AIReadinessScorer:
    """
    AI Readiness Assessment Scoring Engine.

    Calculates scores from 1-5 responses, converts to 0-100 scale,
    applies dimension weights, and determines maturity level.
    """

    # Grade thresholds
    GRADE_THRESHOLDS = {
        90: "A",
        80: "B",
        70: "C",
        60: "D",
        0: "F"
    }

    # Maturity thresholds
    MATURITY_THRESHOLDS = {
        76: MaturityLevel.OPTIMIZING,
        51: MaturityLevel.SCALING,
        26: MaturityLevel.EXPERIMENTING,
        0: MaturityLevel.EXPLORING
    }

    def __init__(self, sector: str = "general"):
        """
        Initialize scorer for a specific sector.

        Args:
            sector: Industry sector for sector-specific questions
        """
        self.sector = sector
        self.questions = get_questions_for_sector(sector)
        self.dimension_weights = DIMENSION_WEIGHTS

    def score_assessment(
        self,
        responses: Dict[str, int],
        organization_name: str = "Organization",
        assessment_id: str = "assessment_001"
    ) -> AssessmentResult:
        """
        Score a complete assessment.

        Args:
            responses: Dict mapping question_id -> response value (1-5)
            organization_name: Name of the organization
            assessment_id: Unique assessment identifier

        Returns:
            AssessmentResult with all scores and analysis
        """
        dimension_scores = {}

        # Score each dimension
        for dim_id, dim_data in self.questions.items():
            dim_score = self._score_dimension(dim_id, dim_data, responses)
            dimension_scores[dim_id] = dim_score

        # Calculate overall weighted score
        overall_score = self._calculate_overall_score(dimension_scores)

        # Determine maturity level and grade
        maturity_level = self._determine_maturity(overall_score)
        grade = self._determine_grade(overall_score)

        # Identify top strengths and improvements
        top_strengths = self._identify_strengths(dimension_scores)
        top_improvements = self._identify_improvements(dimension_scores)

        # Generate recommendations
        recommendations = self._generate_recommendations(dimension_scores, maturity_level)

        return AssessmentResult(
            assessment_id=assessment_id,
            organization_name=organization_name,
            sector=self.sector,
            overall_score=overall_score,
            maturity_level=maturity_level,
            grade=grade,
            dimension_scores=dimension_scores,
            top_strengths=top_strengths,
            top_improvements=top_improvements,
            recommendations=recommendations
        )

    def _score_dimension(
        self,
        dim_id: str,
        dim_data: Dict[str, Any],
        responses: Dict[str, int]
    ) -> DimensionScore:
        """Score a single dimension."""
        questions = dim_data["questions"]
        question_scores = {}
        strengths = []
        improvements = []

        for q in questions:
            q_id = q["id"]
            response = responses.get(q_id)

            if response is not None:
                question_scores[q_id] = response

                # Identify strengths (4-5) and improvements (1-2)
                if response >= 4:
                    strengths.append(q["text"][:80] + "..." if len(q["text"]) > 80 else q["text"])
                elif response <= 2:
                    improvements.append(q["text"][:80] + "..." if len(q["text"]) > 80 else q["text"])

        # Calculate dimension score (convert 1-5 to 0-100)
        if question_scores:
            avg_response = sum(question_scores.values()) / len(question_scores)
            # Convert 1-5 scale to 0-100: (response - 1) / 4 * 100
            dim_score = ((avg_response - 1) / 4) * 100
        else:
            dim_score = 0

        return DimensionScore(
            dimension_id=dim_id,
            dimension_name=dim_data["name"],
            score=round(dim_score, 1),
            question_count=len(question_scores),
            question_scores=question_scores,
            strengths=strengths[:3],  # Top 3
            improvements=improvements[:3],  # Top 3
            weight=dim_data["weight"]
        )

    def _calculate_overall_score(self, dimension_scores: Dict[str, DimensionScore]) -> float:
        """Calculate weighted overall score."""
        total_weight = 0
        weighted_sum = 0

        for dim_id, dim_score in dimension_scores.items():
            weight = self.dimension_weights.get(dim_id, dim_score.weight)
            weighted_sum += dim_score.score * weight
            total_weight += weight

        if total_weight > 0:
            return round(weighted_sum / total_weight, 1)
        return 0

    def _determine_maturity(self, score: float) -> MaturityLevel:
        """Determine maturity level from overall score."""
        for threshold, level in sorted(self.MATURITY_THRESHOLDS.items(), reverse=True):
            if score >= threshold:
                return level
        return MaturityLevel.EXPLORING

    def _determine_grade(self, score: float) -> str:
        """Determine letter grade from overall score."""
        for threshold, grade in sorted(self.GRADE_THRESHOLDS.items(), reverse=True):
            if score >= threshold:
                return grade
        return "F"

    def _identify_strengths(self, dimension_scores: Dict[str, DimensionScore]) -> List[str]:
        """Identify top organizational strengths."""
        strengths = []

        # Sort dimensions by score (highest first)
        sorted_dims = sorted(
            dimension_scores.items(),
            key=lambda x: x[1].score,
            reverse=True
        )

        for dim_id, dim_score in sorted_dims:
            if dim_score.score >= 60:  # Above average
                strengths.append(f"{dim_score.dimension_name}: {dim_score.score:.0f}/100")
                strengths.extend([f"  - {s}" for s in dim_score.strengths[:2]])

        return strengths[:6]  # Top 6 items

    def _identify_improvements(self, dimension_scores: Dict[str, DimensionScore]) -> List[str]:
        """Identify top areas for improvement."""
        improvements = []

        # Sort dimensions by score (lowest first)
        sorted_dims = sorted(
            dimension_scores.items(),
            key=lambda x: x[1].score
        )

        for dim_id, dim_score in sorted_dims:
            if dim_score.score < 60:  # Below average
                improvements.append(f"{dim_score.dimension_name}: {dim_score.score:.0f}/100")
                improvements.extend([f"  - {i}" for i in dim_score.improvements[:2]])

        return improvements[:6]  # Top 6 items

    def _generate_recommendations(
        self,
        dimension_scores: Dict[str, DimensionScore],
        maturity_level: MaturityLevel
    ) -> List[str]:
        """Generate prioritized recommendations based on scores and maturity."""
        recommendations = []

        # Maturity-specific recommendations
        maturity_recs = {
            MaturityLevel.EXPLORING: [
                "Establish an AI steering committee with executive sponsorship",
                "Conduct AI literacy training for leadership team",
                "Inventory existing data assets and assess quality",
                "Identify 2-3 low-risk, high-value AI pilot use cases",
                "Develop a data governance framework foundation"
            ],
            MaturityLevel.EXPERIMENTING: [
                "Scale successful pilots with clear success metrics",
                "Invest in cloud infrastructure for AI workloads",
                "Build or acquire core AI/ML technical talent",
                "Establish AI ethics guidelines and review process",
                "Create reusable AI/ML platform components"
            ],
            MaturityLevel.SCALING: [
                "Implement MLOps for production model management",
                "Expand AI training programs across the organization",
                "Develop AI Center of Excellence governance model",
                "Integrate AI into strategic planning processes",
                "Establish continuous model monitoring and retraining"
            ],
            MaturityLevel.OPTIMIZING: [
                "Drive AI innovation through dedicated R&D function",
                "Explore advanced AI (GenAI, autonomous systems)",
                "Share AI best practices across business units",
                "Measure and optimize AI ROI portfolio-wide",
                "Lead industry AI standards and collaboration"
            ]
        }

        recommendations.extend(maturity_recs.get(maturity_level, [])[:3])

        # Dimension-specific recommendations for low-scoring areas
        for dim_id, dim_score in sorted(dimension_scores.items(), key=lambda x: x[1].score):
            if dim_score.score < 50:
                dim_rec = self._get_dimension_recommendation(dim_id, dim_score.score)
                if dim_rec and len(recommendations) < 7:
                    recommendations.append(dim_rec)

        return recommendations[:7]

    def _get_dimension_recommendation(self, dim_id: str, score: float) -> Optional[str]:
        """Get specific recommendation for a low-scoring dimension."""
        recs = {
            "data_maturity": "PRIORITY: Invest in data quality and governance - this is foundational for all AI initiatives",
            "technology_infrastructure": "PRIORITY: Modernize technology stack with cloud and API capabilities for AI workloads",
            "process_operations": "PRIORITY: Document and automate key processes to create foundation for AI optimization",
            "workforce_culture": "PRIORITY: Launch AI literacy program and secure executive championship for AI initiatives",
            "governance_compliance": "PRIORITY: Establish AI ethics framework and risk management before scaling AI"
        }
        return recs.get(dim_id)


# =============================================================================
# Factory Functions
# =============================================================================

def create_scorer(sector: str = "general") -> AIReadinessScorer:
    """Factory function to create a sector-specific scorer."""
    return AIReadinessScorer(sector=sector)


def calculate_quick_score(responses: Dict[str, int], sector: str = "general") -> Dict[str, Any]:
    """
    Quick scoring function for simple use cases.

    Returns dict with overall_score, maturity_level, and grade.
    """
    scorer = create_scorer(sector)
    result = scorer.score_assessment(responses)

    return {
        "overall_score": result.overall_score,
        "maturity_level": result.maturity_level.value,
        "grade": result.grade,
        "dimension_scores": {
            dim_id: ds.score for dim_id, ds in result.dimension_scores.items()
        }
    }
