import numpy as np
from sectionproperties.pre.library import rectangular_section

from concreteproperties import (
    Concrete,
    ConcreteLinear,
    ConcreteSection,
    RectangularStressBlock,
    SteelBar,
    SteelElasticPlastic,
    add_bar_rectangular_array,
)
from concreteproperties.results import BiaxialBendingResults

concrete = Concrete(
    name="40 MPa Concrete",
    density=2.4e-6,
    stress_strain_profile=ConcreteLinear(elastic_modulus=32.8e3),
    ultimate_stress_strain_profile=RectangularStressBlock(
        compressive_strength=40,
        alpha=0.79,
        gamma=0.87,
        ultimate_strain=0.003,
    ),
    flexural_tensile_strength=3.8,
    colour="lightgrey",
)

steel = SteelBar(
    name="500 MPa Steel",
    density=7.85e-6,
    stress_strain_profile=SteelElasticPlastic(
        yield_strength=500,
        elastic_modulus=200e3,
        fracture_strain=0.05,
    ),
    colour="grey",
)

col = rectangular_section(d=350, b=600, material=concrete)

# add bars to column
geom = add_bar_rectangular_array(
    geometry=col,
    area=450,
    material=steel,
    n_x=6,
    x_s=492 / 5,
    n_y=3,
    y_s=121,
    anchor=(54, 54),
    exterior_only=True,
)

conc_sec = ConcreteSection(geom)
# conc_sec.plot_section()

n_list = np.linspace(0, 7400e3, 5)
biaxial_results = []

for n in n_list:
    biaxial_results.append(
        conc_sec.biaxial_bending_diagram(n=n, n_points=24, progress_bar=True)
    )
    
BiaxialBendingResults.plot_multiple_diagrams_3d(biaxial_results)