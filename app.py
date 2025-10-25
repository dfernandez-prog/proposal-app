import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="💘 A Special Question", page_icon="💘", layout="centered")

st.title("💘 A Special Question 💘")
st.write("Do you want to be my girlfriend?")

# --- Collect a (optional) name so you know who answered ---
name = st.text_input("Your name (optional)")

# --- The choices ---
answer = st.radio("Choose one:", ["Yes 💖", "No 💔", "Maybe 🤔"], index=0, horizontal=True)

# --- Where we store responses locally (CSV file) ---
DATA_PATH = Path("responses.csv")

# Ensure the CSV exists with headers
if not DATA_PATH.exists():
  pd.DataFrame(columns=["timestamp", "name", "answer"]).to_csv(DATA_PATH, index=False)

# --- Submit button ---
if st.button("Submit"):
  # Append the new row
  new_row = pd.DataFrame([{
      "timestamp": datetime.utcnow().isoformat(),
      "name": name.strip() if name else "",
      "answer": answer
  }])
  # Read → append → save
  df = pd.read_csv(DATA_PATH)
  df = pd.concat([df, new_row], ignore_index=True)
  df.to_csv(DATA_PATH, index=False)

  st.success("Thanks for your answer! 💐")

st.divider()

# --- Admin view (to see all answers) ---
with st.expander("Admin: View responses"):
  admin_key_input = st.text_input("Enter admin key", type="password")
  admin_key_secret = st.secrets.get("ADMIN_KEY", "")  # set this in Streamlit Cloud

  if admin_key_input and admin_key_input == admin_key_secret:
    try:
      df = pd.read_csv(DATA_PATH)
      st.subheader("Responses")
      st.dataframe(df, use_container_width=True)
      st.download_button(
        "Download CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="responses.csv",
        mime="text/csv",
      )
    except Exception as e:
      st.error(f"Could not read responses: {e}")
  else:
    st.caption("Enter the admin key to view/download responses.")
