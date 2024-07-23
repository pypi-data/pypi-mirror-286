## carrying on


# main = current up-to-date profiling excel
# addition = excel file with new learners



################################################
## to open addition doc and start columns where 'name' appears: ##

file_path = (r'C:\Users\Siphiwe\Desktop\projects\Almost\Grade 8 2024.xlsx')

 # function to determine the header row based on specific criteria
def find_header_row(file_path):
    header_row = None
    max_rows = 10                # for optimization
    
    # read the Excel file without header to scan each row
    df = pd.read_excel(file_path, header=None, nrows=max_rows)
    
    # iterate through each row to find the header row
    for i, row in enumerate(df.values):
        # convert each cell to lowercase string for case-insensitive search
        row_lower = [str(cell).lower() for cell in row]
        
        if 'name' in row_lower:
            # find the index of the first occurrence of 'name'
            name_index = row_lower.index('name')
            
            # if 'school name' is not in the row before 'name', consider it as header
            if 'school name' not in row_lower[:name_index]:
                header_row = i
                break
    return header_row

# determine the header row dynamically
header_row = find_header_row(file_path, max_rows=10)

# read the Excel file skipping rows based on the determined header row
addition = pd.read_excel(file_path,
                        header=header_row,                  # use the detected header row
                        usecols=lambda column: column not in ['Unnamed: 0']        # skip specific columns like 'Unnamed'
                        )
# now the df contains all columns starting from the row with the first occurrence of 'name'
# this is how allexcel sheets are to be read 
####################################################




# to add a concat column of surname and name
main['Full Name'] = main['Surname'] + ' ' + main['First Name']
addition['Full Name'] = addition['Surname'] + ' ' + addition['First Name']

## Step 1 compare 'Full Name' columns to find matches
main.set_index('Full Name', inplace=True)                  # set the Full Name column as the index 
addition.set_index('Full Name', inplace=True)
new_names = addition.index.difference(main.index)          # to find names that are present addition but aren't in main 
common_names = addition.index.intersection(main.index)     # to find names that are already profiled

print(len(common_names))


############################################## SEN PHA ##################################################
# Senior Phase
   ## creating a df called added_names ##
   added_names = pd.DataFrame(columns=main.columns)                            # create 'added_names' DataFrame with columns from main
   columns_to_keep_empty = ['No.', 'LURITS Number', 'FIRST ADDITIONAL LANGUAGE', 'Other, (Specify)']  
   
   # populate 'added_names' with rows from addition corresponding to new_names
   for name in new_names:
       if name in addition.index:
         row = addition.loc[name].copy()                                                         # copy the row from addition DataFrame
         for col in main.columns:                                                                # columns in main but not in addition
            if col not in columns_to_keep_empty and col not in addition.columns:
                row[col] = 'X'                                                                   # fill missing columns with 'X'
         added_names = added_names.append(row)                                                   # add the row to added_names
       else:        
         pass
    added_names.loc[:, 'FIRST ADDITIONAL LANGUAGE'] = main.iloc[5]['FIRST ADDITIONAL LANGUAGE']  # copy the FAL from main
   

   # export as Excel file
   excel_file_path = 'SENPHAadded_names.xlsx'

   added_names.to_excel(excel_file_path, index=False)
#####################################





#################################### FET #########################################

   # FET Phase
   ## creating a df called added_names ##
   added_names = pd.DataFrame(columns=main.columns)                            # create 'added_names' DataFrame with columns from main
   columns_to_keep_empty = ['No.', 'LURITS Number', 'FIRST ADDITIONAL LANGUAGE', 'Other, (Specify)'] 



# define the combinations for subject strean
# the user does this
combination_A = ['ACCOUNTING', 'BUSINESS STUDIES', 'ECONOMICS']
combination_B = ['PHYSICAL SCIENCES', 'LIFE SCIENCES', 'GEOGRAPHY']
combination_C = ['GEOGRAPHY', 'HISTORY', 'TOURISM']

# to create a dictionary that'll map stream values to combinations
stream_combinations = {
    'A': combination_A,
    'B': combination_B,
    'C': combination_C
}

# define the maths type
mType_A = ['MATHEMATICS']
mType_B = ['MATHEMATICAL LITERACY']

# to create a dictionary that'll map stream values to combinations
mType_combinations = {
    'A': mType_A,
    'B': mType_B,
}


for name in new_names:
   try:
        row = addition.loc[name]                                                      # to populate a row
        if 'Stream' not in row or 'Math Type' not in row:                             # ensure 'Stream' and 'Math Type' columns exist in 'addition', if not:
            raise ValueError(f"Missing 'Stream' or 'Math Type' column for entry: {name}")

        stream_value = row['Stream']                                                  # read 'Stream' value
        columns_to_fill = stream_combinations.get(stream_value, [])                   # get columns to fill with 'X'

        mType_value = row['Math Type']                                                # read 'Math Type' value
        math_column_to_fill = mType_combinations.get(mType_value, [])                 # get columns related to math type

        for column in columns_to_fill:                                                # update added_names for the current row
            if column in added_names.columns:
                added_names.loc[name, column] = 'X'

        for column in math_column_to_fill:                                            # update added_names for the current row
            if column in added_names.columns:
                added_names.loc[name, column] = 'X'


        added_names.loc[name, ['No.', 'LURITS Number', 'Other, (Specify)']] = ''      # set specific columns to empty

        added_names.loc[:, 'FIRST ADDITIONAL LANGUAGE'] = main.iloc[5]['FIRST ADDITIONAL LANGUAGE']    # copy the FAL from main

        constant_columns = ['LIFE ORIENTATION']                                       # fill specified constant columns with 'X'
        added_names[constant_columns] = 'X'

    except KeyError as e:
        print(f"KeyError: {e}. Skipping entry: {name}")
    except ValueError as e:
        print(f"ValueError: {e}. Skipping entry: {name}")
    except Exception as e:
        print(f"Error: {e}. Skipping entry: {name}")    



    # export as Excel file
   excel_file_path = 'FETadded_names.xlsx'
   added_names.to_excel(excel_file_path, index=False)




