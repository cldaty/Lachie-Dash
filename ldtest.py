import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Intraoperative Training Dashboard",
    layout="wide"
)

st.markdown("""
<style>

.stApp {
    background-color: #0a0f1c;
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #050814;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span,
    color: white !important;
}

[data-baseweb="select"] {
    background-color: #0a0f1c !important;
}

[data-baseweb="select"] > div {
    background-color: #0a0f1c !important;
    color: white !important;
}

div[data-baseweb="popover"] {
    background-color: #0a0f1c !important;
    border: 1px solid cyan !important;
}

[data-testid="stFileUploader"] {
    background-color: #0b1022 !important;
    border: 1px solid rgba(0, 255, 255, 0.3) !important;
    border-radius: 12px;
    padding: 10px;
}

/* The upload dropzone text area */
[data-testid="stFileUploaderDropzone"] {
    background-color: #0a0f1c !important;
    color: white !important;
}

/* The "Browse files" button */
[data-testid="stFileUploader"] button {
    background-color: #111a33 !important;
    color: cyan !important;
    border: 1px solid cyan !important;
}

[data-testid="stMetric"] {
    background-color: rgba(0,255,255,0.1);
    border: 1px solid cyan;
    border-radius: 15px;
    padding: 15px;
    box-shadow: 0px 0px 10px cyan;
}

[data-testid="stMetric"] label {
    color: white !important;
    opacity: 1 !important;
}

[data-testid="stMetric"] div {
    color: white !important;
}

h1 {
    color: cyan;
    text-align: center;
}

h2 {
    color: white !important;
    text-align: center;
}

div[data-testid="stSelectbox"] label {
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

st.sidebar.header("Upload File")

uploaded_file = st.sidebar.file_uploader(
    "Upload a CSV file",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image("SaberLabLogoTransparentWhite.png", width=600)

st.title("Intraoperative Training Dashboard")

st.sidebar.header("Filters")

participant = st.sidebar.selectbox(
    "Select Trainee",
    sorted(df["participant"].unique()),
    key="participant_filter"
)

filtered_df = df[
    (df["participant"] == participant)
]

if filtered_df.empty:
    st.warning("No data for selected filters")
    st.stop()

participant_df =df[df["participant"] == participant]

total_procedures =len(participant_df)
appendix_count = (participant_df["procedure"] == "appendix").sum()
gallbladder_count = (participant_df["procedure"] == "gallbladder").sum()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Procedures", total_procedures)

with col2:
    st.metric("Appendix Cases", appendix_count)

with col3:
    st.metric("Gallbladder Cases", gallbladder_count)

procedure = st.selectbox(
    "Procedure Type",
    sorted(df["procedure"].unique()),
    key="procedure_filter"
)

filtered_df = df[
    (df["procedure"] == procedure)
]

if filtered_df.empty:
    st.warning("No data for selected filters")
    st.stop()

col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    st.header(f"Procedure: {procedure}")

col1, col2 = st.columns(2)

with col1:
    st.metric(
    "Coagulating Actions",
    f"{filtered_df['coagulating.actions'].mean():.2f}"
)

with col2:
    st.metric(
    "Dissecting Actions",
    f"{filtered_df['dissecting.actions'].mean():.2f}"
)

plot_df = df[df["procedure"] == procedure].copy()

plot_df["highlight"] = (
    plot_df["participant"] == participant
)

plot_df = plot_df.sort_values("video")

fig = px.scatter(
   plot_df,
    x="video",
    y="coagulating.actions", 
    title=f"Coagulating Actions",
    color="highlight",
    color_discrete_map={
        False: "lightgray",
        True: "hotpink"
    },
    size="severity.grade",
    hover_data=["participant", "procedure"]
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0a0f1c",
    plot_bgcolor="#0a0f1c",
    font=dict(color="cyan"),   # axes, ticks, legend
    title=dict(
        text="Coagulating Actions",
        font=dict(color="white")
    )
)

st.plotly_chart(fig, use_container_width=True)

fig = px.scatter(
    plot_df,
    x="video",
    y="dissecting.actions", 
    title=f"Dissecting Actions",
    color="highlight",
    color_discrete_map={
        False: "lightgray",
        True: "hotpink"
    },
    size="severity.grade",
    hover_data=["participant", "procedure"]
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0a0f1c",
    plot_bgcolor="#0a0f1c",
    font=dict(color="cyan"),   # axes, ticks, legend
    title=dict(
        text="Dissecting Actions",
        font=dict(color="white")
    )
)

st.plotly_chart(fig, use_container_width=True)

fig = px.scatter(
   plot_df,
    x="video",
    y="dexterity.index", 
    title=f"Dexterity Index",
    color="highlight",
    color_discrete_map={
        False: "lightgray",
        True: "hotpink"
    },
    size="severity.grade",
    hover_data=["participant", "procedure"]
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0a0f1c",
    plot_bgcolor="#0a0f1c",
    font=dict(color="cyan"),   # axes, ticks, legend
    title=dict(
        text="Dexterity Index",
        font=dict(color="white")
    )
)

st.plotly_chart(fig, use_container_width=True)









