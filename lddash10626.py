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

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] p {
    color: white !important;
}

[data-baseweb="select"] > div {
    background-color: #0a0f1c !important;
    color: white !important;
}

[data-baseweb="select"] span {
    color: white !important;
}

div[data-baseweb="menu"] {
    background-color: #0a0f1c !important;
    border: 1px solid cyan !important;
}

div[data-baseweb="menu"] ul {
    background-color: #0a0f1c !important;
}

div[data-baseweb="menu"] li {
    background-color: #0a0f1c !important;
    color: white !important;
}

div[data-baseweb="menu"] li:hover {
    background-color: #111a33 !important;
    color: cyan !important;
}

[data-testid="stFileUploader"] {
    background-color: #0b1022 !important;
    border: 1px solid rgba(0, 255, 255, 0.3) !important;
    border-radius: 12px;
    padding: 10px;
}

[data-testid="stFileUploaderDropzone"] {
    background-color: #0a0f1c !important;
    color: white !important;
}

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

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image("SaberLabLogoTransparentWhite.png", width=600)

st.title("Intraoperative Training Dashboard")

st.sidebar.header("Upload File")

uploaded_file = st.sidebar.file_uploader(
    "Upload a CSV file",
    type=["csv"]
)

if uploaded_file is None:
    st.markdown("""
    <div style="
        background-color: rgba(0,255,255,0.1);
        border: 1px solid cyan;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: cyan;
        font-size: 18px;
        box-shadow: 0px 0px 10px cyan;
        margin-top: 20px;
    ">
        Please upload your CSV file to begin
    </div>
    """, unsafe_allow_html=True)

    st.stop()

df = pd.read_csv(uploaded_file)


st.sidebar.header("Filters")

participant = st.sidebar.selectbox(
    "Select Trainee:",
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

total_Procedures =len(participant_df)
Appendix_count = (participant_df["Procedure"] == "Appendix").sum()
Gallbladder_count = (participant_df["Procedure"] == "Gallbladder").sum()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Procedures", total_Procedures)

with col2:
    st.metric("Appendix Cases", Appendix_count)

with col3:
    st.metric("Gallbladder Cases", Gallbladder_count)

Procedure = st.selectbox(
    "Select Procedure Type:",
    sorted(participant_df["Procedure"].unique()),
    key="Procedure_filter"
)

participant_procedure_df = df[
    (df["participant"] == participant) &
    (df["Procedure"] == Procedure)
]

if participant_procedure_df.empty:
    st.warning("No data for selected filters")
    st.stop()

col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    st.header(f"Procedure: {Procedure}")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
    "Number of Coagulating Actions",
    f"{participant_procedure_df['Coagulating Actions'].mean():.2f}"
)

with col2:
    st.metric(
    "Number of Dissecting Actions",
    f"{participant_procedure_df['Dissecting Actions'].mean():.2f}"
)

with col3:
    st.metric(
    "Dexterity Index",
    f"{participant_procedure_df['Dexterity Index'].mean():.2f}"
)

plot_df = df[df["Procedure"] == Procedure].copy()

plot_df["Participant Group"] = plot_df["participant"].apply(
    lambda x: "Selected Participant"
    if x == participant
    else "All Participants"
)

color="Participant Group",
color_discrete_map={
    "All Participants": "lightgray",
    "Selected Participant": "hotpink"
}

plot_df = plot_df.sort_values("video")

symbol_map = {
    "Uncomplicated": "circle",
    "Complicated": "triangle-up"
}

st.markdown("### Graph Legend")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
<span style="color:hotpink;">■</span> Selected Participant

<span style="color:lightgray;">■</span> All Participants
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
● Uncomplicated Case

▲ Complicated Case
""")

fig = px.scatter(
   plot_df,
    x="video",
    y="Coagulating Actions", 
    title=f"Coagulating Actions",
    color="Participant Group",
    color_discrete_map={
        "All Participants": "lightgray",
        "Selected Participant": "hotpink"
    },
    symbol="Severity category",
    symbol_map=symbol_map,
    hover_data=["participant", "Procedure"]
)

fig.for_each_trace(
    lambda trace: trace.update(
        marker=dict(
            size=16 if "Selected Participant" in trace.name else 8
        )
    )
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0a0f1c",
    plot_bgcolor="#0a0f1c",
    font=dict(color="cyan"),   # axes, ticks, legend
    title=dict(
        text="Coagulating Actions",
        font=dict(color="white")
    ),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

fig = px.scatter(
    plot_df,
    x="video",
    y="Dissecting Actions", 
    title=f"Dissecting Actions",
    color="Participant Group",
    color_discrete_map={
        "All Participants": "lightgray",
        "Selected Participant": "hotpink"
    },
    symbol="Severity category",
    symbol_map=symbol_map,
    hover_data=["participant", "Procedure"]
)

fig.for_each_trace(
    lambda trace: trace.update(
        marker=dict(
            size=16 if "Selected Participant" in trace.name else 8
        )
    )
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0a0f1c",
    plot_bgcolor="#0a0f1c",
    font=dict(color="cyan"),   # axes, ticks, legend
    title=dict(
        text="Dissecting Actions",
        font=dict(color="white")
    ),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

fig = px.scatter(
   plot_df,
    x="video",
    y="Dexterity Index", 
    title=f"Dexterity Index",
    color="Participant Group",
    color_discrete_map={
        "All Participants": "lightgray",
        "Selected Participant": "hotpink"
    },
    symbol="Severity category",
    symbol_map=symbol_map,
    hover_data=["participant", "Procedure"]
)

fig.for_each_trace(
    lambda trace: trace.update(
        marker=dict(
            size=16 if "Selected Participant" in trace.name else 8
        )
    )
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0a0f1c",
    plot_bgcolor="#0a0f1c",
    font=dict(color="cyan"),   # axes, ticks, legend
    title=dict(
        text="Dexterity Index",
        font=dict(color="white")
    ),
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)









