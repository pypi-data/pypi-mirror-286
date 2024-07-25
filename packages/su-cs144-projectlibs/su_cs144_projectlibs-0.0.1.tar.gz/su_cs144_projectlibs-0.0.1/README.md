# SU project libs for Python 3 for CS144

`su-cs144-projectlibs` is a support library for 2024 CS114 semester project conducted in computer science department at Stellenbosch University.

## Installation

This library requires a functioning Python 3 environment.

### With pip
For Python versions 3.8 - 3.10, due to compatability infeasibilities, the current safest option is to install most requirements manually before installing this package.

```bash
python3 -m pip --upgrade pip
python3 -m pip --upgrade wheel
python3 -m pip --upgrade setuptools
```

After the above commands execute sucessfully, install `su-cs144-projectlibs` simply with
```bash
python3 -m pip install --upgrade su-cs144-projectlibs
```

To test that you have installed the library correctly, run this command:
```bash
python3 -c 'from compass import Compass; c = Compass(2, 2, 4); print(c.get_next_trajectory())'
```
This should print a tuple where the first element is a float and the second an integer.

## Contributors

- Dylan Callaghan
- Marcel Dunaiski

## License

This project is licensed. See the [LICENSE](LICENSE) file for details.
