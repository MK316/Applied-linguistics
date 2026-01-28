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
palette_name = st.sidebar.selectbox("Color palette", list(PALETTES.keys()))
palette = PALETTES[palette_name]

tab1, tab2, tab3 = st.tabs(["1) Bar chart", "2) Pie chart", "3) (Empty)"])


# =========================================================
# TAB 1 — BAR CHART
# =========================================================
with tab1:
    st.title("📊 Bar Chart Builder")

    # 1) cols/rows
    st.subheader("1) Data size")
    c1, c2 = st.columns(2)
    with c1:
        n_value_cols = st.number_input("Number of value columns", 1, 10, 3, 1, key="bar_ncols")
    with c2:
        n_rows = st.number_input("Number of series (rows)", 1, 50, 5, 1, key="bar_nrows")

    internal_value_cols = [f"Value_{i}" for i in range(1, int(n_value_cols) + 1)]
    sheet_cols = ["Series"] + internal_value_cols

    # 2) worksheet
    st.subheader("2) Worksheet input")
    st.caption("• 첫 열은 Series(계열 이름) • 값 열은 숫자")
    df_bar_input = st.data_editor(
        pd.DataFrame([[""] * len(sheet_cols) for _ in range(int(n_rows))], columns=sheet_cols),
        use_container_width=True,
        hide_index=True,
        num_rows="fixed",
        key="bar_sheet",
    )

    # 3) legend names (rename Value columns)
    st.subheader("3) Legend names")
    st.caption("Value 컬럼의 표시 이름(legend)을 입력하세요.")
    if "bar_value_col_labels" not in st.session_state or len(st.session_state["bar_value_col_labels"]) != len(internal_value_cols):
        st.session_state["bar_value_col_labels"] = [f"Category {i}" for i in range(1, int(n_value_cols) + 1)]

    df_bar_legend = st.data_editor(
        pd.DataFrame({
            "Column": internal_value_cols,
            "Legend label": st.session_state["bar_value_col_labels"],
        }),
        use_container_width=True,
        hide_index=True,
        num_rows="fixed",
        disabled=["Column"],
        key="bar_legend_editor",
    )
    st.session_state["bar_value_col_labels"] = df_bar_legend["Legend label"].astype(str).tolist()
    bar_col_label_map = dict(zip(internal_value_cols, st.session_state["bar_value_col_labels"]))

    # 4) x/y axis names
    st.subheader("4) Axis names")
    x_axis_label = st.text_input("X-axis label", value="Series", key="bar_xlabel")
    y_axis_label = st.text_input("Y-axis label", value="Value", key="bar_ylabel")

    # 5) title
    st.subheader("5) Chart title")
    bar_title = st.text_input("Title", value="", key="bar_title")

    # 6) generate button
    st.subheader("6) Generate")
    bar_generate = st.button("📈 Generate bar chart", key="bar_generate")

    if bar_generate:
        df = df_bar_input.copy()
        df["Series"] = df["Series"].astype(str).replace("nan", "").str.strip()

        for c in internal_value_cols:
            df[c] = pd.to_numeric(df[c], errors="coerce")

        df = df.loc[~((df["Series"] == "") & (df[internal_value_cols].isna().all(axis=1)))]

        if df.empty:
            st.warning("No valid data. Please enter series names and numeric values.")
        else:
            long_df = df.melt(
                id_vars="Series",
                value_vars=internal_value_cols,
                var_name="Category",
                value_name="Value",
            ).dropna(subset=["Value"])

            if long_df.empty:
                st.warning("No numeric values found.")
            else:
                long_df["Category"] = long_df["Category"].map(bar_col_label_map)

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
                    xaxis_title=x_axis_label.strip() if x_axis_label.strip() else "Series",
                    yaxis_title=y_axis_label.strip() if y_axis_label.strip() else "Value",
                    legend_title_text="",
                    margin=dict(l=20, r=20, t=80, b=20),
                )
                st.plotly_chart(fig, use_container_width=True)


# =========================================================
# TAB 2 — PIE CHART
# =========================================================
with tab2:
    st.title("🥧 Pie Chart Builder")

    # 1) cols/rows
    # pie는 "조각"이 필요하므로: rows=조각 개수, cols는 사실상 1개(Value)면 충분
    st.subheader("1) Data size")
    c1, c2 = st.columns(2)
    with c1:
        n_slices = st.number_input("Number of slices (rows)", 1, 30, 5, 1, key="pie_nrows")
    with c2:
        st.info("Pie chart uses one numeric column (Value).")

    # 2) worksheet (Slice + Value)
    st.subheader("2) Worksheet input")
    st.caption("• 첫 열은 Slice(조각 이름) • Value는 숫자")
    df_pie_default = pd.DataFrame([["", ""] for _ in range(int(n_slices))], columns=["Slice", "Value"])
    df_pie_input = st.data_editor(
        df_pie_default,
        use_container_width=True,
        hide_index=True,
        num_rows="fixed",
        key="pie_sheet",
    )

    # 3) legend names (pie는 legend가 Slice 이름이므로, 여기서는 'Slice 라벨 정리' 단계)
    st.subheader("3) Legend (slice labels)")
    st.caption("필요하면 Slice 이름을 여기에서 일괄 수정하세요. (아래 표가 기준으로 적용됩니다.)")

    # slice labels editor: 사용자가 slice 이름만 편집하도록 제공
    # (워크시트에 입력한 Slice를 가져와서 편집 가능하게)
    slice_series = df_pie_input["Slice"].astype(str).fillna("").tolist()
    df_slice_editor = st.data_editor(
        pd.DataFrame({"Slice label": slice_series}),
        use_container_width=True,
        hide_index=True,
        num_rows="fixed",
        key="pie_slice_editor",
    )

    # 4) x, y 축이름 (pie에 맞게 label/value 이름으로 사용)
    st.subheader("4) Names (label / value)")
    pie_label_name = st.text_input("Label name (acts like X)", value="Slice", key="pie_xlabel")
    pie_value_name = st.text_input("Value name (acts like Y)", value="Value", key="pie_ylabel")

    # 5) title
    st.subheader("5) Chart title")
    pie_title = st.text_input("Title", value="", key="pie_title")

    # 6) generate button
    st.subheader("6) Generate")
    pie_generate = st.button("🥧 Generate pie chart", key="pie_generate")

    if pie_generate:
        df = df_pie_input.copy()

        # apply edited slice labels
        df["Slice"] = df_slice_editor["Slice label"].astype(str).replace("nan", "").str.strip()
        df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

        df = df.loc[~((df["Slice"] == "") & (df["Value"].isna()))]

        if df.empty:
            st.warning("No valid data. Please enter slice labels and numeric values.")
        else:
            # Rename columns for display (optional)
            display_label = pie_label_name.strip() if pie_label_name.strip() else "Slice"
            display_value = pie_value_name.strip() if pie_value_name.strip() else "Value"

            df_plot = df.rename(columns={"Slice": display_label, "Value": display_value}).dropna(subset=[display_value])

            if df_plot.empty:
                st.warning("No numeric values found.")
            else:
                fig = px.pie(
                    df_plot,
                    names=display_label,
                    values=display_value,
                    color_discrete_sequence=palette,
                    title=pie_title.strip() if pie_title.strip() else None,
                )
                fig.update_layout(
                    height=520,
                    title=dict(x=0.5, xanchor="center", font=dict(size=24)),
                    margin=dict(l=20, r=20, t=80, b=20),
                )
                st.plotly_chart(fig, use_container_width=True)


with tab3:
    st.empty()
