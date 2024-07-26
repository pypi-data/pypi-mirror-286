import dolfin_estim as destimation

##### starting estimation
def identifying_parameter(method="", delta=1.2, load_type="body_force", load_params={}, refine=False, noise_from_images=True, noise=0, mesh_size=0.1, regul=0.0, regul_number=0.3, run=1, cube_params={}, nu=0.3, u_params=None, res_basename="./"):
    if method=="EGM":
        E=destimation.EGM(refine=refine, noise=noise, cube_params=cube_params, mesh_size=mesh_size, regul=regul, regul_number=regul_number, run=run, noise_from_images=noise_from_images, load_type=load_type, load_params=load_params, nu=nu)
    elif method=="FEMU":
        E=destimation.FEMU(noise=noise, refine=refine, mesh_size=mesh_size, regul=regul, regul_number=regul_number, run=run, load_type=load_type, cube_params=cube_params, load_params=load_params, noise_from_images=noise_from_images, nu=nu)
    elif method=="VFM":
        E=destimation.VFM_plane_waves(delta=delta, noise=noise, noise_from_images=noise_from_images, load_type=load_type, regul_number=regul_number,refine=refine, mesh_size=mesh_size, cube_params=cube_params, load_params=load_params, regul=regul, run=run, nu=nu, u_params=u_params, res_basename=res_basename)
    elif method=="VFM_deng":
        E=destimation.VFM(noise=noise, noise_from_images=noise_from_images, load_type=load_type, refine=refine, mesh_size=mesh_size, cube_params=cube_params,load_params=load_params, regul=regul, regul_number=regul_number, run=run, nu=nu)
    return(E)