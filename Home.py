import os
import streamlit as st

st.set_page_config(page_title="Khoa học màu sắc", page_icon="🎨", layout="wide")

BASE = os.path.dirname(os.path.abspath(__file__))


def show_logo(filename, caption):
    path = os.path.join(BASE, "assets", filename)
    if os.path.exists(path):
        st.image(path, width=160)
    else:
        st.info(f"Chưa có {filename} trong thư mục assets/")


c1, c2, c3 = st.columns([1, 4, 1])
with c1:
    show_logo("logo_truong.png", "Logo trường")
with c2:
    st.markdown(
        "<h1 style='text-align:center;'>KHOA HỌC MÀU SẮC</h1>"
        "<h4 style='text-align:center;'>Ứng dụng Matlab trong công nghệ in</h4>"
        "<p style='text-align:center;'>Trường Đại học Công Nghệ Kỹ thuật TP.HCM – Khoa In và Truyền thông</p>",
        unsafe_allow_html=True,
    )
with c3:
    show_logo("logo_khoa.png", "Logo khoa")

st.divider()
st.markdown(
    """
### Nội dung trang web
| STT | Nội dung |
|---|---|
| 1 | Chuyển đổi không gian màu sRGB ⇄ XYZ |
| 2 | Tính giá trị X, Y, Z từ file phổ đo |
| 3 | Biểu đồ CIE 1931 hình móng ngựa |
| 4 | Gamut màu của thiết bị RGB |
| 5 | Gamut màu của máy in từ file gamut |
| 6 | Đặc tính hoá máy in nửa tông |
| 7 | **Kiểm tra sai lệch màu Delta E** |
| 8 | **Chuyển đổi đa không gian màu** |
| 9 | **Phổ phản xạ dưới nhiều nguồn sáng** |

Chọn từng trang ở thanh bên trái.
"""
)
st.caption("Sinh viên thực hiện: Huỳnh Thị Thúy Hằng – MSSV 23458001")
