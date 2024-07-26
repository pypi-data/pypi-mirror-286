import dolfin
import meshio
import numpy

import dolfin_mech as dmech


##### getting mesh+displacement field from images

def get_disp_field_and_mesh_from_images(refine=False, noise=0, mesh_size=0.1, regul=0.0, run=1, load_type="body_force", regul_number=None, cube_params={}):
    cube_params["l"]=mesh_size
    if load_type=="body_force":
        folder_name="run_warp_grav"
        test_name="grav"
        name_regul="-discrete-equilibrated-tractions-normal-tangential-regul="
    else:
        folder_name="run_warp_compx"
        test_name="compx"
        name_regul="-discrete-equilibrated-tractions-tangential-regul="
    if refine:
        refine_number="1"
        mesh=dolfin.Mesh("./generate_images/square-"+test_name+"-h="+str(mesh_size)+"-meshrefined.xml")
        X0 = mesh.coordinates()[:, 0].min()
        xmin_sd = dolfin.CompiledSubDomain("near(x[0], x0) && on_boundary", x0=X0)
        xmin_id = 1
        X1 = mesh.coordinates()[:, 0].max()
        xmax_sd = dolfin.CompiledSubDomain("near(x[0], x0) && on_boundary", x0=X1)
        xmax_id = 2
        boundaries_mf = dolfin.MeshFunction("size_t", mesh, mesh.topology().dim()-1)
        boundaries_mf.set_all(0)
        xmin_sd.mark(boundaries_mf, xmin_id)
        xmax_sd.mark(boundaries_mf, xmax_id)  
    else:
        refine_number="0"
        mesh=dolfin.Mesh("./generate_images/square-"+test_name+"-h="+str(mesh_size)+"-meshcoarse.xml")
        X0 = mesh.coordinates()[:, 0].min()
        xmin_sd = dolfin.CompiledSubDomain("near(x[0], x0) && on_boundary", x0=X0)
        xmin_id = 1
        X1 = mesh.coordinates()[:, 0].max()
        xmax_sd = dolfin.CompiledSubDomain("near(x[0], x0) && on_boundary", x0=X1)
        xmax_id = 2
        boundaries_mf = dolfin.MeshFunction("size_t", mesh, mesh.topology().dim()-1) 
        boundaries_mf.set_all(0)
        xmin_sd.mark(boundaries_mf, xmin_id)
        xmax_sd.mark(boundaries_mf, xmax_id)  
    regul_number_str="-b="+str(regul_number)
    if noise==0:
        mesh_meshio = meshio.read("./"+folder_name+"/square-"+str(test_name)+"-tagging-noise="+str(noise)+"-h="+str(mesh_size)+str(name_regul)+str(regul)+regul_number_str+"-refine="+refine_number+"_020.vtu")
        u_meshio = mesh_meshio.point_data["displacement"]
    else:
        mesh_meshio = meshio.read("./"+folder_name+"/square-"+str(test_name)+"-tagging-noise="+str(noise)+"-run="+str(run)+"-h="+str(mesh_size)+str(name_regul)+str(regul)+regul_number_str+"-refine="+refine_number+"_020.vtu")
        u_meshio = mesh_meshio.point_data["displacement"]
    u_meshio = u_meshio.tolist()
    u_meshio = [item for sublist in u_meshio for item in sublist[:2]]     
    fe_u = dolfin.VectorElement(
                family="CG",
                cell=mesh.ufl_cell(),
                degree=1)
    U_fs = dolfin.FunctionSpace(mesh, fe_u)
    U=dolfin.Function(U_fs)
    U.vector().set_local(u_meshio)
    return(U, mesh, boundaries_mf)


##### computing displacement field with EF calculation

def compute_displacement_field(refine=False, noise=0, mesh_size=0.1, load_params={}, cube_params={}, u_params=None, res_basename="./", write_vtus_with_preserved_connectivity=False, verbose=0):
    cube_params["l"]=mesh_size
    mat_params={"model":"CGNH", "parameters":{"E":1., "nu":0.3}}
    step_params = {"dt_ini":1/20}
    const_params = {"type":"blox"}
    if u_params is not None:
        cube_params["refine"]=False
        cube_params_fine=cube_params
        cube_params_fine["l"]=1/100
        mesh_fine, boundaries_mf_fine, xmin_id_fine, xmax_id_fine, ymin_id_fine, ymax_id_fine = dmech.run_RivlinCube_Mesh(dim=2, params=cube_params_fine)
        cube_params_coarse=cube_params
        cube_params_coarse["l"]=0.1
        mesh_coarse, boundaries_mf_coarse, xmin_id_coarse, xmax_id_coarse, ymin_id_coarse, ymax_id_coarse=dmech.run_RivlinCube_Mesh(dim=2, params=cube_params_coarse)
        u, v = u_params["u"], u_params["v"]
        V0 = dolfin.assemble(dolfin.Constant(1)*v)
        U_norm =  (dolfin.assemble(dolfin.inner(u, u)*v)/2/V0)**(1/2)
        scale = float(noise)*U_norm
        fe_u_coarse = dolfin.VectorElement(
                family="CG",
                cell=mesh_coarse.ufl_cell(),
                degree=1)
        fe_u_fine = dolfin.VectorElement(
                family="CG",
                cell=mesh_fine.ufl_cell(),
                degree=1)
        U_fs_coarse=dolfin.FunctionSpace(mesh_coarse, fe_u_coarse)
        U_fs_fine=dolfin.FunctionSpace(mesh_fine, fe_u_fine)
        noise_vector=dolfin.Function(U_fs_coarse)
        noise_vector.vector()[:] = numpy.random.normal(loc=0.0, scale=scale, size=noise_vector.vector().get_local().shape)
        noise_projected=dolfin.project(noise_vector, U_fs_fine)
        U=dolfin.Function(U_fs_fine)
        U.vector()[:]=(u.vector().get_local()+noise_projected.vector().get_local())
        return(U, mesh_fine, boundaries_mf_fine)
    else:
        if refine:
            cube_params["refine"]=True
            mesh, boundaries_mf, xmin_id, xmax_id, ymin_id, ymax_id = dmech.run_RivlinCube_Mesh(dim=2, params=cube_params)
            X0 = cube_params.get("X0", 0.)
            xmin_sd = dolfin.CompiledSubDomain("near(x[0], x0) && on_boundary", x0=X0)
            xmin_id = 1
            X1 = cube_params.get("X1", 1.)
            xmax_sd = dolfin.CompiledSubDomain("near(x[0], x0) && on_boundary", x0=X1)
            xmax_id = 2
            boundaries_mf = dolfin.MeshFunction("size_t", mesh, mesh.topology().dim()-1) 
            boundaries_mf.set_all(0)
            xmax_sd.mark(boundaries_mf, xmax_id)
            xmin_sd.mark(boundaries_mf, xmin_id)
        else:
            cube_params["refine"]=False
            mesh, boundaries_mf, xmin_id, xmax_id, ymin_id, ymax_id = dmech.run_RivlinCube_Mesh(dim=2, params=cube_params)
        u, v = dmech.run_RivlinCube_Hyperelasticity(
                    dim                                    = 2                                 ,
                    cube_params                            = cube_params                       ,
                    mat_params                             = mat_params                        ,
                    step_params                            = step_params                       ,
                    const_params                           = const_params                      ,
                    load_params                            = load_params                       ,
                    get_results                            = 1                                 ,
                    res_basename                           = res_basename,
                    write_vtus_with_preserved_connectivity  = write_vtus_with_preserved_connectivity,
                    verbose=verbose)
        V0 = dolfin.assemble(dolfin.Constant(1)*v)
        U_norm =  (dolfin.assemble(dolfin.inner(u, u)*v)/2/V0)**(1/2)
        scale = float(noise)*U_norm
        noise_vector = u.copy(deepcopy=True)
        noise_vector.vector()[:] = numpy.random.normal(loc=0.0, scale=scale, size=u.vector().get_local().shape)        
        fe_u = dolfin.VectorElement(
                    family="CG",
                    cell=mesh.ufl_cell(),
                    degree=1)
        U_fs=dolfin.FunctionSpace(mesh, fe_u)
        U=dolfin.Function(U_fs)
        U.vector()[:]=(u.vector().get_local()+noise_vector.vector().get_local())
        return(U, mesh, boundaries_mf)