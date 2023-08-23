from enum import Enum


class DeviceType(Enum):
    CPU = "cpu"
    CUDA = "cuda"
    IPU = "ipu"
    XPU = "xpu"
    MKLDNN = "mkldnn"
    OPENGL = "opengl"
    OPENCL = "opencl"
    IDEEP = "ideep"
    HIP = "hip"
    VE = "ve"
    FPGA = "fpga"
    ORT = "ort"
    XLA = "xla"
    LAZY = "lazy"
    VULKAN = "vulkan"
    MPS = "mps"
    META = "meta"
    HPU = "hpu"
    MTIA = "mtia"
