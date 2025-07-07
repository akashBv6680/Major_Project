import streamlit as st
import pandas as pd
# import sweetviz as sv # Temporarily comment out sweetviz to remove its dependency
import numpy as np
import warnings
import os
# import streamlit.components.v1 as components # Not strictly needed if not embedding raw HTML

import matplotlib.pyplot as plt # New import
import seaborn as sns          # New import

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

st.set_page_config(
    page_title="Data Insights App", # Changed title slightly
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Data Insights App: Explore Your Data") # Changed title slightly
st.markdown(
    "Upload a *CSV* or *Excel (.xlsx)* file, then explore basic statistics and visualizations of your dataset.")

# --- File Uploader ---
uploaded_file = st.file_uploader("Choose your data file", type=["csv", "xlsx"])

df = None
if uploaded_file is not None:
    st.success(f"File '{uploaded_file.name}' uploaded successfully!")
    file_type = uploaded_file.name.split('.')[-1].lower()

    try:
        if file_type == "csv":
            df = pd.read_csv(uploaded_file)
        elif file_type == "xlsx":
            df = pd.read_excel(uploaded_file)

        if df is not None and not df.empty:
            st.write("### Data Preview (First 5 rows):")
            st.dataframe(df.head())
            st.write(f"DataFrame Shape: {df.shape[0]} rows, {df.shape[1]} columns")
            st.markdown("---")

            # --- Basic Data Overview Section ---
            st.header("Basic Data Overview")
            if st.checkbox("Show DataFrame Info (df.info())"):
                import io
                buffer = io.StringIO()
                df.info(buf=buffer)
                s = buffer.getvalue()
                st.text(s)

            if st.checkbox("Show Descriptive Statistics (df.describe())"):
                st.dataframe(df.describe())

            if st.checkbox("Show Missing Values"):
                missing_data = df.isnull().sum()
                st.write("Number of missing values per column:")
                st.dataframe(missing_data[missing_data > 0])
                if missing_data.sum() == 0:
                    st.info("No missing values found in the DataFrame!")
            st.markdown("---")
            # --- End Basic Data Overview Section ---

            st.header("1. Select Features for Visualization")

            all_columns = df.columns.tolist()

            # Let user select columns for plotting
            columns_to_plot = st.multiselect(
                "Select columns to visualize:",
                options=all_columns,
                default=[]
            )

            st.markdown("---")
            st.header("2. Generate Basic Visualizations")

            if st.button("Generate Visualizations"):
                if not columns_to_plot:
                    st.warning("Please select at least one column to visualize.")
                else:
                    st.write("### Visualizations:")
                    for col in columns_to_plot:
                        st.subheader(f"Visualization for: {col}")

                        # Handle numerical vs categorical for plots
                        if pd.api.types.is_numeric_dtype(df[col]):
                            st.write(f"**Histogram for {col}:**")
                            fig, ax = plt.subplots(figsize=(8, 4))
                            sns.histplot(df[col].dropna(), kde=True, ax=ax)
                            st.pyplot(fig)
                            plt.close(fig) # Close the figure to free memory

                            st.write(f"**Box Plot for {col}:**")
                            fig, ax = plt.subplots(figsize=(8, 2))
                            sns.boxplot(x=df[col].dropna(), ax=ax)
                            st.pyplot(fig)
                            plt.close(fig) # Close the figure to free memory

                        elif pd.api.types.is_object_dtype(df[col]) or pd.api.types.is_categorical_dtype(df[col]):
                            st.write(f"**Count Plot for {col}:**")
                            fig, ax = plt.subplots(figsize=(10, 5))
                            sns.countplot(y=df[col].dropna(), order=df[col].value_counts().index, ax=ax)
                            plt.tight_layout()
                            st.pyplot(fig)
                            plt.close(fig) # Close the figure to free memory
                        else:
                            st.info(f"Cannot generate standard plot for column '{col}' due to unsupported data type.")
                        st.markdown("---")

            # --- Sweetviz related section (commented out or removed for now) ---
            # If you want to keep the Sweetviz structure but disable it:
            # st.markdown("---")
            # st.header("Sweetviz Report (currently disabled due to environment issues)")
            # st.info("The Sweetviz report generation is currently disabled. Please use the basic visualizations above.")
            # st.write("We are working on resolving the environment issues to enable Sweetviz in the future.")

        else:
            st.warning(
                "The uploaded file resulted in an empty DataFrame or could not be processed. Please check your data.")

    except Exception as e:
        st.error(f"An error occurred while reading or processing the file: {e}")
        st.info("Please ensure your file is a valid CSV or XLSX and try again.")
        st.exception(e)
else:
    st.info("Upload your data file to get started.")

st.markdown("---")
st.markdown("Built with ❤️ using Streamlit, Pandas, Matplotlib, and Seaborn.")
