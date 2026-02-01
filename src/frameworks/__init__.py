"""
Enterprise AI Framework Generator Module

Generates comprehensive, board-ready AI frameworks based on assessment results:
- AI Strategy Framework (~2,500 lines) - Strategic pillars, OKRs, talent strategy, technology recommendations
- AI Governance Framework (~2,500 lines) - Three Lines of Defense, RACI, policies, lifecycle governance
- Responsible AI / Ethics Framework (~4,300 lines) - EU AI Act, NIST AI RMF, bias frameworks, ethics board
- MLOps Framework (~1,800 lines) - ML lifecycle, feature stores, deployment, monitoring
- Data Strategy Framework (~1,200 lines) - Data governance, quality, architecture, AI data practices
"""

from .strategy_builder import AIStrategyBuilder
from .governance_builder import GovernanceFrameworkBuilder
from .ethics_framework import EthicsFrameworkBuilder
from .mlops_builder import MLOpsFrameworkBuilder
from .data_strategy_builder import DataStrategyBuilder

__all__ = [
    'AIStrategyBuilder',
    'GovernanceFrameworkBuilder',
    'EthicsFrameworkBuilder',
    'MLOpsFrameworkBuilder',
    'DataStrategyBuilder'
]
