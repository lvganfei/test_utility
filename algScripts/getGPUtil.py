import GPUtil
import time


max_memory = 0
memory_list = []
memory_total = 0
while True:
    gpus = GPUtil.getGPUs()
    for gpu in gpus:
        print(gpu,gpu.memoryTotal)
        memory = gpu.memoryUsed
        print(memory)
        if memory < 20:
            continue
        memory_list.append(memory)
        memory_total += memory
        if memory > max_memory:
            max_memory = memory
        print(max_memory)

        print(memory_total)
        avg = memory_total / len(memory_list)
        print(avg)

    time.sleep(5)
