import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon as ShapelyPolygon
from shapely.ops import unary_union

# ==========================================
# 1. CORE SIMULATION LOGIC
# ==========================================

def build_service_area_polygon(choice, inputs):
    if choice == 'Rectangle':
        W = inputs['W']
        H = inputs['H']
        return ShapelyPolygon([(0, 0), (W, 0), (W, H), (0, H)])
    else:
        return ShapelyPolygon(inputs['vertices'])

def create_single_hex_poly(cx, cy, R):
    angles =[np.pi / 6 + i * np.pi / 3 for i in range(6)]
    points =[(cx + R * np.cos(a), cy + R * np.sin(a)) for a in angles]
    return ShapelyPolygon(points)

def generate_hex_grid_over_polygon(service_poly, R):
    x_step = np.sqrt(3) * R
    y_step = 1.5 * R
    
    minx, miny, maxx, maxy = service_poly.bounds
    min_col = int(minx / x_step) - 2
    max_col = int(maxx / x_step) + 2
    min_row = int(miny / y_step) - 2
    max_row = int(maxy / y_step) + 2
    
    centers = []
    hex_polys =[]
    
    for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
            cx = col * x_step
            cy = row * y_step
            if row % 2 != 0:
                cx += x_step / 2.0
                
            hex_poly = create_single_hex_poly(cx, cy, R)
            if hex_poly.intersects(service_poly):
                centers.append((cx, cy))
                hex_polys.append(hex_poly)
                
    return centers, hex_polys

def compute_coverage_metrics(service_poly, hex_polys, R):
    total_cells = len(hex_polys)
    target_area = service_poly.area
    theoretical_hex_area = 1.5 * np.sqrt(3) * (R ** 2)
    
    combined_hexes = unary_union(hex_polys)
    covered_region_inside = combined_hexes.intersection(service_poly)
    covered_area_inside = covered_region_inside.area
    
    coverage_ratio = covered_area_inside / target_area if target_area > 0 else 0
    
    return {
        'total_cells': total_cells,
        'service_area': target_area,
        'single_hex_area': theoretical_hex_area,
        'covered_area_inside': covered_area_inside,
        'coverage_ratio': coverage_ratio
    }

def plot_layout(service_poly, hex_polys, centers, metrics, R, shape_type):
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Plot Hexagons
    for hp in hex_polys:
        x, y = hp.exterior.xy
        ax.fill(x, y, facecolor='lightblue', edgecolor='black', alpha=0.5, linewidth=1)
        
    # Plot Cell Centers
    if centers:
        cx, cy = zip(*centers)
        ax.scatter(cx, cy, color='red', marker='.', s=20, zorder=3, label='Cell Centers')
        
    # Plot Service Area Boundary
    if service_poly.geom_type == 'Polygon':
        polys_to_plot = [service_poly]
    else:
        polys_to_plot = service_poly.geoms
        
    for i, poly in enumerate(polys_to_plot):
        x, y = poly.exterior.xy
        label = 'Service Area' if i == 0 else None
        ax.plot(x, y, color='red', linestyle='--', linewidth=2.5, zorder=4, label=label)
        
    ax.set_aspect('equal')
    plt.grid(True, linestyle=':', alpha=0.6)
    
    minx, miny, maxx, maxy = service_poly.bounds
    pad = R * 2
    ax.set_xlim(minx - pad, maxx + pad)
    ax.set_ylim(miny - pad, maxy + pad)
    
    title_str = (
        f"Hexagonal Cell Layout over {shape_type}\n"
        f"Radius (R) = {R} | Total Cells = {metrics['total_cells']} | "
        f"Coverage = {metrics['coverage_ratio']*100:.1f}%"
    )
    plt.title(title_str, fontsize=14, pad=15)
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.legend(loc='upper right')
    
    return fig

# ==========================================
# 2. STREAMLIT WEB UI
# ==========================================

st.set_page_config(page_title="Hex Cell Simulator", layout="wide")

st.title("📡 Wireless Communication Hex Simulator")
st.markdown("Design and visualize cellular hexagonal grid layouts over various geographic spaces.")

# Sidebar for User Inputs
st.sidebar.header("⚙️ Simulation Parameters")

# Shape Selection
shape_choice = st.sidebar.radio(
    "Select Service Area Type:",
    ('Rectangle', 'Regular Polygon', 'Geographic Map Outline')
)

shape_inputs = {}

if shape_choice == 'Rectangle':
    st.sidebar.markdown("**Rectangle Setup**")
    W = st.sidebar.number_input("Width (W)", min_value=1.0, value=200.0, step=10.0)
    H = st.sidebar.number_input("Height (H)", min_value=1.0, value=150.0, step=10.0)
    shape_inputs = {'W': W, 'H': H, 'type': 'Rectangle'}

elif shape_choice == 'Regular Polygon':
    st.sidebar.markdown("**Polygon Setup**")
    N = st.sidebar.number_input("Number of Sides (N)", min_value=3, value=6, step=1)
    
    center_x, center_y = 250, 250
    poly_radius = 200
    vertices =[]
    for i in range(N):
        angle = 2 * np.pi * i / N
        x = center_x + poly_radius * np.cos(angle)
        y = center_y + poly_radius * np.sin(angle)
        vertices.append((x, y))
        
    shape_inputs = {'vertices': vertices, 'type': f'Regular {N}-Sided Polygon'}

elif shape_choice == 'Geographic Map Outline':
    st.sidebar.markdown("**Geographic Map Setup**")
    st.sidebar.info("Using a pre-programmed irregular shape approximating real geographic area.")
    shape_inputs['vertices'] =[
        (90, 300), (120, 350), (100, 380), (110, 410), (150, 420), 
        (160, 460), (200, 460), (220, 440), (250, 450), (280, 420), 
        (300, 430), (320, 400), (350, 390), (380, 400), (400, 390), 
        (420, 360), (450, 340), (460, 300), (430, 280), (420, 250), 
        (440, 220), (380, 200), (350, 210), (320, 180), (300, 120), 
        (260, 80), (250, 40), (210, 30), (200, 60), (170, 80), 
        (180, 120), (150, 150), (120, 150), (110, 180), (130, 210), 
        (90, 240), (60, 270)
    ]
    shape_inputs['type'] = 'Ethiopia Map Outline'

# Radius Input
st.sidebar.markdown("---")
st.sidebar.markdown("**Cell Setup**")
R = st.sidebar.number_input("Cell Radius (R)", min_value=0.1, value=20.0, step=1.0, 
                            help="Recommended: 0.5 - 20 (or 15-30 for the geographic map)")

# Action Button
generate_btn = st.sidebar.button("🚀 Generate Layout")

# Main Page Execution
if generate_btn or 'simulated' not in st.session_state:
    st.session_state['simulated'] = True
    
    with st.spinner("Generating Layout..."):
        # Run logic
        service_poly = build_service_area_polygon(shape_choice, shape_inputs)
        centers, hex_polys = generate_hex_grid_over_polygon(service_poly, R)
        metrics = compute_coverage_metrics(service_poly, hex_polys, R)
        fig = plot_layout(service_poly, hex_polys, centers, metrics, R, shape_inputs['type'])
        
        # Display Metrics Dashboard
        st.subheader("📊 Simulation Results")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Cell Count", f"{metrics['total_cells']}")
        col2.metric("Target Service Area", f"{metrics['service_area']:,.2f} sq units")
        col3.metric("Coverage Ratio", f"{metrics['coverage_ratio']*100:.2f} %")
        
        col4, col5 = st.columns(2)
        col4.metric("Theoretical Single Hex Area", f"{metrics['single_hex_area']:,.2f} sq units")
        col5.metric("Covered Area (Strictly Inside)", f"{metrics['covered_area_inside']:,.2f} sq units")
        
        st.markdown("---")
        
        # Display Plot
        st.subheader("🗺️ Layout Visualization")
        st.pyplot(fig)

st.sidebar.markdown("---")
st.sidebar.caption("Project 1: Hexagonal Cell Planning and Cluster Layout")
