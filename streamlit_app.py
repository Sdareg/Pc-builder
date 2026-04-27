import streamlit as st
import sys
import os

# Add the final_project directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'final_project'))

from models import Build
from data_manager import load_catalog

# Page configuration
st.set_page_config(
    page_title="PC Build Configurator",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load components catalog once
@st.cache_data
def get_catalog():
    return load_catalog(os.path.join(os.path.dirname(__file__), 'final_project', 'parts_menu.txt'))

catalog = get_catalog()
categories = ["CPU", "Motherboard", "GPU", "RAM", "Storage", "PSU", "Case"]

# Initialize session state for build
if 'current_build' not in st.session_state:
    st.session_state.current_build = Build("New Build")

# Main App
st.title("🖥️ PC Build Configurator v1.0")
st.markdown("---")

# Header section
col1, col2 = st.columns([3, 1])
with col1:
    build_name = st.text_input("Build Name", value=st.session_state.current_build.name)
    if build_name != st.session_state.current_build.name:
        st.session_state.current_build.name = build_name

with col2:
    total_cost = st.session_state.current_build.get_total()
    st.metric("Total Estimated Cost", f"${total_cost}")

st.markdown("---")

# Layout
left_col, right_col = st.columns([1, 1])

with left_col:
    st.subheader("Add Components")
    
    selected_category = st.selectbox("Select Component Type", categories)
    
    filtered_parts = [c for c in catalog if c.type == selected_category]
    
    if filtered_parts:
        part_options = [f"{p.name} (${p.price})" for p in filtered_parts]
        selected_part_index = st.selectbox(f"Select {selected_category}", range(len(part_options)), format_func=lambda x: part_options[x])
        
        selected_part = filtered_parts[selected_part_index]
        
        if st.button("✅ Add to Build", use_container_width=True):
            st.session_state.current_build.add_item(selected_part)
            st.success(f"Added {selected_part.name} to your build!")
            st.rerun()
    else:
        st.warning(f"No parts found for {selected_category}")

with right_col:
    st.subheader("Current Build")
    
    build_table = []
    for category, part in st.session_state.current_build.parts.items():
        build_table.append({
            "Component": category,
            "Selection": part.name if part else "🔴 Not Selected",
            "Price": f"${part.price}" if part else "-"
        })
    
    st.table(build_table)

st.markdown("---")

# Compatibility Status
st.subheader("Build Status")
errors = st.session_state.current_build.get_status()

if not errors:
    st.success("✅ All components are compatible!")
else:
    st.error("⚠️ Compatibility Issues Found:")
    for error in errors:
        st.write(f"  ✖ {error}")

# Power Calculation
total_watts = sum(p.tdp for p in st.session_state.current_build.parts.values() if p and p.type != "PSU")
psu = st.session_state.current_build.parts["PSU"]

st.markdown("---")
st.subheader("Power Consumption")
col_p1, col_p2 = st.columns(2)
with col_p1:
    st.metric("System Power Draw", f"{total_watts}W")
with col_p2:
    if psu:
        st.metric("PSU Capacity", f"{psu.tdp}W")
        if total_watts > psu.tdp:
            st.error("⚠️ Insufficient Power Supply!")

# Save Build
st.markdown("---")
if st.button("💾 Export Build", use_container_width=True):
    output = []
    output.append(f"BUILD NAME: {st.session_state.current_build.name}\n")
    output.append("-" * 30 + "\n")
    for cat, p in st.session_state.current_build.parts.items():
        name = p.name if p else "None"
        output.append(f"{cat}: {name}\n")
    output.append("-" * 30 + "\n")
    output.append(f"Total Cost: ${st.session_state.current_build.get_total()}\n")
    
    build_content = ''.join(output)
    
    st.download_button(
        label="📥 Download Build File",
        data=build_content,
        file_name=f"{st.session_state.current_build.name}.txt",
        mime="text/plain",
        use_container_width=True
    )

# Reset Build
if st.button("🔄 Reset Build", type="secondary", use_container_width=True):
    st.session_state.current_build = Build("New Build")
    st.rerun()