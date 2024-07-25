import moapy.project.wgsd.wgsd_flow as wgsd_flow
import concreteproperties.results as res

from moapy.project.wgsd.wgsd_flow import Material, Geometry, PMOptions, Lcom
from moapy.auto_convert import auto_schema, MBaseModel
from concreteproperties.concrete_section import ConcreteSection
from pydantic import Field as dataclass_field

class DgnCode(MBaseModel):
    """
    DgnCode
    """
    name: str = dataclass_field(default="", description="DgnCode")

    class Config:
        title = "DgnCode"

class AxialForceOpt(MBaseModel):
    """
    Moment Interaction Curve
    """
    Nx: float = dataclass_field(default=0.0, description="Axial Force")

    class Config:
        title = "Axial Force Option"

@auto_schema
def calc_rc_mm_interaction_curve(material: Material, geometry: Geometry, opt: PMOptions, axialforce: AxialForceOpt):
    """
    Moment Interaction Curve
    """
    pm = wgsd_flow.get_dgncode(opt.dgncode)
    comp = pm.calc_compound_section(material, geometry, opt)
    if type(comp) is ConcreteSection:
        return comp.biaxial_bending_diagram(n=axialforce.Nx)

    return ''

class AngleOpt(MBaseModel):
    """
    Angle Option
    """
    theta: float = dataclass_field(default=0.0, description="theta")

    class Config:
        title = "Theta Option"

class ElasticModulusOpt(MBaseModel):
    """
    Elastic Modulus Option
    """
    E: float = dataclass_field(default=200.0, description="Elastic Modulus")

    class Config:
        title = "Elastic Modulus Option"

@auto_schema
def calc_rc_pm_interaction_curve(material: Material, geometry: Geometry, opt: PMOptions, angle: AngleOpt):
    """
    Axial Moment Interaction Curve
    """
    pm = wgsd_flow.get_dgncode(opt.dgncode)
    comp = pm.calc_compound_section(material, geometry, opt)
    if type(comp) is ConcreteSection:
        return comp.moment_interaction_diagram(theta=angle.theta)

    return ''

@auto_schema
def calc_rc_uls_stress(material: Material, geometry: Geometry, code: DgnCode, theta: AngleOpt, axialForce: AxialForceOpt):
    """
    reinforced concrete ultimate stress
    """
    pm = wgsd_flow.get_dgncode(code.name)
    comp = pm.calc_compound_section(material, geometry)
    if type(comp) is ConcreteSection:
        ultimate_results = comp.ultimate_bending_capacity(theta=theta.theta, n=axialForce.Nx)
        return comp.calculate_ultimate_stress(ultimate_results)

    return ''

@auto_schema
def calc_rc_uls_bending_capacity(material: Material, geometry: Geometry, code: DgnCode, theta: AngleOpt, axialForce: AxialForceOpt):
    """
    reinforced concrete ultimate bending capacity
    """
    pm = wgsd_flow.get_dgncode(code.name)
    comp = pm.calc_compound_section(material, geometry)
    if type(comp) is ConcreteSection:
        return comp.ultimate_bending_capacity(theta=theta.theta, n=axialForce.Nx)

    return ''

@auto_schema
def calc_rc_cracked_stress(material: Material, geometry: Geometry, code: DgnCode, lcom: Lcom):
    """
    reinforced concrete cracked stress
    """
    pm = wgsd_flow.get_dgncode(code.name)
    comp = pm.calc_compound_section(material, geometry)
    if type(comp) is ConcreteSection:
        cracked_res = comp.calculate_cracked_properties(theta=0.0)
        return comp.calculate_cracked_stress(cracked_res, n=lcom.f.Nz, m=lcom.f.Mx)

    return ''

@auto_schema
def calc_rc_cracked_properties(material: Material, geometry: Geometry):
    sect = wgsd_flow.MSection(material, geometry)
    comp_sect = sect.calc_compound_section()
    return comp_sect.calculate_cracked_properties()

@auto_schema
def calc_rc_uncracked_stress(material: Material, geometry: Geometry, lcb: Lcom):
    sect = wgsd_flow.MSection(material, geometry)
    comp_sect = sect.calc_compound_section()
    return comp_sect.calculate_uncracked_stress(n=lcb.f.Nz, m_x=lcb.f.Mx, m_y=lcb.f.My)

@auto_schema
def calc_rc_moment_curvature(material: Material, geometry: Geometry):
    sect = wgsd_flow.MSection(material, geometry)
    comp_sect = sect.calc_compound_section()
    return comp_sect.moment_curvature_analysis()

@auto_schema
def calc_extreme_bar(material: Material, geometry: Geometry, angle: AngleOpt):
    sect = wgsd_flow.MSection(material, geometry)
    comp_sect = sect.calc_compound_section()
    return comp_sect.extreme_bar(theta=angle.theta)

@auto_schema
def calc_cracking_moment(material: Material, geometry: Geometry, angle: AngleOpt):
    sect = wgsd_flow.MSection(material, geometry)
    comp_sect = sect.calc_compound_section()
    return comp_sect.calculate_cracking_moment(theta=angle.theta)

@auto_schema
def calc_gross_properties(material: Material, geometry: Geometry):
    sect = wgsd_flow.MSection(material, geometry)
    comp_sect = sect.calc_compound_section()
    return comp_sect.get_gross_properties()

@auto_schema
def calc_transformed_gross_properties(material: Material, geometry: Geometry, m: ElasticModulusOpt):
    sect = wgsd_flow.MSection(material, geometry)
    comp_sect = sect.calc_compound_section()
    return comp_sect.get_transformed_gross_properties(m.E)

# result = calc_gross_properties(material=wgsd_flow.Material(), geometry=wgsd_flow.Geometry(), angle=AngleOpt(theta=0.0))
# result = calc_transformed_gross_properties(material=wgsd_flow.Material(), geometry=wgsd_flow.Geometry(), m=ElasticModulusOpt())
# print(result)