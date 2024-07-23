## carrying on..

# main = Roll over doc
# update = Retention Schedule



# still need to figure: what to do with the class
# more cleaning
main['Grade'] = pd.to_numeric(main['Grade'], errors='coerce')     # make sure data type is float, if it says error then make it NaN

# to add a concat column of surname and name
main['Full Name'] = main['Surname'] + ' ' + main['First Name']
update['Full Name'] = update['Surname'] + ' ' + update['First Name']


# taking learners back #
#################################################
## Step 1 compare 'Full Name' columns to find matches
    # set the Full Name column as the index 
main.set_index('Full Name', inplace=True)
update.set_index('Full Name', inplace=True)
    # to find the set of index labels that are present in both main and update, 
    # essentially finding matches based on 'Full Name' 
common_names = main.index.intersection(update.index)

# row refers to the entire row where 'name' is, 'name' is the specific 'Full Name' value that matched
for name in common_names:                        # 'name' represents each index label of the common_names (the intersection)
    row1 = main.loc[name]                        # location: allows us to access rows and columns in the DataFrame using their labels rather than numeric indices
    row2 = update.loc[name]
#################################################


#################################################
## Step 2: return learners back to the previous grade
returned_learners = []
# all learners that match have to be returned (update = retention schedule)
# learners that fall in the 'else' must be reviewed manually
if main.loc[name, 'Grade'] - update.loc[name, 'Grade'] == 1:
        main.loc[name,'Grade'] -= 1
        returned_learners.append(name)                # save the names in a list
    else:
        print(f"'{name}' was not adjusted. Please review")
print(f"Learners that have been returned to the previous grade: {returned_learners}")
#################################################


#################################################
# to see names of learners in 'update' that were not found on 'main'
learners_not_found = []                                     # an empty list 
print("List of learners not found:")                        # a heading
for index_label in update.index:
    if index_label not in common_names:                     # meaning not in the intersection, meaning not a match
        learners_not_found.append(index_label)              # append means add
print(learners_not_found)                                   # to see learners not found on 'main'

print(len(learners_not_found))                              # to see number of learners not found
#################################################



##################################################################################################
## an extra effort
## flip the names on the learners_not_found list and look for matches again
# Function to flip names
def flip_name(full_name):
    if isinstance(full_name, str):                          # Check if full_name is a string
        parts = full_name.split()                           # Split the full name into parts (assuming a simple first name last name format)
        flipped_name = ' '.join(reversed(parts))            # Reverse the order of parts and join with a space
        return flipped_name

# Flip all names in the list
# here 'name' refers to an individual element from the list, basically 'value'
flipped_names = [flip_name(name) for name in learners_not_found]
print("Flipped names:")
for name in flipped_names:
    print(name)

# look for matches with the flipped names
common_names2 = main.index.intersection(flipped_names)
# check if there's any matches
print(len(common_names2))
# if there are matches, print them and ask whether to adjust
for name in common_names2:
    print(name)

# if user wants to adjust                       
if len(common_names2) >= 1:
    for name in common_names2:
        print(name)
        user_input = input(f"Return '{name}' to the previous grade? (yes/no): ").strip().lower()
        if user_input == 'yes':
            main.loc[name,'Grade'] -= 1
            print(f"'{name}' has been returned to the previous grade")
        elif user_input == 'no':
            pass  # do nothing
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
else:
    pass  # do nothing
##################################################################################################



# save and export excel file
output_file = r'C:\Users\Siphiwe\Desktop\projects\Almost\RetentionImplemented.xlsx'           # Define the file path and name
main.to_excel(output_file, index=True)           # Save DataFrame to Excel


## Step 3: color the Returned learners rows Yellow

# Load workbook
wb = load_workbook(output_file)          # defined above
sheet_name = 'FET Template'              # Specify the sheet name
ws = wb[sheet_name]                      

# Iterate over rows in the DataFrame
for index, row in main.iterrows():
    if index in returned_learners:
        # find row number based on index label (add 2 to skip header and 1-based indexing in Excel)
        row_num = main.index.get_loc(index) + 2
        
        # apply yellow fill to the entire row
        yellow_fill = PatternFill(start_color='FFFF00', end_color='FFFF00', fill_type='solid')
        for cell in ws[f"A{row_num}":f"{ws.max_column}{row_num}"]:      # adjust range as needed
            cell.fill = yellow_fill                                     # apply fill color

# Save the workbook
wb.save(output_file)                # output_file is defined above








######### alternative approaches, rejected #########

# to check if everything else matches on the rows that matched
# i.e the full name on both docs matches, now lets check if all other rows match as well
for name in common_names:                        # 'name' should represent each index label of the common_names (the intersection)
    row1 = main.loc[name]                        # location: allows us to access rows and columns in the DataFrame using their labels rather than numeric indices
    row2 = update.loc[name]
    
    # Check if everything else on the row matches
    if all(row1 == row2):
        print(f"Matching row found for '{name}':")
        ##print(row1)
    else:
        print(f"Row does not match for '{name}':")


# to see number of rows that matched
num_matched = len(common_names)
# Number of rows in update that did not match
num_not_matched = len(update) - num_matched

print(f"Number of learners not found: {num_not_matched}")

