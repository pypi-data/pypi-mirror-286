# My Package

A sample Python package.

## Installation

You can install the package using pip:

```
pip install roundr
```

## Usage

Here is an example of how to use the package:

```python
from roundr import roundr

roundr(32.56,1) # 32.6
roundr(349.5) # 350
roundr(6.54,1) | roundr(6.54) # 6.5
roundr('6.55') # 6.6
roundr(6.56,'1') # 6.6
roundr(6,'e') # "Invalid input, try again!"
roundr('r',3) # "Invalid input, try again!"
```
