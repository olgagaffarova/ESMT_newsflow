from pathlib import Path
import json

import pandas as pd
import streamlit as st


st.set_page_config(page_title="ESMT Ranking News — Cron Test", layout="wide")

DATA_DIR = Path("data")
NEWS_PATH = DATA_DIR / "news.csv"
STATUS_PATH = DATA_DIR / "collector_status.csv"
STATE_PATH = DATA_DIR / "run_state.json"


@st.cache_data(ttl=60)
def load_news(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    frame["published_at"] = pd.to_datetime(frame["published_at"], utc=True, errors="coerce")
    frame["is_important"] = (
        frame["is_important"].astype(str).str.lower().eq("true")
    )
    return frame.sort_values("published_at", ascending=False, na_position="last")


st.title("ESMT Ranking News — online cron test")
st.caption(
    "This small app reads the CSV created by the scheduled collector notebook. "
    "It intentionally uses only one live source for the first infrastructure test."
)

if not NEWS_PATH.exists():
    st.info(
        "No collected data yet. Open the repository on GitHub, go to Actions, "
        "select ‘Daily ranking news collector’, and click ‘Run workflow’."
    )
    st.stop()

news = load_news(NEWS_PATH)

last_run = "unknown"
if STATE_PATH.exists():
    state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    last_run = state.get("last_successful_run_utc", "unknown")

status_text = "not available"
if STATUS_PATH.exists():
    status = pd.read_csv(STATUS_PATH)
    if not status.empty:
        row = status.iloc[0]
        status_text = f"{row.get('status', 'unknown')} · {int(row.get('fetched_items', 0))} fetched"

col1, col2, col3 = st.columns(3)
col1.metric("Stored articles", len(news))
col2.metric("Important", int(news["is_important"].sum()))
col3.metric("Collector", status_text)
st.caption(f"Last successful run (UTC): {last_run}")

important_only = st.toggle("Show Important only", value=False)
search = st.text_input("Search title or excerpt", placeholder="ranking, methodology, accreditation…")

view = news.copy()
if important_only:
    view = view[view["is_important"]]
if search.strip():
    mask = (
        view[["title", "excerpt"]]
        .fillna("")
        .agg(" ".join, axis=1)
        .str.contains(search.strip(), case=False, regex=False)
    )
    view = view[mask]

display_columns = [
    "published_at",
    "publisher",
    "title",
    "is_important",
    "important_reasons",
    "url",
]

st.dataframe(
    view[display_columns],
    width="stretch",
    hide_index=True,
    column_config={
        "published_at": st.column_config.DatetimeColumn("Published", format="YYYY-MM-DD HH:mm"),
        "publisher": "Source",
        "title": "Title",
        "is_important": "Important",
        "important_reasons": "Reason",
        "url": st.column_config.LinkColumn("Original"),
    },
)
