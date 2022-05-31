# Bitcalc

## Description
A command line utility and module for quick conversion and comparison of bit/byte values

## Installation
You can easily install bitcalc into your Python 3+ environment's site-packages from PyPi with pip:
```
pip install bitcalc
```

Or install the latest version of the repository with pip:
```
pip install git+https://github.com/miliarch/bitcalc.git
```

Once installed, the main bitcalc program interface can be invoked by issuing bitcalc commands in your terminal of choice.

Consider using [virtualenv](https://virtualenv.pypa.io/en/stable/) to create an isolated Python environment for your project. It makes managing Python environments a lot easier (less clutter/conflict in system Python's site-packages).

If you'd rather not use pip to install bitcalc, you can simply clone this repository and copy the bitcalc module into your project directory.

## Help
```
usage: bitcalc [-h] [-b {2,10}] [-d DURATION] [-r RATE] [-a] count label [target_labels [target_labels ...]]

Bitcalc - A command line utility for quick conversion and comparison of bit/byte values

positional arguments:
  count                 specify bit/byte count (numeric)
  label                 specify short unit label of count
  target_labels         specify target short unit label conversion target(s)

                         short unit labels:
                          ambiguous: [b|B] (handled as base-2 by default)
                          base-2: [Kib|KiB|Mib|MiB|Gib|GiB|Tib|TiB|Pib|PiB]
                          base-10: [kb|kB|Mb|MB|Gb|GB|Tb|TB|Pb|PB]

optional arguments:
  -h, --help            show this help message and exit
  -b {2,10}, --base {2,10}
                        specify base for ambiguous unit labels
  -d DURATION, --duration DURATION
                        specify duration for conversion to rate (y:w:d:h:m:s)
                         format examples: [1:30:20|42|3:12:37:15]
                         requires: target_labels specified (first used)
  -r RATE, --rate RATE  specify rate for conversion to duration (e.g.: 10/s)
                         requires: target_labels specified (first used)
  -a, --alt             print alternate table (both base-2 and base-10 units)
```

For more information about IEC and SI notation, see [Ubuntu Units Policy](https://wiki.ubuntu.com/UnitsPolicy).

## Usage and Output Examples
**$ bitcalc 5 GiB B KiB MiB**
```
Value: 5 Gibibytes (GiB)
+-------------------+------------------------+
| (lbl) Unit Label  |                  Value |
+-------------------+------------------------+
|   (B) Bytes       |             5368709120 |
| (KiB) Kibibytes   |                5242880 |
| (MiB) Mebibytes   |                   5120 |
+-------------------+------------------------+
```

**$ bitcalc 5 GiB**
```
Value: 5 Gibibytes (GiB)
+-------------------+------------------------+
| (lbl) Unit Label  |                  Value |
+-------------------+------------------------+
|   (b) Bits        |            42949672960 |
|   (B) Bytes       |             5368709120 |
| (Kib) Kibibits    |               41943040 |
| (KiB) Kibibytes   |                5242880 |
| (Mib) Mebibits    |                  40960 |
| (MiB) Mebibytes   |                   5120 |
| (Gib) Gibibits    |                     40 |
| (GiB) Gibibytes   |                      5 |
| (Tib) Tebibits    |              0.0390625 |
| (TiB) Tebibytes   |             0.00488281 |
| (Pib) Pebibits    |             0.00003815 |
| (PiB) Pebibytes   |             0.00000477 |
+-------------------+------------------------+
```

**$ bitcalc 5 GiB --alt**
```
Value: 5 Gibibytes (GiB)
+-------------------------+-------------------------+
|          Value (base-2) |         Value (base-10) |
+-------------------------+-------------------------+
|         42949672960 b   |          42949672960 b  |
|          5368709120 B   |           5368709120 B  |
|            41943040 Kib |          42949672.96 kb |
|             5242880 KiB |           5368709.12 kB |
|               40960 Mib |            42949.673 Mb |
|                5120 MiB |             5368.709 MB |
|                  40 Gib |                42.95 Gb |
|                   5 GiB |                5.369 GB |
|           0.0390625 Tib |           0.04294967 Tb |
|          0.00488281 TiB |           0.00536871 TB |
|          0.00003815 Pib |           0.00004295 Pb |
|          0.00000477 PiB |           0.00000537 PB |
+-------------------------+-------------------------+
```

**$ bitcalc 5 GiB MiB --duration 10:35**
```
Value: 5 Gibibytes (GiB)
Duration: 0:10:35
Data rate: 8.063 MiB/s
```

**$ bitcalc 5 TiB MiB --rate 37/s**
```
Value: 5 Tebibytes (TiB)
Duration: 1 day, 15:21:39
Data rate: 37 MiB/s
```

## Version History / Change Log

* 2019-12-21 - v1.4 - Implemented data rate and duration handling (does not yet account for overhead)
* 2019-11-23 - v1.3 - Pinned to Python 3+
* 2019-11-23 - v1.2 - Name simplification and re-write; support of targeted conversion and output of combo value output (base-2 and base-10); introduction of setup.py for pip installation and modular import
* 2019-02-16 - v1.1 - Refactoring and general improvements
* 2016-09-14 - v1.0 - First functional release

## About
This is a little project that's been in the works for a while. Frequently dealing with storage/filesystem management, I found that I'd often need to convert between different bit and byte values. Most of the time, I'd just head over to [Matisse's Bit Calculator](http://www.matisse.net/bitcalc/), as it suited my needs perfectly. Over time this became a bit cumbersome, and I sought to find a locally executable equivalent. **I didn't find one, so I built one!**