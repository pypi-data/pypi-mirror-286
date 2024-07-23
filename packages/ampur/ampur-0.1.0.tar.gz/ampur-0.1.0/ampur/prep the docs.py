import pandas as pd  
from openpyxl import load_workbook            # for coloring
from openpyxl.styles import PatternFill
pd.set_option('display.max_columns', 200) 

# read in the docs
main = pd.read_excel(r'C:\Users\Siphiwe\Desktop\projects\Almost\PRUDENS-SECONDARY-SCHOOL-Learners.xlsx',sheet_name='FET Template', header=4)
update = pd.read_excel(r'C:\Users\Siphiwe\Desktop\projects\Almost\LearnerSyllabusExport_700111195_2023_ENGLISH_20221201 - Prudens.xlsx',sheet_name='FET Template', header=4)


### cleaning ###

# dropping columns
main = main.drop('Unnamed: 0',axis=1)
update = update.drop('Unnamed: 0',axis=1)







