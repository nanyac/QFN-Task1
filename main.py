# Define global constants such as 
# Quiescent point
# period
# Input Supply timing
# Output Supply timing
# RF timing : delay=+2.07000E-05 width=+1.40000E-06
# VNA timing

import os.path
# входной файл
global std_in_filepath
std_in_filepath = "406c_EH-M_in.mps"

# цикл валидации файла
while 1:
    print(f"Назначьте полный путь до файла, с которым нужно работать")
    std_in_filepath = str(input())
    if os.path.exists(std_in_filepath):
        if std_in_filepath.split('.')[-1].strip() == 'mps':
            print(f'Путь {std_in_filepath} принят.')
            break
        else: print("Неправильное расширение. Программа работает только с .mps")
    else: print("Нет такого файла")

# выходной файл
global std_out_filepath
std_out_filepath = std_in_filepath.replace(os.path.dirname(std_in_filepath)+"\\", "").replace("in", "out") # под каким именем будет сохранён файл
print(f"Файл будет сохранён под именем {std_out_filepath} в папке программы")

# read chunks
from chunk_utils import *
from chunk_parser import *
# each chunk has its own pulsed point params
chunk_in_list = ParseIn(std_in_filepath)

if (True == False):     # проверка работы считывания: успех
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
# возвращает chunk_out_list
V_delta = 0
def calcChunkOuts(frequencies: list, chunk_in_list: list) -> list:
    _chunk_out_list = []
    _frequencies = frequencies
    for _cur_freq in _frequencies:
        # создаётся output-чанк 
        _cur_chunk_out = ChunkOut(_cur_freq)
        _cur_chunk_out._s_dVgs = dict()
        # в каждом чанке просматривается 
        for cur_chunk_in in chunk_in_list:
            # получаем dVgs
            _dVgs = V_delta + cur_chunk_in.getDeltaVgs()
            # текущие s-параметры,..
            _cur_s_params = cur_chunk_in._s_freq[_cur_freq]
            # ...которые будут assigned в текущий output-чанк
            # и теперь это аргумент функции
            _cur_chunk_out._s_dVgs[_dVgs] = _cur_s_params
        _chunk_out_list.append(_cur_chunk_out)
    return _chunk_out_list

chunk_out_list = calcChunkOuts(frequencies, chunk_in_list)

if (True == False):   # проверка обработки
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

# Для недопущения ухода в "-" графика
from CLI import *
# CLI loop
while 1:
    print("Введите команду","0 - выход",
          "1 - создать файл со всеми частотами", 
          "2 - создать файл с определённой частотой",
          "3 - сменить V_delta", sep='\n')
    cmd_input = input()
    if cmd_input == '0': exit(0)

    # файл со всеми частотами    
    if cmd_input == '1':
        # файл со всеми output чанками
        with open(std_out_filepath, "+wt", encoding="utf-8") as file:
            # start loop
            for chunk in chunk_out_list:
                # chunk header
                # !! F = 0.1 GHz
                file.writelines(f"!! F = { ToGHzStr(float(chunk._freq)) }\n")
                file.writelines(f"!\n")
                file.writelines(f"! Frequency: F={chunk._freq}\n")
                str_header = f"""!
! Quiescent point : Vgs={mpsValueFormat(Vgs_Quiescent)} Vds={mpsValueFormat(Vds_Quiescent)}
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
    
    # одна частота
    elif cmd_input == '2':
        # отформатированные частоты типа ['0.2 GHz', '0.25 GHz', '0.3 GHz'...]
        frmtd_frequencies = [ToGHzStr(float(freq)) for freq in frequencies]
        # словарь для удобства доступа и дальнейшей работы с полем _freq из ChunkOut
        frmtd_freqs_dict = dict().fromkeys(frmtd_frequencies)
        # заполнение словаря
        for freq in frequencies:
            frmtd_freqs_dict[ToGHzStr(float(freq))] = freq
        print(f"Участвовавшие в эксперименте частоты:\n{frmtd_frequencies}")
        # ожидание ввода конкретной частоты
    
        while 1:
            print("Какую частоту хотите вывести?")
            # ввод в формате "1.0 GHz"
            freq_input = input()
            # если есть частота в списке форматированных частот
            if freq_input in frmtd_frequencies:
                freq_str = frmtd_freqs_dict[freq_input]
                # debug
                single_frequency_filename = f"{std_out_filepath}_{freq_input.replace(' ','_')}.mps"
                print(f"Файл будет сохранён как: {single_frequency_filename}")
                # успешно введена частота => выход
                break
        
        # имя у файла: std_out_filepath+"1.0_GHz.mps"
        with open(single_frequency_filename, "+wt", encoding="utf-8") as file:
            # start loop
            selected_chunk = ChunkOut("")
            # найти необходимый чанк, у которого частота == freq_str
            for chunk in chunk_out_list:
                if chunk._freq == freq_str:
                    selected_chunk = chunk
                    del chunk
                    break
            
            # chunk header
            # !! F = 0.1 GHz
            file.writelines(f"!! F = { freq_input }\n")     # using freq_input из ввода конкретной частоты
            file.writelines(f"!\n")
            file.writelines(f"! Frequency: F={freq_str}\n") # using freq_str из ввода конкретной частоты
            str_header = f"""!
! Quiescent point : Vgs={mpsValueFormat(Vgs_Quiescent)} Vds={mpsValueFormat(Vds_Quiescent)}
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
            for dVg in list(selected_chunk._s_dVgs.keys()):
                # data
                file.writelines(f"{lessAccurate(dVg)} {selected_chunk._s_dVgs[dVg]}\n")

    # сменить Vgs_Quiescent
    elif cmd_input == '3':
        print(f"Смена V_delta\nПример: +0.123E-4\nТекущее значение:{V_delta}; Исходное значение:{V_delta}")
        # получить на вход число
        input_value = float(input())
        # записать его в глобальную переменную. 
        # Vgs_Quiescent = input_value только создаст переменную в main.py
        V_delta = input_value
        # посчитать чанки заново
        chunk_out_list = calcChunkOuts(frequencies, chunk_in_list)
        print(f"Готово. Успешно заменено на {V_delta}")
