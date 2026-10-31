import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import colour

st.set_page_config(layout="wide")
st.write("## Kiểm tra sai lệch màu ΔE theo nhiều công thức")

D50 = colour.CCS_ILLUMINANTS["CIE 1931 2 Degree Standard Observer"]["D50"]


def lab2rgb(Lab):
    XYZ = colour.Lab_to_XYZ(Lab, illuminant=D50)
    rgb = colour.XYZ_to_sRGB(XYZ, illuminant=D50, chromatic_adaptation_transform="Bradford")
    return np.clip(rgb, 0, 1)


c1, c2 = st.columns([1, 2])
with c1:
    st.write("### Màu chuẩn (Lab)")
    L0 = st.number_input("L*", 0.0, 100.0, 50.0)
    a0 = st.number_input("a*", -128.0, 127.0, 40.0)
    b0 = st.number_input("b*", -128.0, 127.0, 20.0)
    nguong = st.slider("Ngưỡng dung sai ΔE00", 0.5, 10.0, 3.0, 0.5)
with c2:
    st.write("### Các mẫu đo (sửa trực tiếp trong bảng, có thể thêm dòng)")
    df0 = pd.DataFrame({"Mẫu": ["M1", "M2", "M3", "M4"],
                        "L": [50.5, 52.0, 48.0, 55.0],
                        "a": [39.0, 42.0, 35.0, 30.0],
                        "b": [21.0, 17.0, 25.0, 30.0]})
    df = st.data_editor(df0, num_rows="dynamic", hide_index=True)

df = df.dropna()
if len(df) == 0:
    st.warning("Chưa có mẫu nào.")
    st.stop()

ref = np.array([L0, a0, b0])
S = df[["L", "a", "b"]].to_numpy(dtype=float)
R = np.tile(ref, (len(S), 1))

kq = pd.DataFrame({
    "Mẫu": df["Mẫu"].values,
    "ΔE76": colour.delta_E(R, S, method="CIE 1976"),
    "ΔE94": colour.delta_E(R, S, method="CIE 1994"),
    "ΔE CMC(2:1)": colour.delta_E(R, S, method="CMC", l=2, c=1),
    "ΔE00": colour.delta_E(R, S, method="CIE 2000"),
})
kq["Kết luận"] = np.where(kq["ΔE00"] <= nguong, "Đạt", "Không đạt")
st.write("### Kết quả")
st.dataframe(kq.round(2), hide_index=True)

g1, g2 = st.columns(2)
with g1:
    fig, ax = plt.subplots(figsize=(6, 4))
    mau = ["tab:green" if v <= nguong else "tab:red" for v in kq["ΔE00"]]
    ax.bar(kq["Mẫu"], kq["ΔE00"], color=mau)
    ax.axhline(nguong, color="k", ls="--", label=f"Ngưỡng = {nguong}")
    ax.set_ylabel("ΔE00")
    ax.set_title("Sai lệch màu so với màu chuẩn")
    ax.legend()
    st.pyplot(fig, clear_figure=True)
with g2:
    n = len(S)
    fig, ax = plt.subplots(figsize=(6, 4))
    for i in range(n):
        ax.add_patch(plt.Rectangle((i, 0.5), 0.9, 0.5, color=lab2rgb(ref)))
        ax.add_patch(plt.Rectangle((i, 0.0), 0.9, 0.5, color=lab2rgb(S[i])))
        ax.text(i + 0.45, -0.12, kq["Mẫu"].iloc[i], ha="center")
    ax.set_xlim(0, n)
    ax.set_ylim(-0.25, 1.05)
    ax.axis("off")
    ax.set_title("Hàng trên: màu chuẩn – hàng dưới: mẫu đo")
    st.pyplot(fig, clear_figure=True)

st.caption("ΔE00 phù hợp với cảm nhận thị giác hơn ΔE76. Ngưỡng dung sai tuỳ yêu cầu khách hàng/tiêu chuẩn "
           "(ví dụ ISO 12647-2 thường dùng ΔE*ab ≈ 5 cho màu đặc – bạn nên đối chiếu tiêu chuẩn của khoa).")
