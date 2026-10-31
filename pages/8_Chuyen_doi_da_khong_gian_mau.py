import numpy as np
import pandas as pd
import streamlit as st
import colour

st.set_page_config(layout="wide")
st.write("## Chuyển đổi đồng thời nhiều không gian màu")

CCS = colour.CCS_ILLUMINANTS["CIE 1931 2 Degree Standard Observer"]
D50, D65 = CCS["D50"], CCS["D65"]
W50, W65 = colour.xy_to_XYZ(D50), colour.xy_to_XYZ(D65)


def tu_rgb(rgb):
    XYZ65 = colour.sRGB_to_XYZ(rgb)
    XYZ50 = colour.chromatic_adaptation(XYZ65, W65, W50)
    return XYZ65, XYZ50


def tu_lab(Lab):
    XYZ50 = colour.Lab_to_XYZ(Lab, illuminant=D50)
    rgb = colour.XYZ_to_sRGB(XYZ50, illuminant=D50, chromatic_adaptation_transform="Bradford")
    return np.clip(rgb, 0, 1)


nguon = st.sidebar.radio("Nhập màu từ", ["Bảng chọn màu", "sRGB (0–255)", "CIELab (D50)"])
if nguon == "Bảng chọn màu":
    hexc = st.sidebar.color_picker("Chọn màu", "#E8731A")
    rgb = np.array(colour.notation.HEX_to_RGB(hexc), dtype=float)
elif nguon == "sRGB (0–255)":
    r = st.sidebar.number_input("R", 0, 255, 232)
    g = st.sidebar.number_input("G", 0, 255, 115)
    b = st.sidebar.number_input("B", 0, 255, 26)
    rgb = np.array([r, g, b]) / 255.0
else:
    L = st.sidebar.number_input("L*", 0.0, 100.0, 60.0)
    a = st.sidebar.number_input("a*", -128.0, 127.0, 40.0)
    b = st.sidebar.number_input("b*", -128.0, 127.0, 60.0)
    rgb = tu_lab(np.array([L, a, b]))

XYZ65, XYZ50 = tu_rgb(rgb)
Lab = colour.XYZ_to_Lab(XYZ50, illuminant=D50)
LCh = colour.Lab_to_LCHab(Lab)
xyY = colour.XYZ_to_xyY(XYZ65)
hsv = colour.RGB_to_HSV(rgb)
k = 1 - rgb.max()
cmy = (1 - rgb - k) / (1 - k) if k < 1 else np.zeros(3)
hexs = "#%02X%02X%02X" % tuple((rgb * 255).round().astype(int))

st.markdown(f"<div style='background:{hexs};height:90px;border:1px solid #888;border-radius:8px;"
            f"text-align:center;line-height:90px;font-size:22px;'>{hexs}</div>", unsafe_allow_html=True)

bang = pd.DataFrame({
    "Không gian màu": ["sRGB (0–255)", "HSV (H°, S%, V%)", "XYZ (D65, 0–100)", "xyY (D65)",
                       "CIELab (D50)", "LCh(ab) (D50)", "CMYK gần đúng (%)"],
    "Giá trị": [
        "R=%.0f, G=%.0f, B=%.0f" % tuple(rgb * 255),
        "H=%.0f, S=%.0f, V=%.0f" % (hsv[0] * 360, hsv[1] * 100, hsv[2] * 100),
        "X=%.2f, Y=%.2f, Z=%.2f" % tuple(XYZ65 * 100),
        "x=%.4f, y=%.4f, Y=%.2f" % (xyY[0], xyY[1], xyY[2] * 100),
        "L*=%.2f, a*=%.2f, b*=%.2f" % tuple(Lab),
        "L*=%.2f, C*=%.2f, h=%.1f°" % tuple(LCh),
        "C=%.0f, M=%.0f, Y=%.0f, K=%.0f" % (cmy[0] * 100, cmy[1] * 100, cmy[2] * 100, k * 100),
    ]})
st.table(bang)
st.caption("CMYK ở đây chỉ là công thức đổi đơn giản từ RGB, không dùng ICC profile nên không phản ánh màu in thực tế.")
