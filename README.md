# Hex_sim
Project 1: Hexagonal Cell Planning & Cluster Layout
Development Summary & Roadmap
1. Project Overview
This project is a simulation tool designed to model and visualize wireless communication cellular networks. It generates pointy-top hexagonal cell grids over various geographical service areas, computing key network metrics such as total cell count, theoretical cell area, and coverage ratios.
2. Incremental Development (What We Have Built)
The simulator was developed in iterative phases, evolving from a basic script to a fully deployed, zero-dependency web application:
Phase 1: Core Mathematical Grid
Developed the foundational geometry to generate mathematically perfect "pointy-top" hexagons. Implemented staggered row logic (
x
_
s
t
e
p
=
3
R
x_step= 
3
​
 R
, 
y
_
s
t
e
p
=
1.5
R
y_step=1.5R
) to create a seamless, non-overlapping tessellation over a standard rectangular area.
Phase 2: Advanced Geometry & Metrics
Integrated the shapely library to handle complex geometric operations. This allowed the simulator to calculate strict mathematical unions and intersections, accurately determining the exact coverage area strictly inside the service boundaries.
Phase 3: Dynamic Service Areas
Expanded the simulator to support diverse geographic limits:
Standard Rectangles (Width 
×
×
 Height).
Regular Polygons (User-defined 
N
N
-sided equal polygons).
A custom, pre-programmed irregular map outline (modeled after the geographic borders of Ethiopia).
Phase 4: Web UI & Cloud Deployment
Migrated the project from a command-line interface (CLI) to a modern graphical user interface (GUI) using Streamlit. The application was successfully containerized and deployed to the Streamlit Community Cloud, allowing users to interact with the model via a simple URL with zero software dependencies.
3. Current System Assumptions
At this current stage, the simulator operates under idealized mathematical conditions:
Zero Overlap: Cells perfectly tessellate without overlapping, representing a purely theoretical grid rather than actual radio frequency (RF) signal propagation.
Margin Bleed: The system includes any cell that intersects the service area boundary. As a result, coverage naturally "bleeds" outside the perimeter of the target zone, resulting in a calculated coverage ratio that safely hits 100% at the cost of "wasted" area outside the borders.
4. Next Steps & Future Enhancements
To transition the simulator from a geometric model to a highly realistic RF planning tool, the following features will be implemented in the next phase:
1. Realistic Cell Overlap:
Real-world antennas do not create hard hexagonal boundaries; RF signals propagate in overlapping circles. We will introduce an "overlap factor" where cell radii are expanded slightly to ensure continuous signal handoff, computing the exact percentage of overlapping interference areas.
2. Strict Boundary & Margin Handling:
Refining the edge logic to minimize "wasted" coverage outside the target polygon. This may involve clipping cell edges, utilizing smaller "micro-cells" at the borders, or implementing directional sectoring to conform strictly to geographic boundaries.
3. Cluster Layout & Frequency Reuse (Project Phase 2):
Implementing cellular clustering logic to assign frequency channels/colors to the grid. We will introduce variable reuse factors (e.g., 
N
=
3
,
4
,
7
N=3,4,7
) to visualize co-channel interference distances and evaluate spectrum efficiency across the service area.
