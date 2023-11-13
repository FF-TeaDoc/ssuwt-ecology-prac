from pydantic import BaseModel
from pydantic.type_adapter import TypeAdapter
from tabulate import tabulate


class Emision(BaseModel):
    name: str
    value: float
    k: float

    def m0i(self) -> float:
        """Вычисляет массу выбросов газа и пыли."""
        return self.value * V * 10**-6

    def m0in(self) -> float:
        """Вычисляет приведенную массу выбросов газа и пыли."""
        return self.k * self.m0i()

    def c1i(self) -> float:
        """Вычисляет концентрацию загрязнителя выбросов котельной после применения установки газопылеочистки"""
        return self.value * y / 100

    def m1i(self) -> float:
        """Вычисляет массу выбросов газа и пыли загрязнителя за год работы котельной после применения установки газопылеочистки"""
        return self.c1i() * V * 10**-6

    def m1ni(self) -> float:
        """Вычисляет приведенную массу выбросов газа и пыли  при работе котельной за год после применения установки газопылеочистки"""
        return self.m1i() * self.k


if __name__ == "__main__":
    G = 1500.0
    V_ = 530.0
    V = G * V_
    y = 86.0
    a1 = 4.0
    a2 = 8.0
    b1 = 39.0
    b2 = 61.0
    K = 90.0
    Z = 55.0
    air_pollution = ((b1 * a1) + (b2 * a2)) / 100
    Cos = [
        {"name": "CO", "value": 150.0, "k": 1.0},
        {"name": "SO3", "value": 70.0, "k": 22.0},
        {"name": "ПЗУ", "value": 190.0, "k": 70.0},
        {"name": "КУП", "value": 300.0, "k": 40.0},
    ]
    emisions = TypeAdapter(list[Emision]).validate_python(Cos)
    m0n = 0.0
    m1n = 0.0
    mydata = []
    for num, emision in enumerate(emisions):
        mydata.append(
            (
                num + 1,
                emision.name,
                emision.value,
                emision.c1i(),
                emision.m0i(),
                emision.m1i(),
                emision.m0in(),
                emision.m1ni(),
            )
        )
        m0n += emision.m0in()
        m1n += emision.m1ni()
    y0 = 2400.0 * m0n * air_pollution * 0.81
    y1 = 2400.0 * m1n * air_pollution * 0.81
    ynp = y0 - y1
    table = tabulate(
        mydata,
        headers=["#", "Загрязнитель", "C0i", "C1i", "M0i", "M1i", "M0пi", "M1пi"],
        tablefmt="grid",
    )
    print(table)
    print("\n\n", m0n, m1n, y0, y1, ynp, (ynp / ((K * 1000000) + (Z * 1000000))) * 100)
