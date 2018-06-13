import tkinter as tk
from static_failure import StaticFailure
from dynamic_failure import DynamicFailure


class GUI:
    def __init__(self):
        self.top = tk.Tk()
        self.top.title('Failures')
        self.var0 = tk.IntVar()
        self.var = tk.IntVar()
        self.var1 = tk.IntVar()
        self.var2 = tk.IntVar()
        self.data = ('St', 'Sc', 'Sy')
        self.data_dynamic = ('St', 'Sm', 'Se', 'Sa', 'SM')
        self.values = {}
        self.entry = {}
        self.sigma = {}
        self.is_ductile = True
        self._theory = 'von'
        self.S = []
        self.g = None
        self.msg = None

        tk.Radiobutton(self.top, text='Static failure', variable=self.var0, value=1, command=self.failure_type) \
            .pack(anchor=tk.W)
        tk.Radiobutton(self.top, text='Dynamic Failure', variable=self.var0, value=2, command=self.failure_type) \
            .pack(anchor=tk.W)

        self.static = tk.Frame(self.top)

        self.dynamic = tk.Frame(self.top)

        self.top.mainloop()

    def on_submit_static(self):
        # print('Values submitted!')
        self.get_sigma()
        failure = StaticFailure(self.S, self.values)
        self.msg.destroy()
        self.msg = tk.Frame(self.top, bg='White')
        if self._theory == 'von':
            temp = failure.Von_Mises()
        elif self._theory == 'mss':
            temp = failure.MSS()
        elif self._theory == 'mct':
            temp = failure.Modified_Coloumb_Mohr()
        else:
            temp = False
        if temp:
            msg = 'Factor of safety is ' + str(failure.N)
        else:
            msg = 'Change your design'
        tk.Message(self.msg, text=msg).pack()
        self.msg.pack(side=tk.BOTTOM)

    def check(self):
        val = str(self.var.get())
        self.msg.destroy()
        self.g.destroy()
        self.g = tk.Frame(self.top)
        if val == '1':
            self.is_ductile = True
            tk.Radiobutton(self.g, text='Von-Mises theory', command=self.theory, variable=self.var1,
                           value=1).pack(anchor=tk.W)
            tk.Radiobutton(self.g, text='Maximum shear stress theory', command=self.theory, variable=self.var1,
                           value=2).pack(anchor=tk.W)
        elif val == '2':
            self.is_ductile = False
            tk.Radiobutton(self.g, text='Modified Coloumb theory', command=self.theory, variable=self.var1,
                           value=3).pack(anchor=tk.W)
        else:
            pass
        self.g.pack()

    def theory(self):
        val = str(self.var1.get())
        self.msg.destroy()
        if val == '1':
            self._theory = 'von'
        elif val == '2':
            self._theory = 'mss'
        elif val == '3':
            self._theory = 'mct'
        else:
            pass

    def get_sigma(self):
        self.S = []
        for i in range(3):
            self.S.append([])
            for j in range(3):
                index = (i, j)
                self.S[i].append(float(self.sigma[index].get()))

    def failure_type(self):
        val = str(self.var0.get())
        self.dynamic.destroy()
        self.static.destroy()
        try:
            self.g.destroy()
            self.msg.destroy()
        except AttributeError:
            pass
        if val == '1':
            self.static = tk.Frame(self.top)
            try:
                self.msg.destroy()
            except AttributeError:
                pass
            tk.Label(self.static, text="Sigma").pack()
            sigma_widget = tk.Frame(self.static)
            for i in range(3):
                for j in range(3):
                    index = (i, j)
                    e = tk.Entry(sigma_widget)
                    e.grid(row=i, column=j)
                    self.sigma[index] = e
            sigma_widget.pack()
            material_widget = tk.Frame(self.static)
            tk.Label(material_widget, text='Material Properties', pady=5).pack(side=tk.TOP)
            for i in range(len(self.data)):
                f = tk.Frame(material_widget)
                tk.Label(f, text=self.data[i]).pack(anchor=tk.W)
                e = tk.Entry(f)
                self.values[self.data[i]] = e
                e.pack(anchor=tk.E)
                f.pack()
            f = tk.Frame(material_widget)
            tk.Radiobutton(f, text='Ductile', command=self.check, variable=self.var, value=1).pack(anchor=tk.W,
                                                                                                   side=tk.LEFT)
            tk.Radiobutton(f, text='Brittle', command=self.check, variable=self.var, value=2).pack(anchor=tk.W,
                                                                                                   side=tk.RIGHT)
            self.g = tk.Frame(material_widget)
            material_widget.pack()
            f.pack()
            self.msg = tk.Frame(material_widget, bg='White')
            self.static.pack()
            tk.Button(self.static, text="Ok!", command=self.on_submit_static).pack(side=tk.BOTTOM)
        elif val == '2':
            self.dynamic = tk.Frame(self.top)
            material_widget = tk.Frame(self.dynamic)
            tk.Label(material_widget, text='Material Properties', pady=5).pack(side=tk.TOP)
            for i in range(len(self.data_dynamic)):
                # px = 0 if i == 2 else 3
                f = tk.Frame(material_widget)
                tk.Label(f, text=self.data_dynamic[i]).pack(anchor=tk.W)
                e = tk.Entry(f)
                self.entry[self.data_dynamic[i]] = e
                e.pack(anchor=tk.E)
                f.pack()
            material_widget.pack()
            f = tk.Frame(self.dynamic)
            tk.Radiobutton(f, text='Goodman line', variable=self.var2,
                           value=1, command=self.check_dynamic).pack()
            tk.Radiobutton(f, text='Gerber\'s parabola', variable=self.var2,
                           value=2, command=self.check_dynamic).pack()
            f.pack()
            tk.Button(material_widget, text='Ok!', command=self.on_submit_dynamic).pack()
            self.msg = tk.Frame(material_widget)
            self.dynamic.pack()
        else:
            pass

    def on_submit_dynamic(self):
        failure = DynamicFailure(self.entry)
        self.msg.destroy()
        if self._theory == 'god':
            temp = failure.Goodman()
        else:
            temp = failure.Gerber()
        self.msg = tk.Frame(self.top)
        msg = 'Life as per calculation is ' + str(temp)
        tk.Message(self.msg, text=msg).pack()
        self.msg.pack()

    def check_dynamic(self):
        val = str(self.var2.get())
        if val == '1':
            self._theory = 'god'
        elif val == '2':
            self._theory = 'ger'
        else:
            self._theory = 'god'


if __name__ == '__main__':
    g = GUI()
