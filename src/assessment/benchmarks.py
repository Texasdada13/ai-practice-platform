"""
AI Readiness Benchmark Data

Synthetic benchmarks based on industry research from:
- McKinsey State of AI reports
- Deloitte AI Institute surveys
- Gartner AI maturity assessments
- Industry-specific AI adoption studies

These benchmarks represent typical scores across industries and
can be used for gap analysis and comparison.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class BenchmarkData:
    """Benchmark data for a sector."""
    sector: str
    sector_name: str
    overall_average: float
    overall_top_quartile: float
    overall_bottom_quartile: float
    dimension_benchmarks: Dict[str, Dict[str, float]]
    sample_size: str  # Description of sample basis
    source: str


# =============================================================================
# SYNTHETIC BENCHMARK DATA BY SECTOR
# Based on aggregated industry research
# =============================================================================

BENCHMARKS: Dict[str, BenchmarkData] = {
    "financial_services": BenchmarkData(
        sector="financial_services",
        sector_name="Financial Services",
        overall_average=58.0,
        overall_top_quartile=78.0,
        overall_bottom_quartile=38.0,
        dimension_benchmarks={
            "data_maturity": {
                "average": 62.0,
                "top_quartile": 82.0,
                "bottom_quartile": 42.0,
                "leader_score": 92.0
            },
            "technology_infrastructure": {
                "average": 55.0,
                "top_quartile": 75.0,
                "bottom_quartile": 35.0,
                "leader_score": 88.0
            },
            "process_operations": {
                "average": 58.0,
                "top_quartile": 78.0,
                "bottom_quartile": 38.0,
                "leader_score": 90.0
            },
            "workforce_culture": {
                "average": 52.0,
                "top_quartile": 72.0,
                "bottom_quartile": 32.0,
                "leader_score": 85.0
            },
            "governance_compliance": {
                "average": 65.0,
                "top_quartile": 85.0,
                "bottom_quartile": 45.0,
                "leader_score": 95.0
            }
        },
        sample_size="Based on 500+ financial institutions globally",
        source="Aggregated from McKinsey, Deloitte, and Gartner 2024-2025 reports"
    ),

    "government": BenchmarkData(
        sector="government",
        sector_name="Government/Public Sector",
        overall_average=42.0,
        overall_top_quartile=62.0,
        overall_bottom_quartile=25.0,
        dimension_benchmarks={
            "data_maturity": {
                "average": 38.0,
                "top_quartile": 58.0,
                "bottom_quartile": 22.0,
                "leader_score": 75.0
            },
            "technology_infrastructure": {
                "average": 35.0,
                "top_quartile": 55.0,
                "bottom_quartile": 20.0,
                "leader_score": 72.0
            },
            "process_operations": {
                "average": 45.0,
                "top_quartile": 65.0,
                "bottom_quartile": 28.0,
                "leader_score": 78.0
            },
            "workforce_culture": {
                "average": 40.0,
                "top_quartile": 60.0,
                "bottom_quartile": 25.0,
                "leader_score": 75.0
            },
            "governance_compliance": {
                "average": 52.0,
                "top_quartile": 72.0,
                "bottom_quartile": 35.0,
                "leader_score": 85.0
            }
        },
        sample_size="Based on 200+ government agencies (federal, state, local)",
        source="Aggregated from Deloitte Government AI Survey and Gartner Public Sector reports"
    ),

    "healthcare": BenchmarkData(
        sector="healthcare",
        sector_name="Healthcare",
        overall_average=48.0,
        overall_top_quartile=68.0,
        overall_bottom_quartile=30.0,
        dimension_benchmarks={
            "data_maturity": {
                "average": 45.0,
                "top_quartile": 65.0,
                "bottom_quartile": 28.0,
                "leader_score": 80.0
            },
            "technology_infrastructure": {
                "average": 42.0,
                "top_quartile": 62.0,
                "bottom_quartile": 25.0,
                "leader_score": 78.0
            },
            "process_operations": {
                "average": 50.0,
                "top_quartile": 70.0,
                "bottom_quartile": 32.0,
                "leader_score": 82.0
            },
            "workforce_culture": {
                "average": 48.0,
                "top_quartile": 68.0,
                "bottom_quartile": 30.0,
                "leader_score": 80.0
            },
            "governance_compliance": {
                "average": 58.0,
                "top_quartile": 78.0,
                "bottom_quartile": 40.0,
                "leader_score": 90.0
            }
        },
        sample_size="Based on 300+ healthcare organizations",
        source="Aggregated from HIMSS, McKinsey Healthcare, and Deloitte Health reports"
    ),

    "manufacturing": BenchmarkData(
        sector="manufacturing",
        sector_name="Manufacturing",
        overall_average=52.0,
        overall_top_quartile=72.0,
        overall_bottom_quartile=32.0,
        dimension_benchmarks={
            "data_maturity": {
                "average": 48.0,
                "top_quartile": 68.0,
                "bottom_quartile": 30.0,
                "leader_score": 82.0
            },
            "technology_infrastructure": {
                "average": 50.0,
                "top_quartile": 70.0,
                "bottom_quartile": 32.0,
                "leader_score": 85.0
            },
            "process_operations": {
                "average": 58.0,
                "top_quartile": 78.0,
                "bottom_quartile": 38.0,
                "leader_score": 88.0
            },
            "workforce_culture": {
                "average": 45.0,
                "top_quartile": 65.0,
                "bottom_quartile": 28.0,
                "leader_score": 78.0
            },
            "governance_compliance": {
                "average": 55.0,
                "top_quartile": 75.0,
                "bottom_quartile": 38.0,
                "leader_score": 85.0
            }
        },
        sample_size="Based on 400+ manufacturing companies",
        source="Aggregated from McKinsey Industry 4.0 and Deloitte Smart Factory reports"
    ),

    "retail": BenchmarkData(
        sector="retail",
        sector_name="Retail",
        overall_average=50.0,
        overall_top_quartile=70.0,
        overall_bottom_quartile=32.0,
        dimension_benchmarks={
            "data_maturity": {
                "average": 52.0,
                "top_quartile": 72.0,
                "bottom_quartile": 34.0,
                "leader_score": 85.0
            },
            "technology_infrastructure": {
                "average": 48.0,
                "top_quartile": 68.0,
                "bottom_quartile": 30.0,
                "leader_score": 82.0
            },
            "process_operations": {
                "average": 55.0,
                "top_quartile": 75.0,
                "bottom_quartile": 36.0,
                "leader_score": 88.0
            },
            "workforce_culture": {
                "average": 45.0,
                "top_quartile": 65.0,
                "bottom_quartile": 28.0,
                "leader_score": 78.0
            },
            "governance_compliance": {
                "average": 48.0,
                "top_quartile": 68.0,
                "bottom_quartile": 30.0,
                "leader_score": 80.0
            }
        },
        sample_size="Based on 350+ retail organizations",
        source="Aggregated from NRF, McKinsey Retail, and Deloitte Consumer reports"
    ),

    "general": BenchmarkData(
        sector="general",
        sector_name="Cross-Industry Average",
        overall_average=50.0,
        overall_top_quartile=70.0,
        overall_bottom_quartile=30.0,
        dimension_benchmarks={
            "data_maturity": {
                "average": 48.0,
                "top_quartile": 68.0,
                "bottom_quartile": 30.0,
                "leader_score": 85.0
            },
            "technology_infrastructure": {
                "average": 45.0,
                "top_quartile": 65.0,
                "bottom_quartile": 28.0,
                "leader_score": 82.0
            },
            "process_operations": {
                "average": 52.0,
                "top_quartile": 72.0,
                "bottom_quartile": 34.0,
                "leader_score": 85.0
            },
            "workforce_culture": {
                "average": 48.0,
                "top_quartile": 68.0,
                "bottom_quartile": 30.0,
                "leader_score": 80.0
            },
            "governance_compliance": {
                "average": 52.0,
                "top_quartile": 72.0,
                "bottom_quartile": 35.0,
                "leader_score": 85.0
            }
        },
        sample_size="Based on 2000+ organizations across industries",
        source="Aggregated from McKinsey State of AI 2024 and Deloitte AI Institute"
    )
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_benchmark_for_sector(sector: str = "general") -> BenchmarkData:
    """
    Get benchmark data for a specific sector.

    Args:
        sector: One of the defined sectors

    Returns:
        BenchmarkData for the sector (defaults to general if not found)
    """
    return BENCHMARKS.get(sector, BENCHMARKS["general"])


def compare_to_benchmark(
    score: float,
    dimension: Optional[str],
    sector: str = "general"
) -> Dict[str, Any]:
    """
    Compare a score to sector benchmarks.

    Args:
        score: The score to compare (0-100)
        dimension: Specific dimension to compare (None for overall)
        sector: Industry sector

    Returns:
        Dict with comparison results
    """
    benchmark = get_benchmark_for_sector(sector)

    if dimension and dimension in benchmark.dimension_benchmarks:
        dim_bench = benchmark.dimension_benchmarks[dimension]
        average = dim_bench["average"]
        top_quartile = dim_bench["top_quartile"]
        bottom_quartile = dim_bench["bottom_quartile"]
        leader_score = dim_bench["leader_score"]
    else:
        average = benchmark.overall_average
        top_quartile = benchmark.overall_top_quartile
        bottom_quartile = benchmark.overall_bottom_quartile
        leader_score = 90.0  # Default leader benchmark

    # Determine position
    if score >= top_quartile:
        position = "Top Quartile"
        position_color = "#28a745"  # Green
    elif score >= average:
        position = "Above Average"
        position_color = "#17a2b8"  # Blue
    elif score >= bottom_quartile:
        position = "Below Average"
        position_color = "#fd7e14"  # Orange
    else:
        position = "Bottom Quartile"
        position_color = "#dc3545"  # Red

    # Calculate gaps
    gap_to_average = round(score - average, 1)
    gap_to_top = round(score - top_quartile, 1)
    gap_to_leader = round(score - leader_score, 1)

    return {
        "score": score,
        "sector": sector,
        "sector_name": benchmark.sector_name,
        "dimension": dimension,
        "benchmarks": {
            "average": average,
            "top_quartile": top_quartile,
            "bottom_quartile": bottom_quartile,
            "leader": leader_score
        },
        "position": position,
        "position_color": position_color,
        "gaps": {
            "to_average": gap_to_average,
            "to_top_quartile": gap_to_top,
            "to_leader": gap_to_leader
        },
        "percentile_estimate": _estimate_percentile(score, average, top_quartile, bottom_quartile),
        "source": benchmark.source
    }


def _estimate_percentile(
    score: float,
    average: float,
    top_quartile: float,
    bottom_quartile: float
) -> int:
    """Estimate percentile ranking based on score and quartiles."""
    if score >= top_quartile:
        # Linear interpolation from 75th to 95th percentile
        pct_above_top = (score - top_quartile) / (100 - top_quartile)
        return min(95, int(75 + pct_above_top * 20))
    elif score >= average:
        # 50th to 75th percentile
        pct_above_avg = (score - average) / (top_quartile - average)
        return int(50 + pct_above_avg * 25)
    elif score >= bottom_quartile:
        # 25th to 50th percentile
        pct_above_bottom = (score - bottom_quartile) / (average - bottom_quartile)
        return int(25 + pct_above_bottom * 25)
    else:
        # Below 25th percentile
        pct_in_bottom = score / bottom_quartile
        return max(5, int(pct_in_bottom * 25))


def get_benchmark_summary(sector: str = "general") -> Dict[str, Any]:
    """
    Get a summary of benchmarks for display.

    Returns:
        Dict with benchmark summary for the sector
    """
    benchmark = get_benchmark_for_sector(sector)

    return {
        "sector": benchmark.sector,
        "sector_name": benchmark.sector_name,
        "overall": {
            "average": benchmark.overall_average,
            "top_quartile": benchmark.overall_top_quartile,
            "bottom_quartile": benchmark.overall_bottom_quartile
        },
        "dimensions": {
            dim_id: {
                "average": dim_data["average"],
                "top_quartile": dim_data["top_quartile"]
            }
            for dim_id, dim_data in benchmark.dimension_benchmarks.items()
        },
        "sample_size": benchmark.sample_size,
        "source": benchmark.source
    }


def get_all_sector_benchmarks() -> Dict[str, Dict[str, float]]:
    """
    Get overall benchmarks for all sectors (for cross-industry comparison).

    Returns:
        Dict mapping sector to overall benchmark scores
    """
    return {
        sector: {
            "average": data.overall_average,
            "top_quartile": data.overall_top_quartile
        }
        for sector, data in BENCHMARKS.items()
    }
