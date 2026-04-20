import json
import streamlit as st
import time

# 1. Configuration & Settings
with open("./settings.json", "r") as f:
    timer_settings = json.load(f)

st.set_page_config(layout="wide")

# Initialize Session States
st.session_state.setdefault("timer_active", True)
st.session_state.setdefault("proceeding", False)
st.session_state.setdefault("start_time", int(time.time()))
st.session_state.mode = "decision" # Set the mode to "decision" for this page

def get_additives():
    return {"Bentonite": 35.0, "Barite": 10.0}

def get_storage(additive):
    storage = {"Bentonite": 100.0, "Barite": 50.0}
    return storage.get(additive, 0.0)

@st.fragment(run_every=1.0)
def render_timer(duration):
    # Calculate time
    elapsed = int(time.time()) - st.session_state.start_time
    remaining = max(0, duration - elapsed)

    if st.session_state.timer_active and remaining > 0:
        mins, secs = divmod(remaining, 60)
        with st.container(border=True):
            st.subheader(f"⏱️ Auto-proceed in: {mins:02d}:{secs:02d}")
            if st.button("Stop Timer", width='stretch'):
                st.session_state.timer_active = False
                st.rerun() # Force fragment update
    
    elif not st.session_state.timer_active:
        st.warning("Timer Paused. Adjust duration in settings if needed.")
        
    else:
        # TIMER FINISHED
        st.session_state.proceeding = True
        st.session_state.timer_active = False
        st.rerun() # This triggers the main app to see the 'proceeding' state

def app():
    st.title("IDMMS Dashboard")
    st.header("AI Decision")
    st.write("Based on the current mud properties, the AI recommends:")

    # 1. Additive Inputs
    ADDITIVES = get_additives()
    columns = st.columns(len(ADDITIVES))
    
    for i, (additive, amount) in enumerate(ADDITIVES.items()):
        with columns[i]:
            with st.container(border=True):
                st.subheader(additive)
                max_val = get_storage(additive)
                # Note: width is controlled by the column, number_input doesn't take 'width'
                st.number_input(
                    "Amount (g)", 
                    value=amount, 
                    min_value=0.0, 
                    step=0.5, 
                    key=f"input_{additive}", 
                    max_value=max_val, 
                    help=f"Max: {max_val}g"
                )

    # 2. The Timer Fragment
    duration = timer_settings["minutes"] * 60 + timer_settings["seconds"]
    render_timer(duration)

    # 3. Decision Logic
    st.write("") # Spacer
    col1, col2, col3 = st.columns(3)
    
    with col2:
        # Check if timer finished OR button clicked
        if st.button("Proceed Now", type="primary", width='stretch') or st.session_state.proceeding:
            st.session_state.proceeding = True
            st.session_state.timer_active = False
            if "start_time" in st.session_state:
                del st.session_state["start_time"]
            st.session_state.mode = "loading"
            st.switch_page("1_Home.py") 

        if st.button("See Report", type="secondary", width='stretch'):
            st.switch_page("pages/3_Report.py")

if __name__ == "__main__":
    app()