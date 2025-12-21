import math

# Функции заданные явно, для 3 итерации, так как для процессов нельзя использовать лямбда функции
def func_polynomial(x):
    return x ** 2

def func_complex(x):
    return x**3 + 2*x

def complex_test_func(x):
    return (
        (math.gamma(x + 2) * math.sin(x ** 2) * math.exp(math.log(x + 1) ** 2))
        / (math.factorial(max(1, int(x))) * math.sqrt(x ** 3 + 1))
    )