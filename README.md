# Python Bit Calculator (pybitcalc)

## Synopsis
    python bitcalc.py [-a amount] [-t type] [-b base]

## Description
    A simple python2/3 program for printing a conversion table of different byte values to console.

## Command Line Options
```
-a float, --amount float
    Specify amount bits/bytes

        
-b int, --base int
    Specify which base notation to use (only affects -t b and B).
    See Ubuntu's Units Policy for more info:
    https://wiki.ubuntu.com/UnitsPolicy
        
    Valid Options
    2 - 1024 bytes in kilobyte/base-2/IEC Notation (default)
    10 - 1000 bytes in kilobyte/base-10/SI Notation

-h, --help
    Print usage information

        
-t string, --type string
    Specify type of amount
        
    Valid Options
    Flexible - b, B (default base-2)
    base-2 - Kib, KiB, Mib, MiB, Gib, GiB, Tib, TiB, Pib, PiB
    base-10 - kb, kB, Mb, MB, Gb, GB, Tb, TB, Pb, PB
```

## Usage and Output Examples
**$ ./bitcalc.py -a 1024 -t B**
```
Bytes selected, no base specified, using base-2.
Run again and specify -b 10 or --base 10 for base-10.

Unit Type           Value
  b - Bits          8192
  B - Bytes         1024
Kib - Kibibits      8
KiB - Kibibytes     1
Mib - Mebibits      0.0078125
MiB - Mebibytes     0.0009765625
Gib - Gibibits      0.000007629394531
GiB - Gibibytes     0.000000953674316
Tib - Tebibits      0.000000007450581
TiB - Tebibytes     0.000000000931323
Pib - Pebibits      0.000000000007276
PiB - Pebibytes     0.000000000000909
```

**$ ./bitcalc.py -a 1000 -t B -b 10**
```
Unit Type           Value
 b - Bits           8000
 B - Bytes          1000
kb - Kilobits       8
kB - Kilobytes      1
Mb - Megabits       0.008
MB - Megabytes      0.001
Gb - Gigabits       0.000008
GB - Gigabytes      0.000001
Tb - Terabits       0.000000008
TB - Terabytes      0.000000001
Pb - Petabits       0.000000000008
PB - Petabytes      0.000000000001
```

**$ ./bitcalc.py -a 53.7 -t GiB**
```
Unit Type           Value
  b - Bits          461279487590.4
  B - Bytes         57659935948.8
Kib - Kibibits      450468249.6
KiB - Kibibytes     56308531.2
Mib - Mebibits      439910.4
MiB - Mebibytes     54988.8
Gib - Gibibits      429.6
GiB - Gibibytes     53.7
Tib - Tebibits      0.41953125
TiB - Tebibytes     0.05244140625
Pib - Pebibits      0.000409698486328
PiB - Pebibytes     0.000051212310791
```

**$ ./bitcalc.py -a 53.7 -t GB**
```
Unit Type           Value
 b - Bits           429600000000
 B - Bytes          53700000000
kb - Kilobits       429600000
kB - Kilobytes      53700000
Mb - Megabits       429600
MB - Megabytes      53700
Gb - Gigabits       429.6
GB - Gigabytes      53.7
Tb - Terabits       0.4296
TB - Terabytes      0.0537
Pb - Petabits       0.0004296
PB - Petabytes      0.0000537
```

## Version History / Change Log
09/14/2016 - v1.0 - First functional release

## About
This is a little project that's been in the works for a while. Frequently dealing with storage/filesystem management, I found that I'd often need to convert between different bit and byte values. Most of the time, I'd just head over to [Matisse's Bit Calculator](http://www.matisse.net/bitcalc/), as it suited my needs perfectly. Over time, this became a bit cumbersome for my needs (connect to internet, launch browser, visit site), and I sought to find a locally executable equivalent. **I didn't find one!**

I originally built this bit calculator as a Java GUI program. This was great, until I:
* Developed a preference for command line applications
* Discovered how much of a blast Python programming can be

I don't currently have plans to release the Java code, but I might just revisit it in the future.
