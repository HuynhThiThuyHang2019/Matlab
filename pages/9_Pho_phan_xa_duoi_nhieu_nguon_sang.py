import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.io
import streamlit as st
import colour

st.set_page_config(layout="wide")
st.write("## Màu của mẫu in dưới các nguồn sáng khác nhau")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = scipy.io.loadmat(os.path.join(ROOT, "halftone.mat"))
P = np.vstack((data["W"], data["P"]))          # 121 x 31 (400-700 nm, bước 10 nm)
wl = np.arange(400, 701, 10)

shape = colour.SpectralShape(400, 700, 10)
cmfs = colour.MSDS_CMFS["CIE 1931 2 Degree Standard Observer"].copy().align(shape)
ILLS = ["D65", "D50", "A", "FL2"]
TEN = {"D65": "D65 (ánh sáng ngày)", "D50": "D50 (chuẩn ngành in)",
       "A": "A (đèn sợi đốt)", "FL2": "FL2 (đèn huỳnh quang)"}


def nhan(k):
    return "Vàng %d%% – Tím %d%%" % ((k % 11) * 10, (k // 11) * 10)


def tinh(refl, ten):
    ill = colour.SDS_ILLUMINANTS[ten].copy().align(shape)
    sd = colour.SpectralDistribution(dict(zip(wl, refl)))
    trang = colour.SpectralDistribution(dict(zip(wl, np.ones(len(wl)))))
    XYZ = colour.sd_to_XYZ(sd, cmfs, ill) / 100
    xyw = colour.XYZ_to_xy(colour.sd_to_XYZ(trang, cmfs, ill) / 100)
    Lab = colour.XYZ_to_Lab(XYZ, illuminant=xyw)
    rgb = np.clip(colour.XYZ_to_sRGB(XYZ, illuminant=xyw, chromatic_adaptation_transform="Bradford"), 0, 1)
    return Lab, rgb


c1, c2 = st.columns(2)
kA = c1.selectbox("Mẫu A", range(121), index=60, format_func=nhan)
kB = c2.selectbox("Mẫu B", range(121), index=70, format_func=nhan)

kq = {}
for ten in ILLS:
    kq[ten] = (tinh(P[kA], ten), tinh(P[kB], ten))

fig, axes = plt.subplots(1, 2, figsize=(11, 3.6), gridspec_kw={"width_ratios": [2, 1.4]})
ax = axes[0]
for i, ten in enumerate(ILLS):
    (_, rA), (_, rB) = kq[ten]
    ax.add_patch(plt.Rectangle((i * 1.1, 0), 0.5, 1, color=rA))
    ax.add_patch(plt.Rectangle((i * 1.1 + 0.5, 0), 0.5, 1, color=rB))
    ax.text(i * 1.1 + 0.5, -0.12, ten, ha="center")
ax.set_xlim(-0.1, len(ILLS) * 1.1)
ax.set_ylim(-0.25, 1.05)
ax.axis("off")
ax.set_title("Mẫu A (trái) và mẫu B (phải) dưới từng nguồn sáng")
axes[1].plot(wl, P[kA], "r", label="A: " + nhan(kA))
axes[1].plot(wl, P[kB], "b", label="B: " + nhan(kB))
axes[1].set_xlabel("Bước sóng (nm)")
axes[1].set_ylabel("Phổ phản xạ")
axes[1].set_ylim(0, 1)
axes[1].legend(fontsize=7)
fig.tight_layout()
st.pyplot(fig, clear_figure=True)

hang = []
for ten in ILLS:
    (LA, _), (LB, _) = kq[ten]
    hang.append({"Nguồn sáng": TEN[ten],
                 "Lab mẫu A": "%.1f, %.1f, %.1f" % tuple(LA),
                 "Lab mẫu B": "%.1f, %.1f, %.1f" % tuple(LB),
                 "ΔE00 (A–B)": round(float(colour.delta_E(LA, LB, method="CIE 2000")), 2)})
st.dataframe(pd.DataFrame(hang), hide_index=True)
st.info("Nếu ΔE00 giữa hai mẫu thay đổi mạnh khi đổi nguồn sáng, hai mẫu có thể là cặp đồng màu dị phổ "
        "(metamerism): giống nhau dưới nguồn sáng này nhưng khác nhau dưới nguồn sáng khác.")
