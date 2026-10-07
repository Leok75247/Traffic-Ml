# Ambulance Traffic State Prediction Using Hidden Markov Models
## Project Constitution

> This file is the highest-priority project constraint. Any coding agent must read it before making changes.

## 1. Exact Project Identity

**Project title:** Ambulance Traffic State Prediction Using Hidden Markov Models

**Project type:** Small academic mini-project and working demonstration.

The application uses sequential traffic observations to infer hidden traffic conditions and estimate the next likely traffic condition.

The ambulance/emergency-response context is the application context. The project itself is **not** an ambulance routing or dispatch system.

## 2. Core Problem

Given a chronological sequence of traffic observations for a road/sensor/segment, infer hidden traffic states:

- Low Traffic
- Medium Traffic
- High Traffic

and estimate the likely next traffic state.

## 3. Required Algorithmic Scope

The machine-learning core is limited to:

1. Hidden Markov Models (HMM)
2. Forward algorithm
3. Viterbi algorithm
4. Baum-Welch / Forward-Backward

No unrelated machine-learning algorithms may be introduced.

## 4. Explicitly Prohibited ML

Do not add:

- Random Forest
- XGBoost
- SVM
- KNN
- Decision Trees
- Logistic Regression
- AdaBoost
- Neural Networks
- CNN
- RNN
- LSTM
- GRU
- Transformers
- Reinforcement Learning
- K-Means
- SOM
- Recommendation models
- Ensemble models

These are not needed for the project.

## 5. Explicitly Prohibited Product Features

Do not build:

- Route optimization
- Shortest-path routing
- Live ambulance navigation
- GPS tracking
- Dispatch workflow
- Hospital integration
- Mobile application
- User authentication
- Payments
- Chatbot
- LLM integration
- Paid external AI APIs
- Google Maps dependency
- Real-time external traffic API
- Microservices
- Kubernetes
- Kafka
- Redis
- Complex cloud infrastructure

## 6. Architecture Principle

Prefer a small monolithic application with clear boundaries:

React frontend -> FastAPI backend -> HMM/data layer

Do not split the system into unnecessary services.

## 7. Library Principle

Prefer mature, well-documented libraries for engineering work.

Preferred stack:

- Python
- Pandas
- NumPy
- SciPy where mathematically useful
- FastAPI
- Pydantic
- React
- Vite
- Tailwind CSS
- Recharts or Plotly
- Lucide icons
- pytest

For HMM functionality, a mature HMM library may be used as a reference/validation layer, but the project must still expose understandable Forward, Viterbi, and Baum-Welch concepts and tests.

Do not select obscure, experimental libraries merely to appear novel.

## 8. Correctness Rules

- Never fabricate metrics.
- Never fabricate model outputs.
- Never hardcode fake predictions into the UI.
- Every displayed numerical result must originate from the actual backend computation.
- Distinguish actual measured results from examples.
- If synthetic data is used, label it clearly.
- Never claim real-world emergency-response improvement unless it has actually been measured with appropriate evidence.

## 9. Scope Control

When a proposed feature is not necessary to answer the core problem, do not implement it.

Priority order:

**Correctness > explainability > simplicity > reliability > visual polish > extra features**

## 10. UI Direction

The UI should feel like a restrained emergency-operations analytics product.

Desired qualities:

- clean
- understated
- professional
- mature
- readable
- premium without being flashy
- generous whitespace
- strong typography
- subtle borders and shadows
- limited accent usage

Avoid "AI slop":

- purple gradient dashboards
- excessive green success panels
- neon cyberpunk
- giant glowing text
- excessive glassmorphism
- rainbow charts
- excessive animation
- decorative 3D effects
- meaningless KPI cards

The visual language should feel closer to an established operations/analytics product than a generic AI landing page.

## 11. Data and Privacy

No personal data is required.

Do not collect:

- names
- phone numbers
- exact user locations
- medical records
- vehicle identifiers
- authentication information

The project should run locally and avoid external data transmission during the demo.

## 12. Mapping

Maps are optional and not part of the core project.

The core application must work without any map provider.

If a map is ever added later, it must be optional and must not become a dependency of the ML workflow.

## 13. Academic Presentation

The application and documentation must be one coherent project.

Do not organize the project by academic numbering or create a section/folder/page naming scheme based on course modules.

Use natural project concepts such as:

- Data
- Preprocessing
- HMM
- Forward
- Viterbi
- Baum-Welch
- Results
- Visualization
- Dashboard
- Testing

## 14. AI Agent Behavior

Before modifying code:

1. Read this file.
2. Read the relevant specification files.
3. Inspect existing code.
4. Make the smallest correct change.
5. Run relevant tests.
6. Report what changed and what remains.

Do not rewrite the entire project for small fixes.

Do not change architecture without documenting the reason and obtaining explicit approval.
