# MLA with Voltera
Trying to create microlens arrays on the Voltera V-One platform

# Usage
```
$ python spiral.py > lenses.txt
```
then
```
$ python change_project.py
```
This generates `output.kicad_pcb` which can be opened with KiCad. From KiCad, you can then export a Gerber file for the copper layer, which contains the microlens geometry.

# References
`spirals.py` is a modification of https://gist.github.com/JoanTheSpark/e3fab5a8af44f7f8779c
