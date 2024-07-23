import os

import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
_RELEASE = True

if not _RELEASE:
    _streamlit_imp_custom_model_history = components.declare_component(
        "streamlit_imp_custom_model_history",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _streamlit_imp_custom_model_history = components.declare_component("streamlit_imp_custom_model_history", path=build_dir)


def streamlit_imp_custom_model_history():
    return _streamlit_imp_custom_model_history()

if not _RELEASE:
    streamlit_imp_custom_model_history()

else:
    streamlit_imp_custom_model_history()


