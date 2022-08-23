# Pegar ponto na frequencia e no tempo
# tamanho em y a gosto
# fonte gaussiana
# gif
# script pro prof.
# por no git


import meep as mp
import matplotlib.pyplot as plt


pml_thickness = 1.0
# y size of our cell
y_size = 3
# x size of our cell, not including pml
x_raw = 6
# x size of our cell, including pml
x_size = x_raw + pml_thickness * 2

# size of the cell in x and y, with z = 0
cell = mp.Vector3(x_size, y_size, 0)

wg_width = 0.5

# imagem do microplastico passando -> parametros de espalhamento

# here we define the format and position of our waveguide, as well as the epsilon
geometry = [
    mp.Block(
        mp.Vector3(wg_width, y_size, mp.inf),
        center=mp.Vector3(),
        material=mp.Medium(epsilon=9),
    )
]

# f = c  / lambda, where c is the speed of light and normalized to 1
# the waveguide has to to half the wavelenth so that it is single mode
# my_frequency = 1.0 / (10 ** 6)  # 10 ** 6
my_frequency = 1.0

# the gaussian source is centered close to the edge, with a space of 1 to the pml
# sources = [
#     mp.Source(
#         mp.ContinuousSource(frequency=my_frequency),
#         component=mp.Ez,
#         size=mp.Vector3(0, y_size, 0),
#         # center=mp.Vector3(-x_raw - 0.5, 0),
#         center=mp.Vector3(-x_raw / 2.0 + 0.5, 0),
#     )
# ]
sources = [
    mp.EigenModeSource(
        src=mp.GaussianSource(my_frequency, fwidth=0.2 * my_frequency),
        center=mp.Vector3(-x_raw / 2.0 + 0.5, 0),
        size=mp.Vector3(y=y_size),
        eig_match_freq=True,
        eig_parity=mp.ODD_Z + mp.EVEN_Y,
    )
]

pml_layers = [mp.PML(pml_thickness, direction=mp.X)]

resolution = 50

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

mon_pt = mp.Vector3(x_raw / 2.0 - wg_width, 0)

# taxa de amostragem
sim.run(
    mp.at_beginning(mp.output_epsilon),
    mp.to_appended("ey", mp.at_every(0.6, mp.output_efield_z)),
    until=200,
    # until_after_sources=mp.stop_when_fields_decayed(50, mp.Ez, mon_pt, 2.78e-15),
)

# eps_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Dielectric)
# plt.figure()
# plt.imshow(eps_data.transpose(), interpolation="spline36", cmap="binary")
# plt.axis("on")
# plt.savefig("waveguide_Dielectric.png")

# ey_data = sim.get_array(center=mp.Vector3(), size=cell, component=mp.Ey)
# plt.figure()
# plt.imshow(eps_data.transpose(), interpolation="spline36", cmap="binary")
# plt.imshow(ey_data.transpose(), interpolation="spline36", cmap="RdBu", alpha=0.9)
# plt.axis("on")
# plt.savefig("waveguide_ey.png")

#  python meep_testing.py; sudo h5topng -t 0:329 -R -Zc dkbluered -a yarg -A meep_testing-eps-000000.00.h5 meep_testing-ez.h5; convert meep_testing-ez.t*.png challange.gif; rm meep_testing-ez.t*.png -f;
#  python challenge.py; sudo h5topng -t 0:329 -R -Zc dkbluered -a yarg -A challenge-eps-000000.00.h5 challenge-ez.h5; convert challenge-ez.t*.png ez.gif; rm challenge-ez.t*.png -f;
