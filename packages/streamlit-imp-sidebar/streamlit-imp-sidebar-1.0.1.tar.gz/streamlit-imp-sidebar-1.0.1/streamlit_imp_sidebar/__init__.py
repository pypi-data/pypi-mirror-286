import os
import streamlit as st
import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
_RELEASE = True
if not _RELEASE:
    _custom_sidebar = components.declare_component(
        "streamlit_imp_sidebar",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _custom_sidebar = components.declare_component("streamlit_imp_sidebar", path=build_dir)


def custom_sidebar(key=None):
    return _custom_sidebar(key=key)

if not _RELEASE:
    # Call the custom sidebar component and capture its return value
    returned_df = custom_sidebar()

    # Depending on the return value, render different content
    if returned_df == "home":
        st.dataframe({"col1": [1, 2], "col2": [3, 4]})
        st.write("This is the home page (New Scenario).")
    elif returned_df == "model_history":
        st.write("This is the model history page.")

    # Display the returned value for debugging purposes
    st.write(returned_df)
else:
    res = custom_sidebar(1)
    st.write(res)

