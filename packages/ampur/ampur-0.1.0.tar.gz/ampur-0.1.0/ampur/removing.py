## carrying on...

# main = most recent profiling doc
# removal = excel file with learners that should be removed



# to add a concat column of surname and name
main['Full Name'] = main['Surname'] + ' ' + main['First Name']
removal['Full Name'] = removal['Surname'] + ' ' + removal['First Name']


#  #

## Step 1 compare 'Full Name' columns to find matches
    # set the Full Name column as the index 
main.set_index('Full Name', inplace=True)
removal.set_index('Full Name', inplace=True)
    # to find matches based on 'Full Name' 
common_names = main.index.intersection(removal.index)


# save and export excel file
output_file = r'C:\Users\Siphiwe\Desktop\projects\Almost\RetentionImplemented.xlsx'           # define the file path and name
main.to_excel(output_file, index=True)                                                        # save DataFrame to Excel

############################
# to color the rows
# define the Excel file path
excel_file_path = 'main_with_common_names_colored.xlsx'

# write main DataFrame to Excel
main.to_excel(excel_file_path, sheet_name='Sheet1', index=False)

# load the workbook and select the active worksheet
wb = openpyxl.load_workbook(excel_file_path)
ws = wb.active

# apply red color fill to rows with common names in 'Full Name' column (column A)
red_fill = PatternFill(start_color='FFFF0000', end_color='FFFF0000', fill_type='solid')
for row_num in range(2, ws.max_row + 1):  # Skip header row (1)
    full_name = ws[f'A{row_num}'].value  # Get 'Full Name' from column A
    if full_name in common_names:
        for col_num in range(1, ws.max_column + 1):
            ws.cell(row=row_num, column=col_num).fill = red_fill

# save the workbook with applied styles
wb.save(excel_file_path)


# to remove index ('Full Name')
main_modified = pd.read_excel(excel_file_path, index_col=0)            # 'Full Name' is the first column since it's the index

# remove the index ('Full Name' column) from the DataFrame
main_modified.reset_index(drop=True, inplace=True)

# save the modified DataFrame back to Excel without index
excel_file_path_no_index = 'main_data_no_index.xlsx'
main_modified.to_excel(excel_file_path_no_index, index=False)




