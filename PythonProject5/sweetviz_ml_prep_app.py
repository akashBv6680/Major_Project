import streamlit as st
import pandas as pd
import sweetviz as sv
import numpy as np  # Used for numerical type detection
import warnings
import os

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

st.set_page_config(
    page_title="Sweetviz ML Prep App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Sweetviz ML Prep App: Feature & Target Selection")
st.markdown(
    "Upload a *CSV* or *Excel (.xlsx)* file, then select your features (X) and target (y) for a tailored Sweetviz report.")

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

            st.header("1. Select Features (X) and Target (y)")

            all_columns = df.columns.tolist()

            # --- Feature Inputs (X) ---
            # Allow user to select multiple feature columns
            selected_features = st.multiselect(
                "Select your *Feature Columns (X)*:",
                options=all_columns,
                default=[col for col in all_columns if col != all_columns[-1]]  # Default to all except last
            )

            # --- Target Variable (y) ---
            # Allow user to select a single target column
            # Options for target should exclude selected features
            target_options = [col for col in all_columns if col not in selected_features]
            selected_target = st.selectbox(
                "Select your *Target Variable (y)*:",
                options=['None'] + target_options,  # Add 'None' option
                index=0 if 'None' in ['None'] + target_options else (
                    target_options.index(all_columns[-1]) + 1 if all_columns[-1] in target_options else 0)
                # Default to 'None' or last available
            )

            # Convert 'None' string to actual None for Sweetviz
            target_feat_for_sv = selected_target if selected_target != 'None' else None

            st.markdown("---")
            st.header("2. Generate Sweetviz Report")

            if st.button("Generate Sweetviz Report"):
                if not selected_features and target_feat_for_sv is None:
                    st.warning(
                        "Please select at least some features or a target variable to generate a meaningful report.")
                else:
                    with st.spinner("Generating Sweetviz report... This might take a moment."):
                        # Sweetviz will analyze the entire DataFrame, but if target_feat is provided,
                        # it will highlight relationships with that target.
                        my_report = sv.analyze(df, target_feat=target_feat_for_sv)

                        report_html_path = "sweetviz_ml_prep_report.html"
                        my_report.save_html(report_html_path)

                        st.success("Sweetviz report generated!")
                        st.write("### Interactive Report:")

                        # Provide a download button for the HTML report
                        try:
                            if os.path.exists(report_html_path):
                                with open(report_html_path, "rb") as f:  # Open in binary read mode
                                    html_content = f.read()

                                st.download_button(
                                    label="Download Sweetviz Report (HTML)",
                                    data=html_content,
                                    file_name="sweetviz_ml_prep_report.html",
                                    mime="text/html"
                                )
                                st.info("""
                                The interactive Sweetviz report is ready!
                                If you selected a target variable, Sweetviz will show its relationship with all other features.
                                """)
                            else:
                                st.error(f"Sweetviz report HTML file not found at {report_html_path}.")

                        except Exception as e:
                            st.error(f"Error preparing report for download: {e}")
                            st.warning("Could not create download button. Please check file permissions or try again.")
                        finally:
                            # Clean up the temporary HTML file
                            if os.path.exists(report_html_path):
                                os.remove(report_html_path)

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
st.markdown("Built with ❤️ using Streamlit and Sweetviz.")
