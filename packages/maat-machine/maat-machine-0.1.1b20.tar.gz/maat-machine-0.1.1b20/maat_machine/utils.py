import os
import sys
import platform
import subprocess

import distro

import re

import keras
import tensorflow as tf
from tensorflow import config as tf_config
import sklearn
import pandas as pd
import numpy as np
import scipy as sp

import maat_machine.pprint as mpprn

def print_system_info():
    os_name = platform.system()
    os_version = platform.release()
    print(f"Python version: {sys.version}")
    print(f"Version info: {sys.version_info}")
    print(f"Platform: {os_name} - {os_version}")
    print(f"OS distribution: {distro.name(pretty=True)}")


def display_system_info():
    os_name = platform.system()
    os_version = platform.release()
    mpprn.displayitwell(f"<hr>🐍&nbsp;Python version:<br>&emsp;&emsp;&emsp;&emsp;{sys.version}", color='darkorange', font_weight='bold', inline=False)
    mpprn.displayitwell(f"🍃&nbsp;Version info:<br>&emsp;&emsp;&emsp;&emsp;{sys.version_info}", color='darkblue', font_weight='bold', inline=False)
    mpprn.displayitwell(f"💻&nbsp;Platform:<br>&emsp;&emsp;&emsp;&emsp;{os_name} - {os_version}", color='darkred', font_weight='bold', inline=False)
    mpprn.displayitwell(f"&emsp;&emsp;&emsp;&emsp;OS distribution: {distro.name(pretty=True)}<hr>", color='darkred', font_weight='bold', inline=False)


def print_gpu_info():
    print("⚙️ GPU Information:")
    devices = tf_config.list_physical_devices('GPU')
    if devices:
        print('\n'.join([f"\t✅ {tf_config.experimental.get_device_details(device).get('device_name', 'Unknown GPU')}" for device in devices]))
    else:
        print("\t🛑 No GPUs found.")


def display_gpu_info():
    mpprn.displayitwell("<hr>⚙️&nbsp;GPU Information:", color='darkgreen', font_weight='bold', inline=False)
    devices = tf_config.list_physical_devices('GPU')
    if devices:
        mpprn.displayitwell(
            '<ul style="margin-top: -0.8em">' \
            + '</li>'.join([f"<li style=\"list-style: none; padding-left: 1em;\">✅&nbsp;{tf_config.experimental.get_device_details(device).get('device_name', 'Unknown GPU')}" for device in devices]) \
            + '</ul><hr>',
            font_weight='bold', inline=False
        )
    else:
        mpprn.displayitwell("&emsp;&emsp;&emsp;&emsp;🛑&nbsp;No GPUs found.<hr>")


def print_libraries_info():
    print("📦 Python Packages Information:")
    print(f"\t🧠 TensorFlow version: {tf.__version__}")
    print(f"\t🧠 Keras version: {keras.__version__}")
    print(f"\t📊 Scikit-learn version: {sklearn.__version__}")
    print(f"\t📰 Pandas version: {pd.__version__}")
    print(f"\t1️⃣ NumPy version: {np.__version__}")
    print(f"\t⚛️ SciPy version: {sp.__version__}")


def display_libraries_info():
    mpprn.displayitwell("<hr>📦&nbsp;Python Packages Information:", color='darkorange', font_weight='bold', inline=False)
    mpprn.displayitwell(
        "<ul style=\"margin-top: -0.8em\">" \
            + f"<li style=\"list-style: none; padding-left: 1em;\">🧠&nbsp;TensorFlow version: {tf.__version__}</li>" \
            + f"<li style=\"list-style: none; padding-left: 1em;\">🧠&nbsp;Keras version: {keras.__version__}</li>" \
            + f"<li style=\"list-style: none; padding-left: 1em;\">📊&nbsp;Scikit-learn version: {sklearn.__version__}</li>" \
            + f"<li style=\"list-style: none; padding-left: 1em;\">📰&nbsp;Pandas version: {pd.__version__}</li>" \
            + f"<li style=\"list-style: none; padding-left: 1em;\">1️⃣&nbsp;NumPy version: {np.__version__}</li>" \
            + f"<li style=\"list-style: none; padding-left: 1em;\">⚛️&nbsp;SciPy version: {sp.__version__}</li>" \
        + "</ul><hr>",
        font_weight='bold', inline=False
    )


def get_cuda_version_nvidia_smi():
    pattern = r"CUDA Version:\s*([\d\.]+)"
    try:
        output = subprocess.check_output("nvidia-smi", shell=True).decode()
        for line in output.split('\n'):
            if "CUDA Version" in line:
                cuda_version = re.search(pattern, line).group(1)
                return cuda_version.strip()
        return "CUDA Version not found"
    except Exception as e:
        return str(e)


def get_cuda_version_nvcc():
    pattern = r"V([\d\.]+)"
    try:
        output = os.popen('/usr/local/cuda/bin/nvcc --version').read()
        version = re.search(pattern, output).group(1)
        return version.strip()
    except Exception as e:
        return str(e)


def get_cudnn_version():
    try:
        output = subprocess.check_output("cat /usr/include/cudnn_version.h | grep CUDNN_MAJOR -A 2", shell=True).decode()
        lines = output.split('\n')
        major = [line for line in lines if 'CUDNN_MAJOR' in line][0].split()[-1]
        minor = [line for line in lines if 'CUDNN_MINOR' in line][0].split()[-1]
        patch = [line for line in lines if 'CUDNN_PATCHLEVEL' in line][0].split()[-1]
        return f"{major}.{minor}.{patch}"
    except Exception as e:
        return str(e)


def print_gpu_libraries_info():
    print("📦 GPU Libraries Information:")
    print(f"\t🧠 CUDA version (installed): {get_cuda_version_nvcc()}")
    print(f"\t🧠 CUDA version (recommended by Nvidia SMI): {get_cuda_version_nvidia_smi()}")
    print(f"\t🧠 cuDNN version: {get_cudnn_version()}")


def display_gpu_libraries_info():
    mpprn.displayitwell("<hr>📦&nbsp;GPU Libraries Information:", color='darkgreen', font_weight='bold', inline=False)
    mpprn.displayitwell(
        "<ul style=\"margin-top: -0.8em\">" \
            + f"<li style=\"list-style: none; padding-left: 1em;\">🧠&nbsp;CUDA version (installed): {get_cuda_version_nvcc()}</li>" \
            + f"<li style=\"list-style: none; padding-left: 1em;\">🧠&nbsp;CUDA version (recommended by Nvidia SMI): {get_cuda_version_nvidia_smi()}</li>" \
            + f"<li style=\"list-style: none; padding-left: 1em;\">🧠&nbsp;cuDNN version: {get_cudnn_version()}</li>" \
        + "</ul><hr>",
        font_weight='bold', inline=False
    )


def print_environment_info():
    print_system_info()
    print_gpu_info()
    print_libraries_info()


def display_environment_info():
    display_system_info()
    display_gpu_info()
    display_gpu_libraries_info()
    display_libraries_info()
