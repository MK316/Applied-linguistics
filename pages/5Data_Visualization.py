import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Chart Builder", layout="wide")

# =========================================================
# 0. Initialize sample data (run once)
# =========================================================
if "initialized" not in st.session_state:
    # --- Bar chart sample ---
    st.session_state["bar_ncols"] = 3
    st.session_state["bar_nrows"] = 3
    st.session_state["bar_sheet"] = pd.DataFrame(
        {
            "Series": ["Agree", "Neutral", "Disagree"],
            "Value_1": [45, 30, 25],
            "Value_2": [50, 25, 25],
            "Value_3": [48, 28, 24],
        }
    )
    st.session_state["bar_legends"] = ["Category A", "Category B", "Category C"]
    st.session_state["bar_xlabel"] = "Response type"
    st.session_state["bar_ylabel"] = "Percentage (%)"
    st.session_state["bar_title"] = "Student Responses by Category"

    # --- Pie chart sample ---
    st.session_state["pie_nrows"] = 3
    st.session_state["pie_sheet"] = pd.DataFrame(
        {
            "Slice": ["Agree", "Neutral", "Disagree"],
            "Value": [45, 30, 25],
        }
    )
    st.session_state["pie_title"] = "Distribution of Responses"

    st.session_state["initialized"] = True


# =========================================================
# Sidebar – color palettes
# =========================================================
st.sidebar.header("🎨 Color options")
PALETTES = {
    "Pastel": px.colors.qualitative.Pastel,
    "Bold": px.colors.qualitative.Bold,
    "Set2": px.colors.qualitative.Set2,
    "Dark2": px.colors.qualitative.Dark2,
    "Vivid": px.colors.qualitative.Vivid,
    "Safe": px.colors.qualitative.Safe,
    "Prism": px.colors.qualitative.Prism,
    "Alphabet": px.colors.qualitative.Alphabet,
}
palette = PALETTES[st.sidebar.selectbox("Color palette", PALETTES.keys())]

tab1, tab2, tab3 = st.tabs(["1) Bar chart", "2) Pie chart", "3) CSV upload"])

# =========================================================
# TAB 1 — BAR CHART (manual)
# =========================================================
with tab1:
    st.title("📊 Bar Chart Builder")

    # 1) size
    st.subheader("1) Data size")
    c1, c2 = st.columns(2)
    with c1:
        n_cols = st.number_input(
            "Number of value columns", 1, 10, st.session_state["bar_ncols"], 1, key="bar_ncols"
        )
    with c2:
        n_rows = st.number_input(
            "Number of series (rows)", 1, 50, st.session_state["bar_nrows"], 1, key="bar_nrows"
        )

    value_cols = [f"Value_{i}" for i in range(1, n_cols + 1)]

    # 2) worksheet
    st.subheader("2) Worksheet input")
    df_bar = st.data_editor(
        st.session_state["bar_sheet"],
        use_container_width=True,
        hide_index=True,
        num_rows="fixed",
        key="bar_sheet",
    )

    # 3) legend names
    st.subheader("3) Legend names")
    df_leg = st.data_editor(
        pd.DataFrame({"Legend label": st.session_state["bar_legends"]}),
        use_container_width=True,
        hide_index=True,
        num_rows="fixed",
        key="bar_legends",
    )
    legend_map = dict(zip(value_cols, df_leg["Legend label"]))

    # 4) axis names
    st.subheader("4) Axis names")
    x_label = st.text_input("X-axis label", st.session_state["bar_xlabel"], key="bar_xlabel")
    y_label = st.text_input("Y-axis label", st.session_state["bar_ylabel"], key="bar_ylabel")

    # 5) title
    st.subheader("5) Chart title")
    bar_title = st.text_input("Title", st.session_state["bar_title"], key="bar_title")

    # 6) generate
    st.subheader("6) Generate")
    if st.button("📈 Generate bar chart"):
        df = df_bar.copy()
        df["Series"] = df["Series"].astype(str).str.strip()
        for c in value_cols:
            df[c] = pd.to_numeric(df[c], errors="coerce")

        long_df = df.melt(
            id_vars="Series", value_vars=value_cols, var_name="Category", value_name="Value"
        ).dropna()

        long_df["Category"] = long_df["Category"].map(legend_map)

        fig = px.bar(
            long_df,
            x="Series",
            y="Value",
            color="Category",
            barmode="group",
            color_discrete_sequence=palette,
            title=bar_title,
        )
        fig.update_layout(
            height=520,
            title=dict(x=0.5, font=dict(size=24)),
            xaxis_title=x_label,
            yaxis_title=y_label,
            legend_title_text="",
        )
        st.plotly_chart(fig, use_container_width=True)

# =========================================================
# TAB 2 — PIE CHART (manual)
# =========================================================
with tab2:
    st.title("🥧 Pie Chart Builder")

    # 1) size
    st.subheader("1) Data size")
    n_rows = st.number_input(
        "Number of slices", 1, 30, st.session_state["pie_nrows"], 1, key="pie_nrows"
    )

    # 2) worksheet
    st.subheader("2) Worksheet input")
    df_pie = st.data_editor(
        st.session_state["pie_sheet"],
        use_container_width=True,
        hide_index=True,
        num_rows="fixed",
        key="pie_sheet",
    )

    # 5) title
    st.subheader("5) Chart title")
    pie_title = st.text_input("Title", st.session_state["pie_title"], key="pie_title")

    # 6) generate
    st.subheader("6) Generate")
    if st.button("🥧 Generate pie chart"):
        df = df_pie.copy()
        df["Slice"] = df["Slice"].astype(str).str.strip()
        df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

        fig = px.pie(
            df,
            names="Slice",
            values="Value",
            color_discrete_sequence=palette,
            title=pie_title,
        )
        fig.update_layout(
            height=520,
            title=dict(x=0.5, font=dict(size=24)),
        )
        st.plotly_chart(fig, use_container_width=True)

# =========================================================
# TAB 3 — CSV upload (기존 코드 그대로 사용)
# =========================================================
with tab3:
    st.info("CSV 업로드 탭은 기존 구현을 그대로 사용하면 됩니다.")
