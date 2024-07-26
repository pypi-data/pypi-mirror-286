import datetime
import os
import setuptools

# version = os.environ['CI_COMMIT_TAG']
version = datetime.date.today().strftime("%Y.%m.%d")+"-2"

setuptools.setup(
    name="dolfin_estim",
    version=version,
    author="Alice Peyraut",
    author_email="alice.peyraut@polytechnique.edu",
    description=open("README.md", "r").readlines()[1][:-1],
    long_description = open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.inria.fr/apeyraut/dolfin_estim",
    packages=["dolfin_estim"],
    license="GPLv3",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=["meshio", "numpy", "scipy",  "fire",  "ufl", "dolfin_mech", "dolfin_warp"],
)
