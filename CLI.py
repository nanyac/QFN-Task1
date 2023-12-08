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


def ToGHzStr(freq: float) -> str:
    """Returns frequency in GHz\n
    Example:
    "0.1 GHz" """  
    freq /= 10.**9
    result_str = f"{str(freq)} GHz"
    return result_str