import os
import subprocess as sp

from dotenv import load_dotenv
import psutil


def load_config():
    ret = load_dotenv('.dm')

    if not ret:
        print("ERROR")
        exit(1)



def bash_command(command):
    res = sp.check_output(command)
    return res


def get_gpuinfo():
    ns = os.popen('nvidia-smi')
    lines_ns = ns.readlines()
    gpu_memory = list()
    gpu_procc = list()
    gpu_temp = list()
    n_gpu = 0
    for line in lines_ns:
        if line.find('%') != -1:
            n_gpu += 1
            splited = line.replace("|", "").replace("MiB", "").split(" ")
            res = list(filter(lambda x: x != "", splited))
            temp = int(res[1][:-1])
            cur_usage, max_usage = int(res[6]), int(res[8])
            gpu_procc.append(float(res[9].replace("%", "")))
            gpu_memory.append({"gpu_usage": cur_usage, "gpu_total": max_usage})
            gpu_temp.append(temp)

    return gpu_procc, gpu_memory, gpu_temp


def get_gpuname():
    ns = os.popen("nvidia-smi --query | fgrep 'Product Name'")
    lines_ns = ns.readlines()

    names = []
    for line in lines_ns:
        n = line.lstrip().rstrip().split(":")[-1]
        names.append(n)

    return names


def get_cpuinfo():
    """
    :return: cpu usage(%)
    """
    return {"cpu_usage": psutil.cpu_percent(interval=0.1)}


def get_cpucore():
    ns = os.popen("grep -c processor /proc/cpuinfo")
    lines_ns = ns.readlines()
    return lines_ns[0].rstrip()


def get_memoryinfo():
    vmemory = psutil.virtual_memory()
    return {"memory_usage": vmemory[0] - vmemory[1], "memory_total": vmemory[0]}
