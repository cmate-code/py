from pathlib import Path
from datetime import datetime
from openpyxl import workbook, Workbook

dir = Path(input('Enter the path of the directory: '))
ft = input('Enter the type of the file: ') # ft = FileType

WB = Workbook()
WS = WB.active

WS.append(['Filename', 'Last edit', 'Path'])

for i in dir.rglob('*'):
    if i.is_file() and i.suffix.lower() == ft:
        print(i.name, datetime.fromtimestamp(i.stat().st_mtime), i)
        WS.append([str(i.name), str(datetime.fromtimestamp(i.stat().st_mtime)), str(i)])

WB.save(dir/'list.xlsx')