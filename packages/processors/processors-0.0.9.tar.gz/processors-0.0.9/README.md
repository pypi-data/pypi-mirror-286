# Processors

This repo groups together preprocessing and postprocessing functions to allow easy clean up of data.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Usage

```python
from processors import TextProcessor
process = TextProcessor()
processor.process("       this is%20absolutely%20horrible%20  text 😠!!!! !!??? ?    that needs to be   cleaned up         ")
'This is absolutely horrible text :angry face: ! That needs to be cleaned up.'
```
