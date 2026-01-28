import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Chart Builder", layout="wide")

# =========================================================
# 0) Safe defaults (KeyError-proof)
#    Always ensure keys exist before reading them.
# =========================================================
st.session_state.setdefault("bar_ncols", 3)
st.session_state.setdefault("bar_nrows", 3)
st.session_state.setdefault(
    "bar_sheet_df",
    pd.DataFrame(
        {
            "Series": ["Agree", "Neutral", "Disagree"],
            "Value_1": [45, 30, 25],
            "Value_2": [50, 25, 25],
            "Value_3": [48, 28, 24],
        }
    ),
)
st.session_state.setdefault(
    "bar_legends_df",
    pd.DataFrame(
        {
            "Column": ["Value_1", "Value_2", "Value_3"],
            "Legend label": ["Category A", "Category B", "Category C"],
        }
    ),
)
st.session_state.setdefault("bar_xlabel", "Response type")
st.session_state.setdefault("bar_ylabel", "Percentage (%)")
st.session_state.setdefault("bar_title", "Student Responses by Category")

st.session_state.setdefault("pie_nrows", 3)
st.session_state.setdefault(
    "pie_sheet_df",
    pd.DataFrame({"Slice": ["Agree", "Neutral", "Disagree"], "Value": [45, 30, 25]}),
)
st.session_state.setdefault("pie_title", "Distribution of Responses")

# =========================================================
# Sidebar – color palettes (this triggers reruns often)
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
palette_name = st.sidebar.selectbox("Color palette", list(PALETTES.keys()), key="palette_name")
palette = PALETTES[palette_name]

tab1, tab2, tab3 = st.tabs(["1) Bar chart", "2) Pie chart", "3) CSV upload"])

# =========================================================
# TAB 1 — BAR CHART (manual)
# =========================================================
with tab1:
    st.title("📊 Bar Chart Builder")

    # 1) Data size
    st.subheader("1) Data size")
    c1, c2 = st.columns(2)
    with c1:
        n_cols = st.number_input(
            "Number of value columns",
            min_value=1,
            max_value=10,
            value=int(st.session_state.get("bar_ncols", 3)),
            step=1,
            key="bar_ncols_widget",
        )
    with c2:
        n_rows = st.number_input(
            "Number of series (rows)",
            min_value=1,
            max_value=50,
            value=int(st.session_state.get("bar_nrows", 3)),
            step=1,
            key="bar_nrows_widget",
        )

    value_cols = [f"Value_{i}" for i in range(1, int(n_cols) + 1)]
    sheet_cols = ["Series"] + value_cols

    # Seed dataframe: if mismatch, rebuild empty
    seed = st.session_state.get("bar_sheet_df").copy()
    if list(seed.columns) != sheet_cols or len(seed) != int(n_rows):
        seed = pd.DataFrame([[""] * len(sheet_cols) for _ in range(int(n_rows))], columns=sheet_cols)

    # 2) Worksheet input
    st.subheader("2) Worksheet input")
    df_bar = st.data_editor(
        seed,
        use_container_width=True,
        hide_index=True,
        num_rows="fixed",
        key="bar_sheet_editor",
    )

    # 3) Legend names
    st.subheader("3) Legend names")
    leg_seed = st.session_state.get("bar_legends_df").copy()
    if "Column" not in leg_seed.columns or "Legend label" not in leg_seed.columns or list(leg_seed["Column"]) != value_cols:
        leg_seed = pd.DataFrame({"Column": value_cols, "Legend label": [f"Category {i}" for i in range(1, len(value_cols) + 1)]})

    df_leg = st.data_editor(
        leg_seed,
        use_container_width=True,
        hide_index=True,
        num_rows="fixed",
        disabled=["Column"],
        key="bar_legend_editor",
    )
    legend_map = dict(zip(df_leg["Column"], df_leg["Legend label"].astype(str)))

    # 4) Axis names
    st.subheader("4) Axis names")
    x_label = st.text_input("X-axis label", st.session_state.get("bar_xlabel", "Series"), key="bar_xlabel_widget")
    y_label = st.text_input("Y-axis label", st.session_state.get("bar_ylabel", "Value"), key="bar_ylabel_widget")

    # 5) Title
    st.subheader("5) Chart title")
    bar_title = st.text_input("Title", st.session_state.get("bar_title", ""), key="bar_title_widget")

    # 6) Generate
    st.subheader("6) Generate")
    if st.button("📈 Generate bar chart", key="bar_generate"):
        df = df_bar.copy()
        df["Series"] = df["Series"].astype(str).replace("nan", "").str.strip()
        for c in value_cols:
            df[c] = pd.to_numeric(df[c], errors="coerce")

        df = df.loc[~((df["Series"] == "") & (df[value_cols].isna().all(axis=1)))].copy()
        if df.empty:
            st.warning("No valid data.")
        else:
            long_df = df.melt(
                id_vars="Series",
                value_vars=value_cols,
                var_name="Category",
                value_name="Value",
            ).dropna(subset=["Value"])

            if long_df.empty:
                st.warning("No numeric values found.")
            else:
                long_df["Category"] = long_df["Category"].map(legend_map)

                fig = px.bar(
                    long_df,
                    x="Series",
                    y="Value",
                    color="Category",
                    barmode="group",
                    color_discrete_sequence=palette,
                    title=bar_title.strip() if bar_title.strip() else None,
                )
                fig.update_layout(
                    height=520,
                    title=dict(x=0.5, xanchor="center", font=dict(size=24)),
                    xaxis_title=x_label.strip() if x_label.strip() else "Series",
                    yaxis_title=y_label.strip() if y_label.strip() else "Value",
                    legend_title_text="",
                    margin=dict(l=20, r=20, t=80, b=20),
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
        "Number of slices",
        min_value=1,
        max_value=30,
        value=int(st.session_state.get("pie_nrows", 3)),
        step=1,
        key="pie_nrows_widget",
    )

    # 2) worksheet
    st.subheader("2) Worksheet input")
    pie_seed = st.session_state.get("pie_sheet_df").copy()
    if list(pie_seed.columns) != ["Slice", "Value"] or len(pie_seed) != int(n_rows):
        pie_seed = pd.DataFrame([["", ""] for _ in range(int(n_rows))], columns=["Slice", "Value"])

    df_pie = st.data_editor(
        pie_seed,
        use_container_width=True,
        hide_index=True,
        num_rows="fixed",
        key="pie_sheet_editor",
    )

    # 5) title
    st.subheader("5) Chart title")
    pie_title = st.text_input("Title", st.session_state.get("pie_title", ""), key="pie_title_widget")

    # 6) generate
    st.subheader("6) Generate")
    if st.button("🥧 Generate pie chart", key="pie_generate"):
        df = df_pie.copy()
        df["Slice"] = df["Slice"].astype(str).replace("nan", "").str.strip()
        df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
        df = df.loc[~((df["Slice"] == "") & (df["Value"].isna()))].copy()

        if df.empty:
            st.warning("No valid data.")
        else:
            fig = px.pie(
                df,
                names="Slice",
                values="Value",
                color_discrete_sequence=palette,
                title=pie_title.strip() if pie_title.strip() else None,
            )
            fig.update_layout(
                height=520,
                title=dict(x=0.5, xanchor="center", font=dict(size=24)),
                margin=dict(l=20, r=20, t=80, b=20),
            )
            st.plotly_chart(fig, use_container_width=True)

# =========================================================
# TAB 3 — CSV upload (same logic as before, stable)
# =========================================================
with tab3:
    st.title("📁 CSV Upload → Chart")
    st.subheader("0) Choose chart type")
    csv_chart_type = st.radio("Chart type", ["Bar chart", "Pie chart"], horizontal=True, key="csv_chart_type")

    st.subheader("1) Upload CSV")
    uploaded = st.file_uploader("Upload a CSV file", type=["csv"], key="csv_uploader")

    if uploaded is None:
        st.info("CSV 업로드 시: 첫 번째 열=라벨, 나머지 숫자열=값으로 인식합니다.")
    else:
        df_raw = pd.read_csv(uploaded)
        if df_raw.empty or df_raw.shape[1] < 2:
            st.warning("CSV는 최소 2개 열이 필요합니다.")
            st.stop()

        st.subheader("2) Preview")
        st.dataframe(df_raw, use_container_width=True, hide_index=True)

        label_col = df_raw.columns[0]
        df = df_raw.copy()
        df[label_col] = df[label_col].astype(str).replace("nan", "").str.strip()

        candidate_value_cols = list(df_raw.columns[1:])
        numeric_cols = []
        for c in candidate_value_cols:
            df[c] = pd.to_numeric(df[c], errors="coerce")
            if df[c].notna().any():
                numeric_cols.append(c)

        if not numeric_cols:
            st.warning("값으로 쓸 수 있는 숫자 열이 없습니다.")
            st.stop()

        st.subheader("5) Chart title")
        csv_title = st.text_input("Title", value="", key="csv_title")

        if csv_chart_type == "Bar chart":
            st.subheader("3) Legend names (from CSV columns)")
            df_leg = st.data_editor(
                pd.DataFrame({"Column": numeric_cols, "Legend label": numeric_cols}),
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                disabled=["Column"],
                key="csv_bar_legend_editor",
            )
            legend_map_csv = dict(zip(df_leg["Column"], df_leg["Legend label"].astype(str)))

            st.subheader("4) Axis names")
            csv_x_label = st.text_input("X-axis label", value=label_col, key="csv_bar_xlabel")
            csv_y_label = st.text_input("Y-axis label", value="Value", key="csv_bar_ylabel")

            st.subheader("6) Generate")
            if st.button("📈 Generate from CSV (Bar)", key="csv_bar_generate"):
                df_use = df.loc[~((df[label_col] == "") & (df[numeric_cols].isna().all(axis=1)))].copy()
                long_df = df_use.melt(
                    id_vars=label_col,
                    value_vars=numeric_cols,
                    var_name="Category",
                    value_name="Value",
                ).dropna(subset=["Value"])

                if long_df.empty:
                    st.warning("숫자 값이 없습니다.")
                else:
                    long_df["Category"] = long_df["Category"].map(legend_map_csv)
                    fig = px.bar(
                        long_df,
                        x=label_col,
                        y="Value",
                        color="Category",
                        barmode="group",
                        color_discrete_sequence=palette,
                        title=csv_title.strip() if csv_title.strip() else None,
                    )
                    fig.update_layout(
                        height=520,
                        title=dict(x=0.5, xanchor="center", font=dict(size=24)),
                        xaxis_title=csv_x_label.strip() if csv_x_label.strip() else label_col,
                        yaxis_title=csv_y_label.strip() if csv_y_label.strip() else "Value",
                        legend_title_text="",
                        margin=dict(l=20, r=20, t=80, b=20),
                    )
                    st.plotly_chart(fig, use_container_width=True)

        else:
            st.subheader("3) Select a value column (Pie)")
            value_col = st.selectbox("Value column", numeric_cols, index=0, key="csv_pie_valuecol")

            st.subheader("6) Generate")
            if st.button("🥧 Generate from CSV (Pie)", key="csv_pie_generate"):
                df_use = df[[label_col, value_col]].dropna(subset=[value_col]).copy()
                df_use = df_use.loc[~(df_use[label_col] == "")]

                if df_use.empty:
                    st.warning("유효한 데이터가 없습니다.")
                else:
                    fig = px.pie(
                        df_use,
                        names=label_col,
                        values=value_col,
                        color_discrete_sequence=palette,
                        title=csv_title.strip() if csv_title.strip() else None,
                    )
                    fig.update_layout(
                        height=520,
                        title=dict(x=0.5, xanchor="center", font=dict(size=24)),
                        margin=dict(l=20, r=20, t=80, b=20),
                    )
                    st.plotly_chart(fig, use_container_width=True)
