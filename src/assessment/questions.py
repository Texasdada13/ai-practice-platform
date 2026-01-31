"""
AI Readiness Assessment Question Bank

50 core questions across 5 dimensions + sector-specific questions
Each question scored 1-5:
  1 = Not Started / No capability
  2 = Initial / Ad-hoc
  3 = Developing / Partial
  4 = Established / Mature
  5 = Optimizing / Leading
"""

from typing import Dict, List, Any

# Available sectors
SECTORS = [
    "financial_services",
    "government",
    "healthcare",
    "manufacturing",
    "retail",
    "general"
]

# Dimension weights for overall score calculation
DIMENSION_WEIGHTS = {
    "data_maturity": 0.25,
    "technology_infrastructure": 0.20,
    "process_operations": 0.20,
    "workforce_culture": 0.20,
    "governance_compliance": 0.15
}

# =============================================================================
# CORE QUESTIONS (40 questions - 8 per dimension)
# =============================================================================

CORE_QUESTIONS = {
    "data_maturity": {
        "name": "Data Maturity",
        "description": "Evaluates data quality, governance, accessibility, and integration capabilities",
        "weight": 0.25,
        "questions": [
            {
                "id": "dm_1",
                "text": "How would you rate your organization's overall data quality (accuracy, completeness, consistency)?",
                "options": [
                    {"value": 1, "label": "Poor - Data is unreliable, many errors and gaps"},
                    {"value": 2, "label": "Fair - Some quality issues, manual cleanup often needed"},
                    {"value": 3, "label": "Good - Generally reliable, occasional issues"},
                    {"value": 4, "label": "Very Good - High quality with automated validation"},
                    {"value": 5, "label": "Excellent - Enterprise-wide quality standards enforced"}
                ]
            },
            {
                "id": "dm_2",
                "text": "Does your organization have a formal data governance framework?",
                "options": [
                    {"value": 1, "label": "No governance - Data managed ad-hoc"},
                    {"value": 2, "label": "Informal - Some guidelines exist but not enforced"},
                    {"value": 3, "label": "Partial - Governance for some critical data"},
                    {"value": 4, "label": "Established - Formal framework with data stewards"},
                    {"value": 5, "label": "Advanced - Automated governance with continuous monitoring"}
                ]
            },
            {
                "id": "dm_3",
                "text": "How accessible is data across your organization for analytics and decision-making?",
                "options": [
                    {"value": 1, "label": "Siloed - Data trapped in departmental systems"},
                    {"value": 2, "label": "Limited - Access requires IT requests and long delays"},
                    {"value": 3, "label": "Moderate - Some self-service access available"},
                    {"value": 4, "label": "Good - Data catalog and self-service tools available"},
                    {"value": 5, "label": "Excellent - Unified data platform with real-time access"}
                ]
            },
            {
                "id": "dm_4",
                "text": "What is the state of your data integration across systems?",
                "options": [
                    {"value": 1, "label": "No integration - Systems completely disconnected"},
                    {"value": 2, "label": "Point-to-point - Some manual integrations"},
                    {"value": 3, "label": "Partial - ETL pipelines for key systems"},
                    {"value": 4, "label": "Integrated - Enterprise data warehouse/lake"},
                    {"value": 5, "label": "Real-time - Event-driven architecture with streaming"}
                ]
            },
            {
                "id": "dm_5",
                "text": "Do you have a data catalog or metadata management system?",
                "options": [
                    {"value": 1, "label": "None - No documentation of data assets"},
                    {"value": 2, "label": "Spreadsheets - Manual tracking in spreadsheets"},
                    {"value": 3, "label": "Basic - Simple catalog for some data"},
                    {"value": 4, "label": "Established - Enterprise data catalog with lineage"},
                    {"value": 5, "label": "Advanced - AI-powered discovery and auto-cataloging"}
                ]
            },
            {
                "id": "dm_6",
                "text": "How much of your data is labeled and ready for machine learning?",
                "options": [
                    {"value": 1, "label": "None - No labeled datasets"},
                    {"value": 2, "label": "Minimal - Less than 10% labeled"},
                    {"value": 3, "label": "Some - 10-30% labeled for specific use cases"},
                    {"value": 4, "label": "Substantial - 30-60% with labeling processes"},
                    {"value": 5, "label": "Extensive - 60%+ with automated labeling pipelines"}
                ]
            },
            {
                "id": "dm_7",
                "text": "What is your organization's data volume and variety capability?",
                "options": [
                    {"value": 1, "label": "Limited - Only structured data in databases"},
                    {"value": 2, "label": "Basic - Structured data with some documents"},
                    {"value": 3, "label": "Moderate - Multiple data types including logs"},
                    {"value": 4, "label": "Advanced - Big data including unstructured content"},
                    {"value": 5, "label": "Comprehensive - All data types including real-time streams"}
                ]
            },
            {
                "id": "dm_8",
                "text": "How do you handle data privacy and protection?",
                "options": [
                    {"value": 1, "label": "Ad-hoc - No formal privacy controls"},
                    {"value": 2, "label": "Basic - Password protection and access lists"},
                    {"value": 3, "label": "Developing - Privacy policies and some encryption"},
                    {"value": 4, "label": "Mature - Comprehensive privacy program with PII controls"},
                    {"value": 5, "label": "Advanced - Automated privacy compliance and data masking"}
                ]
            }
        ]
    },

    "technology_infrastructure": {
        "name": "Technology Infrastructure",
        "description": "Assesses cloud readiness, compute capabilities, APIs, and security posture",
        "weight": 0.20,
        "questions": [
            {
                "id": "ti_1",
                "text": "What is your organization's cloud adoption status?",
                "options": [
                    {"value": 1, "label": "On-premise only - No cloud presence"},
                    {"value": 2, "label": "Exploring - Evaluating cloud options"},
                    {"value": 3, "label": "Partial - Some workloads in cloud"},
                    {"value": 4, "label": "Cloud-first - Majority of new apps in cloud"},
                    {"value": 5, "label": "Cloud-native - Full cloud with multi-cloud strategy"}
                ]
            },
            {
                "id": "ti_2",
                "text": "Do you have access to GPU/TPU or specialized AI compute resources?",
                "options": [
                    {"value": 1, "label": "None - Only standard CPUs"},
                    {"value": 2, "label": "Limited - Can request cloud GPUs ad-hoc"},
                    {"value": 3, "label": "Moderate - Some dedicated GPU resources"},
                    {"value": 4, "label": "Good - GPU clusters for ML workloads"},
                    {"value": 5, "label": "Excellent - Scalable AI infrastructure (on-demand GPUs/TPUs)"}
                ]
            },
            {
                "id": "ti_3",
                "text": "What is the state of your API infrastructure?",
                "options": [
                    {"value": 1, "label": "None - No APIs, point-to-point integrations"},
                    {"value": 2, "label": "Basic - Some REST APIs for internal use"},
                    {"value": 3, "label": "Developing - API gateway with documentation"},
                    {"value": 4, "label": "Mature - API-first design, versioning, rate limiting"},
                    {"value": 5, "label": "Advanced - Full API ecosystem with marketplace"}
                ]
            },
            {
                "id": "ti_4",
                "text": "How mature is your DevOps/MLOps capability?",
                "options": [
                    {"value": 1, "label": "None - Manual deployments only"},
                    {"value": 2, "label": "Basic - Some CI/CD for applications"},
                    {"value": 3, "label": "Developing - CI/CD with automated testing"},
                    {"value": 4, "label": "Mature - Full DevOps with infrastructure as code"},
                    {"value": 5, "label": "Advanced - MLOps with model monitoring and retraining"}
                ]
            },
            {
                "id": "ti_5",
                "text": "What is your cybersecurity posture for AI systems?",
                "options": [
                    {"value": 1, "label": "Basic - Standard firewalls and antivirus"},
                    {"value": 2, "label": "Developing - Security policies and monitoring"},
                    {"value": 3, "label": "Established - SOC with incident response"},
                    {"value": 4, "label": "Advanced - Zero trust with AI threat detection"},
                    {"value": 5, "label": "Leading - Automated security with adversarial ML defense"}
                ]
            },
            {
                "id": "ti_6",
                "text": "Do you have containerization and orchestration capabilities?",
                "options": [
                    {"value": 1, "label": "None - Traditional VM or bare metal only"},
                    {"value": 2, "label": "Exploring - Piloting Docker containers"},
                    {"value": 3, "label": "Developing - Containers in production, basic orchestration"},
                    {"value": 4, "label": "Mature - Kubernetes with auto-scaling"},
                    {"value": 5, "label": "Advanced - Service mesh with serverless capabilities"}
                ]
            },
            {
                "id": "ti_7",
                "text": "What is your network infrastructure capability for AI workloads?",
                "options": [
                    {"value": 1, "label": "Limited - Basic internet connectivity"},
                    {"value": 2, "label": "Standard - Enterprise WAN with VPN"},
                    {"value": 3, "label": "Good - High-bandwidth with CDN"},
                    {"value": 4, "label": "Advanced - Edge computing capabilities"},
                    {"value": 5, "label": "Leading - 5G/Edge AI with low-latency inference"}
                ]
            },
            {
                "id": "ti_8",
                "text": "How do you manage AI/ML model storage and versioning?",
                "options": [
                    {"value": 1, "label": "None - No formal model management"},
                    {"value": 2, "label": "Basic - Models stored in shared drives"},
                    {"value": 3, "label": "Developing - Git for code, separate model storage"},
                    {"value": 4, "label": "Mature - Model registry with versioning"},
                    {"value": 5, "label": "Advanced - Full ML lifecycle management platform"}
                ]
            }
        ]
    },

    "process_operations": {
        "name": "Process & Operations",
        "description": "Evaluates automation potential, workflow documentation, and operational readiness",
        "weight": 0.20,
        "questions": [
            {
                "id": "po_1",
                "text": "How well documented are your business processes?",
                "options": [
                    {"value": 1, "label": "Not documented - Tribal knowledge only"},
                    {"value": 2, "label": "Partially - Key processes in documents"},
                    {"value": 3, "label": "Moderate - Process maps for main workflows"},
                    {"value": 4, "label": "Well documented - Standard procedures with metrics"},
                    {"value": 5, "label": "Comprehensive - Process mining with optimization"}
                ]
            },
            {
                "id": "po_2",
                "text": "What is your current level of process automation?",
                "options": [
                    {"value": 1, "label": "Manual - Most processes are manual"},
                    {"value": 2, "label": "Basic - Some spreadsheet automation"},
                    {"value": 3, "label": "Moderate - RPA for repetitive tasks"},
                    {"value": 4, "label": "Advanced - Intelligent automation with rules engines"},
                    {"value": 5, "label": "Hyperautomation - AI-driven process orchestration"}
                ]
            },
            {
                "id": "po_3",
                "text": "Do you have identified use cases for AI implementation?",
                "options": [
                    {"value": 1, "label": "None - No use cases identified"},
                    {"value": 2, "label": "Ideas - Some brainstorming done"},
                    {"value": 3, "label": "Documented - Use case backlog exists"},
                    {"value": 4, "label": "Prioritized - ROI-based prioritization complete"},
                    {"value": 5, "label": "Roadmap - Multi-year AI implementation roadmap"}
                ]
            },
            {
                "id": "po_4",
                "text": "How do you currently handle decision-making in operations?",
                "options": [
                    {"value": 1, "label": "Intuition - Gut feel and experience"},
                    {"value": 2, "label": "Reports - Basic reporting for decisions"},
                    {"value": 3, "label": "Dashboards - Real-time KPI monitoring"},
                    {"value": 4, "label": "Analytics - Predictive analytics inform decisions"},
                    {"value": 5, "label": "AI-assisted - AI recommendations with human oversight"}
                ]
            },
            {
                "id": "po_5",
                "text": "What is your change management capability?",
                "options": [
                    {"value": 1, "label": "Ad-hoc - Changes happen without process"},
                    {"value": 2, "label": "Basic - Change approval exists"},
                    {"value": 3, "label": "Formal - CAB and change management process"},
                    {"value": 4, "label": "Mature - Agile change with rollback capability"},
                    {"value": 5, "label": "Advanced - Continuous delivery with feature flags"}
                ]
            },
            {
                "id": "po_6",
                "text": "How do you measure and track operational performance?",
                "options": [
                    {"value": 1, "label": "Not tracked - No formal metrics"},
                    {"value": 2, "label": "Basic - Monthly reports on key metrics"},
                    {"value": 3, "label": "Regular - Weekly KPI tracking"},
                    {"value": 4, "label": "Real-time - Live dashboards with alerts"},
                    {"value": 5, "label": "Predictive - AI-powered anomaly detection"}
                ]
            },
            {
                "id": "po_7",
                "text": "What is your incident and problem management maturity?",
                "options": [
                    {"value": 1, "label": "Reactive - Fix issues as they occur"},
                    {"value": 2, "label": "Basic - Ticketing system exists"},
                    {"value": 3, "label": "Structured - ITIL-based incident management"},
                    {"value": 4, "label": "Proactive - Root cause analysis and prevention"},
                    {"value": 5, "label": "Predictive - AI predicts and prevents incidents"}
                ]
            },
            {
                "id": "po_8",
                "text": "How integrated are your operational systems?",
                "options": [
                    {"value": 1, "label": "Siloed - Separate systems with manual handoffs"},
                    {"value": 2, "label": "Basic - Some system integrations"},
                    {"value": 3, "label": "Moderate - Workflow automation between systems"},
                    {"value": 4, "label": "Integrated - Unified operations platform"},
                    {"value": 5, "label": "Intelligent - AI-orchestrated end-to-end operations"}
                ]
            }
        ]
    },

    "workforce_culture": {
        "name": "Workforce & Culture",
        "description": "Assesses AI literacy, change readiness, leadership buy-in, and talent capabilities",
        "weight": 0.20,
        "questions": [
            {
                "id": "wc_1",
                "text": "What is the general AI literacy level across your organization?",
                "options": [
                    {"value": 1, "label": "Low - Limited awareness of AI concepts"},
                    {"value": 2, "label": "Basic - General awareness but limited understanding"},
                    {"value": 3, "label": "Moderate - Key staff understand AI fundamentals"},
                    {"value": 4, "label": "Good - Widespread AI literacy with training programs"},
                    {"value": 5, "label": "High - AI-savvy workforce with continuous learning"}
                ]
            },
            {
                "id": "wc_2",
                "text": "Does your organization have AI/ML technical talent?",
                "options": [
                    {"value": 1, "label": "None - No data science or ML expertise"},
                    {"value": 2, "label": "Limited - 1-2 data analysts"},
                    {"value": 3, "label": "Emerging - Small data science team forming"},
                    {"value": 4, "label": "Established - Data science team with ML engineers"},
                    {"value": 5, "label": "Advanced - Center of Excellence with AI specialists"}
                ]
            },
            {
                "id": "wc_3",
                "text": "How supportive is executive leadership of AI initiatives?",
                "options": [
                    {"value": 1, "label": "Skeptical - Leadership doesn't see AI value"},
                    {"value": 2, "label": "Cautious - Interested but risk-averse"},
                    {"value": 3, "label": "Supportive - Leadership backs pilot projects"},
                    {"value": 4, "label": "Champion - Executive sponsor for AI program"},
                    {"value": 5, "label": "Visionary - AI is core to business strategy"}
                ]
            },
            {
                "id": "wc_4",
                "text": "What is your organization's appetite for innovation and change?",
                "options": [
                    {"value": 1, "label": "Resistant - Strong preference for status quo"},
                    {"value": 2, "label": "Cautious - Change accepted when necessary"},
                    {"value": 3, "label": "Open - Willing to try new approaches"},
                    {"value": 4, "label": "Embracing - Innovation encouraged and rewarded"},
                    {"value": 5, "label": "Leading - Culture of continuous experimentation"}
                ]
            },
            {
                "id": "wc_5",
                "text": "Do you have AI training and upskilling programs?",
                "options": [
                    {"value": 1, "label": "None - No AI-related training"},
                    {"value": 2, "label": "Ad-hoc - Occasional workshops or webinars"},
                    {"value": 3, "label": "Basic - Online courses available"},
                    {"value": 4, "label": "Structured - Formal AI curriculum and certifications"},
                    {"value": 5, "label": "Comprehensive - Role-based AI learning paths"}
                ]
            },
            {
                "id": "wc_6",
                "text": "How is AI/data work organized in your company?",
                "options": [
                    {"value": 1, "label": "No structure - IT handles everything"},
                    {"value": 2, "label": "Informal - Some people assigned data tasks"},
                    {"value": 3, "label": "Team - Dedicated analytics/BI team"},
                    {"value": 4, "label": "Embedded - Data roles in business units + central team"},
                    {"value": 5, "label": "Hub and spoke - AI CoE with embedded specialists"}
                ]
            },
            {
                "id": "wc_7",
                "text": "What is employee sentiment toward AI adoption?",
                "options": [
                    {"value": 1, "label": "Fearful - Concerns about job displacement"},
                    {"value": 2, "label": "Uncertain - Mixed feelings about AI"},
                    {"value": 3, "label": "Neutral - Neither positive nor negative"},
                    {"value": 4, "label": "Positive - See AI as opportunity for growth"},
                    {"value": 5, "label": "Enthusiastic - Actively seeking AI tools and training"}
                ]
            },
            {
                "id": "wc_8",
                "text": "How do you attract and retain AI talent?",
                "options": [
                    {"value": 1, "label": "No strategy - Standard hiring process"},
                    {"value": 2, "label": "Basic - Job postings for data roles"},
                    {"value": 3, "label": "Developing - Competitive salaries for AI roles"},
                    {"value": 4, "label": "Strong - Employer brand for tech talent"},
                    {"value": 5, "label": "Leading - Top destination for AI professionals"}
                ]
            }
        ]
    },

    "governance_compliance": {
        "name": "Governance & Compliance",
        "description": "Evaluates AI ethics, privacy, risk management, and regulatory compliance",
        "weight": 0.15,
        "questions": [
            {
                "id": "gc_1",
                "text": "Does your organization have an AI ethics framework?",
                "options": [
                    {"value": 1, "label": "None - No consideration of AI ethics"},
                    {"value": 2, "label": "Awareness - Discussions happening"},
                    {"value": 3, "label": "Draft - Principles being developed"},
                    {"value": 4, "label": "Established - Formal AI ethics policy"},
                    {"value": 5, "label": "Embedded - Ethics review for all AI projects"}
                ]
            },
            {
                "id": "gc_2",
                "text": "How do you ensure AI fairness and prevent bias?",
                "options": [
                    {"value": 1, "label": "Not addressed - No bias considerations"},
                    {"value": 2, "label": "Awareness - Know it's important"},
                    {"value": 3, "label": "Manual - Ad-hoc bias reviews"},
                    {"value": 4, "label": "Systematic - Bias testing in ML pipeline"},
                    {"value": 5, "label": "Automated - Continuous fairness monitoring"}
                ]
            },
            {
                "id": "gc_3",
                "text": "What is your approach to AI explainability and transparency?",
                "options": [
                    {"value": 1, "label": "Black box - No explainability requirements"},
                    {"value": 2, "label": "Basic - Can explain simple models"},
                    {"value": 3, "label": "Developing - XAI tools for some models"},
                    {"value": 4, "label": "Mature - Explainability required for decisions"},
                    {"value": 5, "label": "Advanced - Full model interpretability platform"}
                ]
            },
            {
                "id": "gc_4",
                "text": "How do you manage AI-related risks?",
                "options": [
                    {"value": 1, "label": "Not managed - No AI risk framework"},
                    {"value": 2, "label": "Informal - Some risk discussions"},
                    {"value": 3, "label": "Basic - AI risks in enterprise risk register"},
                    {"value": 4, "label": "Structured - AI risk assessment process"},
                    {"value": 5, "label": "Comprehensive - AI risk committee with monitoring"}
                ]
            },
            {
                "id": "gc_5",
                "text": "What is your compliance posture for AI regulations (GDPR, AI Act, etc.)?",
                "options": [
                    {"value": 1, "label": "Unaware - Don't know applicable regulations"},
                    {"value": 2, "label": "Aware - Know regulations exist"},
                    {"value": 3, "label": "Assessing - Gap analysis underway"},
                    {"value": 4, "label": "Compliant - Meet current requirements"},
                    {"value": 5, "label": "Proactive - Ahead of emerging regulations"}
                ]
            },
            {
                "id": "gc_6",
                "text": "Do you have AI model governance and oversight?",
                "options": [
                    {"value": 1, "label": "None - Models deployed without oversight"},
                    {"value": 2, "label": "Basic - Approval needed for production"},
                    {"value": 3, "label": "Developing - Model documentation required"},
                    {"value": 4, "label": "Mature - Model governance board reviews"},
                    {"value": 5, "label": "Advanced - Automated model monitoring and audit"}
                ]
            },
            {
                "id": "gc_7",
                "text": "How do you handle AI-related vendor and third-party risk?",
                "options": [
                    {"value": 1, "label": "Not considered - Use vendors without AI review"},
                    {"value": 2, "label": "Basic - Standard vendor assessment"},
                    {"value": 3, "label": "Developing - AI-specific questions in assessment"},
                    {"value": 4, "label": "Mature - AI vendor risk framework"},
                    {"value": 5, "label": "Advanced - Continuous third-party AI monitoring"}
                ]
            },
            {
                "id": "gc_8",
                "text": "What audit and accountability mechanisms exist for AI systems?",
                "options": [
                    {"value": 1, "label": "None - No AI audit capability"},
                    {"value": 2, "label": "Basic - Can review AI decisions on request"},
                    {"value": 3, "label": "Developing - Audit trails for key AI systems"},
                    {"value": 4, "label": "Established - Regular AI audits conducted"},
                    {"value": 5, "label": "Comprehensive - Real-time AI audit dashboard"}
                ]
            }
        ]
    }
}

# =============================================================================
# SECTOR-SPECIFIC QUESTIONS (10 per sector - 2 per dimension)
# =============================================================================

SECTOR_QUESTIONS = {
    "financial_services": {
        "name": "Financial Services",
        "questions": [
            # Data Maturity
            {
                "id": "fs_dm_1",
                "dimension": "data_maturity",
                "text": "How do you handle financial data lineage and auditability?",
                "options": [
                    {"value": 1, "label": "Not tracked - No data lineage"},
                    {"value": 2, "label": "Manual - Spreadsheet documentation"},
                    {"value": 3, "label": "Partial - Lineage for regulatory data"},
                    {"value": 4, "label": "Comprehensive - Full data lineage platform"},
                    {"value": 5, "label": "Real-time - Automated lineage with audit trails"}
                ]
            },
            {
                "id": "fs_dm_2",
                "dimension": "data_maturity",
                "text": "What is your capability for real-time transaction data processing?",
                "options": [
                    {"value": 1, "label": "Batch only - End of day processing"},
                    {"value": 2, "label": "Near real-time - Hourly updates"},
                    {"value": 3, "label": "Partial real-time - Some systems streaming"},
                    {"value": 4, "label": "Real-time - Sub-second processing"},
                    {"value": 5, "label": "Advanced - Complex event processing"}
                ]
            },
            # Technology Infrastructure
            {
                "id": "fs_ti_1",
                "dimension": "technology_infrastructure",
                "text": "How mature is your fraud detection technology infrastructure?",
                "options": [
                    {"value": 1, "label": "Basic - Rule-based only"},
                    {"value": 2, "label": "Developing - Some ML models"},
                    {"value": 3, "label": "Moderate - ML with regular updates"},
                    {"value": 4, "label": "Advanced - Real-time ML scoring"},
                    {"value": 5, "label": "Leading - Adaptive AI with network analysis"}
                ]
            },
            {
                "id": "fs_ti_2",
                "dimension": "technology_infrastructure",
                "text": "What is your core banking system's AI integration capability?",
                "options": [
                    {"value": 1, "label": "Legacy - No API or AI capability"},
                    {"value": 2, "label": "Limited - Basic batch interfaces"},
                    {"value": 3, "label": "Moderate - API layer available"},
                    {"value": 4, "label": "Modern - Real-time APIs with AI hooks"},
                    {"value": 5, "label": "Advanced - AI-native banking platform"}
                ]
            },
            # Process & Operations
            {
                "id": "fs_po_1",
                "dimension": "process_operations",
                "text": "How automated is your KYC/AML process?",
                "options": [
                    {"value": 1, "label": "Manual - Paper-based review"},
                    {"value": 2, "label": "Basic - Digital forms with manual review"},
                    {"value": 3, "label": "Partial - Automated screening, manual decisions"},
                    {"value": 4, "label": "Advanced - AI-assisted with human oversight"},
                    {"value": 5, "label": "Intelligent - End-to-end AI with explainability"}
                ]
            },
            {
                "id": "fs_po_2",
                "dimension": "process_operations",
                "text": "What is your loan/credit decisioning automation level?",
                "options": [
                    {"value": 1, "label": "Manual - Underwriter reviews all"},
                    {"value": 2, "label": "Basic - Scorecard with manual override"},
                    {"value": 3, "label": "Moderate - Automated for simple cases"},
                    {"value": 4, "label": "Advanced - ML models with explanation"},
                    {"value": 5, "label": "Intelligent - Real-time AI with fair lending compliance"}
                ]
            },
            # Workforce & Culture
            {
                "id": "fs_wc_1",
                "dimension": "workforce_culture",
                "text": "Do you have quantitative/data science talent for financial modeling?",
                "options": [
                    {"value": 1, "label": "None - No quant expertise"},
                    {"value": 2, "label": "Limited - Basic analytics"},
                    {"value": 3, "label": "Developing - Some quant resources"},
                    {"value": 4, "label": "Established - Quant team for modeling"},
                    {"value": 5, "label": "Advanced - World-class quant talent"}
                ]
            },
            {
                "id": "fs_wc_2",
                "dimension": "workforce_culture",
                "text": "How AI-literate is your risk management function?",
                "options": [
                    {"value": 1, "label": "Low - Traditional risk approaches only"},
                    {"value": 2, "label": "Basic - Awareness of AI in risk"},
                    {"value": 3, "label": "Moderate - Some AI projects in risk"},
                    {"value": 4, "label": "Good - Risk team uses AI tools"},
                    {"value": 5, "label": "Advanced - AI-native risk management"}
                ]
            },
            # Governance & Compliance
            {
                "id": "fs_gc_1",
                "dimension": "governance_compliance",
                "text": "How do you validate AI models for regulatory compliance (SR 11-7, etc.)?",
                "options": [
                    {"value": 1, "label": "No validation - Models not reviewed"},
                    {"value": 2, "label": "Basic - Ad-hoc validation"},
                    {"value": 3, "label": "Developing - Annual model validation"},
                    {"value": 4, "label": "Mature - Model risk management program"},
                    {"value": 5, "label": "Advanced - Continuous validation with automation"}
                ]
            },
            {
                "id": "fs_gc_2",
                "dimension": "governance_compliance",
                "text": "What is your AI fair lending compliance capability?",
                "options": [
                    {"value": 1, "label": "Not addressed - No fair lending AI review"},
                    {"value": 2, "label": "Basic - Manual fair lending testing"},
                    {"value": 3, "label": "Developing - Bias testing for models"},
                    {"value": 4, "label": "Mature - Automated fair lending analysis"},
                    {"value": 5, "label": "Advanced - Real-time fairness monitoring"}
                ]
            }
        ]
    },

    "government": {
        "name": "Government/Public Sector",
        "questions": [
            # Data Maturity
            {
                "id": "gov_dm_1",
                "dimension": "data_maturity",
                "text": "How do you manage citizen/constituent data across agencies?",
                "options": [
                    {"value": 1, "label": "Siloed - Each agency maintains separate data"},
                    {"value": 2, "label": "Limited sharing - Manual data requests"},
                    {"value": 3, "label": "Partial - Some cross-agency data sharing"},
                    {"value": 4, "label": "Integrated - Shared data platform"},
                    {"value": 5, "label": "Unified - Enterprise citizen data hub"}
                ]
            },
            {
                "id": "gov_dm_2",
                "dimension": "data_maturity",
                "text": "What is your capability for open data and transparency?",
                "options": [
                    {"value": 1, "label": "None - No open data initiatives"},
                    {"value": 2, "label": "Basic - Some datasets published"},
                    {"value": 3, "label": "Moderate - Open data portal exists"},
                    {"value": 4, "label": "Advanced - Comprehensive open data with APIs"},
                    {"value": 5, "label": "Leading - Real-time open data with analytics"}
                ]
            },
            # Technology Infrastructure
            {
                "id": "gov_ti_1",
                "dimension": "technology_infrastructure",
                "text": "What is your FedRAMP/StateRAMP cloud authorization status?",
                "options": [
                    {"value": 1, "label": "Not started - No cloud authorization"},
                    {"value": 2, "label": "Planning - Assessment underway"},
                    {"value": 3, "label": "Partial - Some systems authorized"},
                    {"value": 4, "label": "Authorized - Primary systems in authorized cloud"},
                    {"value": 5, "label": "Advanced - Multi-cloud with continuous ATO"}
                ]
            },
            {
                "id": "gov_ti_2",
                "dimension": "technology_infrastructure",
                "text": "How modern is your legacy system integration capability?",
                "options": [
                    {"value": 1, "label": "Mainframe-bound - No modern integration"},
                    {"value": 2, "label": "Basic - File-based integration"},
                    {"value": 3, "label": "Developing - API wrappers for legacy"},
                    {"value": 4, "label": "Modernizing - Hybrid architecture"},
                    {"value": 5, "label": "Advanced - Microservices with legacy abstraction"}
                ]
            },
            # Process & Operations
            {
                "id": "gov_po_1",
                "dimension": "process_operations",
                "text": "How automated are citizen service delivery processes?",
                "options": [
                    {"value": 1, "label": "Manual - Paper forms and in-person"},
                    {"value": 2, "label": "Basic - Online forms available"},
                    {"value": 3, "label": "Moderate - Self-service portal"},
                    {"value": 4, "label": "Advanced - Automated eligibility and processing"},
                    {"value": 5, "label": "Intelligent - AI-powered citizen services"}
                ]
            },
            {
                "id": "gov_po_2",
                "dimension": "process_operations",
                "text": "What is your procurement process automation level?",
                "options": [
                    {"value": 1, "label": "Manual - Paper-based procurement"},
                    {"value": 2, "label": "Basic - E-procurement for some"},
                    {"value": 3, "label": "Moderate - Full e-procurement"},
                    {"value": 4, "label": "Advanced - Automated vendor matching"},
                    {"value": 5, "label": "Intelligent - AI-driven procurement optimization"}
                ]
            },
            # Workforce & Culture
            {
                "id": "gov_wc_1",
                "dimension": "workforce_culture",
                "text": "How do you compete for AI talent against private sector?",
                "options": [
                    {"value": 1, "label": "Cannot compete - Significant talent gap"},
                    {"value": 2, "label": "Challenging - Rely on contractors"},
                    {"value": 3, "label": "Developing - Special hiring authorities"},
                    {"value": 4, "label": "Competitive - Mission-driven talent strategy"},
                    {"value": 5, "label": "Strong - Recognized AI career destination"}
                ]
            },
            {
                "id": "gov_wc_2",
                "dimension": "workforce_culture",
                "text": "What AI training exists for government employees?",
                "options": [
                    {"value": 1, "label": "None - No AI training programs"},
                    {"value": 2, "label": "Basic - Awareness sessions"},
                    {"value": 3, "label": "Developing - Online courses available"},
                    {"value": 4, "label": "Structured - AI curriculum for employees"},
                    {"value": 5, "label": "Comprehensive - Role-based AI certifications"}
                ]
            },
            # Governance & Compliance
            {
                "id": "gov_gc_1",
                "dimension": "governance_compliance",
                "text": "How do you ensure AI algorithmic accountability for public decisions?",
                "options": [
                    {"value": 1, "label": "Not addressed - No accountability framework"},
                    {"value": 2, "label": "Aware - Discussing requirements"},
                    {"value": 3, "label": "Developing - Policies being drafted"},
                    {"value": 4, "label": "Established - Impact assessments required"},
                    {"value": 5, "label": "Advanced - Public AI registry with audits"}
                ]
            },
            {
                "id": "gov_gc_2",
                "dimension": "governance_compliance",
                "text": "What is your compliance with AI executive orders and mandates?",
                "options": [
                    {"value": 1, "label": "Non-compliant - Not tracking requirements"},
                    {"value": 2, "label": "Aware - Know requirements exist"},
                    {"value": 3, "label": "Partial - Working toward compliance"},
                    {"value": 4, "label": "Compliant - Meet current mandates"},
                    {"value": 5, "label": "Leading - Exceed requirements"}
                ]
            }
        ]
    },

    "healthcare": {
        "name": "Healthcare",
        "questions": [
            # Data Maturity
            {
                "id": "hc_dm_1",
                "dimension": "data_maturity",
                "text": "How interoperable is your health data (FHIR, HL7)?",
                "options": [
                    {"value": 1, "label": "Siloed - No interoperability"},
                    {"value": 2, "label": "Basic - HL7 v2 messaging"},
                    {"value": 3, "label": "Developing - Some FHIR APIs"},
                    {"value": 4, "label": "Advanced - FHIR-based data exchange"},
                    {"value": 5, "label": "Leading - Real-time FHIR ecosystem"}
                ]
            },
            {
                "id": "hc_dm_2",
                "dimension": "data_maturity",
                "text": "What is your clinical data quality and standardization level?",
                "options": [
                    {"value": 1, "label": "Poor - Unstructured notes only"},
                    {"value": 2, "label": "Basic - Mix of structured and unstructured"},
                    {"value": 3, "label": "Moderate - Standard terminologies (ICD, SNOMED)"},
                    {"value": 4, "label": "Good - Quality metrics and NLP extraction"},
                    {"value": 5, "label": "Excellent - AI-enhanced data capture"}
                ]
            },
            # Technology Infrastructure
            {
                "id": "hc_ti_1",
                "dimension": "technology_infrastructure",
                "text": "How AI-ready is your EHR platform?",
                "options": [
                    {"value": 1, "label": "Legacy - No AI capability"},
                    {"value": 2, "label": "Basic - Vendor AI modules available"},
                    {"value": 3, "label": "Moderate - Can integrate third-party AI"},
                    {"value": 4, "label": "Advanced - AI APIs and CDS hooks"},
                    {"value": 5, "label": "Leading - AI-native EHR platform"}
                ]
            },
            {
                "id": "hc_ti_2",
                "dimension": "technology_infrastructure",
                "text": "What is your capability for medical imaging AI?",
                "options": [
                    {"value": 1, "label": "None - Traditional radiology only"},
                    {"value": 2, "label": "Exploring - Piloting AI readers"},
                    {"value": 3, "label": "Partial - AI for some modalities"},
                    {"value": 4, "label": "Deployed - AI triage and detection"},
                    {"value": 5, "label": "Advanced - Full AI imaging workflow"}
                ]
            },
            # Process & Operations
            {
                "id": "hc_po_1",
                "dimension": "process_operations",
                "text": "How automated is your clinical documentation?",
                "options": [
                    {"value": 1, "label": "Manual - All typed by clinicians"},
                    {"value": 2, "label": "Basic - Templates and macros"},
                    {"value": 3, "label": "Moderate - Voice recognition"},
                    {"value": 4, "label": "Advanced - Ambient clinical intelligence"},
                    {"value": 5, "label": "Leading - AI scribe with auto-coding"}
                ]
            },
            {
                "id": "hc_po_2",
                "dimension": "process_operations",
                "text": "What is your patient scheduling optimization level?",
                "options": [
                    {"value": 1, "label": "Manual - Phone-based scheduling"},
                    {"value": 2, "label": "Basic - Online booking available"},
                    {"value": 3, "label": "Moderate - Automated reminders"},
                    {"value": 4, "label": "Advanced - Predictive no-show management"},
                    {"value": 5, "label": "Intelligent - AI-optimized scheduling"}
                ]
            },
            # Workforce & Culture
            {
                "id": "hc_wc_1",
                "dimension": "workforce_culture",
                "text": "What is clinician acceptance of AI tools?",
                "options": [
                    {"value": 1, "label": "Resistant - Distrust of AI"},
                    {"value": 2, "label": "Skeptical - Concerns about reliability"},
                    {"value": 3, "label": "Cautious - Will try with evidence"},
                    {"value": 4, "label": "Supportive - Embrace as decision support"},
                    {"value": 5, "label": "Enthusiastic - Champion AI adoption"}
                ]
            },
            {
                "id": "hc_wc_2",
                "dimension": "workforce_culture",
                "text": "Do you have clinical informatics expertise?",
                "options": [
                    {"value": 1, "label": "None - No informatics staff"},
                    {"value": 2, "label": "Limited - IT handles clinical systems"},
                    {"value": 3, "label": "Developing - Some informaticists"},
                    {"value": 4, "label": "Established - Clinical informatics team"},
                    {"value": 5, "label": "Advanced - CMIO and data science team"}
                ]
            },
            # Governance & Compliance
            {
                "id": "hc_gc_1",
                "dimension": "governance_compliance",
                "text": "How do you ensure AI compliance with FDA/clinical regulations?",
                "options": [
                    {"value": 1, "label": "Not addressed - No regulatory framework"},
                    {"value": 2, "label": "Aware - Know FDA requirements"},
                    {"value": 3, "label": "Developing - Compliance process forming"},
                    {"value": 4, "label": "Established - FDA 510(k) process for AI"},
                    {"value": 5, "label": "Advanced - Continuous compliance monitoring"}
                ]
            },
            {
                "id": "hc_gc_2",
                "dimension": "governance_compliance",
                "text": "What is your clinical AI validation process?",
                "options": [
                    {"value": 1, "label": "None - No validation required"},
                    {"value": 2, "label": "Basic - Vendor validation accepted"},
                    {"value": 3, "label": "Moderate - Local testing before deployment"},
                    {"value": 4, "label": "Rigorous - Clinical trials and IRB review"},
                    {"value": 5, "label": "Comprehensive - Continuous monitoring and revalidation"}
                ]
            }
        ]
    },

    "manufacturing": {
        "name": "Manufacturing",
        "questions": [
            # Data Maturity
            {
                "id": "mfg_dm_1",
                "dimension": "data_maturity",
                "text": "How connected is your operational technology (OT) data?",
                "options": [
                    {"value": 1, "label": "Disconnected - No OT data collection"},
                    {"value": 2, "label": "Basic - Some sensors with manual data"},
                    {"value": 3, "label": "Moderate - SCADA data collected"},
                    {"value": 4, "label": "Connected - IIoT with data historian"},
                    {"value": 5, "label": "Unified - IT/OT converged data platform"}
                ]
            },
            {
                "id": "mfg_dm_2",
                "dimension": "data_maturity",
                "text": "What is your product quality data capture capability?",
                "options": [
                    {"value": 1, "label": "Manual - Paper-based QC records"},
                    {"value": 2, "label": "Basic - Digital inspection records"},
                    {"value": 3, "label": "Moderate - SPC data with some automation"},
                    {"value": 4, "label": "Advanced - Vision systems and inline inspection"},
                    {"value": 5, "label": "Comprehensive - AI quality prediction"}
                ]
            },
            # Technology Infrastructure
            {
                "id": "mfg_ti_1",
                "dimension": "technology_infrastructure",
                "text": "What is your edge computing capability for AI?",
                "options": [
                    {"value": 1, "label": "None - All processing centralized"},
                    {"value": 2, "label": "Basic - Some local PLCs"},
                    {"value": 3, "label": "Developing - Edge gateways deployed"},
                    {"value": 4, "label": "Advanced - Edge AI for real-time inference"},
                    {"value": 5, "label": "Leading - Distributed AI across plant floor"}
                ]
            },
            {
                "id": "mfg_ti_2",
                "dimension": "technology_infrastructure",
                "text": "How mature is your digital twin capability?",
                "options": [
                    {"value": 1, "label": "None - No digital twin"},
                    {"value": 2, "label": "Basic - CAD models only"},
                    {"value": 3, "label": "Developing - Static digital twin"},
                    {"value": 4, "label": "Advanced - Live digital twin with data"},
                    {"value": 5, "label": "Leading - AI-powered predictive twin"}
                ]
            },
            # Process & Operations
            {
                "id": "mfg_po_1",
                "dimension": "process_operations",
                "text": "What is your predictive maintenance capability?",
                "options": [
                    {"value": 1, "label": "Reactive - Fix when broken"},
                    {"value": 2, "label": "Scheduled - Time-based maintenance"},
                    {"value": 3, "label": "Condition-based - Monitor key parameters"},
                    {"value": 4, "label": "Predictive - ML models for failure prediction"},
                    {"value": 5, "label": "Prescriptive - AI recommends optimal actions"}
                ]
            },
            {
                "id": "mfg_po_2",
                "dimension": "process_operations",
                "text": "How optimized is your production scheduling?",
                "options": [
                    {"value": 1, "label": "Manual - Spreadsheet scheduling"},
                    {"value": 2, "label": "Basic - MRP/ERP scheduling"},
                    {"value": 3, "label": "Moderate - APS with constraints"},
                    {"value": 4, "label": "Advanced - Real-time optimization"},
                    {"value": 5, "label": "Intelligent - AI-driven dynamic scheduling"}
                ]
            },
            # Workforce & Culture
            {
                "id": "mfg_wc_1",
                "dimension": "workforce_culture",
                "text": "What is operator acceptance of AI-assisted manufacturing?",
                "options": [
                    {"value": 1, "label": "Resistant - Prefer traditional methods"},
                    {"value": 2, "label": "Skeptical - Concerns about job impact"},
                    {"value": 3, "label": "Neutral - Will follow if required"},
                    {"value": 4, "label": "Supportive - See value in AI assistance"},
                    {"value": 5, "label": "Enthusiastic - Actively request AI tools"}
                ]
            },
            {
                "id": "mfg_wc_2",
                "dimension": "workforce_culture",
                "text": "Do you have industrial data science capability?",
                "options": [
                    {"value": 1, "label": "None - No data science for manufacturing"},
                    {"value": 2, "label": "Limited - Rely on vendor analytics"},
                    {"value": 3, "label": "Developing - Engineers doing data analysis"},
                    {"value": 4, "label": "Established - Industrial data science team"},
                    {"value": 5, "label": "Advanced - AI CoE for manufacturing"}
                ]
            },
            # Governance & Compliance
            {
                "id": "mfg_gc_1",
                "dimension": "governance_compliance",
                "text": "How do you validate AI for safety-critical applications?",
                "options": [
                    {"value": 1, "label": "Not addressed - No AI in safety systems"},
                    {"value": 2, "label": "Basic - Standard testing only"},
                    {"value": 3, "label": "Developing - Safety assessment for AI"},
                    {"value": 4, "label": "Established - IEC 61508 compliance for AI"},
                    {"value": 5, "label": "Advanced - Certified AI safety systems"}
                ]
            },
            {
                "id": "mfg_gc_2",
                "dimension": "governance_compliance",
                "text": "What is your AI model change management for production?",
                "options": [
                    {"value": 1, "label": "None - No change control"},
                    {"value": 2, "label": "Basic - Manual approval process"},
                    {"value": 3, "label": "Moderate - Change management with testing"},
                    {"value": 4, "label": "Mature - Automated testing and rollback"},
                    {"value": 5, "label": "Advanced - Continuous validation in production"}
                ]
            }
        ]
    },

    "retail": {
        "name": "Retail",
        "questions": [
            # Data Maturity
            {
                "id": "ret_dm_1",
                "dimension": "data_maturity",
                "text": "How unified is your customer data across channels?",
                "options": [
                    {"value": 1, "label": "Siloed - Separate data per channel"},
                    {"value": 2, "label": "Basic - Some data consolidation"},
                    {"value": 3, "label": "Moderate - CDP with partial integration"},
                    {"value": 4, "label": "Unified - Single customer view"},
                    {"value": 5, "label": "Real-time - Unified profile with live updates"}
                ]
            },
            {
                "id": "ret_dm_2",
                "dimension": "data_maturity",
                "text": "What is your product data management capability?",
                "options": [
                    {"value": 1, "label": "Basic - Spreadsheets and catalogs"},
                    {"value": 2, "label": "Developing - PIM system implemented"},
                    {"value": 3, "label": "Moderate - Rich product attributes"},
                    {"value": 4, "label": "Advanced - AI-enhanced product data"},
                    {"value": 5, "label": "Comprehensive - Knowledge graph for products"}
                ]
            },
            # Technology Infrastructure
            {
                "id": "ret_ti_1",
                "dimension": "technology_infrastructure",
                "text": "How AI-enabled is your e-commerce platform?",
                "options": [
                    {"value": 1, "label": "Basic - Static product catalog"},
                    {"value": 2, "label": "Developing - Rule-based recommendations"},
                    {"value": 3, "label": "Moderate - ML personalization"},
                    {"value": 4, "label": "Advanced - Real-time AI across journey"},
                    {"value": 5, "label": "Leading - Conversational commerce with AI"}
                ]
            },
            {
                "id": "ret_ti_2",
                "dimension": "technology_infrastructure",
                "text": "What is your in-store AI technology capability?",
                "options": [
                    {"value": 1, "label": "None - Traditional retail only"},
                    {"value": 2, "label": "Basic - Self-checkout"},
                    {"value": 3, "label": "Moderate - Computer vision pilots"},
                    {"value": 4, "label": "Advanced - Smart shelves and analytics"},
                    {"value": 5, "label": "Leading - Autonomous store technology"}
                ]
            },
            # Process & Operations
            {
                "id": "ret_po_1",
                "dimension": "process_operations",
                "text": "How AI-driven is your demand forecasting?",
                "options": [
                    {"value": 1, "label": "Basic - Historical averages"},
                    {"value": 2, "label": "Developing - Statistical forecasting"},
                    {"value": 3, "label": "Moderate - ML models for forecasting"},
                    {"value": 4, "label": "Advanced - Multi-factor AI forecasting"},
                    {"value": 5, "label": "Leading - Real-time demand sensing"}
                ]
            },
            {
                "id": "ret_po_2",
                "dimension": "process_operations",
                "text": "What is your pricing optimization capability?",
                "options": [
                    {"value": 1, "label": "Static - Fixed pricing"},
                    {"value": 2, "label": "Basic - Periodic price reviews"},
                    {"value": 3, "label": "Moderate - Competitive price matching"},
                    {"value": 4, "label": "Advanced - Dynamic pricing rules"},
                    {"value": 5, "label": "Intelligent - AI-optimized pricing"}
                ]
            },
            # Workforce & Culture
            {
                "id": "ret_wc_1",
                "dimension": "workforce_culture",
                "text": "How AI-equipped are your store associates?",
                "options": [
                    {"value": 1, "label": "Not equipped - No AI tools"},
                    {"value": 2, "label": "Basic - Mobile devices for lookup"},
                    {"value": 3, "label": "Moderate - Task management apps"},
                    {"value": 4, "label": "Advanced - AI clienteling tools"},
                    {"value": 5, "label": "Leading - AI assistant for associates"}
                ]
            },
            {
                "id": "ret_wc_2",
                "dimension": "workforce_culture",
                "text": "What analytics capability exists in merchandising?",
                "options": [
                    {"value": 1, "label": "Basic - Sales reports only"},
                    {"value": 2, "label": "Developing - BI dashboards"},
                    {"value": 3, "label": "Moderate - Category analytics"},
                    {"value": 4, "label": "Advanced - Predictive merchandising"},
                    {"value": 5, "label": "Leading - AI-driven assortment optimization"}
                ]
            },
            # Governance & Compliance
            {
                "id": "ret_gc_1",
                "dimension": "governance_compliance",
                "text": "How do you manage AI personalization vs privacy?",
                "options": [
                    {"value": 1, "label": "Not addressed - No privacy consideration"},
                    {"value": 2, "label": "Basic - Cookie consent only"},
                    {"value": 3, "label": "Moderate - Privacy policy and opt-out"},
                    {"value": 4, "label": "Advanced - Preference center and consent management"},
                    {"value": 5, "label": "Leading - Privacy-preserving personalization"}
                ]
            },
            {
                "id": "ret_gc_2",
                "dimension": "governance_compliance",
                "text": "What is your AI pricing fairness governance?",
                "options": [
                    {"value": 1, "label": "None - No pricing oversight"},
                    {"value": 2, "label": "Basic - Legal review of pricing"},
                    {"value": 3, "label": "Moderate - Price discrimination policies"},
                    {"value": 4, "label": "Advanced - Fairness testing for pricing AI"},
                    {"value": 5, "label": "Comprehensive - Automated pricing ethics review"}
                ]
            }
        ]
    },

    "general": {
        "name": "General/Cross-Industry",
        "questions": [
            # Data Maturity
            {
                "id": "gen_dm_1",
                "dimension": "data_maturity",
                "text": "How do you ensure data freshness for AI applications?",
                "options": [
                    {"value": 1, "label": "Stale - Data updated infrequently"},
                    {"value": 2, "label": "Batch - Daily/weekly updates"},
                    {"value": 3, "label": "Regular - Multiple daily updates"},
                    {"value": 4, "label": "Near real-time - Hourly or better"},
                    {"value": 5, "label": "Real-time - Streaming data pipelines"}
                ]
            },
            {
                "id": "gen_dm_2",
                "dimension": "data_maturity",
                "text": "What external data do you leverage for AI?",
                "options": [
                    {"value": 1, "label": "None - Internal data only"},
                    {"value": 2, "label": "Limited - Some purchased datasets"},
                    {"value": 3, "label": "Moderate - Third-party data providers"},
                    {"value": 4, "label": "Extensive - Multiple external sources"},
                    {"value": 5, "label": "Comprehensive - Real-time external data feeds"}
                ]
            },
            # Technology Infrastructure
            {
                "id": "gen_ti_1",
                "dimension": "technology_infrastructure",
                "text": "How do you manage AI experimentation environments?",
                "options": [
                    {"value": 1, "label": "None - Production only"},
                    {"value": 2, "label": "Basic - Shared dev environment"},
                    {"value": 3, "label": "Moderate - Dedicated sandbox"},
                    {"value": 4, "label": "Advanced - On-demand ML environments"},
                    {"value": 5, "label": "Leading - Self-service AI platform"}
                ]
            },
            {
                "id": "gen_ti_2",
                "dimension": "technology_infrastructure",
                "text": "What is your API management maturity for AI services?",
                "options": [
                    {"value": 1, "label": "None - No API management"},
                    {"value": 2, "label": "Basic - Manual API documentation"},
                    {"value": 3, "label": "Moderate - API gateway implemented"},
                    {"value": 4, "label": "Advanced - Full lifecycle API management"},
                    {"value": 5, "label": "Leading - AI API marketplace with monetization"}
                ]
            },
            # Process & Operations
            {
                "id": "gen_po_1",
                "dimension": "process_operations",
                "text": "How do you prioritize AI use cases?",
                "options": [
                    {"value": 1, "label": "Ad-hoc - No formal process"},
                    {"value": 2, "label": "Basic - Leadership decides"},
                    {"value": 3, "label": "Structured - Business case required"},
                    {"value": 4, "label": "Systematic - ROI framework (RICE/similar)"},
                    {"value": 5, "label": "Data-driven - Portfolio optimization"}
                ]
            },
            {
                "id": "gen_po_2",
                "dimension": "process_operations",
                "text": "What is your AI project delivery methodology?",
                "options": [
                    {"value": 1, "label": "None - Ad-hoc development"},
                    {"value": 2, "label": "Basic - Waterfall approach"},
                    {"value": 3, "label": "Agile - Scrum/Kanban for AI"},
                    {"value": 4, "label": "Mature - AI-specific methodology"},
                    {"value": 5, "label": "Advanced - Continuous AI delivery"}
                ]
            },
            # Workforce & Culture
            {
                "id": "gen_wc_1",
                "dimension": "workforce_culture",
                "text": "How do you foster AI innovation internally?",
                "options": [
                    {"value": 1, "label": "Not fostered - No innovation programs"},
                    {"value": 2, "label": "Basic - Suggestion box approach"},
                    {"value": 3, "label": "Moderate - Hackathons and idea contests"},
                    {"value": 4, "label": "Active - Innovation lab or sandbox"},
                    {"value": 5, "label": "Embedded - AI innovation in everyone's role"}
                ]
            },
            {
                "id": "gen_wc_2",
                "dimension": "workforce_culture",
                "text": "What partnerships do you have for AI capability?",
                "options": [
                    {"value": 1, "label": "None - Fully internal"},
                    {"value": 2, "label": "Vendors - Buy AI products"},
                    {"value": 3, "label": "Consultants - Project-based help"},
                    {"value": 4, "label": "Strategic - Long-term AI partners"},
                    {"value": 5, "label": "Ecosystem - Academic and startup partnerships"}
                ]
            },
            # Governance & Compliance
            {
                "id": "gen_gc_1",
                "dimension": "governance_compliance",
                "text": "Do you have an AI Center of Excellence or governance body?",
                "options": [
                    {"value": 1, "label": "None - Decentralized AI efforts"},
                    {"value": 2, "label": "Informal - Some coordination"},
                    {"value": 3, "label": "Forming - CoE being established"},
                    {"value": 4, "label": "Established - Active AI CoE"},
                    {"value": 5, "label": "Mature - CoE with federated model"}
                ]
            },
            {
                "id": "gen_gc_2",
                "dimension": "governance_compliance",
                "text": "How do you measure AI ROI and value?",
                "options": [
                    {"value": 1, "label": "Not measured - No AI metrics"},
                    {"value": 2, "label": "Basic - Project completion tracking"},
                    {"value": 3, "label": "Moderate - Cost savings measured"},
                    {"value": 4, "label": "Comprehensive - Full ROI framework"},
                    {"value": 5, "label": "Advanced - Real-time AI value dashboard"}
                ]
            }
        ]
    }
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_questions_for_sector(sector: str = "general") -> Dict[str, Any]:
    """
    Get all questions for a specific sector (core + sector-specific).

    Args:
        sector: One of SECTORS list

    Returns:
        Dict with dimension questions including sector-specific ones
    """
    if sector not in SECTORS:
        sector = "general"

    # Start with core questions
    questions = {}
    for dim_id, dim_data in CORE_QUESTIONS.items():
        questions[dim_id] = {
            "name": dim_data["name"],
            "description": dim_data["description"],
            "weight": dim_data["weight"],
            "questions": list(dim_data["questions"])  # Copy the list
        }

    # Add sector-specific questions
    sector_qs = SECTOR_QUESTIONS.get(sector, SECTOR_QUESTIONS["general"])
    for q in sector_qs["questions"]:
        dim = q["dimension"]
        if dim in questions:
            questions[dim]["questions"].append(q)

    return questions


def get_all_question_ids(sector: str = "general") -> List[str]:
    """Get list of all question IDs for a sector."""
    questions = get_questions_for_sector(sector)
    ids = []
    for dim_data in questions.values():
        for q in dim_data["questions"]:
            ids.append(q["id"])
    return ids


def get_question_count(sector: str = "general") -> int:
    """Get total question count for a sector."""
    return len(get_all_question_ids(sector))


# Export main data structures
QUESTIONS = CORE_QUESTIONS
