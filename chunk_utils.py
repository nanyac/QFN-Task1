global Vgs_Quiescent
Vgs_Quiescent = -2.20332E-03 

global Ig_Quiescent
Ig_Quiescent=-1.12913E-07 

global Vds_Quiescent
Vds_Quiescent=+5.11725E-03 

global Id_Quiescent
Id_Quiescent=+2.43304E-04

class ChunkIn:
    _Vgs = 0
    _Ig = 0
    _Vds = 0
    _Id = 0
    # Dictionary keys are frequencies
    _s_freq = dict()
    # _s_freq[freq1] = "+0.1E1 +0.2E1 +0.4E1"
    def __init__(self, args: list) -> None:
        self._Vgs = args[0]
        self._Ig = args[1]
        self._Vds = args[2]
        self._Id = args[3]


    def getDeltaList(self) -> list:
        """Return a list of differences between Quiescent and pulsed values for each Vg, Ig, Vds, Id"""
        deltaVgs = Vgs_Quiescent - self._Vgs
        deltaIg = Ig_Quiescent - self._Ig
        deltaVds = Vds_Quiescent - self._Vds
        deltaId = Id_Quiescent - self._Id
        return [deltaVgs, deltaIg, deltaVds, deltaId]
    
    
    def getDeltaVgs(self) -> int:
        """Vgs_Quiescent Vgs_Pulsated"""
        deltaVgs = Vgs_Quiescent - self._Vgs
        return deltaVgs
    

# взять частоту
# из каждого чанка взять для этой частоты pulsed point параметры
# посчитать дельтаV (сделать аргументом функции для каждого остального s параметра)
# из каждого чанка взять для этой частоты все s параметры


class ChunkOut:
    _freq = 0
    _s_dVgs = dict()
    def __init__(self, freq: float) -> None:
        self._freq = freq
