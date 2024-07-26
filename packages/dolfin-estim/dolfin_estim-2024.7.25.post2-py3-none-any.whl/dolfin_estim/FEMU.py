import dolfin
import scipy
import fire
from scipy import optimize

import dolfin_mech as dmech
import dolfin_estim as destimation


def FEMU(nu=0.3, mesh_size=0.1, refine=False, noise=0, cube_params={}, load_params={}, load_type="body_force", noise_from_images=False, regul=0.0, regul_number=0.0, run=1):
    if noise_from_images:
        U, mesh, boundaries_mf=destimation.get_disp_field_and_mesh_from_images(refine=refine, noise=noise, mesh_size=mesh_size, regul=regul, run=run, load_type=load_type, regul_number=regul_number, cube_params=cube_params)
    else:
        U, mesh, boundaries_mf=destimation.compute_displacement_field(refine=refine, noise=noise, mesh_size=mesh_size, load_params=load_params, cube_params=cube_params)
    dV = dolfin.Measure(
        "dx",
        domain=mesh)
    V0 = dolfin.assemble(dolfin.Constant(1)*dV)
    U_norm=(1/2*dolfin.assemble(dolfin.inner(U, U)*dV)/2/V0)**(1/2)
    if not bool(cube_params):
        cube_params = {"X0":0.2, "Y0":0.2, "X1":0.8, "Y1":0.8, "l":mesh_size} 
    sol = scipy.optimize.minimize(J_FEMU, [0.5], args=(nu, U, U_norm, refine, load_params, cube_params), method="Nelder-Mead")
    return(sol.x[0])

def J_FEMU(x, nu, u_meas, u_meas_norm, refine, load_params, cube_params):
    mat_params={"model":"CGNH", "parameters":{"E":x[0], "nu":nu}}
    step_params = {"dt_ini":1/20}
    const_params = {"type":"blox"}
    if refine:
        cube_params["refine"]=True
    else:
        cube_params["refine"]=False
    u, v = dmech.run_RivlinCube_Hyperelasticity(
                dim                                    = 2                                 ,
                cube_params                            = cube_params                       ,
                mat_params                             = mat_params                        ,
                step_params                            = step_params                       ,
                const_params                           = const_params                      ,
                load_params                            = load_params                       ,
                get_results                            = 1                                 ,
                res_basename                           = "./")
    U_err = u.copy(deepcopy=True)

    U_err.vector()[:] -= u_meas.vector()[:]
    J = (dolfin.assemble(dolfin.inner(U_err,U_err)*v)/2/dolfin.assemble(dolfin.Constant(1)*v))/u_meas_norm
    return(J)


if (__name__ == "__main__"):
    fire.Fire(FEMU)
