Vgs_Quiescent = -2.20332E-03
def setGlobalVgsQuiescent(var:float) -> None:   # Метод-обёртка для изменения Vgs_Quiescent
    global Vgs_Quiescent 
    Vgs_Quiescent = var
def getGlobalVgsQuiescent() -> float:           # Метод-обёртка для получения Vgs_Quiescent
    return Vgs_Quiescent


Ig_Quiescent = -1.12913E-07 
def setGlobaIgQuiescent(var: float) -> None:
    global Ig_Quiescent
    Ig_Quiescent = var
def getGlobaIgQuiescent() -> float:
    return Ig_Quiescent


Vds_Quiescent = +5.11725E-03 
def setGlobaVdsQuiescent(var: float) -> None:
    global Vds_Quiescent
    Vds_Quiescent = var
def getGlobaVdsQuiescent() -> float:
    return Vds_Quiescent


Id_Quiescent = +2.43304E-04
def setGlobaIdQuiescent(var: float) -> None:
    global Id_Quiescent
    Id_Quiescent = var
def getGlobaIdQuiescent() -> float:
    return Id_Quiescent


def setAllGlobals(_Vgs_Quiescent, _Ig_Quiescent, _Vds_Quiescent, _Id_Quiescent)->None:
    global Vgs_Quiescent 
    Vgs_Quiescent = _Vgs_Quiescent
    global Ig_Quiescent
    Ig_Quiescent = _Ig_Quiescent
    global Vds_Quiescent
    Vds_Quiescent = _Vds_Quiescent
    global Id_Quiescent
    Id_Quiescent = _Id_Quiescent


def printAllGlobals() -> None:
    print(f"Vgs_Quiescent = {Vgs_Quiescent}\nIg_Quiescent = {Ig_Quiescent}\nVds_Quiescent = {Vds_Quiescent}\nId_Quiescent = {Id_Quiescent}")




class ChunkIn:
    """Входной блок данных"""
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
        """Возвращает разность ТЕПЕРЬ Vgs_pulsed и Vgs_quistient"""
        # self._Vgs - Pulsed Point Vgs
        deltaVgs = self._Vgs - Vgs_Quiescent
        return deltaVgs
    

    def getHeaders(self) -> str:
        """Returns pulsed point values formatted into a string
        like in original file"""
        _ret_str = f"Vgs={self._Vgs} Ig={self._Ig} Vds={self._Vds} Id={self._Id}"
        return _ret_str

# взять частоту
# из каждого чанка взять для этой частоты pulsed point параметры
# посчитать дельтаV (сделать аргументом функции для каждого остального s параметра)
# из каждого чанка взять для этой частоты все s параметры


class ChunkOut:
    """Результирующий блок данных"""
    _freq = 0
    _s_dVgs = dict()
    def __init__(self, freq: float) -> None:
        self._freq = freq


class Task2:
    a1 = 0.0
    a2 = 0.0
    b1 = 0.0
    b2 = 0.0
    Zs = 0.0
    Zin = 0.0
    
    def __init__(self, a1, a2, b1, b2, Zs, Zin):
        self.a1 = a1
        self.a2 = a2
        self.b1 = b1
        self.b2 = b2
        self.Zs = Zs
        self.Zin = Zin
    
        self.Pin_delivered = 1/2*(a1**2 - b1**2)
        
        self.Pin_available = self.Pin_delivered/(1 - 
                                pow((Zin - Zs)/(Zin + Zs), 2))

        self.Pout = 1/2*(b2**2 - a2**2)

        self.Pdc = 1j   #pdc = v_out* i_out?????????
        
        self.PAE = (self.Pout - self.Pin_delivered)/self.Pdc

        self.transduser_eff = (self.Pout - self.Pin_delivered)/self.Pdc

        self.Deff = self.Pout/self.Pdc

        self.Gp = self.Pout/self.Pin_delivered
        
        self.Gt = self.Pout/self.Pin_available
        
        self.PowerGain = self.Pout/self.Pin_delivered
