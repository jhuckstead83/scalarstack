import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Cone Volume Visualizer", layout="centered")

st.title("Cone Volume Visualizer")
st.write("""
Starting with "Tip Up", adjust the fill height of liquid inside the cone and flip it to see how the volume-height changes based on orientation.
Despite the volume staying the same, the perceived fill height changes drastically when the cone is flipped!
""")

# Input slider for volume
fill_fraction = st.slider("Liquid Fill Height (fraction of full cone)", min_value=0.01, max_value=0.99, value=0.33, step=0.01)
flip_cone = st.checkbox("Flip Cone (Tip Up)", value=True)

# Compute height of fill level based on fill_fraction
fill_height = 1 - fill_fraction  # Logic flip for filling from base-up.

# Cone parameters
radius = 1
height = 1

# Mesh for cone
theta = np.linspace(0, 2 * np.pi, 50)
z = np.linspace(0, height, 50)
Theta, Z = np.meshgrid(theta, z)
R = (Z / height) * radius
X = R * np.cos(Theta)
Y = R * np.sin(Theta)

# Flip cone logic
if flip_cone:
    Z = -Z + 1  # Move tip to bottom and base to top
    fill_z = fill_fraction  # Adjust fill height visually
else:
    fill_z = (1 - (fill_height ** 3)) ** (1 / 3)

# Liquid surface disk
theta_disk = np.linspace(0, 2 * np.pi, 100)
if flip_cone:
    x_disk = fill_height * np.cos(theta_disk)
    y_disk = fill_height * np.sin(theta_disk)
else:
    x_disk = fill_z * np.cos(theta_disk)
    y_disk = fill_z * np.sin(theta_disk)
z_disk = np.full_like(theta_disk, fill_z)

# Mesh for filled volume
if flip_cone:
    fill_z_vals = np.linspace(0, fill_height, 25)
else:
    fill_z_vals = np.linspace(0, fill_z, 25)

Theta_fill, Z_fill = np.meshgrid(theta, fill_z_vals)
R_fill = (Z_fill / height) * radius
X_fill = R_fill * np.cos(Theta_fill)
Y_fill = R_fill * np.sin(Theta_fill)

if flip_cone:
    Z_fill = -Z_fill + 1
    cone_colorscale = [[0, '#003f5c'], [1, '#0077be']]  # blue cone
    liquid_colorscale = [[0, 'white'], [1, '#ADD8E6']]  # white fill
else:
    cone_colorscale = [[0, 'white'], [1, '#ADD8E6']]  # white cone
    liquid_colorscale = [[0, '#003f5c'], [1, '#0077be']]  # blue fill
    
if flip_cone:
    cone_opacity = 0.95
    fill_opacity = 0.25
else:
    cone_opacity = 0.25
    fill_opacity = 0.95


# Plotly 3D figure
fig = go.Figure()

# Cone surface
fig.add_trace(go.Surface(
    x=X, y=Y, z=Z,
    colorscale=cone_colorscale,
    opacity=cone_opacity,
    showscale=False,
    name='Cone'))

# Filled volume
fig.add_trace(go.Surface(
    x=X_fill, y=Y_fill, z=Z_fill,
    colorscale=liquid_colorscale,
    opacity=fill_opacity,
    showscale=False,
    name='Filled Volume'))


# Liquid surface
fig.add_trace(go.Scatter3d(
    x=x_disk, y=y_disk, z=z_disk,
    mode='lines', line=dict(color='red', width=5),
    name='Liquid Surface'))

fig.update_layout(
    scene=dict(
        xaxis_title='X', yaxis_title='Y', zaxis_title='Height',
        zaxis=dict(range=[-1, 1], autorange=False),
        aspectmode='cube'
    ),
    margin=dict(l=0, r=0, b=0, t=0),
    height=600
)

st.plotly_chart(fig, use_container_width=True)

