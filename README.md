# Shadrak ![](img/logo-small.png)

> Inspired by [ZipBomb](https://github.com/abdulfatir/ZipBomb)

Shadrak is a script to generate decompression bomb in various formats.

Use cases:
- Crash or keep busy AV/EDR
- Crash automatic forensic tools
- Crash/bypass antispam
- DOS on anything that decompress (more than I can think of)

Currently supporting the following formats: 7z, arc, arj, bcm, br, exe, lrz, jar, qp, rar, sfx, tar.bzip2, tar.gzip, tar.xz, war, zip, zpaq, zst

Future improvements: also working on nested arrays, currently supporting json (thanks to jtorvald) using json.sh, to be integrated in the main tool soon with additional formats (cbor, msgpack, ...). Images are more complex than expected, if you are interested see dev_notes.txt

# Installation

```sh
git clone https://gitlab.com/brn1337/shadrak.git
cd shadrak
# read the source before executing sudo stuff, or don't, I'm a comment not a cop
sudo bash install.sh
```

# Usage

Create a zip archive containing 10 zips, each zip contains 10 zips, each zip contains a 1GB file, for a total of 100GB

```bash
python3 shadrak.py zip
```

Create a rar archive containing 30 zips, with 5 levels of nesting, each containing a 500MB file, for a total of 24PB, with verbose output

```bash
python3 shadrak.py rar -l 5 -n 30 -s 512000 -v
```

Create a 7z archive containing a single 10GB file, quietly

```bash
python3 shadrak.py 7z -l 0 -s 10485760 -q
```

List all supported compression formats

```bash
python3 shadrak.py list
```

Generate every supported zipbomb, with 3 levels of nesting

```bash
bash generator.sh -l 3
```

# References

- https://github.com/abdulfatir/ZipBomb
- https://stackoverflow.com/questions/1459673/how-does-one-make-a-zip-bomb

# License

Shadrak is licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1)

```
CC-BY-NC-SA This license requires that reusers give credit to the creator.
It allows reusers to distribute, remix, adapt, and build upon the material in any medium or format, for noncommercial purposes only.
If others modify or adapt the material, they must license the modified material under identical terms.
- Credit must be given to you, the creator.
- Only noncommercial use of your work is permitted.
- Adaptations must be shared under the same terms.
```
