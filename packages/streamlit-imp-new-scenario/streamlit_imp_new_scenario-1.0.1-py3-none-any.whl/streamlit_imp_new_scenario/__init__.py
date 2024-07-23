import os
import streamlit as st
import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
_RELEASE = True
if not _RELEASE:
    _imp_new_scenario_component = components.declare_component(
        "streamlit_imp_new_scenario",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _imp_new_scenario_component = components.declare_component("streamlit_imp_new_scenario", path=build_dir)

def streamlit_imp_new_scenario_component(base_url):
    component_value = _imp_new_scenario_component(base_url=base_url)
    return component_value


