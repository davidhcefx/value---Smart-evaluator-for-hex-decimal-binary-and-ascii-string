# value - Smart Evaluator for Hex/Decimal/Binary/Ascii String

This tool is similar to [WinDBG](https://docs.microsoft.com/zh-tw/windows-hardware/drivers/debugger/debugger-download-tools)'s `?` evaluation, or [GEF gdb](https://gef.readthedocs.io/en/master/commands/eval/)'s `$` evaluation.

# Use cases

```bash
$ value 48879
0xbeef
$ value 0xb
0b1011
$ value /bin/sh
0x2f62 0x696e 0x2f73 0x68
$ value 2f62696e
'/bin'
$ value 121 184 255  # RGB values
121 = 0x79
184 = 0xb8
255 = 0xff
$ value + - , .
'+' = 0x2b
'-' = 0x2d
',' = 0x2c
'.' = 0x2e
```
