from chunk_utils import *

# for new Chunk
def getValues(line: str, substr:str) -> list:
    """Parses values from line that contains substr"""
    pulsed_list = []
    line = line.replace(substr, "")
    line = line.split(" ")
    for line_expr in line:
        # Here Vgs=+1.1E3 splits in [Vgs, +1.1E3]
        pulsed_list.append(float(line_expr.split('=')[1]))
    return pulsed_list


isChunkStarted = lambda line: line.__contains__("!!")
isReachedPulsed = lambda line: line.__contains__("Pulsed point")
isReachedTable = lambda line: line.__contains__("# Hz S RI R 50")

def ParseIn(filepath: str) -> list:
    """Parses given file and returns list of ChunkIn"""
    chunk_list = []
    cur_chunk_index = -1
    with open(filepath, "rt", encoding="UTF-8") as file:
        line = " "
        # main loop
        while (len(line) != 0):
            line = file.readline()
            if isChunkStarted(line):
                cur_chunk_index += 1
                
            elif isReachedPulsed(line):
                cur_chunk_pulsed = getValues(line, "! Pulsed point : ")
                cur_chunk = ChunkIn(cur_chunk_pulsed)
            
            elif isReachedTable(line):
                # Эти комментарии рассуждают о том, что на самом деле не работает ↓
                # the easiest way to work with this condition is to 
                # create a second file pointer and work with "file_table"
                # file_table = file
                # but move the original one on 1 line forward
                # file.readlines()
                while 1:
                    # get current position
                    file_seek_pos = file.tell()
                    # read line
                    line = file.readline()
                    # Condition to exit from loop
                    if (isChunkStarted(line) or line == ""):
                        # всё, что после цикла и то,
                        # что пишется здесь, эквиваленты в схеме выполнения
                        # просто выходим из цикла
                        break
                    # get frequency value
                    cur_freq = line.split(" ")[0]
                    # get S-params as string by replacing frequency with nothing
                    cur_s_params = line.replace(cur_freq + " ", "")
                    # add s-params to a Chunk object on specified freq
                    cur_chunk._s_freq[cur_freq] = cur_s_params.replace('\n', "")
                    
                # add to list
                chunk_list.append(cur_chunk)
                # back up to previous line
                file.seek(file_seek_pos,  0)
                # it is not allowed to do negative seeks in text mode (in each mode)
                # (not sure about binary mode)
                # file.seek((-1)*file_prev_line_length,  1)
    return chunk_list