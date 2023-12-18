from ecology2 import *
from tabulate import tabulate
import numpy
import matplotlib.pyplot as plt



def cm(M: float, F: float):
    first = A * M * F * m() * kn() * n
    second = (H**2) * ((V * dT) ** (1/3))
    res = first / second
    # print(f"{A} * {M} * {F} * {m()} * {kn()} * {n} / {H**2} * {((V * dT) ** (1/3))} = {res}")
    return res

def xm(F: float):
    res = ((5 * F) / 4) * d_() * H
    # print(f"((5 * {F}) / 4) * {d_()} * {H}) = {res}")
    return res

def d_():
    if vm < 0.5:
        res = 2.49 * (1 + 0.28 * (f() ** (1/3)))
    elif 0.5 < vm <= 2:
        res = 4.95 * vm * (1 + 0.28 + (f() ** (1/3)))
    elif vm > 2:
        res = 7 * (vm**(1/2)) * (1 + 0.28 * (f() ** (1/3)))
    return res

def r():
    res = (3 * uum) / ((2*(uum**2)) - uum + 2)
    return res

def cmu(M: float, F: float):
    res = r() * cm(M, F)
    # print(r(), cm(M, F))
    return res

def p():
    if 0.25 <= uum <= 1:
        res = (8.43 * ((1 - uum)**5)) + 1
    elif uum > 1:
        res = 0.32 * uum + 0.68
    return res

def xmu(F: float):
    res = p() * xm(F)
    # print(p(), xm(F), res)
    return res

def s(xxm_: float, F: float):
    if xxm_ <= 1:
        res = 3 * (xxm_**4) - 8 * (xxm_ ** 3) + 6 * (xxm_ ** 2)
        return res
    elif 1 < xxm_ <= 8:
        res = 1.13 / (0.13 * (xxm_**2) + 1)
        return res
    elif F <= 1.5 and xxm_ > 8:
        res = xxm_ / (3.58 * (xxm_**2) - 35.2 * xxm_ + 120)
        return res
    elif F > 1.5 and xxm_ > 8:
        res = 1 / (0.1 * (xxm_**2) + 2.47 * xxm_ - 17.8)
        return res

def c(xxm__: float, F: float, M: float):
    s_ = s(xxm__, F)
    res = s_ * cmu(M, F)
    print(s_, cmu(M, F), res)
    return res, s_

def um():
    if vm < 0.5:
        return 0.5
    elif 0.5 < vm <= 2:
        return vm
    elif vm > 2:
        return vm * (1 + 0.12 * (f() ** (1/2)))

if __name__ == "__main__":
    dT = dt()
    V = v1()
    vm = vm()
    u = 5.0
    uum = u / um()
    san_raz = [("ю", 13.5), ("c", 7.5), ("в", 15.0), ("з", 12.0)]
    for emision in emisions:
        if emision.name == "SO2":
            x_ = []
            data = []
            y_ = []
            range = (10, 50, 100, 300, 400, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000)

            for num, x in enumerate(range):
                xxm = x/xmu(emision.F)
                res, s__ = c(xxm, emision.F, emision.actual_emissions)
                data.append((num+1, x, xxm, s__, res, emision.name))
                y_.append(res)
                x_.append(x)
            tab = tabulate(
                data,
                headers=["#", "x, м", "x/xmu", "S1", "C, мг/м**3", "Вещество"],
                tablefmt="grid",
                disable_numparse=True
            )
            print(tab)

            plt.plot(x_, y_)
            # plt.xticks(numpy.arange(0, max(x_)+1, 400.0))
            # plt.yticks(numpy.arange(0, max(y_) + 1, 1.0 if emision.name == "CO" else 0.5))
            plt.axhline(y=emision.pdkcc, color="r", linestyle='--')
            plt.xlabel('Х, ми', loc="right")
            plt.ylabel('С, мг/м^3', loc="top")
            plt.title(emision.name)
            plt.show()
            for name, value in san_raz:
                print(f"I_{name} = 3285*({value}/12.5) = {3285*(value/12.5)}")