# Define global constants such as 
# Quiescent point
# period
# Input Supply timing
# Output Supply timing
# RF timing : delay=+2.07000E-05 width=+1.40000E-06
# VNA timing
global Vgs_Quiescent
Vgs_Quiescent = -2.20332E-03 

global Ig_Quiescent
Ig_Quiescent=-1.12913E-07 

global Vds_Quiescent
Vds_Quiescent=+5.11725E-03 

global Id_Quiescent
Id_Quiescent=+2.43304E-04

global std_in_filepath
std_in_filepath = "406c_EH-M_in.mps"
global std_out_filepath
std_out_filepath = "406c_EH-M_out.mps"


# read chunks
from chunk_utils import *
from chunk_parser import *
# each chunk has its own pulsed point params
chunk_in_list = ParseIn(std_in_filepath)

if (True == False):     # проверка работы считывания: успех
    open("read_test.txt").flush()
    with open("read_test.txt","wt", encoding="utf-8") as file:
        for id, chunk in enumerate(chunk_in_list):
            # заголовки
            file.writelines(f"!!A{id+1}\n")
            file.writelines(f"! Pulsed point : {chunk.getHeaders()}\n")
            file.writelines("# Hz S RI R 50\n")
            # для каждой частоты вывести s-параметры
            for freq in list(chunk._s_freq.keys()):
                file.writelines(f"{freq} {chunk._s_freq[freq]}")
                file.writelines("\n")            


# взять частоту
frequencies = []
sample_chunk = chunk_in_list[0]
frequencies = list(sample_chunk._s_freq.keys())
del sample_chunk
unique_frequencies = set(frequencies)
if not(len(unique_frequencies) == len(frequencies)):
    print('Ошибка 1. Возможно данные просканированы неверно')
    exit(1)
del unique_frequencies


# из каждого чанка взять для этой частоты pulsed point параметры
# посчитать дельтаV (сделать аргументом функции для каждого остального s параметра)
# из каждого чанка взять для этой частоты все s параметры
chunk_out_list = []
dVgs_list = []
for cur_freq in frequencies:
    # создаётся output-чанк 
    cur_chunk_out = ChunkOut(cur_freq)
    cur_chunk_out._s_dVgs = dict()
    # в каждом чанке просматривается 
    for cur_chunk_in in chunk_in_list:
        # получаем dVgs
        dVgs = cur_chunk_in.getDeltaVgs()
        # текущие s-параметры,..
        cur_s_params = cur_chunk_in._s_freq[cur_freq]
        # ...которые будут assigned в текущий output-чанк
        # и теперь это аргумент функции
        cur_chunk_out._s_dVgs[dVgs] = cur_s_params
    chunk_out_list.append(cur_chunk_out)


if (True == False):   # проверка обработки
    open("write_test.txt").flush()
    with open("write_test.txt","wt", encoding="utf-8") as file:
        for id, chunk in enumerate(chunk_out_list):
            # заголовки
            file.writelines(f"!!A{id+1}\n")
            file.writelines(f"! Frequency : {chunk._freq}\n")
            file.writelines("# Hz S RI R 50\n")
            # для каждой частоты вывести s-параметры
            for dVg in list(chunk._s_dVgs.keys()):
                file.writelines(f"{dVg} {chunk._s_dVgs[dVg]}")
                file.writelines("\n")   


from CLI import *
# CLI loop
while 1:
    cmd_input = cmd(input("Введите команду\n0 - помощь\n"))

    # файл со всеми output чанками
    open(std_out_filepath).flush()
    with open(std_out_filepath, "+wt", encoding="utf-8") as file:
        # start loop
        for chunk in chunk_out_list:
            # chunk header
            # !! F = 0.1 GHz
            file.writelines(f"!! F = { ToGHzStr(float(chunk._freq)) }\n")
            file.writelines(f"!\n")
            file.writelines(f"! Frequency: F={chunk._freq}\n")
            str_header = """!
! Quiescent point : Vgs=-4.00 Vds=+5.00
! Pulsed point : Vds=+5.35839E-03
! Period : +2.00000E-04
! Input Supply timing : delay=+1.80000E-05 width=+5.50000E-06
! Output Supply timing : delay=+1.93000E-05 width=+3.00000E-06
! RF timing : delay=+2.07000E-05 width=+1.40000E-06
! VNA timing : delay=+2.12000E-05 width=+8.00000E-07\n"""
            file.writelines(str_header)
            # table header
            file.writelines("# Hz S RI R 50\n")
            # start table loop
            for dVg in list(chunk._s_dVgs.keys()):
                # data
                file.writelines(f"{dVg} {chunk._s_dVgs[dVg]}\n")


