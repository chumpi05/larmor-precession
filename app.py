import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import imageio
import io

# Constante giromagnética del protón (MHz/T)
GAMMA = 42.577478518  # MHz/T

st.title("⚛️ Precesión de Protones - Ley de Larmor")
st.write("Visualización interactiva del movimiento de precesión de los protones de Hidrógeno en un campo magnético principal B₀.")

# Entrada de valor para B0
B0 = st.number_input("Ingrese el valor del campo magnético B₀ (Tesla):", min_value=0.0, step=0.1, format="%.3f")

if st.button("Calcular y mostrar precesión"):
    if B0 > 0:
        # Frecuencia de Larmor en MHz
        omega = GAMMA * B0  # MHz
        st.write(f"**Frecuencia de precesión ω = {omega:.3f} MHz**")

        frames = 40  # número de imágenes en el gif
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

            # Eje z = campo B0
            ax.quiver(0, 0, 0, 0, 0, 1, color='r', linewidth=2, label="B₀")
            ax.plot([x], [y], [0], 'bo', markersize=10)

            buf = io.BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)
            images.append(imageio.imread(buf))
            plt.close(fig)

        # Guardar como GIF
        gif_buf = io.BytesIO()
        imageio.mimsave(gif_buf, images, format="GIF", duration=0.2)
        gif_buf.seek(0)

        st.image(gif_buf, caption="Precesión de protón alrededor de B₀", use_container_width=True)

    else:
        st.warning("Ingrese un valor de B₀ mayor que 0.")
