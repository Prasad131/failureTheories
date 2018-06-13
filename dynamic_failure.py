import numpy as np


class DynamicFailure:
    def __init__(self, kwargs):
        self.St = float(kwargs['St'].get())
        self.Sm = float(kwargs['Sm'].get())
        self.Se = float(kwargs['Se'].get())
        self.Sa = float(kwargs['Sa'].get())
        self.SM = float(kwargs['SM'].get())

    def SN_plot(self):
        b = np.log(self.Sm / self.Se) / np.log(1 / 1000)
        a = self.Sm * np.power(1000, -b)
        return a, b

    def SN_val(self, **kwargs):
        a, b = self.SN_plot()
        if 'S' in kwargs:
            s = kwargs['S']
            n = np.power(s / a, 1 / b)
            return n
        if 'N' in kwargs:
            n = kwargs['N']
            s = a * np.power(n, b)
            return s
        return None

    def Goodman(self):
        x = self.Sa / (1 - self.SM / self.St)
        n = self.SN_val(S=x)
        return n

    def Gerber(self):
        x = self.Sa / (1 - np.power(self.SM / self.St, 2))
        n = self.SN_val(S=x)
        return n
