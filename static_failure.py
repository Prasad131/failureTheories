import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt


class StaticFailure:
    def __init__(self, S, kwargs):
        self.St = float(kwargs['St'].get())
        self.Sc = float(kwargs['Sc'].get())
        self.Sy = float(kwargs['Sy'].get())
        self.S = S
        self.N = 1

    def principle_stress(self, mohr_circle=False):
        m = np.matrix(self.S)
        s1, s2, s3 = la.eigvals(m)
        if mohr_circle:
            r1, r2, r3 = abs(s1 - s2) / 2, abs(s2 - s3) / 2, abs(s3 - s1) / 2
            theta = np.arange(0, 2 * np.pi, 0.01)
            x1, y1 = ((s1 + s2) / 2) + r1 * np.cos(theta), r1 * np.sin(theta)
            x2, y2 = ((s2 + s3) / 2) + r2 * x1 / r1, r2 * y1 / r1
            x3, y3 = ((s3 + s1) / 2) + r3 * x1 / r1, r3 * y1 / r1
            max_x, min_x = max(s1, s2, s3), min(s1, s2, s3)
            max_y, min_y = max(r1, r2, r3), min(r1, r2, r3)
            c_x, c_y = (min_x + max_x) / 2, (min_y + max_y) / 2
            plt.plot(x1, y1, x2, y2, x3, y3, [s1], [0], 'bo', [s2], [0], 'bo', [s3], [0], 'bo')
            plt.plot([min_x, max_x], [0, 0], 'r', [c_x, c_x], [min_y, max_y], 'r')
            plt.show()
        return s1, s2, s3

    def MSS(self):
        s1, s2, s3 = self.principle_stress()
        r1, r2, r3 = abs(s1 - s2), abs(s2 - s3), abs(s3 - s1)
        r = max([r1, r2, r3])
        if r < self.Sy:
            self.N = self.Sy / r
            return True
        else:
            return False

    def Von_Mises(self):
        s1, s2, s3 = self.principle_stress()
        se = np.sqrt(s1 ** 2 + s2 ** 2 + s3 ** 2 - s1 * s2 - s2 * s3 - s3 * s1)
        if se < self.Sy:
            self.N = self.Sy / se
            return True
        else:
            return False

    def f(self, x, y):
        temp = (2 * self.St - abs(self.Sc)) / (-abs(self.Sc))
        return 0.5 * (abs(x - y) + temp * (x + y))

    def Modified_Coloumb_Mohr(self):
        s1, s2, s3 = self.principle_stress()
        c1, c2, c3 = self.f(s1, s2), self.f(s2, s3), self.f(s3, s1)
        se = max(s1, s2, s3, c1, c2, c3)
        if se < self.St:
            self.N = self.St / se
            return True
        else:
            return False
