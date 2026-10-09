import streamlit as st
import plotly.graph_objects as go

# --- Clinical Knowledge Base ---
DRUG_DATABASE = {
    "Simvastatin / Lovastatin (Short-Acting Statins)": {
        "class": "HMG-CoA Reductase Inhibitor",
        "optimal_window": "20:00 - 23:00 (Bedtime)",
        "optimal_hour_start": 20,
        "optimal_hour_end": 23,
        "rationale": "Hepatic HMG-CoA reductase activity peaks physiologically between midnight and 04:00. Short half-life statins must be present at peak target enzyme activation.",
        "consequence": "Morning administration results in 30–35% reduced LDL-C lowering efficacy compared to evening dosing.",
        "evidence": "European Heart Journal / ACC/AHA Dyslipidemia Chronotherapy Guidelines",
        "cycle_type": "Hepatic Cholesterol Synthesis (Nocturnal Peak)"
    },
    "Ramipril / Telmisartan (ACEi / ARB Antihypertensives)": {
        "class": "RAAS Inhibitor",
        "optimal_window": "21:00 - 23:00 (Bedtime)",
        "optimal_hour_start": 21,
        "optimal_hour_end": 23,
        "rationale": "Blunts nocturnal non-dipping blood pressure profiles. Normalizing the nocturnal dip (<10% dip is an independent predictor of stroke and cardiovascular mortality) provides target organ protection.",
        "consequence": "Morning-only administration fails to blunt the dangerous early-morning blood pressure surge (06:00–09:00).",
        "evidence": "Hygia Chronotherapy Trial / MAPEC Trial",
        "cycle_type": "Nocturnal Blood Pressure / Sympathetic Dip"
    },
    "Prednisolone / Hydrocortisone (Systemic Glucocorticoids)": {
        "class": "Corticosteroid",
        "optimal_window": "07:00 - 08:30 (Morning with Breakfast)",
        "optimal_hour_start": 7,
        "optimal_hour_end": 9,
        "rationale": "Synchronizes with the endogenous ACTH/cortisol circadian surge (diurnal acrophase at ~08:00), minimizing hypothalamic-pituitary-adrenal (HPA) axis suppression.",
        "consequence": "Evening administration disrupts the circadian rhythm, causes insomnia, and suppresses endogenous ACTH synthesis.",
        "evidence": "Endocrine Society Guidelines on Adrenal Insufficiency & Glucocorticoid Stewardship",
        "cycle_type": "Hypothalamic-Pituitary-Adrenal (HPA) Diurnal Surge"
    },
    "Levothyroxine": {
        "class": "Thyroid Hormone Replacement",
        "optimal_window": "06:00 - 07:00 (Fasting, 60m before breakfast) OR 22:00 (4h post-dinner)",
        "optimal_hour_start": 6,
        "optimal_hour_end": 7,
        "rationale": "Absorption is severely impaired by dietary calcium, dietary fiber, coffee, and postprandial gastric pH alterations.",
        "consequence": "Coadministration with breakfast reduces intestinal bioavailability by up to 40%, producing erratic TSH fluctuations.",
        "evidence": "American Thyroid Association (ATA) Hypothyroidism Guidelines",
        "cycle_type": "Intestinal Bioavailability & Basal Metabolic Phase"
    }
}

st.set_page_config(
    page_title="ChronoRx | Circadian Pharmacodynamics Engine",
    page_icon="⏰",
    layout="wide"
)

st.title("⏰ ChronoRx: Circadian Pharmacodynamics & Administration Engine")
st.caption("Aligns drug delivery with endogenous circadian biological rhythms to optimize clinical efficacy and prevent timing-induced toxicities.")

st.divider()

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.subheader("1. Medication & Schedule Audit")
    
    selected_drug = st.selectbox(
        "Select Pharmacological Agent:",
        list(DRUG_DATABASE.keys())
    )
    
    current_time = st.slider(
        "Current Scheduled Administration Time (24h Clock):",
        min_value=0,
        max_value=23,
        value=8,
        format="%02d:00"
    )

    drug_info = DRUG_DATABASE[selected_drug]
    is_optimal = drug_info["optimal_hour_start"] <= current_time <= drug_info["optimal_hour_end"]

    st.markdown("#### Clinical Alignment Status")
    if is_optimal:
        st.success(f"✅ **Optimal Alignment:** {current_time:02d}:00 falls within the recommended biological window ({drug_info['optimal_window']}).")
    else:
        st.error(f"⚠️ **Circadian Mismatch:** {current_time:02d}:00 sits outside the target therapeutic window ({drug_info['optimal_window']}).")
        st.warning(f"**Clinical Consequence:** {drug_info['consequence']}")

    with st.expander("Biological Mechanism & Pharmacodynamic Rationale", expanded=True):
        st.markdown(f"**Target System:** {drug_info['cycle_type']}")
        st.markdown(f"**Mechanism:** {drug_info['rationale']}")
        st.caption(f"**Evidence Base:** {drug_info['evidence']}")

with col_right:
    st.subheader("2. Circadian Target Rhythm vs Administration")
    
    hours = list(range(24))
    
    if "Cholesterol" in drug_info["cycle_type"]:
        activity = [85, 95, 100, 95, 80, 50, 30, 20, 15, 15, 20, 25, 30, 35, 40, 45, 55, 65, 75, 85, 90, 95, 95, 90]
        curve_label = "Hepatic HMG-CoA Reductase Activity (%)"
    elif "Corticosteroid" in drug_info["cycle_type"]:
        activity = [15, 10, 10, 15, 25, 45, 75, 95, 100, 85, 65, 50, 40, 35, 30, 25, 20, 20, 18, 15, 15, 15, 15, 12]
        curve_label = "Endogenous Cortisol Secretion (%)"
    elif "Blood Pressure" in drug_info["cycle_type"]:
        activity = [40, 35, 30, 30, 45, 70, 90, 95, 85, 75, 70, 65, 65, 60, 60, 65, 70, 75, 80, 85, 85, 70, 55, 45]
        curve_label = "Cardiovascular Event Vulnerability (%)"
    else:
        activity = [90, 85, 80, 80, 80, 95, 100, 60, 40, 35, 40, 60, 40, 35, 40, 50, 45, 40, 35, 40, 80, 90, 95, 90]
        curve_label = "Fasting Gastrointestinal Absorption Efficiency (%)"

    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=hours,
        y=activity,
        mode="lines+markers",
        name=curve_label,
        line=dict(color="#38BDF8", width=3)
    ))
    
    fig.add_vrect(
        x0=drug_info["optimal_hour_start"],
        x1=drug_info["optimal_hour_end"],
        fillcolor="rgba(34, 197, 94, 0.25)",
        layer="below",
        line_width=0,
        annotation_text="Optimal Target Window",
        annotation_position="top left"
    )
    
    fig.add_vline(
        x=current_time,
        line_width=3,
        line_dash="dash",
        line_color="#EF4444" if not is_optimal else "#22C55E",
        annotation_text=f"Selected ({current_time:02d}:00)",
        annotation_position="bottom right"
    )

    fig.update_layout(
        xaxis=dict(title="Hour of Day (24h Clock)", tickmode="linear", tick0=0, dtick=2),
        yaxis=dict(title="Relative Biological Activity (%)", range=[0, 110]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=30, b=20),
        height=380,
        template="plotly_dark"
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- Institutional Order Output ---
st.subheader("📋 Clinician & Nursing Administration Order")
c_sched1, c_sched2 = st.columns(2)

with c_sched1:
    st.info(f"**Recommended Order:** Administer at **{drug_info['optimal_window']}** to maximize target synchrony.")
with c_sched2:
    st.code(
        f"// EHR Administration Token\n"
        f"Medication: {selected_drug.split(' (')[0]}\n"
        f"Administration_Window: {drug_info['optimal_window']}\n"
        f"Circadian_Target: {drug_info['cycle_type']}\n"
        f"Audit_Status: {'SYNCHRONIZED' if is_optimal else 'CIRCADIAN_MISMATCH_WARNING'}",
        language="c"
    )