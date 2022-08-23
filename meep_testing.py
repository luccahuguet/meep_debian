# meep_testing.py
# From the Meep tutorial: plotting permittivity and fields of a straight waveguide

import meep as mp
import numpy as np
import matplotlib.pyplot as plt

my_y = 3

cell = mp.Vector3(16, 8, 0)

geometry = [
    mp.Block(
        mp.Vector3(mp.inf, 1, mp.inf),
        center=mp.Vector3(),
        material=mp.Medium(epsilon=12),
    )
]

# geometry = [
#     mp.Block(
#         mp.Vector3(-0.25, mp.inf, 0.25),
#         center=mp.Vector3(2, 0, 0),
#         material=mp.Medium(epsilon=9),
#     )
# ]

sources = [
    mp.Source(
        mp.ContinuousSource(frequency=0.15), component=mp.Ez, center=mp.Vector3(1, 0)
    )
]

pml_layers = [mp.PML(2.0)]

resolution = 10

sim = mp.Simulation(
    cell_size=cell,
    boundary_layers=pml_layers,
    geometry=geometry,
    sources=sources,
    resolution=resolution,
)

# sim.run(until=50)

sim.run(
    mp.at_beginning(mp.output_epsilon),
    mp.to_appended("ez", mp.at_every(0.6, mp.output_efield_z)),
    until=50,
)

# eps_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Dielectric)
# plt.figure()
# plt.imshow(eps_data.transpose(), interpolation="spline36", cmap="binary")
# plt.axis("on")
# plt.savefig("waveguide_Dielectric.png")

# ez_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ey)
# plt.figure()
# plt.imshow(eps_data.transpose(), interpolation="spline36", cmap="binary")
# plt.imshow(ez_data.transpose(), inteSrpolation="spline36", cmap="RdBu", alpha=0.9)
# plt.axis("on")
# plt.savefig("waveguide_ez2.png")
