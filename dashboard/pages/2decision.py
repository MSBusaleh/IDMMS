import streamlit as st
import plotly.graph_objects as go

def app():
  st.title("IDMMS Dashboard")
  st.header("AI Decision")
  st.write("Based on the current mud properties, the AI recommends using:")
  ADDITIVES = get_additives()
  st.space('medium')
  columns = st.columns(len(ADDITIVES))
  for i, (additive, amount) in enumerate(ADDITIVES.items()):
    with columns[i]:
      with st.container(width='stretch', height='content', horizontal_alignment='center', vertical_alignment='center', border=True):
        st.subheader(additive, text_alignment='center')
        max = get_storage(additive)
        st.number_input("Amount (g)", value=amount, min_value=0.0, step=0.5, key=additive, max_value=max, help=f"Maximum available: {max} kg", width=200)
  st.space(150)
  col1, col2, col3 = st.columns(3)
  with col2:
    st.button("Proceed", type="primary", width='stretch', help="Proceed with the given additives and amounts")
    st.button("See report", type="secondary", width='stretch')
  
  
  
def get_additives():
  return {"Bromine":35.0, "Hashtek Bashtek": 10.0}

def get_storage(additive):
  storage = {"Bromine": 100.0, "Hashtek Bashtek": 50.0}
  return storage.get(additive, 0.0)
  
if __name__ == "__main__":
  app()