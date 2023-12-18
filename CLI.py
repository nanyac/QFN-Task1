global _command

def help() -> None:
    """Provides help string"""
    _help_string = """
    1 - вывести файл
    2 - 
    """


def cmd(input_str: str) -> None:
    if (input_str == '0'):
        # help string
        cmd0()



def cmd0():
    print("")


def cmd2FreqInput():
    """Returns freq as a string"""
    while 1:
        print("Какую частоту хотите вывести?")
        freq_input = input()
        

def mpsValueFormat(value: float) -> str:
    """Возвращает число в scientific notation"""
    str = '{:.2e}'.format(value).title()
    if value > 0:
        str = '+' + str
        return str
    else:
        return str
    

def ToGHzStr(freq: float) -> str:
    """Returns formatted frequency\n
    Example:
    "0.1 GHz" """  
    freq /= 10.**9
    result_str = f"{str(freq)} GHz"
    return result_str
    
def lessAccurate(value:float)->str:
    """Returns 6 digits after point"""
    return "{.6f}".format(value)
