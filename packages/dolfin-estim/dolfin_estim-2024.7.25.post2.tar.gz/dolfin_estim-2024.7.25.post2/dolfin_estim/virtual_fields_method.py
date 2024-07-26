import fire
import ufl
import dolfin
import numpy
from scipy import optimize


import dolfin_mech as dmech
import dolfin_estim as destimation

def VFM(nu=0.3, mesh_size=0.1, refine=False, cube_params={}, load_params={}, load_type="body_force", noise_from_images=False, noise=0, regul=0.0, regul_number=0.0, run=1, tol=1e-6, MAX_ITER=100):
    iter=0
    if noise_from_images:
        U_meas, mesh, boundaries_mf=destimation.get_disp_field_and_mesh_from_images(refine=refine, noise=noise, mesh_size=mesh_size, regul=regul, run=run, load_type=load_type, regul_number=regul_number, cube_params=cube_params)
    else:
        U_meas, mesh, boundaries_mf=destimation.compute_displacement_field(refine=refine, noise=noise, mesh_size=mesh_size, load_params=load_params, cube_params=cube_params)
    dV = dolfin.Measure(
        "dx",
        domain=mesh)
    U_fe = dolfin.VectorElement(
        family='CG',
        cell=mesh.ufl_cell(),
        degree=1)
    U_fs = dolfin.FunctionSpace(
        mesh,
        U_fe)
    num_vertices = mesh.num_vertices()
    I = dolfin.Identity(2)
    TT = dolfin.TensorFunctionSpace(mesh,'P',1)
    shape = 4*(mesh.geometry().dim(),)
    TT_4 = dolfin.TensorFunctionSpace(mesh,'P',1,shape = shape)
    F_meas = I+dolfin.grad(U_meas)
    C_meas = (F_meas.T)*F_meas
    E_meas = (C_meas-I)/2
    E_meas_proj = dolfin.project(E_meas,TT)
    E_meas_array = numpy.array(E_meas_proj.vector()).reshape([-1,4])
    #### initialisation
    E_gue=0.9
    if not bool(cube_params):
        cube_params = {"X0":0.2, "Y0":0.2, "X1":0.8, "Y1":0.8, "l":mesh_size} 
    while True:
        E_o = E_gue
        u_o = dolfin.Function(U_fs) 
        u_o.assign(forward(E_o, nu, refine, load_params, cube_params))
        error = dolfin.assemble((dolfin.inner(u_o-U_meas, u_o-U_meas)*dV))/dolfin.assemble((dolfin.inner(U_meas,U_meas)*dV))
        if error < tol:
            return(E_o)
        if iter > MAX_ITER:  
            break
        iter+=1
        F = I+dolfin.grad(u_o)
        C = (F.T)*F
        Strain_E = (C-I)/2
        dS_dE, L = stress_grad_nh(u_o ,E_o,nu)
        dS_dE_array, Strain_E_array = proj_tensor2(dS_dE,Strain_E,TT)
        L_array = proj_tensor4(L,TT_4)
        dE = solve_VFM(dS_dE_array, Strain_E_array, E_meas_array, L_array, num_vertices)
        E_gue += dE
        if E_gue>10:
            return(10)
        elif E_gue<0:
            return(-10) 
        elif abs(dE) < 1e-4:
            return(E_o)
        

def forward(E=0.9, nu=0.3, refine=False, load_params={}, cube_params={}):
    E, nu = E, nu
    mat_params={"model":"CGNH", "parameters":{"E":E, "nu":nu}}
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
    return(u)


def stress_grad_nh(u, E, nu):
    i,j,k,l,m = ufl.indices(5)
    mu = E/(2*(1+nu))
    lam = E*nu/((1+nu)*(1-2*nu))
    dmu_dE = 1.0/(2.0*(1.0+nu))
    dlam_dE = nu/((1+nu)*(1-2*nu))
    I = dolfin.Identity(2)
    F = I+dolfin.grad(u)
    J = dolfin.det(F)
    C = (F.T)*F
    C_inv = dolfin.inv(C)
    S = mu*(I-dolfin.inv(C))+lam/2*(J*J-1)*dolfin.inv(C) # 2nd Piola-Kirchhoff stress
    dS_dE = dmu_dE*(I-dolfin.inv(C))+dlam_dE/2*(J*J-1)*dolfin.inv(C) #2nd Piola-Kirchhoff stress
    K_tan = dolfin.as_tensor(lam*J*J*C_inv[i,j]*C_inv[k,l]+ (mu+lam/4*J*J)*(C_inv[i,k]*C_inv[j,l]+ C_inv[i,l]*C_inv[j,k]),(i,j,k,l) )
    L = dolfin.as_tensor(K_tan[i,j,k,l]+dolfin.inv(F)[k,i]*dolfin.inv(F)[l,m]*S[m,j],(i,j,k,l))
    return dS_dE, L 


def solve_VFM(dS_dE_array, E_array, E_meas_array, L_array, num_vertices):
    dof_list = [] 
    for i in range(num_vertices):
        dof_list.append(i) 

    def solve_system(part_list):
        A_11_total = 0
        B_1_total = 0
        for el in part_list:
            B = numpy.zeros([1,1])
            A = numpy.zeros([1,1])
            Vir_E1, E_o, E_meas = calc_VF(dS_dE_array, E_array, E_meas_array, L_array, el)
            A[0,0] = numpy.dot(Vir_E1.T,Vir_E1)[0][0]
            B[0] = -numpy.dot((E_meas-E_o).T,Vir_E1)[0][0]
            A_11_total += A[0,0]
            B_1_total += B[0]
        A_total = numpy.zeros([1,1])
        B_total = numpy.zeros([1,1])
        A_total[0,0] = A_11_total
        B_total[0] = B_1_total
        cond = numpy.linalg.cond(A_total)
        if cond >= 1e6:
            temp_beta = numpy.linalg.lstsq(A_total, B_total)[0]
        else:
            temp_beta = numpy.linalg.solve(A_total,B_total)
        return (temp_beta[0,0])
    dE = solve_system(dof_list)
    return dE


def calc_VF(dS_dE_array, E_array, E_meas_array, L_array, index):
    dS_dE_np = ((dS_dE_array[index].reshape([2,2])))
    E = E_array[index].reshape([2,2])
    E_m = E_meas_array[index].reshape([2,2])
    L_np = (L_array[index].reshape([2,2,2,2]))
    index2D1 = [0,1,2,1,0,0]
    index2D2 = [0,1,2,2,2,1]
    S_E = numpy.zeros([2,1])
    E_meas = numpy.zeros([2,1])
    E_o = numpy.zeros([2,1])
    LL = numpy.zeros([2,2])
    for i in range(2):
        for j in range(0,1):
            LL[i,j] = L_np[index2D1[i],index2D2[i],index2D1[j],index2D2[j]]
        for j in range(1,2):
            LL[i,j] = 2*L_np[index2D1[i],index2D2[i],index2D1[j],index2D2[j]]
        S_E[i] = dS_dE_np[index2D1[i],index2D2[i]]
        E_o[i] = E[index2D1[i],index2D2[i]]
        E_meas[i] = E_m[index2D1[i],index2D2[i]]
    inv_LL = numpy.linalg.inv(LL)
    Vir_E1 = numpy.dot(inv_LL,S_E)
    return(Vir_E1, E_o,E_meas)   


def proj_tensor2(dS_dE,E,TT):
    dS_dE_proj = dolfin.project(dS_dE,TT)
    dS_dE_array = numpy.array(dS_dE_proj.vector()).reshape([-1,4])
    E_proj = dolfin.project(E,TT)
    E_array = numpy.array(E_proj.vector()).reshape([-1,4])
    return dS_dE_array,E_array

def proj_tensor4(L, TT_4):
    L_proj = dolfin.project(L, TT_4, solver_type ='cg')
    L_array = numpy.array(L_proj.vector()).reshape([-1,16]) 
    return L_array


if (__name__ == "__main__"):
    fire.Fire(VFM)