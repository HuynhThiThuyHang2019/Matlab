import streamlit as st
import matplotlib.pyplot as plt
import colour
import numpy as np
import scipy

st.set_page_config(layout="wide")

data = scipy.io.loadmat('halftone.mat')
W = data['W']
P = data['P']
P = np.vstack((W,P))
yellow = P[:11,:]
magenta = np.zeros((11,31), np.float64)
magenta[0,:] = P[0,:]
magenta[1,:] = P[11,:]
magenta[2,:] = P[22,:]
magenta[3,:] = P[33,:]
magenta[4,:] = P[44,:]
magenta[5,:] = P[55,:]
magenta[6,:] = P[66,:]
magenta[7,:] = P[77,:]
magenta[8,:] = P[88,:]
magenta[9,:] = P[99,:]
magenta[10,:] = P[110,:]

def ConvertToTristimulusValues(reflection, cmfs, illuminant):
    dict_reflection = {}
    n = len(reflection)
    for i in range(0, n):
        key = 400 + i*10
        dict_reflection[key] = reflection[i]
    sd = colour.SpectralDistribution(dict_reflection)
    # Calculating the sample spectral distribution *CIE XYZ* tristimulus values.
    XYZ = colour.sd_to_XYZ(sd, cmfs, illuminant)
    RGB = colour.XYZ_to_sRGB(XYZ/100)
    RGB = RGB*255
    return RGB.astype(np.uint8)

def gettrc(dig,R,W,Solid,n):
    num = len(dig)
    #--- Cong thuc (11.5)
    R = R**(1/n)
    W = W**(1/n)
    Solid = Solid**(1/n)
    c = np.zeros(num, np.float64)
    for i in range(0, num):
       c[i] = np.sum((Solid - R[i,:])*(Solid - W))/np.sum((Solid - W)*(Solid - W))
    c = 1-c
    p = np.polyfit(dig, c, 3)
    return c, p

chon_item = st.sidebar.radio("Chọn các mục sau", ("Ảnh trộn màu vàng và tím", 
                                                  "Phổ màu vàng và tím trên nền trắng",
                                                  "Đường cong tái tạo tông màu vàng và tím",
                                                  "Trộn hai màu vàng và tím"))
if chon_item == "Ảnh trộn màu vàng và tím":
    cmfs = colour.MSDS_CMFS['CIE 1931 2 Degree Standard Observer']
    illuminant = colour.SDS_ILLUMINANTS['D65']

    SIZE = 40
    image = np.zeros((SIZE*11, SIZE*11, 3), np.uint8)
    k = 0
    for x in range(0, 11):
        for y in range(0, 11):
            recflection = P[k]
            RGB = ConvertToTristimulusValues(recflection, cmfs, illuminant)
            image[x*SIZE:(x+1)*SIZE,y*SIZE:(y+1)*SIZE,:] = RGB
            k = k + 1
    # Đảo ngược hàng để vẽ - khi tính toán thì không cần phải đảo ngược
    image = image[::-1,:,:]
    _, col, _ = st.columns([1, 3, 1])
    with col:
        fig, ax = plt.subplots()        
        ax.imshow(image)
        xticks = list(range(20, 440, 40))
        yticks = list(range(20, 440, 40))
        plt.xticks(xticks, [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        plt.yticks(yticks, [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0])
        plt.xlabel('Yellow')
        plt.ylabel('Magenta')
        plt.title('Mix Yellow and Magenta Colors')
        st.pyplot(fig, clear_figure=True)
elif chon_item == "Phổ màu vàng và tím trên nền trắng":
    w = np.linspace(400, 700, 31)
    col1, col2 = st.columns(2)
    with col1:
        # Màu vàng nâu
        color = '#%02X%02X%02X' % (255, 128, 0)
        fig, ax = plt.subplots(figsize=(5,5))        
        for i in range(0, 11):
            plt.plot(w, yellow[i], color = color)
        plt.yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        plt.xlim((400,700))
        plt.xlabel('Bước sóng (nm)')
        plt.ylabel('Phổ phản xạ')
        plt.title('Phổ màu vàng trên nền trắng với a = 0:0.1:1')
        st.pyplot(fig, clear_figure=True)
    with col2:
        # Màu tím
        color = '#%02X%02X%02X' % (255, 0, 255)
        fig, ax = plt.subplots(figsize=(5,5))        
        for i in range(0, 11):
            plt.plot(w, magenta[i], color = color)
        plt.yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        plt.xlim((400,700))
        plt.xlabel('Bước sóng (nm)')
        plt.ylabel('Phổ phản xạ')
        plt.title('Phổ màu tím trên nền trắng với a = 0:0.1:1')
        st.pyplot(fig, clear_figure=True)
elif chon_item == "Đường cong tái tạo tông màu vàng và tím":
    n = 20
    a_target = np.linspace(0, 1, 11)
    col1, col2 = st.columns(2)
    with col1:
        a_actual, p = gettrc(a_target, yellow, yellow[0,:], yellow[10,:], n)
        x_ve = np.linspace(0,1,101)
        y_ve = np.polyval(p,x_ve)
        color = '#%02X%02X%02X' % (255,128,0)
        fig, ax = plt.subplots(figsize=(5,5))        
        plt.plot(a_target, a_actual, 'o', color = color)
        plt.plot(x_ve, y_ve, color = 'k')

        plt.xlabel('Giá trị mục tiêu của a')
        plt.ylabel('Giá trị thực tế của a')
        plt.title('Đường cong tái tạo tông màu vàng')
        st.pyplot(fig, clear_figure=True)

    with col2:
        a_actual, p = gettrc(a_target, magenta, magenta[0,:], magenta[10,:], n)
        x_ve = np.linspace(0,1,101)
        y_ve = np.polyval(p,x_ve)
        color = '#%02X%02X%02X' % (255,0,255)
        fig, ax = plt.subplots(figsize=(5,5))        
        plt.plot(a_target, a_actual, 'o', color = color)
        plt.plot(x_ve, y_ve, color = 'k')

        plt.xlabel('Giá trị mục tiêu của a')
        plt.ylabel('Giá trị thực tế của a')
        plt.title('Đường cong tái tạo tông màu tím')
        st.pyplot(fig, clear_figure=True)
elif chon_item == "Trộn hai màu vàng và tím":
    _, col, _ = st.columns([1, 3, 1])
    with col:
        pham_vi = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
        a_mag_target = st.number_input('Nhập mục tiêu a của màu tím [0:0.1:1]')
        a_yel_target = st.number_input('Nhập mục tiêu a của màu vàng [0:0.1:1]')
        if st.button('Dự báo'):
            if a_mag_target in pham_vi and a_yel_target in pham_vi:
                vi_tri_mag = pham_vi.index(a_mag_target)
                vi_tri_yel = pham_vi.index(a_yel_target)

                i = vi_tri_mag*11 + vi_tri_yel
                meas = P[i,:]
                n = 20
                a_target = np.linspace(0, 1, 11)
                _, p_mag = gettrc(a_target, magenta, magenta[0,:], magenta[10,:], n)
                _, p_yel = gettrc(a_target, yellow,  yellow[0,:],  yellow[10,:],  n)
                
                a_mag_actual = np.polyval(p_mag, a_mag_target)
                a_yel_actual = np.polyval(p_yel, a_yel_target)

                # get the areas using Dimechel
                Am = a_mag_actual*(1-a_yel_actual)
                Ay = a_yel_actual*(1-a_mag_actual)
                Aw = (1-a_mag_actual)*(1-a_yel_actual)
                Ao = a_mag_actual*a_yel_actual

                # get the colour of the overlap region
                overlap = P[120,:]
                WW = P[0,:]

                pred = np.zeros(31, np.float64)
                for w in range(0, 31):
                    pred[w]=(Am*(magenta[10,w])**(1/n) + Ay*(yellow[10,w])**(1/n) + Ao*(overlap[w])**(1/n) + Aw*(WW[w])**(1/n))**n
                wave = np.linspace(400,700,31)
                fig, ax = plt.subplots(figsize=(5,5))
                plt.plot(wave, meas, 'ro')
                plt.plot(wave, pred, 'b')
                plt.ylim([0, 1])
                plt.legend(['Giá trị mục tiêu', 'Giá trị dự báo'])
                plt.xlabel('Bước sóng (nm)')
                plt.ylabel('Phổ phản xạ')
                plt.title('Phổ phản xạ khi trộn hai màu tím và vàng\ncó tỷ lệ hạt trame a_mag = %.1f và a_yel = %.1f' % (a_mag_target, a_yel_target))
                st.pyplot(fig, clear_figure=True)
