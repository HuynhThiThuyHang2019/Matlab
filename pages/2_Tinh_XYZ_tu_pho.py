import streamlit as st
import colour
import pandas as pd
st.set_page_config(layout="wide")
st.write('## Tính giá trị 3 thành phần')
csv_file = st.sidebar.file_uploader("Upload a csv file", type=["csv"])
if csv_file is not None:
    df = pd.read_csv(csv_file, header = None)
    s = ''
    n = len(df)
    for i in range(0, 5):
        key = int(df.values[i,0])
        value = df.values[i,1]
        s = s + '%3d %8.4f\n' % (key, value)

    s = s + '...\n'

    for i in range(n-5, n):
        key = int(df.values[i,0])
        value = df.values[i,1]
        s = s + '%3d %8.4f\n' % (key, value)

    st.text(s)
    if st.button('Tính XYZ'):
        n = len(df)
        dict_data = {}
        for i in range(0, n):
            key = int(df.values[i,0])
            value = df.values[i,1]
            dict_data[key] = value

        sd = colour.SpectralDistribution(dict_data)
        cmfs = colour.MSDS_CMFS['CIE 1931 2 Degree Standard Observer']
        illuminant = colour.SDS_ILLUMINANTS['D65']

        # Calculating the sample spectral distribution *CIE XYZ* tristimulus values.
        XYZ = colour.sd_to_XYZ(sd, cmfs, illuminant)
        X = XYZ[0]
        Y = XYZ[1]
        Z = XYZ[2]
        s = 'X = %.2f, Y = %.2f, Z = %.2f' % (X, Y, Z)
        st.write(s)
 