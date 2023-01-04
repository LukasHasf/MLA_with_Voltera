import io

with io.open("lenses.txt", "r", encoding='utf-16-le') as infile:
    lenses = infile.readlines()
with open("MLA_arr/MLA_arr.kicad_pcb", "r") as infile:
    template = infile.readlines()

output = []
for line in template:
    if "%lenses" in line:
        for lensline in lenses:
            output.append(lensline)
    else:
        output.append(line)

with io.open("output.kicad_pcb", "w", encoding='utf-8') as outfile:
    for line in output:
        outfile.write(line)
