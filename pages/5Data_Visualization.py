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

tab1, tab2, tab3 = st.tabs(["1) Bar chart", "2) Pie chart", "3) CSV upload"])


# =========================================================
# TAB 1 — BAR CHART (manual)
# =========================================================
with tab1:
    st.title("📊 Bar Chart Builder (Manual)")

    # 1) cols/rows
    st.subheader("1) Data size")
    c1, c2 = st.columns(2)
    with c1:
        n_cols = st.number_input("Number of value columns", 1, 10, 3, 1, key="bar_ncols")
    with c2:
        n_rows = st.number_input("Number of series (rows)", 1, 50, 5, 1, key="bar_nrows")

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
    legend_map = dict(zip(value_cols, df_legends["Legend label"].astype(str)))

    # 4) x, y axis names
    st.subheader("4) Axis names")
    x_label = st.text_input("X-axis label", value="Series", key="bar_xlabel")
    y_label = st.text_input("Y-axis label", value="Value", key="bar_ylabel")

    # 5) title
    st.subheader("5) Chart title")
    bar_title = st.text_input("Title", value="", key="bar_title")

    # 6) generate
    st.subheader("6) Generate")
    if st.button("📈 Generate bar chart", key="bar_generate"):
        df = df_bar.copy()
        df["Series"] = df["Series"].astype(str).replace("nan", "").str.strip()
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
# TAB 2 — PIE CHART (manual) : 3), 4) 없음
# =========================================================
with tab2:
    st.title("🥧 Pie Chart Builder (Manual)")

    # 1) rows
    st.subheader("1) Data size")
    n_rows = st.number_input("Number of slices", 1, 30, 5, 1, key="pie_nrows")

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
    pie_title = st.text_input("Title", value="", key="pie_title")

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
# TAB 3 — CSV UPLOAD (Bar/Pie 선택 → 자동 차트)
# =========================================================
with tab3:
    st.title("📁 CSV Upload → Chart")

    # 먼저 차트 타입 선택
    st.subheader("0) Choose chart type")
    csv_chart_type = st.radio("Chart type", ["Bar chart", "Pie chart"], horizontal=True, key="csv_chart_type")

    # CSV 업로드
    st.subheader("1) Upload CSV")
    uploaded = st.file_uploader("Upload a CSV file", type=["csv"], key="csv_uploader")

    if uploaded is None:
        st.info("CSV 파일을 업로드하면, 첫 번째 열은 라벨(Series/Slice)로, 나머지 숫자 열은 값으로 인식합니다.")
    else:
        try:
            df_raw = pd.read_csv(uploaded)
        except Exception as e:
            st.error(f"CSV 읽기 실패: {e}")
            st.stop()

        if df_raw.empty or df_raw.shape[1] < 2:
            st.warning("CSV는 최소 2개 이상의 열이 필요합니다. (라벨 1열 + 값 1열 이상)")
            st.stop()

        st.subheader("2) Preview")
        st.dataframe(df_raw, use_container_width=True, hide_index=True)

        # 자동 인식: 첫 열 = 라벨
        label_col = df_raw.columns[0]
        candidate_value_cols = list(df_raw.columns[1:])

        # 숫자열만 추려보기 (non-numeric은 NaN 처리 후 drop 가능)
        df = df_raw.copy()
        df[label_col] = df[label_col].astype(str).replace("nan", "").str.strip()

        numeric_cols = []
        for c in candidate_value_cols:
            df[c] = pd.to_numeric(df[c], errors="coerce")
            if df[c].notna().any():
                numeric_cols.append(c)

        if not numeric_cols:
            st.warning("값으로 쓸 수 있는 숫자 열이 없습니다. (두 번째 열 이후에 숫자 데이터가 있어야 합니다.)")
            st.stop()

        # 제목 입력 (공통)
        st.subheader("5) Chart title")
        csv_title = st.text_input("Title", value="", key="csv_title")

        if csv_chart_type == "Bar chart":
            # Bar: legend 이름(=값 열 이름) + 축 이름
            st.subheader("3) Legend names (from CSV columns)")
            if "csv_bar_legends" not in st.session_state or len(st.session_state["csv_bar_legends"]) != len(numeric_cols):
                st.session_state["csv_bar_legends"] = numeric_cols[:]  # 기본: 컬럼명 그대로

            df_csv_leg = st.data_editor(
                pd.DataFrame({"Column": numeric_cols, "Legend label": st.session_state["csv_bar_legends"]}),
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                disabled=["Column"],
                key="csv_bar_legend_editor",
            )
            legend_map_csv = dict(zip(numeric_cols, df_csv_leg["Legend label"].astype(str)))

            st.subheader("4) Axis names")
            csv_x_label = st.text_input("X-axis label", value=label_col, key="csv_bar_xlabel")
            csv_y_label = st.text_input("Y-axis label", value="Value", key="csv_bar_ylabel")

            st.subheader("6) Generate")
            if st.button("📈 Generate from CSV (Bar)", key="csv_bar_generate"):
                # 빈 라벨 + 전부 NaN인 행 제거
                df_use = df.loc[~((df[label_col] == "") & (df[numeric_cols].isna().all(axis=1)))].copy()
                if df_use.empty:
                    st.warning("유효한 데이터가 없습니다.")
                else:
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
            # Pie: 값 열 선택만 있으면 충분
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
