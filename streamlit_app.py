import streamlit as st
import sys
import os

# Add the final_project directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'final_project'))

from models import Build, Component
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

# Initialize session state
if 'builds' not in st.session_state:
    st.session_state.builds = {}
    # Create default initial build
    default_build = Build("New Build")
    st.session_state.builds["New Build"] = default_build
    
if 'active_build_name' not in st.session_state:
    st.session_state.active_build_name = "New Build"

# Helper functions
def get_active_build():
    return st.session_state.builds[st.session_state.active_build_name]

def create_new_build(build_name):
    if build_name and build_name not in st.session_state.builds:
        new_build = Build(build_name)
        st.session_state.builds[build_name] = new_build
        st.session_state.active_build_name = build_name
        return True
    return False

def delete_build(build_name):
    if build_name in st.session_state.builds and len(st.session_state.builds) > 1:
        del st.session_state.builds[build_name]
        # Switch to first remaining build
        st.session_state.active_build_name = next(iter(st.session_state.builds.keys()))

def export_build(build):
    output = []
    output.append(f"BUILD NAME: {build.name}\n")
    output.append("-" * 30 + "\n")
    for cat, p in build.parts.items():
        name = p.name if p else "None"
        output.append(f"{cat}: {name}\n")
    output.append("-" * 30 + "\n")
    output.append(f"Total Cost: ${build.get_total()}\n")
    return ''.join(output)

# Main App
st.title("🖥️ PC Build Configurator v1.1")
st.markdown("---")

# Tab Navigation
tab_create, tab_manage, tab_import = st.tabs(["🔨 Create Build", "📦 Manage Builds", "📤 Import / Export"])

# --------------------------
# CREATE BUILD TAB
# --------------------------
with tab_create:
    
    # Build selector
    col_select, col_total = st.columns([3,1])
    with col_select:
        active_build = st.selectbox(
            "Active Build", 
            options=list(st.session_state.builds.keys()),
            index=list(st.session_state.builds.keys()).index(st.session_state.active_build_name)
        )
        if active_build != st.session_state.active_build_name:
            st.session_state.active_build_name = active_build
            st.rerun()
    
    current_build = get_active_build()
    
    with col_total:
        st.metric("Total Estimated Cost", f"${current_build.get_total()}")

    st.markdown("---")

    # Layout
    left_col, right_col = st.columns([1, 1])

    with left_col:
        st.subheader("Add Components")
        
        selected_category = st.selectbox("Select Component Type", categories, key="create_cat")
        
        filtered_parts = [c for c in catalog if c.type == selected_category]
        
        if filtered_parts:
            part_options = [f"{p.name} (${p.price})" for p in filtered_parts]
            selected_part_index = st.selectbox(f"Select {selected_category}", range(len(part_options)), format_func=lambda x: part_options[x], key="create_part")
            
            selected_part = filtered_parts[selected_part_index]
            
            if st.button("✅ Add to Build", use_container_width=True, key="add_btn"):
                current_build.add_item(selected_part)
                st.success(f"Added {selected_part.name} to your build!")
                st.rerun()
        else:
            st.warning(f"No parts found for {selected_category}")

    with right_col:
        st.subheader("Current Build")
        
        build_table = []
        for category, part in current_build.parts.items():
            build_table.append({
                "Component": category,
                "Selection": part.name if part else "🔴 Not Selected",
                "Price": f"${part.price}" if part else "-"
            })
        
        st.table(build_table)

    st.markdown("---")

    # Compatibility Status
    st.subheader("Build Status")
    errors = current_build.get_status()

    if not errors:
        st.success("✅ All components are compatible!")
    else:
        st.error("⚠️ Compatibility Issues Found:")
        for error in errors:
            st.write(f"  ✖ {error}")

    # Power Calculation
    total_watts = sum(p.tdp for p in current_build.parts.values() if p and p.type != "PSU")
    psu = current_build.parts["PSU"]

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

# --------------------------
# MANAGE BUILDS TAB
# --------------------------
with tab_manage:
    st.subheader("📦 Manage Saved Builds")
    st.markdown("---")
    
    # Create new build
    st.subheader("Create New Build")
    new_build_name = st.text_input("New Build Name")
    if st.button("➕ Create Build", use_container_width=True):
        if create_new_build(new_build_name):
            st.success(f"Build '{new_build_name}' created!")
            st.rerun()
        else:
            st.error("Build name already exists or is invalid")
    
    st.markdown("---")
    
    # List all builds
    st.subheader("Your Builds")
    
    for build_name, build in list(st.session_state.builds.items()):
        with st.expander(f"🔹 {build_name}"):
            col_info, col_actions = st.columns([3, 1])
            
            with col_info:
                st.write(f"Total Parts: {sum(1 for p in build.parts.values() if p)}/7")
                st.write(f"Total Cost: ${build.get_total()}")
                status = "✅ Valid" if not build.get_status() else "⚠️ Has Issues"
                st.write(f"Status: {status}")
                
            with col_actions:
                if st.button("✏️ Switch", key=f"switch_{build_name}"):
                    st.session_state.active_build_name = build_name
                    st.rerun()
                
                if st.button("🗑️ Delete", key=f"del_{build_name}", disabled=len(st.session_state.builds)<=1):
                    delete_build(build_name)
                    st.rerun()
            
            # Quick export
            build_content = export_build(build)
            st.download_button(
                label="📥 Download",
                data=build_content,
                file_name=f"{build_name}.txt",
                mime="text/plain",
                key=f"dl_{build_name}"
            )

# --------------------------
# IMPORT / EXPORT TAB
# --------------------------
with tab_import:
    st.subheader("📤 Import Build")
    st.markdown("Upload a previously saved build file:")
    
    uploaded_file = st.file_uploader("Choose a build file", type="txt")
    
    if uploaded_file is not None:
        content = uploaded_file.read().decode("utf-8")
        lines = content.splitlines()
        
        # Extract build name
        build_name = lines[0].replace("BUILD NAME: ", "").strip()
        
        if build_name in st.session_state.builds:
            st.error(f"Build '{build_name}' already exists!")
        else:
            # Create new build
            imported_build = Build(build_name)
            
            # Find parts in catalog and add to build
            for line in lines[2:-3]:
                if ":" in line:
                    cat, part_name = line.split(":", 1)
                    cat = cat.strip()
                    part_name = part_name.strip()
                    
                    if part_name != "None":
                        # Find component in catalog
                        for comp in catalog:
                            if comp.name == part_name:
                                imported_build.add_item(comp)
                                break
            
            st.session_state.builds[build_name] = imported_build
            st.success(f"Build '{build_name}' imported successfully!")
            st.balloons()
    
    st.markdown("---")
    
    st.subheader("📥 Export All Builds")
    st.write(f"You have {len(st.session_state.builds)} saved builds")
    
    if st.button("Export All Builds"):
        export_all = []
        for name, build in st.session_state.builds.items():
            export_all.append(export_build(build))
            export_all.append("\n" + "="*40 + "\n\n")
        
        st.download_button(
            label="📥 Download All Builds",
            data=''.join(export_all),
            file_name="all_pc_builds.txt",
            mime="text/plain"
        )

    st.markdown("---")
    st.info("💡 Build files are standard text files that you can share, backup, or import on any device running this app.")