#!/usr/bin/env python
#-*- coding:utf-8 -*-
# ----------------------------------------------------------------------------
import io
import geolib as geo
import matplotlib.pyplot as plt
import numpy as npy
import openpyxl
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter
import pandas as pd
import streamlit as st
from weasyprint import HTML


# ---------------------------------------------------------------------------
# GENERACIÓN DE ARCHIVOS EN MEMORIA (EXCEL Y PDF)
# ---------------------------------------------------------------------------
def generar_excel(datos):
    output = io.BytesIO()
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Propiedades"

    header_fill = PatternFill("solid", fgColor="1F497D")
    section_fill = PatternFill("solid", fgColor="DCE6F1")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    section_font = Font(name="Calibri", size=11, bold=True, color="1F497D")

    ws["A1"] = "REPORTE DE PROPIEDADES GEOMÉTRICAS - FIC-UCOL"
    ws["A1"].font = Font(name="Calibri", size=14, bold=True, color="1F497D")

    ws.append([])
    ws.append(["Propiedad", "Símbolo", "Valor"])

    for col in range(1, 4):
        cell = ws.cell(row=3, column=col)
        cell.fill = header_fill
        cell.font = header_font

    filas = [
        ("Ejes Originales", "", ""),
        ("Área", "A", datos["Area"]),
        ("Centroide X", "Xg", datos["Xg"]),
        ("Centroide Y", "Yg", datos["Yg"]),
        ("Inercia X", "Ix", datos["Ix"]),
        ("Inercia Y", "Iy", datos["Iy"]),
        ("Producto Inercia XY", "Ixy", datos["Ixy"]),
        ("Ejes Centroidales", "", ""),
        ("Inercia Centroidal X", "Ixg", datos["Ixg"]),
        ("Inercia Centroidal Y", "Iyg", datos["Iyg"]),
        ("Producto Inercia Centroidal", "Ixyg", datos["Ixyg"]),
        ("Ejes Principales", "", ""),
        ("Inercia Principal Máx", "I1", datos["Imax"]),
        ("Inercia Principal Mín", "I2", datos["Imin"]),
        ("Ángulo Principal", "φ (°)", datos["phi"]),
    ]

    for item in filas:
        ws.append(list(item))
        r = ws.max_row
        if item[1] == "":
            ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
            ws.cell(row=r, column=1).fill = section_fill
            ws.cell(row=r, column=1).font = section_font
        else:
            cell_val = ws.cell(row=r, column=3)
            cell_val.number_format = (
                "0.000E+00"
                if abs(cell_val.value) > 1000 or (0 < abs(cell_val.value) < 0.01)
                else "0.000"
            )

    for col in ws.columns:
        max_len = max(len(str(cell.value or "")) for cell in col)
        ws.column_dimensions[get_column_letter(col[0].column)].width = max(
            max_len + 4, 12
        )

    wb.save(output)
    return output.getvalue()


def generar_pdf(datos):
    html_str = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        @page {{ size: A4; margin: 15mm; background-color: #f8fafc; }}
        body {{ font-family: sans-serif; color: #1e293b; font-size: 10pt; }}
        .header {{ background-color: #1e3a8a; color: white; padding: 15px; border-radius: 6px; margin-bottom: 20px; }}
        .header h2 {{ margin: 0; }}
        .header p {{ margin: 5px 0 0 0; opacity: 0.8; font-size: 9pt; }}
        .title {{ font-weight: bold; color: #1e3a8a; border-bottom: 2px solid #3b82f6; margin-top: 15px; padding-bottom: 3px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 8px; background: white; }}
        th, td {{ padding: 6px 10px; border-bottom: 1px solid #e2e8f0; text-align: left; }}
        th {{ background: #f1f5f9; }}
        .num {{ text-align: right; font-family: monospace; font-weight: bold; }}
    </style>
    </head>
    <body>
        <div class="header">
            <h2>Reporte de Propiedades Geométricas</h2>
            <p>FIC-UCOL (2025)</p>
        </div>

        <div class="title">📍 Ejes Originales</div>
        <table>
            <tr><th>Propiedad</th><th>Símbolo</th><th style="text-align:right;">Valor</th></tr>
            <tr><td>Área</td><td>A</td><td class="num">{datos['Area']:.3e}</td></tr>
            <tr><td>Centroide X</td><td>Xg</td><td class="num">{datos['Xg']:.3e}</td></tr>
            <tr><td>Centroide Y</td><td>Yg</td><td class="num">{datos['Yg']:.3e}</td></tr>
            <tr><td>Inercia X</td><td>Ix</td><td class="num">{datos['Ix']:.3e}</td></tr>
            <tr><td>Inercia Y</td><td>Iy</td><td class="num">{datos['Iy']:.3e}</td></tr>
            <tr><td>Producto Inercia XY</td><td>Ixy</td><td class="num">{datos['Ixy']:.3e}</td></tr>
        </table>

        <div class="title">🎯 Ejes Centroidales</div>
        <table>
            <tr><th>Propiedad</th><th>Símbolo</th><th style="text-align:right;">Valor</th></tr>
            <tr><td>Inercia Centroidal X</td><td>Ixg</td><td class="num">{datos['Ixg']:.3e}</td></tr>
            <tr><td>Inercia Centroidal Y</td><td>Iyg</td><td class="num">{datos['Iyg']:.3e}</td></tr>
            <tr><td>Producto Inercia Centroidal</td><td>Ixyg</td><td class="num">{datos['Ixyg']:.3e}</td></tr>
        </table>

        <div class="title">📐 Ejes Principales</div>
        <table>
            <tr><th>Propiedad</th><th>Símbolo</th><th style="text-align:right;">Valor</th></tr>
            <tr><td>Inercia Principal Máxima</td><td>I1</td><td class="num">{datos['Imax']:.3e}</td></tr>
            <tr><td>Inercia Principal Mínima</td><td>I2</td><td class="num">{datos['Imin']:.3e}</td></tr>
            <tr><td>Ángulo Principal</td><td>φ</td><td class="num">{datos['phi']:.2f}°</td></tr>
        </table>
    </body>
    </html>
    """
    output = io.BytesIO()
    HTML(string=html_str).write_pdf(output)
    return output.getvalue()


# ---------------------------------------------------------------------------
# LÓGICA Y CÁLCULOS
# ---------------------------------------------------------------------------
def ejecutar(edited_df):
    n = edited_df.shape[0]
    st.markdown(f"**Número de filas en la tabla:** {n}")

    if n < 2:
        st.warning(
            "Se requieren al menos 2 puntos para calcular las propiedades."
        )
        return

    # Captura de coordenadas X e Y vectorizada (Soluciona KeyError)
    try:
        x = edited_df.iloc[:, 0].to_numpy(dtype=float)
        y = edited_df.iloc[:, 1].to_numpy(dtype=float)
    except IndexError:
        st.error(
            "La tabla debe contener al menos 2 columnas numéricas (X e Y)."
        )
        return

    # Grafica la figura
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(x, y, marker="o", linestyle="-", color="#1f77b4")
    ax.set_aspect("equal")
    ax.set_title("Gráfica de la figura", fontsize=11, fontweight="bold")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True, linestyle="--", alpha=0.5)

    st.pyplot(fig)
    plt.close(fig)

    # Calcula propiedades geométricas
    Area, Xg, Yg, Ix, Iy, Ixy, Ixg, Iyg, Ixyg = (
        geo.calculaPropiedadesCentroidales(x, y)
    )
    phi, Imax, Imin = geo.calculaInerciasPrincipales(Ixg, Iyg, Ixyg)

    # Impresión interactiva con st.metric
    st.subheader("Resultados")

    st.markdown("#### 📍 Propiedades respecto a ejes originales")
    c1, c2, c3 = st.columns(3)
    c1.metric("Área", f"{Area:.3e}")
    c2.metric("Centroide X (Xg)", f"{Xg:.3e}")
    c3.metric("Centroide Y (Yg)", f"{Yg:.3e}")

    c4, c5, c6 = st.columns(3)
    c4.metric("Inercia Ix", f"{Ix:.3e}")
    c5.metric("Inercia Iy", f"{Iy:.3e}")
    c6.metric("Producto Inercia Ixy", f"{Ixy:.3e}")

    st.divider()

    st.markdown("#### 🎯 Propiedades respecto a ejes centroidales")
    cg1, cg2, cg3 = st.columns(3)
    cg1.metric("Inercia Ixg", f"{Ixg:.3e}")
    cg2.metric("Inercia Iyg", f"{Iyg:.3e}")
    cg3.metric("Producto Inercia Ixyg", f"{Ixyg:.3e}")

    st.divider()

    st.markdown("#### 📐 Propiedades principales")
    cp1, cp2, cp3 = st.columns(3)
    cp1.metric("Inercia Máx (I1)", f"{Imax:.3e}")
    cp2.metric("Inercia Mín (I2)", f"{Imin:.3e}")
    cp3.metric("Ángulo Principal (φ)", f"{phi:.2f}°")

    # Exportación a Excel / PDF
    datos_calculados = {
        "Area": Area,
        "Xg": Xg,
        "Yg": Yg,
        "Ix": Ix,
        "Iy": Iy,
        "Ixy": Ixy,
        "Ixg": Ixg,
        "Iyg": Iyg,
        "Ixyg": Ixyg,
        "Imax": Imax,
        "Imin": Imin,
        "phi": phi,
    }

    excel_bytes = generar_excel(datos_calculados)
    pdf_bytes = generar_pdf(datos_calculados)

    st.divider()
    st.subheader("📥 Exportar Resultados")
    col_dl1, col_dl2 = st.columns(2)

    with col_dl1:
        st.download_button(
            label="📊 Descargar en Excel (.xlsx)",
            data=excel_bytes,
            file_name="Reporte_Propiedades_Geometricas.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )

    with col_dl2:
        st.download_button(
            label="📄 Descargar en PDF (.pdf)",
            data=pdf_bytes,
            file_name="Reporte_Propiedades_Geometricas.pdf",
            mime="application/pdf",
            use_container_width=True,
        )


# ---------------------------------------------------------------------------
# INTERFAZ PRINCIPAL
# ---------------------------------------------------------------------------
def main():
    st.header(
        "Cálculo de propiedades geométricas de figuras planas, FIC-UCOL (2025)"
    )
    st.subheader("Tabla de coordenadas de nudos")
    st.text(
        "Introducir las coordenadas de los vértices de la figura en sentido"
        " antihorario.\nPara cerrar la figura, incluir al final el primer"
        " vértice.\nEl programa automáticamente calcula los valores al ir"
        " introduciendo datos.\n\nAutor:\n Dr. Guillermo M. Roeder Carbo (2026)"
    )

    st.markdown("### Tabla de coordenadas de vértices de la figura")
    df0 = pd.DataFrame([{"X": 0.0, "Y": 0.0}])
    edited_df = st.data_editor(df0, num_rows="dynamic")

    # Botón de ejecución usando evaluación directa
    if st.button("Ejecutar", type="primary"):
        ejecutar(edited_df)


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
