# Pegar ponto na frequencia e no tempo
# tamanho em y a gosto
# fonte gaussiana
# gif
# script pro prof.
# por no git


import meep as mp

scale = 5

pml_thickness = 1.0 * scale
# y size of our cell
y_size = 3 * scale
# x size of our cell, not including pml
x_raw = 6 * scale
# x size of our cell, including pml
x_size = x_raw + pml_thickness * 2

# size of the cell in x and y, with z = 0
cell = mp.Vector3(x_size, y_size, 0)

# here we define the format and position of our waveguide, as well as the epsilon
geometry = [
    mp.Block(
        mp.Vector3(0.5 * scale, y_size, mp.inf),
        center=mp.Vector3(),
        material=mp.Medium(epsilon=9),
    )
]

# f = c  / lambda, where c is the speed of light and normalized to 1
# the waveguide has to to half the wavelenth so that it is single mode
# my_frequency = 1.0 / (10 ** 6)  # 10 ** 6
my_frequency = 1.0

# the gaussian source is centered close to the edge, with a space of 1 to the pml
sources = [
    mp.Source(
        mp.GaussianSource(frequency=my_frequency),
        component=mp.Ez,
        # center=mp.Vector3(-x_raw / 2.0 - 0.5, 0),
        center=mp.Vector3(-x_raw + (0.5 * scale), 0),
    )
]

pml_layers = [mp.PML(pml_thickness, direction=mp.X)]

resolution = 10

sim = mp.Simulation(
    cell_size=cell,
    boundary_layers=pml_layers,
    geometry=geometry,
    sources=sources,
    resolution=resolution,
)

# periodicidade infinita em y
sim.set_boundary(side=mp.Low, direction=mp.Y, condition=mp.Metallic)
sim.set_boundary(side=mp.High, direction=mp.Y, condition=mp.Metallic)

# taxa de amostragem
sim.run(
    mp.at_beginning(mp.output_epsilon),
    mp.to_appended("challenge2", mp.at_every(0.6, mp.output_efield_z)),
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

#  python meep_testing.py; sudo h5topng -t 0:329 -R -Zc dkbluered -a yarg -A meep_testing-eps-000000.00.h5 meep_testing-ez.h5; convert meep_testing-ez.t*.png ez.gif; rm meep_testing-ez.t*.png -f;
#  python challenge.py; sudo h5topng -t 0:329 -R -Zc dkbluered -a yarg -A challenge-eps-000000.00.h5 challenge-ez.h5; convert challenge-ez.t*.png ez.gif; rm challenge-ez.t*.png -f;
