#!/usr/bin/env python
# -*- coding: utf-8 -*-

import streamlit as st

# Create a list to store the button labels
button_labels = []

# Streamlit app layout
st.title("Dynamic Button Example")

# Sidebar
st.sidebar.header("Dynamic Buttons")

# Input for adding a new button
new_button_label = st.sidebar.text_input("New Button Label", "")
add_button_placeholder = st.empty()  # Create a placeholder for the "Add Button" button

# Check if a new button should be added
if new_button_label:
    if st.sidebar.button("Add Button"):
        button_labels.append(new_button_label)
        add_button_placeholder.empty()  # Remove the "Add Button" button

# Input for removing a button
button_to_remove = st.sidebar.selectbox("Remove Button", button_labels)
if st.sidebar.button("Remove") and button_to_remove:
    button_labels.remove(button_to_remove)

# Create a "Clear Sidebar" button
if st.sidebar.button("Clear Sidebar"):
    st.experimental_rerun()  # Rerun the app to clear the sidebar widgets

# Display buttons
st.subheader("Buttons")
for label in button_labels:
    st.button(label)
