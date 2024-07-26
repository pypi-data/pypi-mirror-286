import subprocess
import argparse

def get_gpu_number():
    result = subprocess.check_output('rocm-smi -i', shell=True)
    result = result.decode('utf-8')
    results = result.split('\nGPU[')
    ids = []
    for item in results:
        if ']\t\t' in item:
            ids.append(int(item.split(']\t\t')[0]))
    gpu_number = max(ids) + 1
    print(f'[INFO] Checked {gpu_number} GPUs from `rocm-smi -i`')
    assert gpu_number >= 2, "This tool only works on the gpu number larger than 2"
    return gpu_number


def get_link_topo_matrix(gpu_number):
    topo_cmd = 'rocm-smi --shownodesbw'
    result = subprocess.check_output(topo_cmd, shell=True)
    result = result.decode('utf-8')
    space_flag = '         '
    full_flag = ''
    for i in range(gpu_number):
        flag = f'GPU{i}'
        if i == gpu_number - 1:
            full_flag += flag
        else:
            full_flag += flag + space_flag

    data = result.split(full_flag)[1]
    data = data.split('\n')
    data = data[1:gpu_number + 1]
    output_map = {}
    for gid, item in enumerate(data):
        items = item.split(' ')
        while '' in items:
            items.remove('')
        matrix_flag = items[1:]
        try:
            gpu_id_incode = matrix_flag.index('50000-50000')
        except:
            gpu_id_incode = gid
        output_map[gid] = gpu_id_incode
    return output_map

def get_visible_gpu_id(output_map, gid):
    print(f'GPU-{gid} in `HIP_VISIBLE_DIVICES` is \"{output_map[gid]}\"')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--devices",
        "-d",
        "-D",
        type = str,
        help = "The gpu id shown in rocm-smi, e.g., rocmgid --device 0, if multiple devices: rocmgid --device 0,1,2"
    )
    args = parser.parse_args()
    _devices = args.devices
    if _devices != None:
        gnum = get_gpu_number()
        node_matrix = get_link_topo_matrix(gnum)
        devices = [int(di) for di in _devices.split(',')]
        for d in devices:
            get_visible_gpu_id(node_matrix, d)

if __name__ == '__main__':
    main()