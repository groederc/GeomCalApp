import streamlit as st
import pandas as pd
import numpy as npy
import matplotlib.pyplot as plt
import geolib as geo
# ---------------------------------------------------------------------------
def ejecutar(edited_df):
    n = edited_df.shape[0]
    st.markdown(f"Número de filas en la tabla {n}")
    if n == 0 or n == 1: return
    x = npy.zeros(n)
    y = npy.zeros(n)

    # Captura las coordenadas x, y.
    for i in range(n):
        x[i] = edited_df.loc[i,0]
        y[i] = edited_df.loc[i,1]
        #st.markdown(f"Xi:{x[i]}")
        #st.markdown(f"Yi:{y[i]}")
    
    # Grafica la figura
    #st.subheader("Gráfica de la figura")
    #st.line_chart(edited_df, x="X", y="Y")
    #fig,ax = plt.subplots(figsize=(2, 4))
    fig,ax = plt.subplots()
    plt.figure(figsize=(1, 1))
    ax.tick_params(axis='both', labelsize=4, color='red')

    ax.set_aspect('equal')
    #fig.patch.set_alpha(0)
    #fig.set_facecolor("none")
    #fig.set_figwidth(4)
    #fig.set_figheight(1)

    ax.set_title("Gráfica de la figura")
    ax.plot(x,y)
    st.pyplot(fig)
    
    # Calcula propiedades geométricas
    Area,Xg,Yg,Ix,Iy,Ixy,Ixg,Iyg,Ixyg = geo.calculaPropiedadesCentroidales(x,y)
    str0  = "Propiedades respecto a ejes originales\n"
    str1 = "Area ={0:10.3e},  Xg ={1:10.3e},   Yg ={2:10.3e}\n".format(Area,Xg,Yg)
    str2 = "I_x  ={0:10.3e}, Iy ={1:10.3e}, Ixy ={2:10.3e}\n".format(Ix,Iy,Ixy)
        
    str0g = "\n\nPropiedades respecto a ejes centroidales\n"
    str1g = "Ixg  ={0:10.3e}, Iyg ={1:10.3e}, Ixyg ={2:10.3e}\n".format(Ixg,Iyg,Ixyg)

    phi,Imax,Imin = geo.calculaInerciasPrincipales(Ixg,Iyg,Ixyg)
    str0p = "\n\nPropiedades principales\n"
    str1p = "I1  ={0:10.3e}, I2 ={1:10.3e}, phi ={2:10.3f}\n".format(Imax,Imin,phi)

    # Imprime los resultados
    ss = str0 + str1 + str2 + str0g + str1g + str0p + str1p

    st.subheader("Resultados")
    st.text(ss)
# ---------------------------------------------------------------------------
def main():
    st.header("Cálculo de propiedades geométricas de figuras planas, FIC-UCOL (2025)")
    st.subheader("Tabla de coordenadas de nudos")
    st.text("Introducir las coordenadas de los vértices de la figura en sentido antihorario.\
             \nPara cerrar la figura, incluir al final el primer vértice.\
         \nEl programa automáticamente calcula los valores al ir introduciendo datos.\n\
             \n\nAutores:\n\
                 Dr. Guillermo M. Roeder Carbo\n\
                 Dr. Agustín Orduña Bustamante\n\
                 Dr. Alfredo Sánchez Alejandre.\n")

    st.markdown("### Tabla de coordenadas de vértices de la figura")
    df0 = pd.DataFrame([{"X": 0.0, "Y": 0.0}])
    edited_df = st.data_editor(df0, num_rows="dynamic")
    #button_ejecutar = st.button("Ejecutar", type="primary",on_click=ejecutar(edited_df))
    button_ejecutar = st.button("Ejecutar",type="primary",on_click=ejecutar(edited_df),disabled=True)
# ---------------------------------------------------------------------------
if __name__=="__main__":
    main()
# ---------------------------------------------------------------------------
