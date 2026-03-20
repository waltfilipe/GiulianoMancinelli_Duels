import streamlit as st
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import pandas as pd

st.set_page_config(layout="wide")

st.title("Defensive & Duel Map")

# ==========================
# Eventos
# ==========================
eventos = [
    ("DUEL WON", 41.71, 59.45),
    ("DUEL LOST", 18.61, 41.16),
    ("DUEL WON", 7.14, 55.46),
    ("AERIAL WON", 8.47, 43.82),
    ("FOUL", 56.84, 57.79),
    ("DUEL WON", 27.09, 73.08),
    ("FOULED", 56.84, 67.10),
    ("DUEL WON", 16.78, 65.10),
    ("DUEL WON", 20.44, 67.26),
    ("AERIAL WON", 25.76, 67.43),
    ("DUEL WON", 13.95, 36.51),
    ("DUEL WON", 23.76, 50.14),
    ("CLEARANCE", 19.77, 43.16),
    ("INTERCEPTION", 32.74, 49.48),
    ("DUEL WON", 27.58, 63.11),
    ("DUEL LOST", 15.62, 38.17),
    ("BLOCK", 14.62, 54.63),
    ("DUEL WON", 14.62, 58.29),
    ("CLEARANCE", 13.95, 41.16),
    ("AERIAL LOST", 12.29, 45.98)
]

df = pd.DataFrame(eventos, columns=["tipo", "x", "y"])

# ==========================
# Campo
# ==========================
pitch = Pitch(
    pitch_type='statsbomb',
    pitch_color='#f5f5f5',
    line_color='#4a4a4a'
)

fig, ax = pitch.draw(figsize=(10, 6))

# ==========================
# Plot
# ==========================
for _, row in df.iterrows():
    
    lw = 0.5
    size = 120

    if row["tipo"] == "DUEL LOST":
        marker = 'x'
        color = (1, 0, 0, 0.8)
        lw = 2.5

    elif row["tipo"] == "DUEL WON":
        marker = 'o'
        color = (0, 0.6, 0, 0.9)

    elif row["tipo"] == "AERIAL WON":
        marker = '^'
        color = (0.2, 0.3, 1, 0.9)
        size = 140
        
    elif row["tipo"] == "AERIAL LOST":
        marker = 'v'
        color = (1, 0, 0, 0.8)
        size = 140

    elif row["tipo"] == "FOULED":
        marker = 's'
        color = (1, 0.6, 0, 0.9)

    elif row["tipo"] == "FOUL":
        marker = 'P'
        color = (0.6, 0.2, 0.2, 0.9)
        size = 140

    elif row["tipo"] == "INTERCEPTION":
        marker = 'D'
        color = (0.3, 0.3, 0.3, 0.9)

    elif row["tipo"] == "CLEARANCE":
        marker = 'h'
        color = (0, 0.8, 0.8, 0.9)
        size = 140
        
    elif row["tipo"] == "BLOCK":
        marker = 'p'
        color = (0.6, 0.1, 0.6, 0.9)
        size = 140

    pitch.scatter(
        row.x,
        row.y,
        marker=marker,
        s=size,
        color=color,
        edgecolors=color,
        linewidths=lw,
        ax=ax,
        zorder=3
    )

# ==========================
# Legenda
# ==========================
ax.scatter([], [], marker='o', color=(0, 0.6, 0), label='Duel Won')
ax.scatter([], [], marker='x', color=(1, 0, 0), label='Duel Lost')
ax.scatter([], [], marker='^', color=(0.2, 0.3, 1), label='Aerial Won')
ax.scatter([], [], marker='v', color=(1, 0, 0), label='Aerial Lost')
ax.scatter([], [], marker='D', color=(0.3, 0.3, 0.3), label='Interception')
ax.scatter([], [], marker='h', color=(0, 0.8, 0.8), label='Clearance')
ax.scatter([], [], marker='p', color=(0.6, 0.1, 0.6), label='Block')
ax.scatter([], [], marker='s', color=(1, 0.6, 0), label='Fouled')
ax.scatter([], [], marker='P', color=(0.6, 0.2, 0.2), label='Foul')

ax.legend(
    loc='upper left',
    bbox_to_anchor=(1.02, 1),
    framealpha=1.0,
    facecolor='white',
    edgecolor='black',
    title="Eventos",
    fontsize=10
)

# ==========================
# Attack Direction Arrow
# ==========================
pitch.arrows(
    40, 85, 60, 85,
    color='#4a4a4a',
    width=1.5,
    headwidth=4,
    headlength=5,
    ax=ax,
    clip_on=False
)

ax.text(
    50, 88,
    'ATTACK DIRECTION',
    ha='center',
    va='center',
    fontsize=9,
    color='#4a4a4a',
    fontweight='bold'
)

# ==========================
# Título
# ==========================
plt.title("Defensive & Duel Map", fontsize=16, fontweight='bold', pad=15)

plt.tight_layout()

# ==========================
# Streamlit render
# ==========================
st.pyplot(fig, use_container_width=True)
