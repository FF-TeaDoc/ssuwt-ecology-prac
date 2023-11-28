from math import pi
from tabulate import tabulate


class Emision:

    def __init__(self, name: str, pdkmr: float, pdkcc: float, danger_class: int, concentration: int, F: float, actual_emissions: float) -> None:
        self.name = name
        self.pdkmr = pdkmr
        self.pdkcc = pdkcc
        self.danger_class = danger_class
        self.concentration = concentration
        self.F = F
        self.actual_emissions = actual_emissions

    def pdv(self) -> float:
        first = (self.pdkmr - self.concentration) * (H ** 2)
        second = A * self.F * m() * kn() * n
        third = (v1() * dt()) ** (1/3)
        return (first / second) * third
    
    def get_sign(self) -> str:
        return "<" if self.pdv() < self.actual_emissions else ">"

def v1() -> float:
    return (pi * w0 * (d**2)) / 4

def f() -> float:
    return (10 ** 3) * ((w0 ** 2) * d) / ((H ** 2) * dt())

def m() -> float:
    _f = f()
    return 1 / (0.67 + 0.1 * (_f ** (1/2)) + 0.34 * (_f ** (1/3)))

def dt() -> float:
    return t_g - t_v

def vm() -> float:
    _ = (v1() * dt()) / H
    return 0.65 * (_ ** (1/3))

def kn() -> float:
    _vm = vm()
    return 0.523 * (_vm ** 2) - 2.13 * _vm + 3.13

if __name__ == "__main__":
    w0 = 10.4
    d = 0.5
    t_g = 100
    t_v = 25.2
    A = 200
    n = 0.8
    H = 9.0
    emisions = [
        Emision("CO", 5.0, 0.04, 4, 1.170, 1.0, 9.100),
        Emision("NO2", 0.085, 0.04, 2, 0.009, 1.0, 0.330),
        Emision("S02", 0.5, 3.0, 4, 0.320, 1.0, 2.100),
        Emision("Пыль золы", 0.05, 0.02, 2, 0.042, 2.5, 0.010)
    ]
    print(v1())
    print(dt())
    print(f())
    print(m())
    print(vm())
    print(kn())
    for emision in emisions:
        print(emision.name, emision.pdv())
    table = tabulate(
        [(emision.name, emision.pdv(), emision.get_sign(), emision.actual_emissions) for emision in emisions],
        headers=["Вещество", "ПДВ", ">/<", "M"],
        tablefmt="grid",
        disable_numparse=True
    )
    print(table)