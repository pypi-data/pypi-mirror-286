import moapy.project.wgsd.wgsd_flow as wgsd_flow
import concreteproperties.results as res

from moapy.project.wgsd.wgsd_flow import Material, Geometry, PMOptions, DgnCodeUS, DgnCodeEU
from moapy.auto_convert import auto_schema, MBaseModel
from concreteproperties.concrete_section import ConcreteSection
from pydantic import Field as dataclass_field

class AxialForceOpt(MBaseModel):
    """
    Moment Interaction Curve
    """
    Nx: float = dataclass_field(default=0.0, description="Axial Force")

    class Config:
        title = "Axial Force Option"

@auto_schema
def calc_rc_mm_interaction_curve(material: Material, geometry: Geometry, opt: PMOptions, axialforce: AxialForceOpt) -> res.BiaxialBendingResults:
    """
    Moment Interaction Curve
    """
    pm = wgsd_flow.get_dgncode(opt.dgncode)
    comp = pm.calc_compound_section(material, geometry, opt)
    if type(comp) is ConcreteSection:
        return comp.biaxial_bending_diagram(n=axialforce.Nx)

    return ''

class ThetaOpt(MBaseModel):
    """
    AxialMoment Interaction Curve
    """
    theta: float = dataclass_field(default=0.0, description="theta")

    class Config:
        title = "Theta Option"

@auto_schema
def calc_rc_pm_interaction_curve(material: Material, geometry: Geometry, opt: PMOptions, theta: ThetaOpt) -> res.MomentInteractionResults:
    """
    Axial Moment Interaction Curve
    """
    pm = wgsd_flow.get_dgncode(opt.dgncode)
    comp = pm.calc_compound_section(material, geometry, opt)
    if type(comp) is ConcreteSection:
        return comp.moment_interaction_diagram(theta=theta.theta)

    return ''

@auto_schema
def calc_rc_uls_stress(material: Material, geometry: Geometry, opt: PMOptions, theta: ThetaOpt, axialForce: AxialForceOpt):
    """
    reinforced concrete ultimate stress
    """
    pm = wgsd_flow.get_dgncode(opt.dgncode)
    comp = pm.calc_compound_section(material, geometry, opt)
    if type(comp) is ConcreteSection:
        ultimate_results = comp.ultimate_bending_capacity(theta=theta.theta, n=axialForce.Nx)
        return comp.calculate_ultimate_stress(ultimate_results)

    return ''

@auto_schema
def calc_rc_cracked_stress(material: Material, geometry: Geometry, opt: PMOptions, theta: ThetaOpt, axialForce: AxialForceOpt):
    """
    reinforced concrete ultimate stress
    """
    pm = wgsd_flow.get_dgncode(opt.dgncode)
    comp = pm.calc_compound_section(material, geometry, opt)
    if type(comp) is ConcreteSection:
        ultimate_results = comp.calculate_cracked_properties(theta=theta.theta, n=axialForce.Nx)
        return comp.calculate_cracked_stress(ultimate_results)

    return ''

result = calc_rc_uls_stress(wgsd_flow.Material(), wgsd_flow.Geometry(), wgsd_flow.PMOptions(), ThetaOpt(), AxialForceOpt())
result.plot_stress()