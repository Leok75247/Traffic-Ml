# NotebookLM Research Prompt

Use this prompt after uploading the documents in this pack plus the BAI702 syllabus,
BAI702 algorithm list, and the documentation for any candidate traffic dataset.

You are the research lead for this college mini-project:

“Ambulance Traffic State Prediction Using Hidden Markov Models”

Your job is NOT to generate application code.

Your job is to produce a rigorous, evidence-based research brief that I can use to
build the project correctly and efficiently within 7 days.

IMPORTANT RULES

1. Use the uploaded sources as the primary evidence.
2. Do not invent facts, dataset properties, metrics, citations, or implementation details.
3. Clearly distinguish:
   - directly supported facts
   - reasonable inference
   - recommendations
   - unresolved uncertainty
4. Do not organize the answer by academic modules.
5. Keep the project small and realistic.
6. Do not expand the scope into a production ambulance platform.
7. Do not recommend unrelated machine-learning algorithms.
8. Do not recommend unnecessary cloud services or paid APIs.
9. Prefer mature, documented libraries over obscure or experimental libraries.
10. Flag anything that could cause major implementation risk within a 7-day timeline.

PROJECT SCOPE

The system should use:
- Hidden Markov Models
- Forward algorithm
- Viterbi algorithm
- Baum-Welch / Forward-Backward

Hidden traffic states:
- Low Traffic
- Medium Traffic
- High Traffic

Observed traffic variables may include:
- speed
- flow/volume
- occupancy
- timestamp
- sensor/entity identifier

The project should estimate the current traffic condition, estimate the next likely
traffic state, and display the most likely hidden-state sequence.

The ambulance/emergency-response context is the application context.

This is NOT:
- ambulance route optimization
- shortest path
- GPS navigation
- dispatch software
- hospital integration
- live ambulance tracking
- Google Maps application
- mobile application
- LLM application
- unrelated ML model comparison

RESEARCH QUESTIONS

A. DATASET RESEARCH
1. Identify the most suitable dataset among the sources available to us.
2. Explain why it is suitable for an HMM.
3. Verify temporal resolution, number of entities/sensors, traffic variables, sequence
   structure, time span, missing-data issues, and geographic metadata.
4. Determine whether the dataset supports chronological sequences, repeated observations
   for the same entity, Low/Medium/High hidden-state modeling, and optional mapping.
5. Identify the minimum subset needed for a 7-day mini-project.
6. Identify the biggest dataset risks.
7. Provide the exact dataset source, version if available, schema, preprocessing requirements,
   licensing/usage notes, and coordinate availability.
Do not claim that a field exists unless the source confirms it.

B. HMM DESIGN
Determine the most practical HMM formulation.
Answer:
- what should the hidden states represent?
- what should observations represent?
- discretized vs continuous emissions?
- simplest academically defensible formulation?
- how should Low/Medium/High states be established?
- how should initial probabilities be estimated?
- how should the transition matrix be estimated?
- how should emissions be estimated?
- how should next-state probability be calculated?
- what assumptions and limitations matter?
Explain in simple viva-ready language.

C. ALGORITHM RESEARCH
Research:
1. Forward
2. Viterbi
3. Baum-Welch / Forward-Backward

For each:
- purpose
- input/output
- key mathematical idea
- complexity if relevant
- implementation risks
- common mistakes
- what should be visible in the demo
- what I should explain in a viva

Also explain Forward vs Viterbi vs Baum-Welch and how they interact.

D. PYTHON LIBRARY RESEARCH
Compare mature Python HMM libraries using:
- documentation
- maintenance status
- stability
- Python compatibility
- simplicity
- training support
- decoding support
- numerical reliability
- hallucination/implementation-risk reduction

Prefer established libraries. Do not recommend obscure packages just for novelty.
Provide:
1. recommended library
2. backup library
3. what to implement ourselves
4. what to delegate to the library
5. why

E. ARCHITECTURE
Evaluate:
React + Vite + Tailwind
        ↓
FastAPI
        ↓
Python HMM layer
        ↓
Pandas / NumPy
        ↓
Traffic dataset

Keep the architecture minimal. Identify unnecessary components and clean API/data
boundaries. Do not recommend microservices unless genuinely necessary.

F. FRONTEND / VISUALIZATION
The visual style is:
- clean
- restrained
- professional
- old-money / institutional
- light modern analytics
- serious emergency-operations feel

Avoid:
- purple AI gradients
- neon
- cyberpunk
- excessive glassmorphism
- giant glowing KPI cards
- generic AI dashboard aesthetics

Determine the best information hierarchy, chart types, KPI choices, technical panels,
explanation content, and clutter to remove.

G. MAP / GEOGRAPHIC CONTEXT
Determine whether a map is genuinely useful.
Compare:
- no map
- Leaflet + OpenStreetMap/OpenFreeMap
- Google Maps

Research API-key requirements, billing, licensing/usage constraints, coordinate
availability, complexity, and benefit to the ML demo.
The map must remain optional.
Do not turn this into route optimization.

H. EVALUATION
Separate:
1. dataset with real traffic-state labels
2. dataset without ground-truth hidden states

Explain appropriate vs inappropriate metrics and how to avoid misleading claims.
Pay particular attention to unsupervised latent-state inference vs supervised accuracy.
Never invent accuracy.

I. 7-DAY FEASIBILITY
Create a realistic day-by-day build plan with:
- objective
- deliverables
- validation checkpoint
- maximum scope
- cuts if time is lost

Identify highest-risk tasks and the absolute minimum viable project.

J. ACADEMIC + ENTREPRENEURIAL VALUE
Explain:
- why the problem is meaningful
- technical demonstration value
- difference from ambulance route optimization
- future product concept
- supported vs speculative claims

FINAL OUTPUT

Return exactly:

1. EXECUTIVE FINDINGS
2. DATASET DECISION
3. HMM DESIGN DECISION
4. ALGORITHM IMPLEMENTATION PLAN
5. PYTHON LIBRARY DECISION
6. SYSTEM ARCHITECTURE
7. FRONTEND / UX DECISION
8. MAP DECISION
9. EVALUATION STRATEGY
10. 7-DAY BUILD PLAN
11. TOP 10 TECHNICAL RISKS
12. WHAT NOT TO BUILD
13. FINAL RECOMMENDED STACK
14. SOURCES / EVIDENCE TABLE
15. OPEN QUESTIONS THAT MUST BE RESOLVED BEFORE CODING

End with:

GO / NO-GO

and explain the decision strictly from the evidence and 7-day feasibility.

Do not write application code.
Do not create fictional results.
Do not silently fill missing information.
