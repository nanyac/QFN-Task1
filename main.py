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


open(std_out_filepath).flush()
with open(std_out_filepath, "+ta", encoding="utf-8") as file:
    pass
    # start loop
        # chunk header
        # '\n'
        # table header
        # start table loop
            # data
            # '\n'

