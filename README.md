\# ConstructAI



AI-powered construction project control assistant that combines \*\*Civil Engineering project controls, MCP, SQLAlchemy, and a local LLM\*\* to analyze project schedules, delays, risks, resources, and recovery strategies.



\## 🚧 Overview



ConstructAI is designed as an AI assistant for construction project control.



Instead of manually checking multiple project-control reports, the user can ask questions in natural language and the system can:



\- Analyze project schedule status

\- Identify critical activities

\- Find activities by name

\- Analyze construction delays

\- Determine delay impact on project completion

\- Identify delayed activities

\- Analyze activity dependencies

\- Identify resource bottlenecks

\- Analyze project risks

\- Generate schedule recovery strategies

\- Provide an overall project-control summary



The AI interacts with the project-control functions through \*\*Model Context Protocol (MCP)\*\* tools.



\## 🏗️ Architecture



```text

&#x20;                   User

&#x20;                    │

&#x20;                    ▼

&#x20;             Natural Language

&#x20;                    │

&#x20;                    ▼

&#x20;            ┌───────────────┐

&#x20;            │   Qwen3 8B    │

&#x20;            │ Local via     │

&#x20;            │    Ollama     │

&#x20;            └───────┬───────┘

&#x20;                    │

&#x20;                    ▼

&#x20;             MCP Tool Calling

&#x20;                    │

&#x20;                    ▼

&#x20;            ┌───────────────┐

&#x20;            │ ConstructAI   │

&#x20;            │  MCP Server   │

&#x20;            └───────┬───────┘

&#x20;                    │

&#x20;         ┌──────────┼──────────┐

&#x20;         ▼          ▼          ▼

&#x20;     Scheduling   Delays     Risks

&#x20;     \& CPM        \& Impact   \& Resources

&#x20;         │          │          │

&#x20;         └──────────┼──────────┘

&#x20;                    ▼

&#x20;               SQLAlchemy

&#x20;                    │

&#x20;                    ▼

&#x20;             Project Database

&#x20;                    │

&#x20;                    ▼

&#x20;            Engineering Result

🤖 AI Stack
Python
MCP 2.1.1
Qwen3 8B
Ollama
SQLAlchemy
SQLite
Natural-language tool calling

The LLM runs locally using Ollama, so the project does not require a paid AI API.

🔧 MCP Tools

ConstructAI currently provides 11 MCP tools:

#	Tool	Purpose
1	analyze_delay	Analyze the impact of an activity delay
2	project_status	Retrieve overall project status
3	critical_activities	Identify critical activities
4	activity_details	Retrieve detailed activity information
5	delayed_activities	Identify delayed activities
6	activity_dependencies	Analyze predecessor and successor relationships
7	schedule_recovery	Generate schedule recovery options
8	resource_bottleneck	Identify resource bottlenecks
9	project_risk_analysis	Analyze project risks
10	project_control_summary	Generate overall project-control information
11	find_activity_tool	Find activities using natural-language activity names
📊 Project Control Capabilities
Schedule Management

ConstructAI can analyze:

Planned start and finish dates
Activity durations
Early and late dates
Total float
Critical activities
Activity dependencies
Project completion date
Delay Analysis

The system can determine:

Delayed activity
Delay duration
Original project finish
New project finish
Project completion impact
Affected downstream activities
Priority of the delay
Recommended corrective action
Schedule Recovery

ConstructAI can recommend recovery strategies such as:

Expediting material procurement
Increasing manpower
Increasing working hours
Prioritizing critical activities
Coordinating successor activities
Controlled activity overlap
🧠 Example AI Workflow
User Question

Electrical Rough-in is delayed by 3 days because of a material shortage. What is the impact on Project 3 and how can we recover the schedule?

AI Tool Workflow
User Question
      │
      ▼
find_activity_tool
      │
      ▼
Find Electrical Rough-in
      │
      ▼
Activity ID = 33
      │
      ▼
analyze_delay
      │
      ▼
Calculate Project Impact
      │
      ▼
schedule_recovery
      │
      ▼
Generate Recovery Strategy
      │
      ▼
Engineering Recommendation
Example Result
Original Project Finish : 2026-11-06
New Project Finish      : 2026-11-09
Project Impact          : 3 days
Priority                : CRITICAL

Recovery Actions:
1. Expedite material procurement
2. Increase manpower
3. Increase working hours
4. Prioritize critical-path activity
5. Coordinate successor activities
🏢 Demo Project

The project currently includes a sample construction schedule:

ConstructAI Building Control Demo

The schedule contains activities covering:

Site Mobilization
Excavation
PCC
Footing Reinforcement
Footing Concrete
Pedestal Reinforcement
Pedestal Concrete
Column Reinforcement
Column Concrete
Slab Reinforcement
Slab Concrete
Masonry
Electrical Rough-in
Plumbing Rough-in
Plastering
Flooring
False Ceiling
Painting
Final MEP Installation
Testing & Commissioning
Final Inspection & Handover
🧪 Testing

The project includes individual test files for major modules and project-control functions.

Examples include:

test_cpm.py
test_delay.py
test_delay_impact.py
test_project_status.py
test_project_risk.py
test_schedule_recovery.py
test_resource_bottleneck.py
test_project_control_summary.py
📁 Project Structure
ConstructAI/
│
├── ai_client.py
├── server.py
│
├── database.py
├── models.py
│
├── cpm.py
├── schedule.py
├── schedule_variance.py
├── forecast.py
│
├── activity_details.py
├── activity_dependencies.py
├── critical_activities.py
├── delayed_activities.py
├── find_activity.py
│
├── delay_analysis.py
├── delay_impact.py
│
├── recovery.py
├── recovery_impact.py
├── schedule_recovery.py
│
├── resource_bottleneck.py
├── project_risk_analysis.py
├── project_control.py
├── project_control_summary.py
├── project_status.py
├── recommendations.py
│
├── requirements.txt
├── README.md
└── .gitignore
🚀 Installation
1. Clone the repository
git clone https://github.com/bilalgit/ConstructAI.git
cd ConstructAI
2. Create a virtual environment
python -m venv venv

Activate it on Windows:

venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Install Ollama

Install Ollama and download the Qwen3 model:

ollama pull qwen3:8b
5. Run ConstructAI

Start the MCP server / AI client according to the project configuration.

💰 Cost

ConstructAI uses a local LLM through Ollama.

AI Model       : Qwen3 8B
Inference      : Local
API Cost       : ₹0

No OpenAI API subscription or paid inference API is required for the current setup.

🎯 Project Objective

The objective of ConstructAI is to explore how Artificial Intelligence and Model Context Protocol can be applied to construction project management and project controls.

The project combines concepts from:

Civil Engineering
Construction Planning
Critical Path Method
Schedule Management
Delay Analysis
Risk Management
Resource Management
Artificial Intelligence
MCP Tool Calling
Local LLMs
Database-driven project controls
🔮 Future Development

Potential future improvements include:

Construction cost control
Quantity tracking
Earned Value Management
Resource leveling
Progress forecasting
Automated daily progress reports
AI-generated weekly/monthly reports
BIM integration
Primavera P6 data integration
Power BI dashboards
Construction document intelligence
Multi-project portfolio monitoring
👨‍💻 Author

Bilal

Civil Engineering | Construction Project Controls | AI Engineering

⭐ If you find this project interesting, feel free to explore the repository.
