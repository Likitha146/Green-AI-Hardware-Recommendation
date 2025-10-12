import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# Load Hardware Dataset
# -------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("hardware_database.csv")

df = load_data()

# -------------------------------
# Workload Metrics
# -------------------------------
def add_workload_metrics(df, workload_type, model_size=1):
    df = df.copy()
    if workload_type.lower() == "training":
        df["Est Time (hrs)"] = model_size * 10 / df["Performance"]
    elif workload_type.lower() == "inference":
        df["Est Latency (ms)"] = 1000 / df["Performance"]
    return df

# -------------------------------
# TCO Calculation
# -------------------------------
electricity_rate = 7
pue = 1.6

def calculate_tco(row, workload_hours=10):
    adjusted_power = row["Power (W)"] * pue
    energy_cost = adjusted_power * workload_hours / 1000 * electricity_rate
    return row["Cost (₹)"] + energy_cost

# -------------------------------
# Carbon Emission
# -------------------------------
emission_factor = 0.708
def calculate_carbon_emission(row, workload_hours=10):
    adjusted_power = row["Power (W)"] * pue
    carbon_kg = (adjusted_power / 1000) * workload_hours * (1 - row["Renewable %"]/100) * emission_factor
    return round(carbon_kg,2)

# -------------------------------
# Recommendation Function
# -------------------------------
def recommend(location, servers, workload, budget, scale, model_size):
    filtered = df[df["Location"] == location].copy()
    filtered = filtered[filtered["Cost (₹)"] <= budget]
    if filtered.empty:
        return filtered

    filtered = add_workload_metrics(filtered, workload, model_size)
    filtered["TCO (₹)"] = filtered.apply(lambda r: calculate_tco(r, workload_hours=model_size*10), axis=1)
    filtered["Carbon Emission (kg)"] = filtered.apply(lambda r: calculate_carbon_emission(r, workload_hours=model_size*10), axis=1)

    # Normalize for scoring
    filtered["Performance_norm"] = (filtered["Performance"] - filtered["Performance"].min()) / (filtered["Performance"].max() - filtered["Performance"].min())
    filtered["Cost_norm"] = (filtered["Cost (₹)"].max() - filtered["Cost (₹)"]) / (filtered["Cost (₹)"].max() - filtered["Cost (₹)"].min())
    filtered["Renewable_norm"] = filtered["Renewable %"] / 100

    # Weighted Scores
    weights = {
        "Prototype": {"Performance_norm":0.2, "Cost_norm":0.6, "Renewable_norm":0.2},
        "Large-scale": {"Performance_norm":0.6, "Cost_norm":0.2, "Renewable_norm":0.2}
    }
    score_weights = weights.get(scale, weights["Prototype"])
    filtered["Final Score"] = (
        filtered["Performance_norm"] * score_weights["Performance_norm"] +
        filtered["Cost_norm"] * score_weights["Cost_norm"] +
        filtered["Renewable_norm"] * score_weights["Renewable_norm"]
    )

    return filtered.sort_values(by="Final Score", ascending=False).head(servers)

# -------------------------------
# Streamlit Frontend
# -------------------------------
st.set_page_config(page_title="🌈 Green AI Hardware v5", layout="wide")

# Colorful Gradient + Dynamic CSS
st.markdown("""
<style>
.stApp {
    background: linear-gradient(120deg, #FFDEE9, #B5FFFC, #FFD1DC);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
    font-family: 'Helvetica', sans-serif;
}
@keyframes gradientBG {
    0%{background-position:0% 50%}
    50%{background-position:100% 50%}
    100%{background-position:0% 50%}
}
h1, h2, h3 {
    color: #1b5e20 !important;
    font-weight: 700;
    text-shadow: 1px 1px 2px #fff;
}
.stButton>button {
    background: linear-gradient(90deg,#ff8a65,#ff7043);
    color: white;
    font-weight: bold;
    padding: 10px 25px;
    border-radius: 12px;
}
div.card {
    background: linear-gradient(135deg,#ffe082,#ffd54f);
    padding:25px;
    border-radius:20px;
    box-shadow: 4px 8px 20px rgba(0,0,0,0.25);
    margin-bottom:20px;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Page Title and Description
st.title("🌍️Green AI Hardware Recommendation")
st.markdown("""
A **production-style student prototype** to recommend AI hardware balancing **Performance**, **Cost**, and **Carbon Impact**.  
Built entirely with **public data**, **Python**, and **custom scoring algorithms**.
""")

# -------------------------------
# Inputs Section (Main Page)
col1, col2, col3 = st.columns(3)
with col1:
    location = st.selectbox("📍 Location", df["Location"].unique())
    workload = st.selectbox("💻 Workload Type", ["Training", "Inference", "General AI"])
with col2:
    scale = st.selectbox("⚖️ Scale / Profile", ["Prototype", "Large-scale"])
    budget = st.number_input("💰 Max Budget (₹)", 100000, 10000000, 3000000, step=50000)
with col3:
    servers = st.slider("🔢 Recommendations", 1, 10, 3)
    model_size = st.slider("📈 Model Size", 1, 10, 1)
    workload_hours = st.slider("⏱️ Workload Hours", 1, 100, 10)

st.markdown("---")

# -------------------------------
# Generate Recommendations
if st.button("🔎 Here is your recommendation"):
    recommendations = recommend(location, servers, workload, budget, scale, model_size)

    if recommendations.empty:
        st.warning("⚠️ No hardware found within your budget for this location.")
    else:
        # Tabs for organized sections
        tab1, tab2, tab3 = st.tabs(["📊 Recommendations", "📉 Visual Insights", "📥 Export Data"])

        with tab1:
            st.subheader("📊 Recommended Hardware")
            st.dataframe(recommendations[['Hardware','Category','Performance','Cost (₹)','TCO (₹)','Renewable %','Carbon Emission (kg)','Final Score']], use_container_width=True)
            
            # Best Hardware Card
            best = recommendations.iloc[0]
            st.markdown(f"""
            <div class="card">
                <h2>🌟 Best Hardware: {best['Hardware']}</h2>
                <p>🏷️ Category: {best['Category']}<br>
                   💰 Cost: ₹{best['Cost (₹)']:,}<br>
                   ⚡ Performance: {best['Performance']}<br>
                   🌱 Renewable: {best['Renewable %']}%<br>
                   🌍 CO₂ Emission: {best['Carbon Emission (kg)']} kg<br>
                   💸 Estimated TCO: ₹{best['TCO (₹)']:,}</p>
            </div>
            """, unsafe_allow_html=True)

        with tab2:
            st.subheader("📉 Visual Insights")
            fig1 = px.scatter(
                recommendations,
                x="Performance", y="TCO (₹)",
                size="Renewable %", color="Carbon Emission (kg)",
                hover_name="Hardware", color_continuous_scale="Plasma"
            )
            st.plotly_chart(fig1, use_container_width=True)

            fig2 = px.bar(
                recommendations,
                x="Hardware", y="Renewable %",
                color="Carbon Emission (kg)", color_continuous_scale="Viridis",
                hover_data=['TCO (₹)', 'Performance']
            )
            st.plotly_chart(fig2, use_container_width=True)

            fig3 = px.line(
                recommendations,
                x="Hardware", y="Final Score",
                markers=True
            )
            st.plotly_chart(fig3, use_container_width=True)

        with tab3:
            st.download_button(
                label="📥 Download Recommendations CSV",
                data=recommendations.to_csv(index=False),
                file_name="hardware_recommendations.csv",
                mime="text/csv"
            )
            st.success("✅ Data ready for export!")
