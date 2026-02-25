import streamlit as st
from datetime import time
import json
import os
from time import sleep

SETTINGS_FILE = "settings.json"

st.set_page_config(layout="wide")
if 'changes' not in st.session_state:
  st.session_state.changes = False

def app():
  st.title("IDMMS Dashboard")
  st.header("Settings")
  st.divider()
  
  current_settings = load_settings()
  cols = st.columns(2, vertical_alignment='center')
  with cols[0]:
    st.subheader("Timer Duration", text_alignment='center')
  with cols[1]:
    col1, col2 = st.columns(2)
    with col1:
      min_val = st.number_input("Minutes", 
                                min_value=0, 
                                max_value=59,
                                value=current_settings["minutes"],
                                on_change=lambda: st.session_state.update({"changes": True}))
    with col2:
      sec_val = st.number_input("Seconds", 
                                min_value=0, 
                                max_value=59,
                                step=10,
                                value=current_settings["seconds"],
                                on_change=lambda: st.session_state.update({"changes": True}))
   
  st.space('large') 
  with st.container(width='stretch', height='content', horizontal_alignment='right', vertical_alignment='center'):
    st.button(
      "Save Settings", 
      type="primary", 
      width='content',
      help="Save the settings and return to Home page", 
      on_click= save_settings,
      args=(min_val, sec_val),
      disabled=not st.session_state.get("changes", False)
      )
    
  global success_msg_placeholder
  success_msg_placeholder = st.empty()
    
# --- Helper Functions ---
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {"minutes": 3, "seconds": 0}

def save_settings(m, s):
    with open(SETTINGS_FILE, "w") as f:
      json.dump({"minutes": m, "seconds": s}, f)
    global success_msg_placeholder
    success_msg_placeholder.success("Settings saved successfully!")
    sleep(2)

if __name__ == "__main__":
  app()
  