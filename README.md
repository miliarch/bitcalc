# Python Bit Calculator (pybitcalc)

## Description
    A simple program for printing a conversion table of bit and byte values for a given input value

## Help
```
usage: bitcalc.py [-h] [-b BASE] amount type

A simple program for printing a conversion table of bit and byte values for a given input value

positional arguments:
  amount                specify bit/byte amount
  type                  specify bit/byte type as short unit label - valid options:
                          ambiguous: [b|B] (handled as base-2 by default)
                          base-2: [Kib|KiB|Mib|MiB|Gib|GiB|Tib|TiB|Pib|PiB]
                          base-10: [kb|kB|Mb|MB|Gb|GB|Tb|TB|Pb|PB]

optional arguments:
  -h, --help            show this help message and exit
  -b BASE, --base BASE  specify base for ambiguous unit labels - valid options: [2|10]
```

For more information about IEC and SI notation, see [Ubuntu Units Policy](https://wiki.ubuntu.com/UnitsPolicy).

## Usage and Output Examples
**$ ./bitcalc.py 1024 B**
```
Bytes selected, no base specified, using base-2.
Run again with -b 10 or --base 10 for base-10.

Input value: 1024.0 B
+-------------------+------------------------+
| (lbl) Unit Label  |         Value (base-2) |
+-------------------+------------------------+
|   (b) Bits        |                   8192 |
|   (B) Bytes       |                   1024 |
| (Kib) Kibibits    |                      8 |
| (KiB) Kibibytes   |                      1 |
| (Mib) Mebibits    |              0.0078125 |
| (MiB) Mebibytes   |           0.0009765625 |
| (Gib) Gibibits    |      0.000007629394531 |
| (GiB) Gibibytes   |      0.000000953674316 |
| (Tib) Tebibits    |      0.000000007450581 |
| (TiB) Tebibytes   |      0.000000000931323 |
| (Pib) Pebibits    |      0.000000000007276 |
| (PiB) Pebibytes   |      0.000000000000909 |
+-------------------+------------------------+
```

**$ ./bitcalc.py 1000 B -b 10**
```
Input value: 1000.0 B
+-------------------+------------------------+
| (lbl) Unit Label  |        Value (base-10) |
+-------------------+------------------------+
|   (b) Bits        |                   8000 |
|   (B) Bytes       |                   1000 |
|  (kb) Kilobits    |                      8 |
|  (kB) Kilobytes   |                      1 |
|  (Mb) Megabits    |                  0.008 |
|  (MB) Megabytes   |                  0.001 |
|  (Gb) Gigabits    |               0.000008 |
|  (GB) Gigabytes   |               0.000001 |
|  (Tb) Terabits    |            0.000000008 |
|  (TB) Terabytes   |            0.000000001 |
|  (Pb) Petabits    |         0.000000000008 |
|  (PB) Petabytes   |         0.000000000001 |
+-------------------+------------------------+
```

**$ ./bitcalc.py 53.7 GiB**
```
Input value: 53.7 GiB
+-------------------+------------------------+
| (lbl) Unit Label  |         Value (base-2) |
+-------------------+------------------------+
|   (b) Bits        |         461279487590.4 |
|   (B) Bytes       |          57659935948.8 |
| (Kib) Kibibits    |            450468249.6 |
| (KiB) Kibibytes   |             56308531.2 |
| (Mib) Mebibits    |               439910.4 |
| (MiB) Mebibytes   |                54988.8 |
| (Gib) Gibibits    |                  429.6 |
| (GiB) Gibibytes   |                   53.7 |
| (Tib) Tebibits    |             0.41953125 |
| (TiB) Tebibytes   |          0.05244140625 |
| (Pib) Pebibits    |      0.000409698486328 |
| (PiB) Pebibytes   |      0.000051212310791 |
+-------------------+------------------------+
```

**$ ./bitcalc.py 53.7 GB**
```
Input value: 53.7 GB
+-------------------+------------------------+
| (lbl) Unit Label  |        Value (base-10) |
+-------------------+------------------------+
|   (b) Bits        |           429600000000 |
|   (B) Bytes       |            53700000000 |
|  (kb) Kilobits    |              429600000 |
|  (kB) Kilobytes   |               53700000 |
|  (Mb) Megabits    |                 429600 |
|  (MB) Megabytes   |                  53700 |
|  (Gb) Gigabits    |                  429.6 |
|  (GB) Gigabytes   |                   53.7 |
|  (Tb) Terabits    |                 0.4296 |
|  (TB) Terabytes   |                 0.0537 |
|  (Pb) Petabits    |              0.0004296 |
|  (PB) Petabytes   |              0.0000537 |
+-------------------+------------------------+
```

## Version History / Change Log

* 02/16/2019 - v1.1 - Refactoring and general improvements
* 09/14/2016 - v1.0 - First functional release

## About
This is a little project that's been in the works for a while. Frequently dealing with storage/filesystem management, I found that I'd often need to convert between different bit and byte values. Most of the time, I'd just head over to [Matisse's Bit Calculator](http://www.matisse.net/bitcalc/), as it suited my needs perfectly. Over time, this became a bit cumbersome for my needs (connect to internet, launch browser, visit site), and I sought to find a locally executable equivalent. **I didn't find one, so I built one!**
