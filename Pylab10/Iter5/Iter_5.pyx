from libc.math cimport sin, cos, exp, log, sqrt, tgamma

cdef double integrate_cython_real(double a, double b, int n_iter) nogil:
    cdef double result = 0.0
    cdef double step = (b - a) / n_iter
    cdef int i
    cdef double x
    cdef int x_int
    cdef double gamma_val, sin_x2, exp_log2, factorial_val, sqrt_val

    for i in range(n_iter):
        x = a + i * step
        x_int = max(1, <int>x)
        gamma_val = tgamma(x + 3)
        sin_x2 = sin(x * x)
        exp_log2 = exp(log(x + 1) * log(x + 1))
        factorial_val = tgamma(x_int + 1)
        sqrt_val = sqrt(x * x * x + 1)
        result += (gamma_val * sin_x2 * exp_log2) / (factorial_val * sqrt_val) * step

    return result

cpdef double integrate_nogil(double a, double b, int n_iter = 1000):
    return integrate_cython_real(a, b, n_iter)