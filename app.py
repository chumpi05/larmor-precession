import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import imageio
import io

# Constante giromagnética del protón (MHz/T)
GAMMA = 42.577478518  # MHz/T

st.title("⚛️ Comparativa de Precesión - Ley de Larmor")
st.write("Visualización de la precesión de los protones de Hidrógeno con **dos valores distintos de B₀**.")

# Entradas para dos valores de B0
B0_1 = st.number_input("Ingrese el primer valor del campo magnético B₀₁ (Tesla):", min_value=0.0, step=0.1, format="%.3f")
B0_2 = st.number_input("Ingrese el segundo valor del campo magnético B₀₂ (Tesla):", min_value=0.0, step=0.1, format="%.3f")

def generar_gif(B0, frames=40):
    """Genera un gif de la precesión para un valor de B0."""
    omega = GAMMA * B0  # MHz
    radius = 1.0
    t = np.linspace(0, 2*np.pi, frames)

    images = []
    for i in range(frames):
        x = radius * np.cos(omega * 1e6 * t[i] / frames)
        y = radius * np.sin(omega * 1e6 * t[i] / frames)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.set_xlim([-1.2, 1.2])
        ax.set_ylim([-1.2, 1.2])
        ax.set_zlim([-1.2, 1.2])
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        # Campo B0 en eje Z
        ax.quiver(0, 0, 0, 0, 0, 1, color='r', linewidth=2, label="B₀")
        ax.plot([x], [y], [0], 'bo', markersize=10)

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        images.append(imageio.imread(buf))
        plt.close(fig)

    # Guardar como GIF
    gif_buf_

