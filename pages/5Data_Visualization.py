import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Chart Builder", layout="wide")

# ---------------------------
# Sidebar – color palettes
# ---------------------------
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

tab1, tab2, tab3 = st.tabs(["1) Bar chart", "2) Pie chart", "3) (Empty)"])

# =========================================================
# TAB 1 — BAR CHART
# =========================================================
with tab1:
    st.title("📊 Bar Chart Builder")

    # 1) size
    st.subheader("1) Data size")
    c1, c2 = st.columns(2)
    with c1:
        n_cols = st.number_input("Number of value columns", 1, 10, 3, 1)
    with c2:
        n_rows = st.number_input("Number of series (rows)", 1, 50, 5, 1)

    value_cols = [f"Value_{i}" for i in range(1, int(n_cols) + 1)]
    sheet_cols = ["Series"] + value_cols

    # 2) worksheet
    st.subheader("2) Worksheet input")
    st.caption("• 첫 열: Series(계열 이름) • 값 열: 숫자")
    df_bar = st.data_editor(
        pd.DataFrame([[""] * len(sheet_cols) for _ in range(int(n_rows))], columns=sheet_cols),
        use_container_width=True,
        hide_index=True,
        num_rows="fixed",
        key="bar_sheet",
    )

    # 3) legend names
    st.subheader("3) Legend names")
    if "bar_legends" not in st.session_state or len(st.session_state["bar_legends"]) != len(value_cols):
        st.session_state["bar_legends"] = [f"Category {i}" for i in range(1, int(n_cols) + 1)]

    df_legends = st.data_editor(
        pd.DataFrame({"Column": value_cols, "Legend label": st.session_state["bar_legends"]}),
        hide_index=True,
        num_rows="fixed",
        disabled=["Column"],
        use_container_width=True,
        key="bar_legend_editor",
    )
    legend_map = dict(zip(value_cols, df_legends["Legend label"]))

    # 4) axis names
    st.subheader("4) Axis names")
    x_label = st.text_input("X-axis label", value="Series")
    y_label = st.text_input("Y-axis label", value="Value")

    # 5) title
    st.subheader("5) Chart title")
    bar_title = st.text_input("Title")

    # 6) generate
    st.subheader("6) Generate")
    if st.button("📈 Generate bar chart"):
        df = df_bar.copy()
        df["Series"] = df["Series"].astype(str).str.strip()

        for c in value_cols:
            df[c] = pd.to_numeric(df[c], errors="coerce")

        df = df.loc[~((df["Series"] == "") & (df[value_cols].isna().all(axis=1)))]

        if df.empty:
            st.warning("No valid data.")
        else:
            long_df = df.melt(
                id_vars="Series",
                value_vars=value_cols,
                var_name="Category",
                value_name="Value",
            ).dropna(subset=["Value"])

            long_df["Category"] = long_df["Category"].map(legend_map)

            fig = px.bar(
                long_df,
                x="Series",
                y="Value",
                color="Category",
                barmode="group",
                color_discrete_sequence=palette,
                title=bar_title if bar_title else None,
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
# TAB 2 — PIE CHART
# =========================================================
with tab2:
    st.title("🥧 Pie Chart Builder")

    # 1) size
    st.subheader("1) Data size")
    n_rows = st.number_input("Number of slices", 1, 30, 5, 1)

    # 2) worksheet
    st.subheader("2) Worksheet input")
    st.caption("• Slice: 조각 이름 • Value: 숫자")
    df_pie = st.data_editor(
        pd.DataFrame([["", ""] for _ in range(int(n_rows))], columns=["Slice", "Value"]),
        use_container_width=True,
        hide_index=True,
        num_rows="fixed",
        key="pie_sheet",
    )

    # 5) title
    st.subheader("5) Chart title")
    pie_title = st.text_input("Title", key="pie_title")

    # 6) generate
    st.subheader("6) Generate")
    if st.button("🥧 Generate pie chart"):
        df = df_pie.copy()
        df["Slice"] = df["Slice"].astype(str).str.strip()
        df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

        df = df.loc[~((df["Slice"] == "") & (df["Value"].isna()))]

        if df.empty:
            st.warning("No valid data.")
        else:
            fig = px.pie(
                df,
                names="Slice",
                values="Value",
                color_discrete_sequence=palette,
                title=pie_title if pie_title else None,
            )
            fig.update_layout(
                height=520,
                title=dict(x=0.5, font=dict(size=24)),
            )
            st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.empty()
