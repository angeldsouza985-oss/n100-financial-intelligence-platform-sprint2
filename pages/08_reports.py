import os
import streamlit as st

st.title("📄 Reports Dashboard")

st.write("Browse generated radar chart reports for each company.")

REPORT_DIR = "reports/radar_charts"

if not os.path.exists(REPORT_DIR):
    st.error("Reports folder not found.")
    st.stop()

images = sorted(
    [
        f for f in os.listdir(REPORT_DIR)
        if f.endswith(".png")
    ]
)

if len(images) == 0:
    st.warning("No reports available.")
    st.stop()

company = st.selectbox(
    "Select Company",
    [img.replace("_radar.png", "") for img in images],
)

image_path = os.path.join(
    REPORT_DIR,
    f"{company}_radar.png"
)

st.subheader(f"{company} Radar Report")

st.image(
    image_path,
    use_container_width=True,
)

with open(image_path, "rb") as file:
    st.download_button(
        label="📥 Download Report",
        data=file,
        file_name=f"{company}_radar.png",
        mime="image/png",
    )

st.success(f"Showing radar report for {company}.")