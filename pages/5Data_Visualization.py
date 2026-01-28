import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# Sidebar – color palettes
# ---------------------------
st.sidebar.header("🎨 Color options")

PALETTES = {
    "Pastel": px.colors.qualitative.Pastel,
    "Bold": px.colors.qualitative.Bold,
    "Set2": px.colors.qualitative.Set2,
    "Dark": px.colors.qualitative.Dark2,
    "Vivid": px.colors.qualitative.Vivid,
    "Safe": px.colors.qualitative.Safe,
}

palette_name = st.sidebar.selectbox("Color palette", list(PALETTES.keys()))
palette = PALETTES[palette_name]

# ---------------------------
# Tabs
# ---------------------------
tab1, tab2, tab3 = st.tabs(["1) Chart Builder", "2) (Empty)", "3) (Empty)"])

with tab1:
    st.title("📊 Chart Builder")

    # 1. Table size
    st.subheader("1) Set table size")
    col1, col2 = st.columns(2)
    with col1:
        n_cols = st.number_input("Number of value columns", 1, 10, 3)
    with col2:
        n_rows = st.number_input("Number of rows", 1, 20, 1)

    # 2. Chart type
    st.subheader("2) Choose chart type")
    chart_type = st.radio("Chart type", ["Bar chart", "Pie chart"], horizontal=True)

    # 3. Spreadsheet input
    st.subheader("3) Enter your data (like a spreadsheet)")
    columns = ["Title"] + [f"Col_{i}" for i in range(1, n_cols + 1)]
    df_default = pd.DataFrame("", index=range(n_rows), columns=columns)

    df_input = st.data_editor(
        df_default,
        use_container_width=True,
        hide_index=True,
        key="data_input"
    )

    # 4. Generate button
    st.subheader("4) Generate chart")
    generate = st.button("📈 Generate chart")

    if generate:
        df = df_input.copy()

        # Convert numeric columns
        value_cols = columns[1:]
        for c in value_cols:
            df[c] = pd.to_numeric(df[c], errors="coerce")

        if chart_type == "Bar chart":
            long_df = df.melt(
                id_vars="Title",
                value_vars=value_cols,
                var_name="Category",
                value_name="Value"
            ).dropna()

            if long_df.empty:
                st.warning("Please enter numeric values.")
            else:
                fig = px.bar(
                    long_df,
                    x="Title",
                    y="Value",
                    color="Category",
                    barmode="group",
                    color_discrete_sequence=palette
                )
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)

        else:  # Pie chart
            # Use first row only
            row = df.iloc[0]
            pie_df = pd.DataFrame({
                "Category": value_cols,
                "Value": row[value_cols].values
            }).dropna()

            if pie_df.empty:
                st.warning("Please enter numeric values for the pie chart.")
            else:
                fig = px.pie(
                    pie_df,
                    names="Category",
                    values="Value",
                    title=row["Title"] if row["Title"] else "Pie chart",
                    color_discrete_sequence=palette
                )
                fig.update_layout(height=500)
                st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.empty()

with tab3:
    st.empty()
