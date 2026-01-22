"""Reusable UI components for the dashboard."""

import pandas as pd
import streamlit as st

# Netzbremse logo URL
LOGO_URL = "https://netzbremse.de/img/hourglass_hu15528090548520832702.png"


def render_header():
    """Render the dashboard header with logo."""
    col1, col2 = st.columns([1, 5])
    with col1:
        st.image(LOGO_URL, width=80)
    with col2:
        st.title("Netzbremse Speedtest Dashboard")


def render_latest_summary(df: pd.DataFrame):
    """
    Render summary cards for the latest measurement.

    Shows the 4 primary metrics: download, upload, latency, jitter.
    """
    if df.empty:
        st.warning("No data available yet.")
        return

    latest = df.iloc[0]  # DataFrame is sorted most recent first

    st.subheader("Latest Measurement")
    st.caption(f"Recorded at: {latest['timestamp'].strftime('%Y-%m-%d %H:%M:%S UTC')}")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Download",
            value=f"{latest['download']:.2f} Mbps",
        )
    with col2:
        st.metric(
            label="Upload",
            value=f"{latest['upload']:.2f} Mbps",
        )
    with col3:
        st.metric(
            label="Latency",
            value=f"{latest['latency']:.2f} ms",
        )
    with col4:
        st.metric(
            label="Jitter",
            value=f"{latest['jitter']:.2f} ms",
        )


def render_recent_table(df: pd.DataFrame, count: int = 5):
    """Render a table of the most recent measurements."""
    if df.empty:
        return

    st.subheader(f"Last {min(count, len(df))} Measurements")

    display_df = df.head(count).copy()
    display_df["timestamp"] = display_df["timestamp"].dt.strftime("%Y-%m-%d %H:%M")

    # Select and rename columns for display
    columns_to_show = ["timestamp", "download", "upload", "latency", "jitter"]
    display_df = display_df[columns_to_show]

    column_rename = {
        "timestamp": "Time",
        "download": "Download (Mbps)",
        "upload": "Upload (Mbps)",
        "latency": "Latency (ms)",
        "jitter": "Jitter (ms)",
    }
    display_df = display_df.rename(columns=column_rename)

    # Format numeric columns
    for col in ["Download (Mbps)", "Upload (Mbps)", "Latency (ms)", "Jitter (ms)"]:
        display_df[col] = display_df[col].apply(lambda x: f"{x:.2f}")

    st.dataframe(display_df, width="stretch", hide_index=True)
