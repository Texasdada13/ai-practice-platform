"""
Enterprise Data Strategy Framework Builder

Generates comprehensive, board-ready Data Strategy frameworks for AI including:
- Data governance and stewardship
- Data architecture and infrastructure
- Data quality management
- Data catalog and discovery
- Data security and privacy
- Master data management
- Data integration and pipelines
- Data literacy and culture
- Data monetization and value
- Regulatory compliance (GDPR, CCPA, etc.)
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

# Optional Claude API integration
try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


# =============================================================================
# ENUMERATIONS
# =============================================================================

class DataMaturityLevel(Enum):
    """Data maturity levels"""
    INITIAL = "Level 1: Initial - Ad-hoc data management"
    MANAGED = "Level 2: Managed - Basic data practices"
    DEFINED = "Level 3: Defined - Standardized processes"
    QUANTIFIED = "Level 4: Quantified - Measured and optimized"
    OPTIMIZING = "Level 5: Optimizing - Continuous improvement"


class DataDomain(Enum):
    """Data domain types"""
    CUSTOMER = "Customer Data"
    PRODUCT = "Product Data"
    FINANCIAL = "Financial Data"
    OPERATIONAL = "Operational Data"
    EMPLOYEE = "Employee Data"
    THIRD_PARTY = "Third-Party Data"
    SENSOR_IOT = "Sensor/IoT Data"
    BEHAVIORAL = "Behavioral Data"


class DataClassification(Enum):
    """Data sensitivity classification"""
    PUBLIC = "Public - No restrictions"
    INTERNAL = "Internal - Organization only"
    CONFIDENTIAL = "Confidential - Need to know"
    RESTRICTED = "Restricted - Highly sensitive"
    REGULATED = "Regulated - Compliance requirements"


class DataQualityDimension(Enum):
    """Data quality dimensions"""
    ACCURACY = "Accuracy"
    COMPLETENESS = "Completeness"
    CONSISTENCY = "Consistency"
    TIMELINESS = "Timeliness"
    VALIDITY = "Validity"
    UNIQUENESS = "Uniqueness"


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class DataStrategyFramework:
    """Complete Data Strategy Framework"""
    organization_name: str
    sector: str
    vision_and_principles: Dict[str, Any]
    data_governance: Dict[str, Any]
    data_architecture: Dict[str, Any]
    data_quality: Dict[str, Any]
    data_catalog: Dict[str, Any]
    data_security_privacy: Dict[str, Any]
    master_data_management: Dict[str, Any]
    data_integration: Dict[str, Any]
    data_for_ai: Dict[str, Any]
    data_literacy: Dict[str, Any]
    data_value_monetization: Dict[str, Any]
    regulatory_compliance: Dict[str, Any]
    team_structure: Dict[str, Any]
    technology_stack: Dict[str, Any]
    implementation_roadmap: List[Dict[str, Any]]
    metrics_and_kpis: Dict[str, Any]
    generated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "organization_name": self.organization_name,
            "sector": self.sector,
            "vision_and_principles": self.vision_and_principles,
            "data_governance": self.data_governance,
            "data_architecture": self.data_architecture,
            "data_quality": self.data_quality,
            "data_catalog": self.data_catalog,
            "data_security_privacy": self.data_security_privacy,
            "master_data_management": self.master_data_management,
            "data_integration": self.data_integration,
            "data_for_ai": self.data_for_ai,
            "data_literacy": self.data_literacy,
            "data_value_monetization": self.data_value_monetization,
            "regulatory_compliance": self.regulatory_compliance,
            "team_structure": self.team_structure,
            "technology_stack": self.technology_stack,
            "implementation_roadmap": self.implementation_roadmap,
            "metrics_and_kpis": self.metrics_and_kpis,
            "generated_at": self.generated_at.isoformat()
        }


# =============================================================================
# DATA STRATEGY BUILDER
# =============================================================================

class DataStrategyBuilder:
    """
    Enterprise Data Strategy Framework Builder

    Generates comprehensive data strategy frameworks tailored to organizational
    needs, maturity, and AI readiness requirements.
    """

    def __init__(self, anthropic_api_key: Optional[str] = None):
        """Initialize builder with optional Claude API integration"""
        self.client = None
        if anthropic_api_key and ANTHROPIC_AVAILABLE:
            try:
                self.client = Anthropic(api_key=anthropic_api_key)
            except Exception:
                self.client = None

    def build_framework(
        self,
        organization_name: str,
        assessment_result: Optional[Dict[str, Any]] = None,
        sector: str = "general",
        primary_cloud: Optional[str] = None,
        regulatory_jurisdictions: Optional[List[str]] = None
    ) -> DataStrategyFramework:
        """
        Build comprehensive Data Strategy Framework.

        Args:
            organization_name: Name of the organization
            assessment_result: Optional AI maturity assessment results
            sector: Industry sector
            primary_cloud: Primary cloud provider
            regulatory_jurisdictions: Applicable regulatory jurisdictions

        Returns:
            Complete DataStrategyFramework
        """
        maturity = self._assess_maturity(assessment_result)
        jurisdictions = regulatory_jurisdictions or ["us", "eu"]

        return DataStrategyFramework(
            organization_name=organization_name,
            sector=sector,
            vision_and_principles=self._build_vision_and_principles(organization_name),
            data_governance=self._build_data_governance(),
            data_architecture=self._build_data_architecture(primary_cloud),
            data_quality=self._build_data_quality(),
            data_catalog=self._build_data_catalog(),
            data_security_privacy=self._build_data_security_privacy(sector),
            master_data_management=self._build_mdm(),
            data_integration=self._build_data_integration(),
            data_for_ai=self._build_data_for_ai(),
            data_literacy=self._build_data_literacy(),
            data_value_monetization=self._build_data_value(),
            regulatory_compliance=self._build_regulatory_compliance(jurisdictions, sector),
            team_structure=self._build_team_structure(),
            technology_stack=self._build_technology_stack(primary_cloud),
            implementation_roadmap=self._build_implementation_roadmap(maturity),
            metrics_and_kpis=self._build_metrics_and_kpis()
        )

    def _assess_maturity(self, assessment_result: Optional[Dict[str, Any]]) -> str:
        """Assess current data maturity"""
        if not assessment_result:
            return DataMaturityLevel.MANAGED.value

        score = assessment_result.get("dimensions", {}).get("data", {}).get("score", 40)
        if score >= 80:
            return DataMaturityLevel.OPTIMIZING.value
        elif score >= 60:
            return DataMaturityLevel.QUANTIFIED.value
        elif score >= 40:
            return DataMaturityLevel.DEFINED.value
        elif score >= 20:
            return DataMaturityLevel.MANAGED.value
        else:
            return DataMaturityLevel.INITIAL.value

    def _build_vision_and_principles(self, org_name: str) -> Dict[str, Any]:
        """Build data vision and principles"""
        return {
            "vision": f"{org_name} will leverage data as a strategic asset to drive AI innovation, operational excellence, and competitive advantage while maintaining the highest standards of data governance, quality, and ethical use.",
            "mission": "Enable data-driven decision making and AI capabilities through trusted, accessible, and well-governed data assets.",
            "principles": {
                "data_as_asset": {
                    "principle": "Data is a Strategic Asset",
                    "description": "Data is treated as a valuable organizational asset, managed with the same rigor as financial assets.",
                    "implications": [
                        "Data has assigned ownership and stewardship",
                        "Data investments are evaluated for ROI",
                        "Data assets are inventoried and valued"
                    ]
                },
                "single_source_of_truth": {
                    "principle": "Single Source of Truth",
                    "description": "Critical data has one authoritative source that is the reference for the organization.",
                    "implications": [
                        "Master data is centrally managed",
                        "Data duplication is minimized",
                        "Reference data is standardized"
                    ]
                },
                "data_quality_by_design": {
                    "principle": "Quality by Design",
                    "description": "Data quality is built into processes from the point of creation, not fixed afterward.",
                    "implications": [
                        "Data quality rules at source",
                        "Validation at point of entry",
                        "Quality metrics monitored continuously"
                    ]
                },
                "data_accessibility": {
                    "principle": "Data Accessibility",
                    "description": "Data is accessible to those who need it, when they need it, in usable formats.",
                    "implications": [
                        "Self-service data access",
                        "Data discovery through catalog",
                        "APIs and tools for data access"
                    ]
                },
                "data_security": {
                    "principle": "Data Security and Privacy",
                    "description": "Data is protected according to its sensitivity, with privacy respected throughout the lifecycle.",
                    "implications": [
                        "Classification-based protection",
                        "Privacy by design",
                        "Regulatory compliance"
                    ]
                },
                "data_ethics": {
                    "principle": "Ethical Data Use",
                    "description": "Data is collected, processed, and used ethically, respecting individuals and communities.",
                    "implications": [
                        "Transparent data practices",
                        "Consent and purpose limitation",
                        "Bias awareness in data use"
                    ]
                }
            }
        }

    def _build_data_governance(self) -> Dict[str, Any]:
        """Build data governance framework"""
        return {
            "purpose": "Establish accountability, policies, and processes for data management across the organization",
            "governance_model": {
                "federated_model": {
                    "description": "Central governance with distributed execution",
                    "central_team": {
                        "role": "Data Governance Office",
                        "responsibilities": [
                            "Define data policies and standards",
                            "Manage governance tools and processes",
                            "Monitor compliance",
                            "Coordinate across domains"
                        ]
                    },
                    "domain_teams": {
                        "role": "Data Stewards in business domains",
                        "responsibilities": [
                            "Implement governance in their domain",
                            "Ensure data quality",
                            "Manage domain-specific metadata",
                            "Escalate issues to central team"
                        ]
                    }
                }
            },
            "roles_and_responsibilities": {
                "chief_data_officer": {
                    "title": "Chief Data Officer (CDO)",
                    "level": "Executive",
                    "responsibilities": [
                        "Overall data strategy ownership",
                        "Data governance program leadership",
                        "Data-driven culture advocacy",
                        "Executive reporting on data initiatives"
                    ],
                    "reports_to": "CEO/COO"
                },
                "data_governance_council": {
                    "title": "Data Governance Council",
                    "composition": ["CDO", "Business domain leaders", "IT leadership", "Legal/Compliance", "Security"],
                    "responsibilities": [
                        "Approve data policies",
                        "Prioritize governance initiatives",
                        "Resolve cross-domain issues",
                        "Monitor governance effectiveness"
                    ],
                    "meeting_frequency": "Monthly"
                },
                "data_owner": {
                    "title": "Data Owner",
                    "level": "Business leadership",
                    "responsibilities": [
                        "Accountable for data in their domain",
                        "Approve data access requests",
                        "Define data quality requirements",
                        "Prioritize data improvements"
                    ],
                    "assignment": "One per major data domain"
                },
                "data_steward": {
                    "title": "Data Steward",
                    "level": "Subject matter expert",
                    "responsibilities": [
                        "Day-to-day data management",
                        "Data quality monitoring and remediation",
                        "Metadata management",
                        "Data documentation"
                    ],
                    "assignment": "Multiple per data domain"
                },
                "data_custodian": {
                    "title": "Data Custodian (Technical)",
                    "level": "IT/Engineering",
                    "responsibilities": [
                        "Technical data management",
                        "Data storage and security",
                        "Access control implementation",
                        "Technical data quality"
                    ]
                }
            },
            "policies": {
                "data_classification_policy": {
                    "purpose": "Define sensitivity levels and handling requirements",
                    "classifications": {
                        DataClassification.PUBLIC.value: {
                            "description": "No restrictions on access or sharing",
                            "examples": ["Public website content", "Published reports"],
                            "handling": "Standard handling"
                        },
                        DataClassification.INTERNAL.value: {
                            "description": "Available to all employees",
                            "examples": ["Internal communications", "General business data"],
                            "handling": "Access controlled to employees"
                        },
                        DataClassification.CONFIDENTIAL.value: {
                            "description": "Limited to those with business need",
                            "examples": ["Customer data", "Financial details", "Strategy documents"],
                            "handling": "Need-to-know access, encryption in transit"
                        },
                        DataClassification.RESTRICTED.value: {
                            "description": "Highly sensitive, strict controls",
                            "examples": ["PII", "PHI", "Payment card data", "Trade secrets"],
                            "handling": "Encryption at rest/transit, audit logging, DLP"
                        },
                        DataClassification.REGULATED.value: {
                            "description": "Subject to regulatory requirements",
                            "examples": ["GDPR personal data", "HIPAA PHI", "PCI data"],
                            "handling": "Regulatory controls, retention requirements"
                        }
                    }
                },
                "data_retention_policy": {
                    "purpose": "Define how long data is retained",
                    "principles": [
                        "Retain only as long as needed for business or legal purposes",
                        "Apply retention periods by data type",
                        "Document retention rationale",
                        "Implement automated retention enforcement"
                    ],
                    "retention_schedule": {
                        "transactional_data": "7 years (financial compliance)",
                        "customer_data": "Duration of relationship + 3 years",
                        "employee_data": "Duration of employment + 7 years",
                        "log_data": "1 year (or per security policy)",
                        "ml_training_data": "Model lifecycle + audit period"
                    }
                },
                "data_access_policy": {
                    "purpose": "Define who can access data and how",
                    "principles": [
                        "Least privilege access",
                        "Role-based access control",
                        "Request and approval workflow for sensitive data",
                        "Regular access reviews"
                    ]
                },
                "data_quality_policy": {
                    "purpose": "Define data quality standards and responsibilities",
                    "principles": [
                        "Quality requirements defined for each data asset",
                        "Quality measured against defined dimensions",
                        "Issues tracked and remediated",
                        "Quality reported to governance"
                    ]
                }
            },
            "processes": {
                "data_issue_management": {
                    "description": "Process for reporting and resolving data issues",
                    "steps": [
                        "Issue reported through governance tool",
                        "Triaged by data steward",
                        "Root cause analysis",
                        "Remediation and prevention",
                        "Closure and documentation"
                    ]
                },
                "data_change_management": {
                    "description": "Process for managing changes to data structures and definitions",
                    "steps": [
                        "Change request submitted",
                        "Impact assessment",
                        "Stakeholder review",
                        "Approval and implementation",
                        "Documentation update"
                    ]
                },
                "data_access_request": {
                    "description": "Process for requesting access to data",
                    "steps": [
                        "Request submitted with business justification",
                        "Data owner approval",
                        "Security/privacy review (for sensitive data)",
                        "Access provisioned",
                        "Periodic access review"
                    ]
                }
            }
        }

    def _build_data_architecture(self, primary_cloud: Optional[str]) -> Dict[str, Any]:
        """Build data architecture framework"""
        cloud_architectures = {
            "aws": {
                "storage": ["S3", "Redshift", "RDS", "DynamoDB"],
                "processing": ["Glue", "EMR", "Athena", "Lambda"],
                "integration": ["Glue ETL", "AppFlow", "DataSync"],
                "analytics": ["QuickSight", "SageMaker"],
                "governance": ["Lake Formation", "Glue Data Catalog"]
            },
            "gcp": {
                "storage": ["GCS", "BigQuery", "Cloud SQL", "Bigtable"],
                "processing": ["Dataflow", "Dataproc", "Cloud Functions"],
                "integration": ["Datastream", "Data Fusion"],
                "analytics": ["Looker", "Vertex AI"],
                "governance": ["Dataplex", "Data Catalog"]
            },
            "azure": {
                "storage": ["ADLS", "Synapse", "SQL Database", "Cosmos DB"],
                "processing": ["Data Factory", "Databricks", "HDInsight"],
                "integration": ["Data Factory", "Logic Apps"],
                "analytics": ["Power BI", "Azure ML"],
                "governance": ["Purview", "Unity Catalog (Databricks)"]
            }
        }

        return {
            "architecture_principles": [
                "Separate storage from compute",
                "Design for scale and flexibility",
                "Enable self-service data access",
                "Ensure data lineage and traceability",
                "Optimize for both batch and real-time",
                "Build for multi-cloud portability where practical"
            ],
            "architecture_patterns": {
                "data_lakehouse": {
                    "description": "Combines data lake flexibility with data warehouse structure",
                    "components": [
                        "Object storage for raw data (Bronze layer)",
                        "Curated layer with schema enforcement (Silver layer)",
                        "Consumption layer with business views (Gold layer)"
                    ],
                    "technologies": ["Delta Lake", "Apache Iceberg", "Apache Hudi"],
                    "benefits": [
                        "Single platform for all analytics",
                        "ACID transactions on data lake",
                        "Schema evolution support",
                        "Time travel capabilities"
                    ],
                    "use_when": "Modern green-field or migration projects"
                },
                "modern_data_warehouse": {
                    "description": "Cloud-native data warehouse with separation of storage and compute",
                    "components": [
                        "Staging area for raw data",
                        "Dimensional models for analytics",
                        "Semantic layer for business definitions"
                    ],
                    "technologies": ["Snowflake", "BigQuery", "Redshift", "Synapse"],
                    "benefits": [
                        "Familiar SQL interface",
                        "Strong governance",
                        "High performance for BI"
                    ],
                    "use_when": "Strong BI/reporting focus, SQL-centric teams"
                },
                "data_mesh": {
                    "description": "Decentralized data ownership with domain teams",
                    "principles": [
                        "Domain-oriented data ownership",
                        "Data as a product",
                        "Self-serve data platform",
                        "Federated computational governance"
                    ],
                    "benefits": [
                        "Scales with organization",
                        "Domain expertise retained",
                        "Reduces central bottleneck"
                    ],
                    "challenges": [
                        "Requires mature data culture",
                        "Coordination complexity",
                        "Tooling requirements"
                    ],
                    "use_when": "Large organizations with strong domain teams"
                }
            },
            "data_zones": {
                "landing_zone": {
                    "purpose": "Initial data ingestion point",
                    "characteristics": [
                        "Raw data as-is from source",
                        "Immutable storage",
                        "Minimal transformation"
                    ],
                    "retention": "Short-term (days to weeks)"
                },
                "raw_zone": {
                    "purpose": "Persistent storage of source data",
                    "characteristics": [
                        "Organized by source",
                        "Schema-on-read",
                        "Historical data preserved"
                    ],
                    "retention": "Long-term"
                },
                "curated_zone": {
                    "purpose": "Cleaned and standardized data",
                    "characteristics": [
                        "Quality validated",
                        "Standardized formats",
                        "Joined and enriched"
                    ],
                    "access": "Data scientists, analysts"
                },
                "consumption_zone": {
                    "purpose": "Business-ready data products",
                    "characteristics": [
                        "Business-defined aggregations",
                        "Optimized for consumption",
                        "Documented and discoverable"
                    ],
                    "access": "Business users, BI tools, applications"
                },
                "sandbox_zone": {
                    "purpose": "Experimentation and development",
                    "characteristics": [
                        "Isolated from production",
                        "Copy of relevant data",
                        "Flexible structure"
                    ],
                    "access": "Data scientists, developers"
                }
            },
            "cloud_services": cloud_architectures.get(primary_cloud, {}),
            "key_capabilities": {
                "data_ingestion": {
                    "batch": "Scheduled bulk data movement",
                    "streaming": "Real-time data ingestion",
                    "change_data_capture": "Capture and replicate changes"
                },
                "data_processing": {
                    "batch_processing": "Large-scale data transformation",
                    "stream_processing": "Real-time data processing",
                    "data_preparation": "Self-service data prep"
                },
                "data_serving": {
                    "olap": "Analytical queries",
                    "oltp": "Transactional workloads",
                    "feature_serving": "ML feature delivery"
                }
            }
        }

    def _build_data_quality(self) -> Dict[str, Any]:
        """Build data quality framework"""
        return {
            "purpose": "Ensure data meets quality standards for reliable analytics and AI",
            "quality_dimensions": {
                DataQualityDimension.ACCURACY.value: {
                    "definition": "Data correctly represents real-world entity or event",
                    "measurement": "Compare against source or reference data",
                    "examples": ["Customer address matches actual address", "Transaction amounts are correct"]
                },
                DataQualityDimension.COMPLETENESS.value: {
                    "definition": "Required data values are present",
                    "measurement": "Percentage of non-null values for required fields",
                    "examples": ["All customers have email", "All orders have customer ID"]
                },
                DataQualityDimension.CONSISTENCY.value: {
                    "definition": "Data is consistent across systems and time",
                    "measurement": "Cross-system reconciliation, business rule validation",
                    "examples": ["Customer count matches across systems", "State codes are valid"]
                },
                DataQualityDimension.TIMELINESS.value: {
                    "definition": "Data is available when needed",
                    "measurement": "Data latency, refresh frequency compliance",
                    "examples": ["Dashboard data is refreshed hourly", "Events processed within 5 minutes"]
                },
                DataQualityDimension.VALIDITY.value: {
                    "definition": "Data conforms to defined formats and ranges",
                    "measurement": "Format validation, range checks",
                    "examples": ["Email addresses are valid format", "Dates are in expected range"]
                },
                DataQualityDimension.UNIQUENESS.value: {
                    "definition": "No unintended duplicate records",
                    "measurement": "Duplicate detection on key fields",
                    "examples": ["No duplicate customer IDs", "No duplicate transactions"]
                }
            },
            "quality_management_process": {
                "define": {
                    "description": "Define quality requirements",
                    "activities": [
                        "Identify critical data elements",
                        "Define quality dimensions for each",
                        "Set quality thresholds",
                        "Document quality rules"
                    ]
                },
                "measure": {
                    "description": "Measure quality against requirements",
                    "activities": [
                        "Implement quality checks",
                        "Execute quality profiling",
                        "Calculate quality scores",
                        "Identify quality issues"
                    ]
                },
                "analyze": {
                    "description": "Analyze quality issues",
                    "activities": [
                        "Root cause analysis",
                        "Impact assessment",
                        "Prioritization"
                    ]
                },
                "improve": {
                    "description": "Remediate quality issues",
                    "activities": [
                        "Data cleansing",
                        "Process improvement",
                        "Source system fixes"
                    ]
                },
                "monitor": {
                    "description": "Ongoing quality monitoring",
                    "activities": [
                        "Continuous quality checks",
                        "Quality dashboards",
                        "Alerting on degradation"
                    ]
                }
            },
            "implementation_approach": {
                "data_profiling": {
                    "description": "Analyze data to understand quality",
                    "techniques": [
                        "Column statistics",
                        "Pattern analysis",
                        "Relationship discovery",
                        "Anomaly detection"
                    ]
                },
                "data_validation": {
                    "description": "Validate data against rules",
                    "types": [
                        "Schema validation",
                        "Business rule validation",
                        "Referential integrity",
                        "Cross-field validation"
                    ]
                },
                "data_cleansing": {
                    "description": "Fix quality issues in data",
                    "techniques": [
                        "Standardization",
                        "Deduplication",
                        "Enrichment",
                        "Imputation"
                    ]
                }
            },
            "quality_tools": ["Great Expectations", "Soda", "Monte Carlo", "dbt tests", "Apache Griffin"],
            "quality_metrics": {
                "dq_score": "Overall data quality score (weighted average of dimensions)",
                "rule_pass_rate": "Percentage of quality rules passing",
                "issue_resolution_time": "Time to resolve quality issues",
                "data_freshness": "Latency of data updates"
            }
        }

    def _build_data_catalog(self) -> Dict[str, Any]:
        """Build data catalog framework"""
        return {
            "purpose": "Enable data discovery, understanding, and governance through centralized metadata",
            "catalog_capabilities": {
                "data_discovery": {
                    "description": "Find relevant data assets",
                    "features": [
                        "Search across all data assets",
                        "Browse by domain/category",
                        "Filter by classification, owner, quality",
                        "View popularity and usage"
                    ]
                },
                "data_documentation": {
                    "description": "Understand data meaning and usage",
                    "features": [
                        "Business descriptions",
                        "Technical metadata",
                        "Data dictionaries",
                        "Usage examples"
                    ]
                },
                "data_lineage": {
                    "description": "Track data flow and transformations",
                    "features": [
                        "Source-to-target lineage",
                        "Transformation documentation",
                        "Impact analysis",
                        "Dependency tracking"
                    ]
                },
                "data_governance": {
                    "description": "Manage data governance through catalog",
                    "features": [
                        "Data classification",
                        "Ownership assignment",
                        "Policy enforcement",
                        "Access requests"
                    ]
                }
            },
            "metadata_types": {
                "technical_metadata": {
                    "description": "System-captured metadata",
                    "examples": [
                        "Table schemas",
                        "Column types",
                        "Row counts",
                        "Last updated timestamps"
                    ]
                },
                "business_metadata": {
                    "description": "Human-provided business context",
                    "examples": [
                        "Business definitions",
                        "Data owners",
                        "Use cases",
                        "Quality requirements"
                    ]
                },
                "operational_metadata": {
                    "description": "Metadata from data operations",
                    "examples": [
                        "Job run history",
                        "Query patterns",
                        "Access logs",
                        "Quality metrics"
                    ]
                },
                "social_metadata": {
                    "description": "User-generated metadata",
                    "examples": [
                        "Ratings and reviews",
                        "Tags",
                        "Questions and answers",
                        "Usage recommendations"
                    ]
                }
            },
            "catalog_standards": {
                "naming_conventions": {
                    "tables": "domain_entity_description (e.g., sales_customer_transactions)",
                    "columns": "snake_case, descriptive names",
                    "documentation": "Required for all production data assets"
                },
                "required_metadata": [
                    "Business description",
                    "Data owner",
                    "Data classification",
                    "Update frequency",
                    "Primary use case"
                ]
            },
            "catalog_tools": ["Alation", "Collibra", "Atlan", "DataHub", "AWS Glue Catalog", "Dataplex", "Purview"]
        }

    def _build_data_security_privacy(self, sector: str) -> Dict[str, Any]:
        """Build data security and privacy framework"""
        sector_requirements = {
            "financial_services": {
                "regulations": ["GLBA", "SOX", "PCI-DSS", "GDPR", "CCPA"],
                "special_requirements": [
                    "Payment card data protection",
                    "Financial reporting data integrity",
                    "Customer financial data privacy"
                ]
            },
            "healthcare": {
                "regulations": ["HIPAA", "HITECH", "GDPR"],
                "special_requirements": [
                    "PHI protection and access controls",
                    "De-identification for analytics",
                    "Patient consent management"
                ]
            },
            "government": {
                "regulations": ["FedRAMP", "FISMA", "Privacy Act"],
                "special_requirements": [
                    "Data residency requirements",
                    "Clearance-based access",
                    "Public records management"
                ]
            }
        }

        return {
            "purpose": "Protect data according to sensitivity and ensure privacy compliance",
            "security_framework": {
                "data_protection": {
                    "encryption_at_rest": {
                        "requirement": "Encrypt all Confidential and Restricted data at rest",
                        "implementation": "AES-256 encryption, managed keys or customer-managed keys"
                    },
                    "encryption_in_transit": {
                        "requirement": "Encrypt all data in transit",
                        "implementation": "TLS 1.2+ for all data transfers"
                    },
                    "encryption_in_use": {
                        "requirement": "Consider for highly sensitive processing",
                        "implementation": "Confidential computing, secure enclaves"
                    }
                },
                "access_control": {
                    "principles": [
                        "Least privilege access",
                        "Role-based access control (RBAC)",
                        "Attribute-based access control (ABAC) for complex scenarios",
                        "Regular access reviews"
                    ],
                    "implementation": [
                        "Centralized identity management",
                        "Data access policies in catalog/governance tool",
                        "Just-in-time access for sensitive data",
                        "Break-glass procedures for emergencies"
                    ]
                },
                "data_masking": {
                    "purpose": "Protect sensitive data while enabling use",
                    "techniques": {
                        "static_masking": "Permanent replacement of sensitive data for non-prod",
                        "dynamic_masking": "Real-time masking based on user permissions",
                        "tokenization": "Replace with non-reversible token, maintain referential integrity",
                        "anonymization": "Remove identifying information permanently"
                    }
                },
                "data_loss_prevention": {
                    "purpose": "Prevent unauthorized data exfiltration",
                    "controls": [
                        "Classify and tag sensitive data",
                        "Monitor data movement",
                        "Block unauthorized transfers",
                        "Alert on policy violations"
                    ]
                }
            },
            "privacy_framework": {
                "privacy_principles": [
                    "Purpose limitation - collect for specified purposes",
                    "Data minimization - collect only necessary data",
                    "Storage limitation - retain only as long as needed",
                    "Accuracy - keep data accurate and current",
                    "Integrity and confidentiality - protect data security",
                    "Accountability - demonstrate compliance"
                ],
                "privacy_by_design": {
                    "description": "Embed privacy into data processes from the start",
                    "practices": [
                        "Privacy impact assessments for new projects",
                        "Default to most privacy-protective options",
                        "Build consent management into systems",
                        "Enable data subject rights fulfillment"
                    ]
                },
                "data_subject_rights": {
                    "right_to_access": "Provide copy of personal data on request",
                    "right_to_rectification": "Correct inaccurate data",
                    "right_to_erasure": "Delete data when no longer needed (right to be forgotten)",
                    "right_to_portability": "Provide data in machine-readable format",
                    "right_to_object": "Opt-out of certain processing",
                    "right_to_restrict": "Limit processing in certain cases"
                },
                "consent_management": {
                    "requirements": [
                        "Clear and specific consent language",
                        "Easy to withdraw consent",
                        "Track consent for audit",
                        "Respect consent preferences in processing"
                    ]
                }
            },
            "sector_specific": sector_requirements.get(sector, {}),
            "security_tools": ["HashiCorp Vault", "AWS KMS", "Azure Key Vault", "Immuta", "Privacera", "OneTrust"]
        }

    def _build_mdm(self) -> Dict[str, Any]:
        """Build Master Data Management framework"""
        return {
            "purpose": "Establish single source of truth for critical business entities",
            "mdm_scope": {
                "customer_data": {
                    "entity": "Customer",
                    "golden_record_attributes": [
                        "Customer ID",
                        "Name",
                        "Contact information",
                        "Demographics",
                        "Relationships"
                    ],
                    "sources": ["CRM", "ERP", "Web", "Call Center"],
                    "matching_rules": [
                        "Exact match on email",
                        "Fuzzy match on name + address",
                        "Phone number match"
                    ]
                },
                "product_data": {
                    "entity": "Product",
                    "golden_record_attributes": [
                        "Product ID",
                        "Name and description",
                        "Category hierarchy",
                        "Attributes and specifications",
                        "Pricing"
                    ],
                    "sources": ["PIM", "ERP", "E-commerce"],
                    "matching_rules": [
                        "Exact match on SKU",
                        "Fuzzy match on name + attributes"
                    ]
                },
                "reference_data": {
                    "types": [
                        "Country codes",
                        "Currency codes",
                        "Industry codes",
                        "Product categories",
                        "Status codes"
                    ],
                    "governance": "Centrally managed, versioned, distributed to systems"
                }
            },
            "mdm_architecture": {
                "registry_style": {
                    "description": "Central registry linking records across systems",
                    "pros": ["Non-invasive", "Quick to implement"],
                    "cons": ["Data quality in sources", "No central golden record"]
                },
                "consolidation_style": {
                    "description": "Central repository with golden record for analytics",
                    "pros": ["Clean data for analytics", "Central quality management"],
                    "cons": ["Not real-time", "Sync complexity"]
                },
                "coexistence_style": {
                    "description": "Central golden record synced back to sources",
                    "pros": ["Best of both", "Single source of truth"],
                    "cons": ["Complex integration", "Higher cost"]
                }
            },
            "data_stewardship": {
                "steward_responsibilities": [
                    "Resolve match exceptions",
                    "Approve golden record changes",
                    "Maintain data quality",
                    "Manage reference data"
                ],
                "workflow": [
                    "Exception identified by matching engine",
                    "Routed to appropriate steward",
                    "Steward reviews and resolves",
                    "Golden record updated",
                    "Changes propagated to subscribers"
                ]
            },
            "mdm_tools": ["Informatica MDM", "Reltio", "Tamr", "Profisee", "SAP MDG", "Microsoft Dynamics MDM"]
        }

    def _build_data_integration(self) -> Dict[str, Any]:
        """Build data integration framework"""
        return {
            "purpose": "Connect and move data across systems reliably and efficiently",
            "integration_patterns": {
                "batch_etl": {
                    "description": "Extract, Transform, Load on schedule",
                    "use_cases": [
                        "Data warehouse loading",
                        "Historical data migration",
                        "Reporting data preparation"
                    ],
                    "technologies": ["Spark", "dbt", "Airflow", "Cloud ETL services"]
                },
                "elt": {
                    "description": "Extract, Load, Transform in target",
                    "use_cases": [
                        "Data lake loading",
                        "Flexible transformation needs",
                        "Schema-on-read scenarios"
                    ],
                    "technologies": ["Fivetran", "Airbyte", "dbt", "Cloud ETL"]
                },
                "real_time_streaming": {
                    "description": "Continuous data flow",
                    "use_cases": [
                        "Real-time analytics",
                        "Event-driven architectures",
                        "IoT data ingestion"
                    ],
                    "technologies": ["Kafka", "Kinesis", "Pub/Sub", "Flink"]
                },
                "change_data_capture": {
                    "description": "Capture and replicate database changes",
                    "use_cases": [
                        "Database replication",
                        "Real-time sync to analytics",
                        "Event sourcing"
                    ],
                    "technologies": ["Debezium", "AWS DMS", "Attunity", "Oracle GoldenGate"]
                },
                "api_integration": {
                    "description": "Connect via APIs",
                    "use_cases": [
                        "SaaS application integration",
                        "Partner data exchange",
                        "Microservices communication"
                    ],
                    "technologies": ["REST APIs", "GraphQL", "API gateways"]
                }
            },
            "integration_best_practices": [
                "Implement idempotent data loads",
                "Track data lineage through integrations",
                "Monitor data quality in pipelines",
                "Implement error handling and retry logic",
                "Version control all integration code",
                "Document data transformations"
            ],
            "data_contracts": {
                "purpose": "Formal agreements between data producers and consumers",
                "contents": [
                    "Schema definition",
                    "Quality expectations",
                    "SLA (freshness, availability)",
                    "Change notification process"
                ],
                "benefits": [
                    "Clear expectations",
                    "Automated contract testing",
                    "Controlled schema evolution"
                ]
            }
        }

    def _build_data_for_ai(self) -> Dict[str, Any]:
        """Build data strategy for AI/ML"""
        return {
            "purpose": "Enable AI/ML through high-quality, accessible, and well-governed data",
            "data_requirements_for_ai": {
                "volume": {
                    "consideration": "Sufficient data for model training",
                    "guidance": [
                        "Assess data volume needs for model types",
                        "Plan for data augmentation if limited",
                        "Consider transfer learning for small datasets"
                    ]
                },
                "quality": {
                    "consideration": "Data quality directly impacts model quality",
                    "guidance": [
                        "Prioritize quality for ML training data",
                        "Implement ML-specific quality checks",
                        "Monitor for data drift"
                    ]
                },
                "labels": {
                    "consideration": "Labeled data for supervised learning",
                    "guidance": [
                        "Establish labeling processes",
                        "Ensure label quality and consistency",
                        "Consider active learning for efficient labeling"
                    ]
                },
                "diversity": {
                    "consideration": "Representative data for fair models",
                    "guidance": [
                        "Assess representation across populations",
                        "Address imbalanced datasets",
                        "Test model performance on subgroups"
                    ]
                }
            },
            "ml_data_infrastructure": {
                "feature_store": {
                    "purpose": "Central repository for ML features",
                    "capabilities": [
                        "Feature versioning",
                        "Point-in-time feature retrieval",
                        "Online and offline serving",
                        "Feature discovery and reuse"
                    ],
                    "benefits": [
                        "Feature reuse across models",
                        "Training-serving consistency",
                        "Reduced feature engineering duplication"
                    ]
                },
                "training_data_management": {
                    "requirements": [
                        "Version training datasets",
                        "Link datasets to model versions",
                        "Enable reproducible training",
                        "Track data lineage to features and models"
                    ]
                },
                "data_labeling": {
                    "approaches": {
                        "manual_labeling": "Human annotation for high-quality labels",
                        "weak_supervision": "Programmatic labeling with heuristics",
                        "active_learning": "Selective labeling of uncertain samples",
                        "semi_supervised": "Leverage unlabeled data"
                    },
                    "quality_control": [
                        "Inter-annotator agreement metrics",
                        "Label review and correction",
                        "Bias assessment in labels"
                    ]
                }
            },
            "data_governance_for_ai": {
                "training_data_governance": [
                    "Document training data provenance",
                    "Assess bias in training data",
                    "Ensure compliant data use",
                    "Retain training data for audit"
                ],
                "fairness_considerations": [
                    "Assess representation in training data",
                    "Identify proxy attributes",
                    "Test for disparate impact",
                    "Document fairness analysis"
                ],
                "privacy_for_ai": [
                    "Minimize PII in training data",
                    "Apply differential privacy where appropriate",
                    "Consider federated learning for sensitive data"
                ]
            }
        }

    def _build_data_literacy(self) -> Dict[str, Any]:
        """Build data literacy framework"""
        return {
            "purpose": "Build organization-wide data skills and culture",
            "literacy_dimensions": {
                "data_reading": {
                    "description": "Ability to read and understand data",
                    "skills": [
                        "Interpret charts and dashboards",
                        "Understand basic statistics",
                        "Identify data quality issues",
                        "Question data appropriately"
                    ]
                },
                "data_working": {
                    "description": "Ability to work with data",
                    "skills": [
                        "Use analytics and BI tools",
                        "Write basic queries",
                        "Prepare data for analysis",
                        "Create visualizations"
                    ]
                },
                "data_analyzing": {
                    "description": "Ability to analyze and derive insights",
                    "skills": [
                        "Apply analytical techniques",
                        "Draw valid conclusions",
                        "Communicate findings",
                        "Recommend actions"
                    ]
                },
                "data_arguing": {
                    "description": "Ability to use data in decision-making",
                    "skills": [
                        "Build data-driven arguments",
                        "Challenge assumptions with data",
                        "Communicate to influence",
                        "Balance data with judgment"
                    ]
                }
            },
            "role_based_requirements": {
                "all_employees": {
                    "level": "Data Aware",
                    "expectations": [
                        "Understand importance of data",
                        "Read basic reports and dashboards",
                        "Know where to find data help"
                    ],
                    "training": "Data awareness (2 hours)"
                },
                "business_analysts": {
                    "level": "Data Proficient",
                    "expectations": [
                        "Self-service analytics",
                        "Create dashboards and reports",
                        "Basic data preparation"
                    ],
                    "training": "Analytics tools, SQL basics (20-40 hours)"
                },
                "data_analysts": {
                    "level": "Data Expert",
                    "expectations": [
                        "Advanced analytics",
                        "Statistical analysis",
                        "Data modeling"
                    ],
                    "training": "Statistics, advanced SQL, Python (80+ hours)"
                },
                "data_scientists": {
                    "level": "Data Master",
                    "expectations": [
                        "ML/AI development",
                        "Advanced statistics",
                        "Big data technologies"
                    ],
                    "training": "ML/AI, advanced programming (continuous)"
                },
                "leaders": {
                    "level": "Data-Driven Decision Maker",
                    "expectations": [
                        "Use data in decisions",
                        "Champion data culture",
                        "Ask the right data questions"
                    ],
                    "training": "Data leadership (8 hours)"
                }
            },
            "culture_building": {
                "practices": [
                    "Celebrate data-driven successes",
                    "Share data and insights openly",
                    "Encourage experimentation",
                    "Make data accessible",
                    "Lead by example"
                ],
                "programs": [
                    "Data champions network",
                    "Lunch and learn sessions",
                    "Internal data community",
                    "Analytics competitions"
                ]
            }
        }

    def _build_data_value(self) -> Dict[str, Any]:
        """Build data value and monetization framework"""
        return {
            "purpose": "Quantify and maximize the value derived from data assets",
            "value_creation_levers": {
                "operational_efficiency": {
                    "description": "Using data to improve operations",
                    "examples": [
                        "Process automation with data",
                        "Predictive maintenance",
                        "Supply chain optimization"
                    ]
                },
                "revenue_enhancement": {
                    "description": "Using data to grow revenue",
                    "examples": [
                        "Personalized recommendations",
                        "Dynamic pricing",
                        "Customer segmentation"
                    ]
                },
                "risk_reduction": {
                    "description": "Using data to reduce risk",
                    "examples": [
                        "Fraud detection",
                        "Credit risk modeling",
                        "Compliance monitoring"
                    ]
                },
                "new_products": {
                    "description": "Creating new data-driven products",
                    "examples": [
                        "Data products for customers",
                        "Analytics as a service",
                        "AI-powered features"
                    ]
                },
                "external_monetization": {
                    "description": "Generating revenue from data assets",
                    "examples": [
                        "Data licensing",
                        "Insights selling",
                        "Benchmarking services"
                    ],
                    "considerations": [
                        "Privacy and consent compliance",
                        "Competitive implications",
                        "Data quality requirements"
                    ]
                }
            },
            "value_measurement": {
                "direct_value": {
                    "description": "Measurable financial impact",
                    "metrics": [
                        "Revenue attributed to data initiatives",
                        "Cost savings from data-driven decisions",
                        "New revenue from data products"
                    ]
                },
                "indirect_value": {
                    "description": "Harder to measure but real impact",
                    "metrics": [
                        "Decision quality improvement",
                        "Time to insight reduction",
                        "Customer satisfaction improvement"
                    ]
                },
                "data_asset_valuation": {
                    "approaches": [
                        "Cost approach - cost to recreate",
                        "Market approach - comparable transactions",
                        "Income approach - future value generated"
                    ]
                }
            }
        }

    def _build_regulatory_compliance(self, jurisdictions: List[str], sector: str) -> Dict[str, Any]:
        """Build regulatory compliance framework"""
        regulations = {
            "gdpr": {
                "name": "General Data Protection Regulation",
                "jurisdiction": "EU",
                "scope": "Personal data of EU residents",
                "key_requirements": [
                    "Lawful basis for processing",
                    "Data subject rights",
                    "Data protection by design",
                    "Data breach notification",
                    "DPO appointment (in some cases)",
                    "DPIA for high-risk processing"
                ],
                "penalties": "Up to €20M or 4% global revenue"
            },
            "ccpa_cpra": {
                "name": "California Consumer Privacy Act / Rights Act",
                "jurisdiction": "California, USA",
                "scope": "California residents' personal information",
                "key_requirements": [
                    "Right to know, delete, correct",
                    "Right to opt-out of sale/sharing",
                    "Non-discrimination",
                    "Privacy policy requirements",
                    "Service provider contracts"
                ],
                "penalties": "Up to $7,500 per intentional violation"
            },
            "hipaa": {
                "name": "Health Insurance Portability and Accountability Act",
                "jurisdiction": "USA",
                "scope": "Protected Health Information (PHI)",
                "key_requirements": [
                    "Privacy Rule - PHI protections",
                    "Security Rule - administrative/technical/physical safeguards",
                    "Breach notification",
                    "Business Associate Agreements"
                ],
                "penalties": "Up to $1.5M per violation category per year"
            },
            "pci_dss": {
                "name": "Payment Card Industry Data Security Standard",
                "jurisdiction": "Global",
                "scope": "Payment card data",
                "key_requirements": [
                    "Build and maintain secure network",
                    "Protect cardholder data",
                    "Maintain vulnerability management",
                    "Implement access control",
                    "Monitor and test networks",
                    "Maintain security policy"
                ],
                "penalties": "Card brand fines, processing restrictions"
            }
        }

        applicable = {}
        if "eu" in [j.lower() for j in jurisdictions]:
            applicable["gdpr"] = regulations["gdpr"]
        if "us" in [j.lower() for j in jurisdictions]:
            applicable["ccpa_cpra"] = regulations["ccpa_cpra"]
        if sector == "healthcare":
            applicable["hipaa"] = regulations["hipaa"]
        if sector == "financial_services":
            applicable["pci_dss"] = regulations["pci_dss"]

        return {
            "applicable_regulations": applicable,
            "compliance_framework": {
                "assessment": "Regular compliance assessments",
                "controls": "Implement required controls",
                "documentation": "Maintain compliance documentation",
                "monitoring": "Ongoing compliance monitoring",
                "audit": "Internal and external audits"
            },
            "data_processing_records": {
                "requirement": "Maintain records of processing activities",
                "contents": [
                    "Processing purpose",
                    "Data categories",
                    "Recipients",
                    "Transfers",
                    "Retention",
                    "Security measures"
                ]
            }
        }

    def _build_team_structure(self) -> Dict[str, Any]:
        """Build data team structure"""
        return {
            "central_data_team": {
                "data_governance": {
                    "roles": ["Data Governance Manager", "Data Stewards"],
                    "responsibilities": ["Policies", "Standards", "Governance tools"]
                },
                "data_engineering": {
                    "roles": ["Data Engineers", "Data Architects"],
                    "responsibilities": ["Data platform", "Pipelines", "Infrastructure"]
                },
                "data_analytics": {
                    "roles": ["Data Analysts", "BI Developers"],
                    "responsibilities": ["Reports", "Dashboards", "Ad-hoc analysis"]
                },
                "data_science": {
                    "roles": ["Data Scientists", "ML Engineers"],
                    "responsibilities": ["ML models", "Advanced analytics"]
                }
            },
            "embedded_roles": {
                "domain_data_stewards": "Business domain experts for data quality",
                "analytics_partners": "Analysts embedded in business units"
            }
        }

    def _build_technology_stack(self, primary_cloud: Optional[str]) -> Dict[str, Any]:
        """Build technology stack recommendations"""
        return {
            "data_storage": {
                "data_lake": ["S3", "GCS", "ADLS", "Delta Lake"],
                "data_warehouse": ["Snowflake", "BigQuery", "Redshift", "Databricks SQL"],
                "operational_db": ["PostgreSQL", "MySQL", "MongoDB"]
            },
            "data_integration": {
                "batch": ["dbt", "Spark", "Airflow", "Fivetran"],
                "streaming": ["Kafka", "Flink", "Kinesis"],
                "cdc": ["Debezium", "AWS DMS"]
            },
            "data_governance": {
                "catalog": ["Alation", "Collibra", "Atlan", "DataHub"],
                "quality": ["Great Expectations", "Soda", "Monte Carlo"]
            },
            "analytics": {
                "bi": ["Tableau", "Power BI", "Looker", "Metabase"],
                "notebooks": ["Jupyter", "Databricks Notebooks"]
            }
        }

    def _build_implementation_roadmap(self, maturity: str) -> List[Dict[str, Any]]:
        """Build implementation roadmap"""
        return [
            {
                "phase": "Phase 1: Foundation",
                "timeline": "Months 1-3",
                "focus": "Establish core governance and infrastructure",
                "objectives": [
                    "Establish Data Governance Council",
                    "Define data policies",
                    "Implement data catalog",
                    "Assess current state"
                ],
                "success_metrics": [
                    "Governance council operational",
                    "Core policies approved",
                    "Catalog with critical data assets"
                ]
            },
            {
                "phase": "Phase 2: Quality & Integration",
                "timeline": "Months 4-6",
                "focus": "Improve data quality and integration",
                "objectives": [
                    "Implement data quality framework",
                    "Modernize data integration",
                    "Define data domains and ownership"
                ],
                "success_metrics": [
                    "Quality monitoring operational",
                    "Key pipelines modernized",
                    "Data owners assigned"
                ]
            },
            {
                "phase": "Phase 3: AI Enablement",
                "timeline": "Months 7-9",
                "focus": "Enable AI/ML with data",
                "objectives": [
                    "Deploy feature store",
                    "Establish ML data practices",
                    "Implement data versioning"
                ],
                "success_metrics": [
                    "Feature store operational",
                    "ML teams using governed data",
                    "Training data versioned"
                ]
            },
            {
                "phase": "Phase 4: Optimization",
                "timeline": "Months 10-12",
                "focus": "Scale and optimize",
                "objectives": [
                    "Enable self-service",
                    "Measure data value",
                    "Build data culture"
                ],
                "success_metrics": [
                    "Self-service adoption",
                    "Value metrics tracked",
                    "Literacy program launched"
                ]
            }
        ]

    def _build_metrics_and_kpis(self) -> Dict[str, Any]:
        """Build metrics and KPIs"""
        return {
            "governance_metrics": {
                "policy_compliance": "% of data assets compliant with policies",
                "stewardship_coverage": "% of data assets with assigned stewards",
                "catalog_coverage": "% of data assets documented in catalog"
            },
            "quality_metrics": {
                "dq_score": "Overall data quality score",
                "critical_data_quality": "Quality of critical data elements",
                "issue_resolution_time": "Time to resolve data issues"
            },
            "usage_metrics": {
                "data_accessibility": "Time to access data for new use cases",
                "self_service_adoption": "% of analytics done self-service",
                "data_reuse": "% of shared data assets"
            },
            "value_metrics": {
                "data_roi": "Return on data investments",
                "decision_quality": "Impact of data on decision quality",
                "ai_enablement": "# of AI models using governed data"
            }
        }
