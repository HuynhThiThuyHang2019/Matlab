import streamlit as st
import colour
import numpy as np

st.set_page_config(layout="centered")

place = st.empty()
figure, axes = colour.plotting.plot_chromaticity_diagram_CIE1931()
axes.set_xlim([-0.1, 0.85])
axes.set_ylim([-0.1, 0.90])
axes.set_title('CIE 1931 Chromaticity Diagram\n2 Degree Standard Observer')
place.pyplot(figure, clear_figure=True)
