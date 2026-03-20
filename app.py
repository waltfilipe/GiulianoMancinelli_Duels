import streamlit as st
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import pandas as pd
from streamlit_image_coordinates import streamlit_image_coordinates
from io import BytesIO
from PIL import Image
from matplotlib.lines import Line2D

# Configuração da página
st.set_page_config(layout="wide", page_title="Análise de Duelos")

st.title("Mapa de Duelos & Ações Defensivas")

# ==========================
# 1. Dados (Atualizados)
# ==========================
events_data = [
    ("DUEL WON", 41.71, 59.45, "videos/Duel Won 1.mp4"),
    ("DUEL LOST", 18.61, 41.16, "videos/Duel Lost 1.mp4"),
    ("DUEL WON", 7.14, 55.46, "videos/Duel Won 2.mp4"),
    ("AERIAL WON", 8.47, 43.82, "videos/Aeriel Won 1.mp4"),
    ("FOUL", 56.84, 57.79, "videos/Foul 1.mp4"),
    ("DUEL WON", 27.09, 73.08, "videos/Duel Won 3.mp4"),
    ("FOULED", 56.84, 67.10, "videos/Fouled 1.mp4"),
    ("DUEL WON", 16.78, 65.10, "videos/Duel Won 4.mp4"),
    ("DUEL WON", 20.44, 67.26, "videos/Duel Won 5.mp4"),
    ("AERIAL WON", 25.76, 67.43, "videos/Aeriel Won 2.mp4"),
    ("DUEL WON", 13.95, 36.51, "videos/Duel Won 6.mp4"),
    ("DUEL WON", 23.76, 50.14, "videos/Duel Won 7.mp4"),
    ("CLEARANCE", 19.77, 43.16, "videos/Clearance 1.mp4"),
    ("INTERCEPTION", 32.74, 49.48, "videos/Interception 1.mp4"),
    ("DUEL WON", 27.58, 63.11, "videos/Duel Won 8.mp4"),
    ("DUEL LOST", 15.62, 38.17, "videos/Duel Lost 2.mp4"),
    ("BLOCK", 14.62, 54.63, "videos/Block 1.mp4"),
    ("DUEL WON", 14.62, 58.29, "videos/Duel Won 9.mp4"),
    ("CLEARANCE", 13.95, 41.16, "videos/Clearance 2.mp4"),
    ("AERIAL LOST", 12.29, 45.98, "videos/Aeriel Lost 1.mp4"),
]

df = pd.DataFrame(events_data, columns=["type", "x", "y", "video"])

# ==========================
# 2. Função de Estilização
# ==========================
def get_style(tipo):
    if tipo == "DUEL LOST": return 'x', (1, 0, 0, 0.8), 120, 2.5
    elif tipo == "DUEL WON": return 'o', (0, 0.6, 0, 0.9), 120, 0.5
    elif tipo == "AERIAL WON": return '^', (0.2, 0.3, 1, 0.9), 140, 0.5
    elif tipo == "AERIAL LOST": return 'v', (1, 0, 0, 0.8), 140, 0.5
    elif tipo == "FOULED": return 's', (1, 0.6, 0, 0.9), 120, 0.5
    elif tipo == "FOUL": return 'P', (0.6, 0.2, 0.2, 0.9), 140, 0.5
    elif tipo == "INTERCEPTION": return 'D', (0.3, 0.3, 0.3, 0.9), 120, 0.5
    elif tipo == "CLEARANCE": return 'h', (0, 0.8, 0.8, 0.9), 140, 0.5
    elif tipo == "BLOCK": return 'p', (0.6, 0.1, 0.6, 0.9), 140, 0.5
    return 'o', 'gray', 100, 0.5

# Layout em duas colunas (Mapa | Info/Vídeo)
col1, col2 = st.columns([1, 1])

# ==========================
# 3. Visualização (Coluna da Esquerda)
# ==========================
with col1:
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#f5f5f5', line_color='#4a4a4a')
    fig, ax = pitch.draw(figsize=(10, 8))
    
    # Plotagem dos eventos no campo
    for _, row in df.iterrows():
        marker, color, size, lw = get_style(row["tipo"])
        pitch.scatter(row.x, row.y, marker=marker, s=size, color=color, 
                      edgecolors=color, linewidths=lw, ax=ax, zorder=3)

    # Legenda Customizada com Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Duel Won', markerfacecolor=(0, 0.6, 0), markersize=10),
        Line2D([0], [0], marker='x', color=(1, 0, 0), label='Duel Lost', markersize=10, lw=0),
        Line2D([0], [0], marker='^', color='w', label='Aerial Won', markerfacecolor=(0.2, 0.3, 1), markersize=10),
        Line2D([0], [0], marker='v', color='w', label='Aerial Lost', markerfacecolor=(1, 0, 0), markersize=10),
        Line2D([0], [0], marker='D', color='w', label='Interception', markerfacecolor=(0.3, 0.3, 0.3), markersize=10),
        Line2D([0], [0], marker='h', color='w', label='Clearance', markerfacecolor=(0, 0.8, 0.8), markersize=10),
        Line2D([0], [0], marker='p', color='w', label='Block', markerfacecolor=(0.6, 0.1, 0.6), markersize=10),
        Line2D([0], [0], marker='s', color='w', label='Fouled', markerfacecolor=(1, 0.6, 0), markersize=10),
        Line2D([0], [0], marker='P', color='w', label='Foul', markerfacecolor=(0.6, 0.2, 0.2), markersize=10),
    ]

    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0.02, 0.98),
              frameon=True, fontsize='small', framealpha=1.0, edgecolor='black', facecolor='white')

    ax.set_title("Defensive & Duel Analysis", fontsize=16, fontweight='bold')

    # Converter Matplotlib para Imagem
    buf = BytesIO()
    plt.savefig(buf, format="png", dpi=120, bbox_inches='tight')
    buf.seek(0)
    image = Image.open(buf)

    # Captura de cliques na imagem
    click = streamlit_image_coordinates(image, width=850)

# ==========================
# 4. Detalhes (Coluna da Direita)
# ==========================
with col2:
    st.subheader("Detalhes do Evento")
    if click:
        st.write(f"Você clicou na posição: **x={click['x']}, y={click['y']}**")
        st.info("Aqui você pode filtrar o dataframe ou carregar o vídeo correspondente à coordenada clicada.")
        # Exemplo: df_selecionado = df[(df.x-click.x).abs() < 2] ...
    else:
        st.write("Clique em um marcador no mapa para ver detalhes ou carregar o vídeo.")

    st.divider()
    st.dataframe(df, use_container_width=True)
  
# ==========================
# Coordinate Mapping Logic
# ==========================
selected_event = None

if click is not None:
    real_w, real_h = image.size
    disp_w, disp_h = click["width"], click["height"]
    
    pixel_x = click["x"] * (real_w / disp_w)
    pixel_y = click["y"] * (real_h / disp_h)
    
    mpl_pixel_y = real_h - pixel_y
    coords = ax.transData.inverted().transform((pixel_x, mpl_pixel_y))
    field_x, field_y = coords[0], coords[1]

    df["dist"] = np.sqrt((df["x"] - field_x)**2 + (df["y"] - field_y)**2)
    
    RADIUS = 5 # Slightly larger radius for easier clicking on smaller display
    candidates = df[df["dist"] < RADIUS]

    if not candidates.empty:
        selected_event = candidates.loc[candidates["dist"].idxmin()]

# ==========================
# Video Player (Right Col)
# ==========================
with col2:
    st.subheader("Video Analysis")
    if selected_event is not None:
        st.success(f"**Selected:** {selected_event['type']}")
        try:
            st.video(selected_event["video"])
        except:
            st.error("Video file not found.")
    else:
        st.info("Click on a marker to play.")
