Green AI Hardware Recommendation Tool is a production-style student prototype designed to recommend AI hardware configurations that balance Performance, Cost, and Carbon Impact.
The tool is interactive, web-based, and built with Python and Streamlit, allowing users to make data-driven decisions about AI infrastructure based on workload, budget, and sustainability.
This project simulates real-world enterprise decision-making by combining technical metrics, environmental impact, and cost considerations.

Key Features

Location-Based Recommendations:
Filter hardware based on availability in different locations.

Workload Metrics Calculation:
Estimates training time, inference latency, and workload-adjusted TCO (Total Cost of Ownership).

Carbon Emission Estimation:
Calculates CO₂ emission based on power usage, workload hours, and renewable energy percentage.

Custom Scoring & Ranking:
Generates a Final Score for each hardware option based on weighted metrics:
Prototype: Focus on cost & sustainability
Large-scale: Focus on performance & scalability

Interactive Visualizations:
Scatter plots (Performance vs TCO)
Bar charts (Renewable %, Carbon Emission)
Line charts (Final Score trend)

Export Options:
Download recommendations as a CSV file for further analysis.

Dynamic UI & Styling:
Gradient backgrounds, colorful cards, and animated visual effects for an engaging user interface.

Workflow
User selects location, workload type, scale/profile, budget, number of servers, model size, and workload hours.
Tool filters hardware database based on input constraints.
Calculates metrics for TCO, carbon emission, and workload performance.
Normalizes and combines metrics to generate a Final Score for ranking.
Displays top recommended hardware in a table and card format.
Visual insights are generated with Plotly charts.
Users can download recommendations for reporting or planning.

How to Run the Project

Clone the repository:

git clone <repo-url>
cd assignment-b


Install dependencies:

pip install streamlit pandas plotly


Place the dataset hardware_database.csv in the project folder.

Run the Streamlit app:

streamlit run app.py


Open the provided URL in the browser to interact with the tool.

Screenshots:
<img width="1751" height="751" alt="Screenshot 2025-10-18 191942" src="https://github.com/user-attachments/assets/be4ec057-6175-4ef0-9b3f-1040462b0c0b" />
<img width="1763" height="406" alt="Screenshot 2025-10-18 192003" src="https://github.com/user-attachments/assets/2abaf8ba-1d22-4b9c-bfab-e7c0fb24cab6" />
<img width="1749" height="526" alt="Screenshot 2025-10-18 192023" src="https://github.com/user-attachments/assets/dd7699b9-2f94-4698-963a-ed1e61d9e9db" />
<img width="1758" height="641" alt="Screenshot 2025-10-18 192053" src="https://github.com/user-attachments/assets/a20a0ed5-649a-4c44-8ab6-ed0cb6ef831b" />
<img width="1756" height="573" alt="Screenshot 2025-10-18 192112" src="https://github.com/user-attachments/assets/16bb2821-2eba-42f2-9532-f040f376331e" />
<img width="1744" height="558" alt="Screenshot 2025-10-18 192136" src="https://github.com/user-attachments/assets/abc9838a-be8c-4b74-bc1e-04a9106f0a62" />

Recommendation Table: Shows top hardware options with TCO, carbon emission, and scores.
Best Hardware Card: Highlights the top recommendation visually.
Visual Insights: Scatter, bar, and line charts for performance and sustainability analysis.
Download Option: CSV export for reporting.

Learning Outcomes

Building a full-stack, data-driven recommendation tool using Python and Streamlit.
Integrating cost, performance, and environmental impact in hardware decision-making.
Implementing custom scoring, normalization, and ranking algorithms.
Using Plotly for interactive data visualizations.
Designing an engaging, production-style UI with CSS and Streamlit components.

Future Enhancements

Real-time pricing: Pull hardware costs from online retailers using APIs.
Cloud Integration: Suggest cloud hardware instances alongside physical servers.
AI-based Optimization: Use ML models to predict best hardware combinations for unknown workloads.
Comparison Dashboard: Compare multiple configurations side by side.
