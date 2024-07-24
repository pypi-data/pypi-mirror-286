<img src="https://raw.githubusercontent.com/puzzle-in-a-mug/paramcheckup/main/docs/_static/logo.png" align="right" />

# paramcheckup

<img src="https://img.shields.io/badge/License-BSD%203--Clause-blue.svg">

This package has a collection of functions that check whether the parameter received has a certain type, returning ``True`` if the input is as expected or ``raising an error`` that indicates what the problem is.



## Install

```
pip install paramcheckup
```



## Example 1


```python
import numpy as np
from scipy import stats
```

Assume a function ``t_test()`` that applies one sample Student's t test to compare means (two sided). This function receives three parameters, which are ``x_data``, ``mu`` and ``alpha``.

```python
def t_test(x_data, mu, alpha):
    tcalc = (x_data.mean() - mu)*np.sqrt(x_data.size)/(x_data.std(ddof=1))
    t_critical = stats.t.ppf(1-alpha/2, x_data.size - 1)
    p_value = (1 - stats.t.cdf(np.abs(tcalc), x_data.size - 1))*2
    if p_value < alpha:
        conclusion = "Reject H0"
    else:
        conclusion = "Fail to reject H0"
    return tcalc, t_critical, p_value, conclusion
```

The ``t_test`` function strongly depends on the ``x_data`` parameter being a one-dimensional ``NumpyArray``. The ``types.is_numpy(value, param_name, func_name)`` function can checks whether ``x_data`` is in fact a ``NumpyArray`` (``True``):



```python
from paramcheckup import types
def t_test(x_data, mu, alpha):
    types.is_numpy(
        value=x_data,
        param_name="x_data",
        kind="function",
        kind_name="t_test",
        stacklevel=4,
        error=True,
    )
    
    tcalc = (x_data.mean() - mu)*np.sqrt(x_data.size)/(x_data.std(ddof=1))
    t_critical = stats.t.ppf(1-alpha/2, x_data.size - 1)
    p_value = (1 - stats.t.cdf(np.abs(tcalc), x_data.size - 1))*2
    if p_value < alpha:
        conclusion = "Reject H0"
    else:
        conclusion = "Fail to reject H0"
    return tcalc, t_critical, p_value, conclusion
```

If the user passes a ``NumpyArray`` as input for ``x_data``, the result of ``types.is_numpy`` will be ``True`` and the calculation will be performed as expected:

```python
x = np.array([1.24, 1.3, 1.11])
result = t_test(x, 3, 0.05)
print(result)
(-31.80244895786038, 4.302652729911275, 0.0009872686643235262, 'Reject H0')
```

However, if you use a ``list`` instead of ``NumpyArray``, an ``TypeError`` will be raised indicating what the error is:

```python
x = [1.24, 1.3, 1.11]
result = t_test(x, 3, 0.05)
The parameter 'x_data' in function 't_test' must be of type *numpy.ndarray*, but its type is *list*.
UserWarning at line 28: The parameter `x_data` in function `t_test` must be of type `numpy.ndarray`, but its type is `list`.
```

The UserWarning informs the line ***where*** the error occurred, ***which parameter*** is wrong and ***how*** this parameter should be to be correct. By default, the error traceback is also showed to the user:

```
Traceback (most recent call last):
  File "...\main.py", line 21, in <module>
    result = t_test(x, 3, 0.05)
  File "...\main.py", line 8, in t_test
    types.is_numpy(x_data, "x_data", "t_test")
  File "...\venv\lib\site-packages\paramcheckup\types.py", line 436, in is_numpy
    raise TypeError("NotNumPyError")
TypeError: NotNumPyError
```

However, it is possible to silence the traceback through the error parameter:

```python
types.is_numpy(
    value=x_data,
    param_name="x_data",
    kind="function",
    kind_name="t_test",
    stacklevel=4,
    error=False, # <------
)
```

> Note that the function also requires the array to have a single dimension. This could be checked using the ``paramcheckup.numpy_arrays.n_dimensions function()``. 

## Example 2

The ``alpha`` parameter indicates the level of significance that should be adopted for the test. It is a value that varies between ``0`` and ``1``. To limit the range of values, you can use the ``numbers.is_between_a_and_b()`` function:

```python
from paramcheckup import types, numbers

def t_test(x_data, mu, alpha):
    types.is_numpy(
        value=x_data,
        param_name="x_data",
        kind="function",
        kind_name="t_test",
        stacklevel=4,
        error=False,
    )

    numbers.is_between_a_and_b(
        number=alpha,
        lower=0,
        upper=1,
        param_name="alpha",
        kind="function",
        kind_name="t_test",
        inclusive=False,
        stacklevel=4,
        error=False,
    )

    tcalc = (x_data.mean() - mu)*np.sqrt(x_data.size)/(x_data.std(ddof=1))
    t_critical = stats.t.ppf(1-alpha/2, x_data.size - 1)
    p_value = (1 - stats.t.cdf(np.abs(tcalc), x_data.size - 1))*2
    if p_value < alpha:
        conclusion = "Reject H0"
    else:
        conclusion = "Fail to reject H0"
    return tcalc, t_critical, p_value, conclusion


x = np.array([1.24, 1.3, 1.11])
alpha = 1.05
result = t_test(x, 3, alpha)
UserWarning at line 39: The value of `alpha` in function `t_test` must be within the range of `0 < alpha < 1`, but it is `1.05`.
```


> Note that the ``inclusive=False`` parameter causes the limits to be open, which makes sense for the significance level. If ``inclusive=True``, we would have obtained the following error:

```python
UserWarning at line 39: The value of `alpha` in function `t_test` must be within the range of `0 <= alpha <= 1`, but it is `1.05`.
```

> Note that ``alpha`` must be of numeric type. This could be checked using function ``paramcheckup.numbers.is_float_or_int()`` ***before*** checking whether the parameter is within a numerical range.


## License

- [BSD 3-Clause License](https://github.com/puzzle-in-a-mug/paramcheckup/blob/main/LICENSE)




