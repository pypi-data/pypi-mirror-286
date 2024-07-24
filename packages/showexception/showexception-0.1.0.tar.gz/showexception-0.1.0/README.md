# QuickColor

**ShowException** is a Python exception display assitant providing pretty print capability of exception details from a specified code area/module name. CLI test functionality provided to demo display characteristics for several exception types.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install **showexception**.

```bash
pip install showexception
```


## Library Usage
```python
from showexception.showexception import exception_details

try:
    x = 1/0

except Exception as e:
    exception_details(e, 'test-except-show')
```


## CLI Utility

The following CLI is included with this package for visualizing a few exceptions.

```bash
# testexcept -h
usage: testexcept [-h] [-r] {test.zero.div,test.name.err,test.type.err} ...

-.-.-. Exception Content Display for python scripts

positional arguments:
  {test.zero.div,test.name.err,test.type.err}
    test.zero.div       display exception info for a divide by zero exception
    test.name.err       display exception info for a name error exception
    test.type.err       display exception info for a type error exception

options:
  -h, --help            show this help message and exit
  -r, --raw             show raw exception details

-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
```


## License

[MIT](https://choosealicense.com/licenses/mit/)

