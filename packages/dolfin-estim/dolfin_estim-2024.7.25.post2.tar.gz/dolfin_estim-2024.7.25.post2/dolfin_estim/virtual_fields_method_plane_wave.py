import fire
import dolfin
import math
from scipy import optimize


import dolfin_mech as dmech
import dolfin_estim as destimation

def VFM_plane_waves(nu=0.3, mesh_size=0.1, cube_params={}, refine=False, delta=1.2, load_params={}, load_type="body_force", noise=0, noise_from_images=False, regul=0.0, regul_number=0.0, run=1, u_params=None, res_basename="./"):
    if noise_from_images:
        U_meas, mesh, boundaries_mf=destimation.get_disp_field_and_mesh_from_images(refine=refine, noise=noise, mesh_size=mesh_size, regul=regul, run=run, load_type=load_type, regul_number=regul_number, cube_params=cube_params)
    else:
        U_meas, mesh, boundaries_mf=destimation.compute_displacement_field(refine=refine, noise=noise, mesh_size=mesh_size, load_params=load_params, cube_params=cube_params, u_params=u_params, res_basename=res_basename)
    kinematics = dmech.Kinematics(U=U_meas)
    dV = dolfin.Measure(
        "dx",
        domain=mesh)
    dS = dolfin.Measure(
        "exterior_facet",
        domain=mesh,
        subdomain_data=boundaries_mf)
    U_fe = dolfin.VectorElement(
        family='CG',
        cell=mesh.ufl_cell(),
        degree=1)
    U_fs = dolfin.FunctionSpace(
        mesh,
        U_fe)
    u_test = get_test_function(u_fct=U_fs, delta=delta)
    if load_type=="body_force":
        W_ext=dolfin.assemble(dolfin.inner(dolfin.Constant([load_params.get("f", 0.3),0.]), u_test) * kinematics.J * dV)
    else:
        N = dolfin.FacetNormal(mesh)
        T = - dolfin.dot(load_params.get("f", 0.3) * N, dolfin.inv(kinematics.F))
        W_ext = dolfin.assemble(dolfin.inner(T, u_test) * kinematics.J * dS(2))
    dE=dolfin.derivative(kinematics.E, U_meas, u_test)
    Sigma_div_byE = 1/2*nu/(1+nu)/(1-2*nu)*(kinematics.J*kinematics.J-1)*dolfin.inv(kinematics.C) + 1/2*1/(1+nu)*(kinematics.I-dolfin.inv(kinematics.C))
    W_int_div_byE=dolfin.inner(Sigma_div_byE, dE)
    E=W_ext/dolfin.assemble(W_int_div_byE*dV)
    return(E)


def get_test_function(u_fct=None, delta=1.2):
    u_test=dolfin.Function(u_fct)
    U_expr = dolfin.Expression(
        ("sin(k*((x[0]-0.2)))",
         "sin(k*((x[0]-0.2)))"),
        k=2*math.pi/delta,
        element=u_fct.ufl_element())
    u_test.interpolate(U_expr)
    return(u_test)


if (__name__ == "__main__"):
    fire.Fire(VFM_plane_waves)