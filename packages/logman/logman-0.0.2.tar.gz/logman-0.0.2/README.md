# logman

**logman** is inspired by the SLF4J LoggerFactory from the Spring ecosystem. It aims to provide a similar experience for Python developers, featuring JSON logging and log rotation capabilities.

visit <https://logman.wimcorp.dev>

## Quickstart

1. Install logman

```bash
$ pip install logman
```

2. Import and use the logger

```python
from logman import LoggerFactory

class MyClass:
  def **init**(self):
    self.logger = LoggerFactory.getLogger(self.__class__.__name__)

  def my_method(self):
      self.logger.info('Hello, World!')

myClass = MyClass()
myClass.my_method()
```

```bash
$ python my_script.py
{"context": "MyClass", "level": "INFO", "timestamp": "2024-07-24 16:25:10.016", "message": "Hello, World!", "thread": "MainThread"}
```

## Run Tests

### pytest

```bash
pip install pytest
python -m unittest discover -s tests -p 'test_*.py'
```

### tox

```bash
pip install tox pytest
tox
```

## Build Docs

### Sphinx

```bash
pip install Sphinx sphinx-autobuild sphinx-rtd-theme myst_parser
cd docs
make html
```
