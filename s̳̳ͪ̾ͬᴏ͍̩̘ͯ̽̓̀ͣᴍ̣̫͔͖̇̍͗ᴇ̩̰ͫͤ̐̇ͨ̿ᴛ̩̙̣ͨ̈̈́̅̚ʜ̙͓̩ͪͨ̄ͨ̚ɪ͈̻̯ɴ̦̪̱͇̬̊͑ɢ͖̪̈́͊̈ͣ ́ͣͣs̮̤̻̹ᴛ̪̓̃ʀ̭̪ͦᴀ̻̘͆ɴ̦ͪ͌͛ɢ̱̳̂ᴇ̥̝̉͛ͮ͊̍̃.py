import re

file = 'Demo.Backend.MutliExpressionCalculator.LinesProcessor'


lines = []
with open(file + '.py','r') as f:
    lines = f.readlines()

new_lines = []

for i in lines:
    result = re.search('#.*', i)
    if (result != None):
        new_lines.append(i.replace(result.group(0),"").rstrip()+ '\n')
    else:
        new_lines.append(i.rstrip() + '\n')

with open(file + '.py','w') as f:
    f.writelines(new_lines)
