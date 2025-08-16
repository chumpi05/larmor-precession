import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import imageio
import io

# Constante giromagnética del protón (MHz/T)
GAMMA = 42.577478518  # MHz/T

st.title("⚛️ Comparativa de Precesión - Ley de Larmor")
st.write("Visualización de la precesión de los protones de Hidrógeno con **dos valores distintos de B₀**, junto con un gráfico comparativo de la frecuencia de Larmor.")

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
    gif_buf = io.BytesIO()
    imageio.mimsave(gif_buf, images, format="GIF", duration=0.2)
    gif_buf.seek(0)

    return gif_buf, omega

if st.button("Start"):
    if B0_1 > 0 and B0_2 > 0:
        # Generar GIFs
        gif1, omega1 = generar_gif(B0_1)
        gif2, omega2 = generar_gif(B0_2)

        col1, col2 = st.columns(2)

        with col1:
            st.image(gif1, caption=f"Precesión con B₀₁ = {B0_1:.3f} T (ω = {omega1:.3f} MHz)", use_container_width=True)

        with col2:
            st.image(gif2, caption=f"Precesión con B₀₂ = {B0_2:.3f} T (ω = {omega2:.3f} MHz)", use_container_width=True)

        # --- Comparación en 2D ---
        st.subheader("📊 Comparativa de Frecuencia de Larmor vs Campo Magnético")

        # Rango de B0 para la curva
        B_vals = np.linspace(0, max(B0_1, B0_2) * 1.2, 100)
        omega_vals = GAMMA * B_vals  # MHz

        fig2, ax2 = plt.subplots()
        ax2.plot(B_vals, omega_vals, 'b-', label="ω = γ·B₀")
        ax2.scatter([B0_1, B0_2], [omega1, omega2], color="red", zorder=5)
        ax2.set_xlabel("Campo magnético B₀ (Tesla)")
        ax2.set_ylabel("Frecuencia de precesión ω (MHz)")
        ax2.set_title("Relación lineal entre ω y B₀")
        ax2.legend()
        ax2.grid(True)

        st.pyplot(fig2)

    else:
        st.warning("Ingrese valores de B₀ mayores que 0 en ambos campos.")


