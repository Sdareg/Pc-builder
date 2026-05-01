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
    
if 'active_build_name' not in st.session_state:
    st.session_state.active_build_name = None

if 'active_tab_index' not in st.session_state:
    st.session_state.active_tab_index = 0

if 'view' not in st.session_state:
    st.session_state.view = 'main'

if 'active_category' not in st.session_state:
    st.session_state.active_category = None

# Helper functions
def get_active_build():
    return st.session_state.builds.get(st.session_state.active_build_name)

def create_new_build(build_name):
    if build_name and build_name not in st.session_state.builds:
        new_build = Build(build_name)
        st.session_state.builds[build_name] = new_build
        st.session_state.active_build_name = build_name
        return True
    return False

def delete_build(build_name):
    if build_name in st.session_state.builds:
        del st.session_state.builds[build_name]
        if st.session_state.active_build_name == build_name:
            if len(st.session_state.builds) > 0:
                st.session_state.active_build_name = next(iter(st.session_state.builds.keys()))
            else:
                st.session_state.active_build_name = None

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

def go_back_main():
    st.session_state.view = 'main'
    st.session_state.active_category = None

# Main App
st.title("🖥️ PC Build Configurator v1.5")
st.markdown("---")

# --------------------------
# CONTROLLED NAVIGATION
# --------------------------

# Define the tab names
tabs = ["📦 Manage Builds", "✏️ Edit Build", "📤 Import / Export"]

# Create segmented control navigation
selected_tab = st.segmented_control(
    "Navigation", 
    options=tabs, 
    default=tabs[st.session_state.active_tab_index],
    key="nav_bar",
    label_visibility="collapsed"
)

# Update the index based on the selection
st.session_state.active_tab_index = tabs.index(selected_tab)

st.markdown("---")

# --------------------------
# MANAGE BUILDS TAB
# --------------------------
if st.session_state.active_tab_index == 0:
    st.subheader("📦 Manage Saved Builds")
    
    # Create new build
    st.subheader("Create New Build")
    new_build_name = st.text_input("New Build Name")
    if st.button("➕ Create Build", use_container_width=True):
        if create_new_build(new_build_name):
            st.success(f"Build '{new_build_name}' created!")
            st.session_state.active_tab_index = 1
            st.rerun()
        else:
            st.error("Build name already exists or is invalid")
    
    st.markdown("---")
    
    # List all builds
    st.subheader("Your Builds")
    
    if not st.session_state.builds:
        st.info("No builds created yet. Create your first build above.")
    else:
        for build_name, build in list(st.session_state.builds.items()):
            with st.expander(f"🔹 {build_name}"):
                col_info, col_actions = st.columns([3, 1])
                
                with col_info:
                    st.write(f"Total Parts: {sum(1 for p in build.parts.values() if p)}/7")
                    st.write(f"Total Cost: ${build.get_total()}")
                    
                    errors = build.get_status()
                    missing_errors = [e for e in errors if e.startswith("Missing essential component")]
                    compatibility_errors = [e for e in errors if not e.startswith("Missing essential component")]
                    
                    if compatibility_errors:
                        status = "⚠️ Compatibility Issues"
                    elif missing_errors:
                        status = "⏳ Incomplete"
                    else:
                        status = "✅ Complete & Valid"
                    
                    st.write(f"Status: {status}")
                    
                with col_actions:
                    if st.button("✏️ Edit Build", key=f"switch_{build_name}"):
                        st.session_state.active_build_name = build_name
                        st.session_state.active_tab_index = 1
                        st.rerun()
                    
                    if st.button("🗑️ Delete", key=f"del_{build_name}"):
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
# EDIT BUILD TAB
# --------------------------
elif st.session_state.active_tab_index == 1:
    if not st.session_state.builds or not st.session_state.active_build_name:
        st.info("No builds available. Go to Manage Builds to create a new build first.")
        st.stop()
    
    current_build = get_active_build()
    
    if st.session_state.view == 'main':
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
        
        with col_total:
            st.metric("Total Estimated Cost", f"${current_build.get_total()}")

        st.markdown("---")

        # Layout
        left_col, right_col = st.columns([1, 1])

        with left_col:
            st.subheader("Add Components")
            
            # Category Buttons Grid
            st.write("Click to browse parts:")
            cat_cols = st.columns(2)
            for idx, cat in enumerate(categories):
                with cat_cols[idx % 2]:
                    if st.button(f"🔹 {cat}", use_container_width=True, type="secondary"):
                        st.session_state.active_category = cat
                        st.session_state.view = 'browser'
                        st.rerun()

        with right_col:
            st.subheader("Current Build")
            
            for category, part in current_build.parts.items():
                col_cat, col_val, col_remove = st.columns([2, 4, 1])
                with col_cat:
                    st.write(f"**{category}**")
                with col_val:
                    if part:
                        st.write(f"{part.name} (${part.price})")
                    else:
                        st.write("🔴 Not Selected")
                with col_remove:
                    if part:
                        if st.button("❌", key=f"remove_{category}", help=f"Remove {category}"):
                            current_build.parts[category] = None
                            st.rerun()
            st.markdown("")

        st.markdown("---")

        # Compatibility Status
        st.subheader("Build Status")
        errors = current_build.get_status()
        
        missing_errors = [e for e in errors if e.startswith("Missing essential component")]
        compatibility_errors = [e for e in errors if not e.startswith("Missing essential component")]
        
        if missing_errors:
            st.warning("⏳ Build Incomplete:")
            for error in missing_errors:
                st.write(f"  ⚪ {error}")
        
        if compatibility_errors:
            st.error("⚠️ Compatibility Issues Found:")
            for error in compatibility_errors:
                st.write(f"  ✖ {error}")
        
        if not errors:
            st.success("✅ Build Complete & All components are compatible!")

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
    
    elif st.session_state.view == 'browser':
        # --------------------------
        # PARTS BROWSER VIEW
        # --------------------------
        st.button("← Go Back", on_click=go_back_main, use_container_width=True)
        st.markdown("---")
        
        cat = st.session_state.active_category
        st.subheader(f"🔹 Browse {cat}s")
        
        # Filter options
        st.subheader("Filters")
        col1, col2 = st.columns(2)
        with col1:
            min_price = st.number_input("Minimum Price", min_value=0, value=0)
        with col2:
            max_price = st.number_input("Maximum Price", min_value=0, value=5000)
        
        filtered_parts = [c for c in catalog if c.type == cat and min_price <= c.price <= max_price]
        
        st.markdown("---")
        st.write(f"Showing {len(filtered_parts)} parts")
        st.markdown("---")
        
        # Parts Grid - 3 columns
        cols = st.columns(3)
        for idx, part in enumerate(filtered_parts):
            with cols[idx % 3]:
                st.markdown(f"### {part.name}")
                
            
                st.image("https://via.placeholder.com/300x200?text={}+Image".format(part.name.replace(" ", "+")), use_column_width=True)
                
                st.markdown(f"**Price:** ${part.price}")
                
                # specs
                if part.socket and part.socket != 'N/A':
                    st.markdown(f"**Socket:** {part.socket}")
                if part.memory and part.memory != 'N/A':
                    st.markdown(f"**Memory:** {part.memory}")
                st.markdown(f"**TDP:** {part.tdp}W")
                
                st.markdown("---")
                
                if st.button("✅ Select This Part", key=f"select_{cat}_{idx}", use_container_width=True, type="primary"):
                    current_build.add_item(part)
                    st.success(f"Added {part.name} to build!")
                    go_back_main()
                    st.rerun()
                
                st.markdown("---")

# --------------------------
# IMPORT / EXPORT TAB
# --------------------------
elif st.session_state.active_tab_index == 2:
    st.subheader("📤 Import / Export")
    st.markdown("Upload a previously saved build file (single build or bulk export file):")
    
    uploaded_file = st.file_uploader("Choose a build file", type="txt")
    
    if uploaded_file is not None:
        content = uploaded_file.read().decode("utf-8")
        build_blocks = content.split("="*40)
        imported_count = 0
        
        for block in build_blocks:
            lines = block.strip().splitlines()
            if not lines:
                continue
                
            # Extract build name
            build_name_line = [l for l in lines if l.startswith("BUILD NAME: ")]
            if not build_name_line:
                continue
                
            build_name = build_name_line[0].replace("BUILD NAME: ", "").strip()
            
            if build_name in st.session_state.builds:
                st.warning(f"Build '{build_name}' already exists, skipped")
                continue
                
            # Create new build
            imported_build = Build(build_name)
            
            # Find parts in catalog and add to build
            for line in lines:
                if ":" in line and not line.startswith("BUILD NAME") and not line.startswith("Total Cost") and not line.startswith("---"):
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
            imported_count +=1
        
        if imported_count > 0:
            st.success(f"Successfully imported {imported_count} build(s)!")
            st.balloons()
            st.rerun()
    
    st.markdown("---")
    
    st.subheader("📥 Export All Builds")
    st.write(f"You have {len(st.session_state.builds)} saved builds")
    
    if st.button("Export All Builds") and st.session_state.builds:
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