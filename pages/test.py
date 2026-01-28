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

# ---------------------------
# Tabs
# ---------------------------
tab1, tab2, tab3 = st.tabs(["1) Chart Builder", "2) (Empty)", "3) (Empty)"])

with tab1:
    st.title("📊 Chart Builder")

    # Title textbox (separate from worksheet)
    st.subheader("0) Chart title")
    chart_title = st.text_input("Chart title", value="")

    # 1) Ask rows/cols
    st.subheader("1) Set table size")
    c1, c2 = st.columns(2)
    with c1:
        n_value_cols = st.number_input("Number of value columns", min_value=1, max_value=10, value=3, step=1)
    with c2:
        n_rows = st.number_input("Number of series (rows)", min_value=1, max_value=50, value=5, step=1)

    # 2) Choose chart type
    st.subheader("2) Choose chart type")
    chart_type = st.radio("Chart type", ["Bar chart", "Pie chart"], horizontal=True)

    # Build worksheet columns
    value_cols = [f"Value_{i}" for i in range(1, int(n_value_cols) + 1)]
    columns = ["Series"] + value_cols

    # 3) Spreadsheet-like input
    st.subheader("3) Enter your data (Series + Values)")
    st.caption("• 첫 열은 계열 이름(Series)입니다. • 값 열에는 숫자를 입력하세요.")

    default_df = pd.DataFrame([[""] * len(columns) for _ in range(int(n_rows))], columns=columns)

    df_input = st.data_editor(
        default_df,
        use_container_width=True,
        hide_index=True,
        num_rows="fixed",
        key="sheet_v2",
    )

    # Pie chart value selection (which value column to use)
    pie_value_col = None
    if chart_type == "Pie chart":
        pie_value_col = st.selectbox("For pie chart, choose a value column", value_cols, index=0)

    # 4) Generate button
    st.subheader("4) Generate chart")
    generate = st.button("📈 Generate chart")

    if generate:
        df = df_input.copy()

        # Clean series names
        df["Series"] = df["Series"].astype(str).replace("nan", "").str.strip()

        # Convert numeric columns
        for c in value_cols:
            df[c] = pd.to_numeric(df[c], errors="coerce")

        # Drop rows where Series is empty AND all values are NaN
        mask_all_empty = (df["Series"] == "") & (df[value_cols].isna().all(axis=1))
        df = df.loc[~mask_all_empty].copy()

        if df.empty:
            st.warning("No valid data. Please enter series names and numeric values.")
        else:
            title_to_show = chart_title.strip()

            if chart_type == "Bar chart":
                long_df = df.melt(
                    id_vars="Series",
                    value_vars=value_cols,
                    var_name="Category",
                    value_name="Value",
                ).dropna(subset=["Value"])

                if long_df.empty:
                    st.warning("No numeric values found for the bar chart.")
                else:
                    fig = px.bar(
                        long_df,
                        x="Series",
                        y="Value",
                        color="Category",
                        barmode="group",
                        color_discrete_sequence=palette,
                        title=title_to_show if title_to_show else None,
                    )
                    fig.update_layout(
                        height=520,
                        title=dict(x=0.5, xanchor="center", font=dict(size=22)),
                        legend_title="Category",
                        margin=dict(l=20, r=20, t=70, b=20),
                    )
                    st.plotly_chart(fig, use_container_width=True)

            else:  # Pie chart
                pie_df = df[["Series", pie_value_col]].dropna(subset=[pie_value_col]).copy()

                if pie_df.empty:
                    st.warning("No numeric values found for the pie chart.")
                else:
                    fig = px.pie(
                        pie_df,
                        names="Series",
                        values=pie_value_col,
                        color_discrete_sequence=palette,
                        title=title_to_show if title_to_show else None,
                    )
                    fig.update_layout(
                        height=520,
                        title=dict(x=0.5, xanchor="center", font=dict(size=22)),
                        margin=dict(l=20, r=20, t=70, b=20),
                    )
                    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.empty()

with tab3:
    st.empty()
