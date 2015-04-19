aloft.py
===

[![Build Status](https://travis-ci.org/natemara/aloft.py.svg?branch=master)](https://travis-ci.org/natemara/aloft.py)

A simple API for NOAA winds aloft data.

Installation
---

The easiest way to install is from PyPi.

```bash
$ pip install aloft.py
```

Example
---

Using the API is incredibly simple:

```python
>>> from aloft.api import winds_aloft

>>> winds = winds_aloft('cvg')
>>> print(winds.winds[3000])
Wind(direction=360, speed=8)
```
