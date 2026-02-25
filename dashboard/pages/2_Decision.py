import json
import streamlit as st
import plotly.graph_objects as go
import time

with open("settings.json", "r") as f:
    timer = json.load(f)
    
st.set_page_config(layout="wide")
if 'timer_running' not in st.session_state:
    st.session_state.timer_running = True
if 'proceeding' not in st.session_state:
    st.session_state.proceeding = False

def app():
  st.title("IDMMS Dashboard")
  st.header("AI Decision")
  st.write("Based on the current mud properties, the AI recommends using:")
  st.markdown("")
  
  ADDITIVES = get_additives()
  columns = st.columns(len(ADDITIVES))
  for i, (additive, amount) in enumerate(ADDITIVES.items()):
    with columns[i]:
      with st.container(border=True):
        st.subheader(additive, text_alignment='center')
        max = get_storage(additive)
        st.number_input("Amount (g)", value=amount, min_value=0.0, step=0.5, key=additive, max_value=max, help=f"Maximum available: {max} kg", width=200)

  duration = timer["minutes"] * 60 + timer["seconds"]
  active_timer(duration)  #3 minutes default

  st.space(150)
  col1, col2, col3 = st.columns(3)
  with col2:
    proceed_btn = st.button("Proceed Now", type="primary", width='stretch', help="Proceed with the given additives and amounts",)
    if proceed_btn or st.session_state.get("proceeding", False):
        st.session_state.update({"timer_active": False, "proceeding": True})
        st.session_state.pop("start_time", None)
        st.switch_page("./1_Home.py")
    if st.button("See report", type="secondary", width='stretch'):
        st.switch_page("pages/3_Report.py")
  
  
  
def get_additives():
  return {"Bromine":35.0, "Hashtek Bashtek": 10.0}

def get_storage(additive):
  storage = {"Bromine": 100.0, "Hashtek Bashtek": 50.0}
  return storage.get(additive, 0.0)


@st.fragment(run_every=1.0) # Automatically reruns this function every 1 second
def active_timer(duration):
    
    if "timer_active" not in st.session_state:
        st.session_state.timer_active = True
    if "start_time" not in st.session_state:
        st.session_state.start_time = int(time.time())
    
    elapsed = int(time.time()) - st.session_state.start_time
    remaining = max(0, duration - elapsed)

    # Stop logic
    if st.session_state.timer_active and remaining > 0:
        mins, secs = divmod(remaining, 60)
        with st.container(border=True):
            st.subheader(f"The system will automatically proceed with the given additives and amounts in: {mins:02d}:{secs:02d}")
            if st.button("Stop Timer", width='stretch'):
                st.session_state.timer_active = False
            
    elif not st.session_state.timer_active:
        st.warning("Timer Paused.")
        st.warning("Note: You can adjust the timer duration from settings")
        
    else:
        st.success("Proceeding...")
        st.session_state.update({"timer_active": False, "proceeding": True})


if __name__ == "__main__":
  app()