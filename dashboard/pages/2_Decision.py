import streamlit as st
import plotly.graph_objects as go
import time
st.set_page_config(layout="wide")
if 'timer_running' not in st.session_state:
    st.session_state.timer_running = True
if 'proceeding' not in st.session_state:
    st.session_state.proceeding = False

def app():
  st.title("IDMMS Dashboard")
  st.header("AI Decision")
  st.write("Based on the current mud properties, the AI recommends using:")
  st.space('medium')
  
  ADDITIVES = get_additives()
  columns = st.columns(len(ADDITIVES))
  for i, (additive, amount) in enumerate(ADDITIVES.items()):
    with columns[i]:
      with st.container(width='stretch', height='content', horizontal_alignment='center', vertical_alignment='center', border=True):
        st.subheader(additive, text_alignment='center')
        max = get_storage(additive)
        st.number_input("Amount (g)", value=amount, min_value=0.0, step=0.5, key=additive, max_value=max, help=f"Maximum available: {max} kg", width=200)



  active_timer(180)  #3 minutes default

  st.space(150)
  col1, col2, col3 = st.columns(3)
  with col2:
    proceed_btn = st.button("Proceed Now", type="primary", width='stretch', help="Proceed with the given additives and amounts", on_click=lambda: st.session_state.update({"proceeding": True}))
    if proceed_btn or st.session_state.proceeding:
        st.switch_page("pages/1_Home.py")
    if st.button("See report", type="secondary", width='stretch'):
        st.switch_page("pages/3_Report.py")
  
  
  
def get_additives():
  return {"Bromine":35.0, "Hashtek Bashtek": 10.0}

def get_storage(additive):
  storage = {"Bromine": 100.0, "Hashtek Bashtek": 50.0}
  return storage.get(additive, 0.0)


@st.fragment(run_every=1.0) # Automatically reruns this function every 1 second
def active_timer(duration):
    
    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()
    if "timer_active" not in st.session_state:
        st.session_state.timer_active = True

    elapsed = time.time() - st.session_state.start_time
    remaining = max(0, duration - int(elapsed))

    # Stop logic
    if st.session_state.timer_active and remaining > 0:
      mins, secs = divmod(remaining, 60)
      with st.container(width='stretch', height='content', horizontal_alignment='center', vertical_alignment='center', border=True, horizontal=True):
        st.subheader(f"The system will automatically proceed with the given additives and amounts in: {mins:02d}:{secs:02d}")
        if st.button("Stop Timer", width='stretch'):
            st.session_state.timer_active = False
            st.rerun()
            
    elif not st.session_state.timer_active:
        st.warning("Timer Paused.")
        st.warning("Note: You can adjust the timer duration from settings")
        
    else:
        st.success("Proceeding...")
        st.session_state.proceeding = True
        

if __name__ == "__main__":
  app()