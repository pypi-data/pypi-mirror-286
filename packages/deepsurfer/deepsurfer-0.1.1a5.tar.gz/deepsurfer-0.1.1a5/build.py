import os
import pathlib
import torch

from setuptools import setup
from torch.utils.cpp_extension import CUDA_HOME, BuildExtension, CUDAExtension

base_dir = pathlib.Path(__file__).parent.parent

ext_modules = []
cmdclass = {}

# CUDA_HOME=None

# Check for CUDA availability
if torch.cuda.is_available() and CUDA_HOME is not None:
    print("CUDA is available. Building with GPU support.")
    csrc_dir = base_dir / 'deepsurfer' / 'extension'
    sources = [
        csrc_dir / 'nearest.cu',
        csrc_dir / 'intersection.cu',
        csrc_dir / 'extension.cxx',
    ]

    extra_compile_args = {'cxx': ['-std=c++14']}
    nvcc_args = [
        '-DCUDA_HAS_FP16=1',
        '-D__CUDA_NO_HALF_OPERATORS__',
        '-D__CUDA_NO_HALF_CONVERSIONS__',
        '-D__CUDA_NO_HALF2_OPERATORS__',
        '-std=c++14',
    ]

    if os.name != 'nt':
        nvcc_args.append('-std=c++14')

    # # starting CUDA-toolkut 12.0, CUB is included in the toolkit
    # # https://github.com/NVIDIA/cccl/discussions/520
    cub_home = os.environ.get('CUB_HOME', os.environ.get('CONDA_PREFIX', os.environ.get('CUDA_HOME', '')))
    if cub_home:
        cub_home += '/include'
        nvcc_args.append(f'-I{cub_home}')

    nvcc_flags_env = os.getenv('NVCC_FLAGS', '')
    if nvcc_flags_env:
        nvcc_args.extend(nvcc_flags_env.split(' '))

    ext_modules.append(
        CUDAExtension(
            'deepsurfer.extension._cuda_extension',
            sources=[str(source.relative_to(base_dir)) for source in sources],
            include_dirs=[str(csrc_dir)],
            define_macros=[('WITH_CUDA', None)],
            extra_compile_args={'cxx': ['-std=c++14'], 'nvcc': nvcc_args}
        )
    )
    cmdclass['build_ext'] = BuildExtension
else:
    print("CUDA is not available. Building without GPU support.")

setup(
    name='deepsurfer',
    ext_modules=ext_modules,
    include_package_data=True,
    cmdclass=cmdclass,
    extras_require={'test': ['pytest>=6.0']},
)
