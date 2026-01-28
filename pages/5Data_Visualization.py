import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Data → Chart", layout="wide")

# ---------------------------
# Sidebar (color option)
# ---------------------------
st.sidebar.header("🎨 Chart Options")
COLOR_OPTIONS = {
    "Blue": "Blues",
    "Green": "Greens",
    "Red": "Reds",
    "Purple": "Purples",
    "Orange": "Oranges",
    "Gray": "Greys",
}
color_scale_label = st.sidebar.selectbox("Color theme", list(COLOR_OPTIONS.keys()))
color_scale = COLOR_OPTIONS[color_scale_label]

# ---------------------------
# Tabs
# ---------------------------
tab1, tab2, tab3 = st.tabs(["1) Chart Builder", "2) (Empty)", "3) (Empty)"])

with tab1:
    st.title("📊 Simple Chart Builder")

    # 1) Ask rows/cols
    st.subheader("1) Set table size")
    c1, c2 = st.columns(2)
    with c1:
        n_cols = st.number_input("Number of columns", min_value=1, max_value=12, value=3, step=1)
    with c2:
        n_rows = st.number_input("Number of rows", min_value=1, max_value=200, value=5, step=1)

    # 2) Choose chart type
    st.subheader("2) Choose chart type")
    chart_type = st.radio("Chart", ["Bar chart", "Pie chart"], horizontal=True)

    # 3) Spreadsheet-like input (with title row)
    st.subheader("3) Enter your data (like a spreadsheet)")
    st.caption("• 첫 번째 열은 항목(라벨), 두 번째 열부터는 값(숫자) 권장. • 파이차트는 기본적으로 첫 번째 '값' 열만 사용합니다.")

    # Build a default dataframe with a "Title" column
    col_names = ["Title"] + [f"Col_{i}" for i in range(1, int(n_cols) + 1)]
    default_df = pd.DataFrame([[""] * len(col_names) for _ in range(int(n_rows))], columns=col_names)

    edited_df = st.data_editor(
        default_df,
        use_container_width=True,
        num_rows="fixed",
        hide_index=True,
        key="data_sheet",
    )

    # Basic validation helpers
    def to_numeric_series(s: pd.Series) -> pd.Series:
        return pd.to_numeric(s, errors="coerce")

    # 4) Plot chart
    st.subheader("4) Chart preview")

    # Clean: drop rows where Title is empty AND all values are empty
    df = edited_df.copy()
    value_cols = [c for c in df.columns if c != "Title"]

    # Convert numeric columns
    for c in value_cols:
        df[c] = to_numeric_series(df[c])

    # Remove fully empty rows
    df["__all_empty__"] = df[value_cols].isna().all(axis=1) & (df["Title"].astype(str).str.strip() == "")
    df = df.loc[~df["__all_empty__"]].drop(columns=["__all_empty__"])

    if df.empty:
        st.info("데이터를 입력하면 여기에서 그래프가 표시됩니다.")
    else:
        # Ensure Title exists for labels
        df["Title"] = df["Title"].astype(str).replace("nan", "").str.strip()
        df.loc[df["Title"] == "", "Title"] = "Item"

        if chart_type == "Bar chart":
            # Bar: long-form (Title, Variable, Value)
            long_df = df.melt(id_vars=["Title"], value_vars=value_cols, var_name="Variable", value_name="Value")
            long_df = long_df.dropna(subset=["Value"])

            if long_df.empty:
                st.warning("바 그래프를 그릴 숫자 데이터가 없습니다. 값 열에 숫자를 입력해 주세요.")
            else:
                fig = px.bar(
                    long_df,
                    x="Title",
                    y="Value",
                    color="Variable",
                    barmode="group",
                    color_discrete_sequence=px.colors.sequential.__dict__.get(color_scale, px.colors.sequential.Blues),
                )
                fig.update_layout(
                    xaxis_title="Title",
                    yaxis_title="Value",
                    legend_title="Series",
                    height=520,
                    margin=dict(l=20, r=20, t=40, b=20),
                )
                st.plotly_chart(fig, use_container_width=True)

        else:  # Pie chart
            # Pie uses first numeric column
            first_value_col = value_cols[0]
            pie_df = df[["Title", first_value_col]].dropna(subset=[first_value_col])

            if pie_df.empty:
                st.warning("파이차트를 그릴 숫자 데이터가 없습니다. 첫 번째 값 열에 숫자를 입력해 주세요.")
            else:
                fig = px.pie(
                    pie_df,
                    names="Title",
                    values=first_value_col,
                    color_discrete_sequence=px.colors.sequential.__dict__.get(color_scale, px.colors.sequential.Blues),
                )
                fig.update_layout(
                    height=520,
                    margin=dict(l=20, r=20, t=40, b=20),
                )
                st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.write("")  # intentionally empty

with tab3:
    st.write("")  # intentionally empty
