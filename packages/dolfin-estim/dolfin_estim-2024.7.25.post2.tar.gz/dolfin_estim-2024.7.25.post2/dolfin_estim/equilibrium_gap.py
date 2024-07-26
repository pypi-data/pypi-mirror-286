import fire
import numpy
import scipy
import dolfin
from scipy import optimize


import dolfin_estim as destimation
import dolfin_mech as dmech
import dolfin_warp as dwarp

def EGM(nu=0.3, mesh_size=0.1, cube_params={}, refine=False, load_params={}, load_type="body_force", noise_from_images=False, noise=0, regul=0.0, regul_number=0.0, run=1):
    if noise_from_images:
        U, mesh, boundaries_mf = destimation.get_disp_field_and_mesh_from_images(refine=refine, noise=noise, mesh_size=mesh_size, regul=regul, run=run, load_type=load_type, regul_number=regul_number, cube_params=cube_params)
    else:
        U, mesh, boundaries_mf = destimation.compute_displacement_field(refine=refine, noise=noise, mesh_size=mesh_size, load_params=load_params, cube_params=cube_params)
    params = {
        "E":1.,  # kPa
        "nu":nu} # [-]
    mat_params = {
        "model":"CGNH",
        "parameters":params}
    problem = dwarp.WarpingProblem(
        mesh=mesh,
        U_family="Lagrange",
        U_degree=1)
    problem.U = U
    #### defining the forces applied
    if load_type=="body_force":
        surface_forces=[]
        volume_forces = [[load_params.get("f", 0.3), 0]]
    else:
        dS = dolfin.Measure(
            "exterior_facet",
            domain=mesh,
            subdomain_data=boundaries_mf)
        surface_forces=[[load_params.get("f", 0.3), dS(2)]]
        volume_forces = []
    E = launching_optimization(problem, mat_params["parameters"], mat_params["model"], surface_forces, volume_forces, load_type, nu)
    return(E)

def launching_optimization(problem, material_parameters, material_model, surface_forces, volume_forces, load_type, nu):
    init = [numpy.log(0.9)]
    initialisation_estimation = {"E":0.9}
    # print("pb1")
    sol = scipy.optimize.minimize(J_EGM, init, args=(problem, material_parameters, material_model, initialisation_estimation, surface_forces, volume_forces, load_type, nu), method="Nelder-Mead", tol=1e-6)
    # print("opti done")
    if not sol.success:
        return (-1.)
    else:
        return (numpy.exp(sol.x[0]))
    
def J_EGM(x, problem, material_parameters, material_model, initialisation_estimation, surface_forces, volume_forces, load_type, nu):
    indice_param=0
    parameters_to_identify = {}
    for key, value in initialisation_estimation.items():
        try:
            material_parameters[key] = numpy.exp(x[indice_param])
            # print("material_parameters[key]=", numpy.exp(x[indice_param]))
            parameters_to_identify[key] = numpy.exp(x[indice_param])
            indice_param += 1
        except:
            pass
    kinematics = dmech.Kinematics(U=problem.U)
    material = dmech.material_factory(kinematics, material_model, material_parameters)
    sigma = material.sigma
    if volume_forces != []:
        # print("before volume regul")
        div_sigma = dwarp.VolumeRegularizationDiscreteEnergy(
            problem=problem,
            model="ciarletgeymonatneohookean",
            young=numpy.exp(x[0]),
            poisson=nu,
            b_fin=volume_forces[0])
        # print("after volume regul")
        div_sigma_value = div_sigma.assemble_ener() 
        # print("div_sigma_value", div_sigma_value)
        return div_sigma_value
    if surface_forces != []:
        N = dolfin.FacetNormal(problem.mesh)
        nf = dolfin.dot(N, dolfin.inv(kinematics.F))
        nf_norm = dolfin.sqrt(dolfin.inner(nf,nf))
        n = nf/nf_norm
        sigma_t = dolfin.dot(sigma, n)
        sigma_t += dolfin.Constant(surface_forces[0][0])*n
        dS = surface_forces[0][1]
        norm_sigma_t = dolfin.assemble(dolfin.inner(sigma_t, sigma_t)
        *kinematics.J*nf_norm*dS)/2/dolfin.assemble(dolfin.Constant(1)*kinematics.J*nf_norm*dS)
        # print("norm_sigma_t", norm_sigma_t)
        return norm_sigma_t



if (__name__ == "__main__"):
    fire.Fire(EGM)
