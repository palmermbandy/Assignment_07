#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2020-Jan-01, Created File
# PBandy, 2020-Aug-19, Added append_row_to_table function
# PBandy, 2020-Aug-19, Added delete_row_from_table function
# PBandy, 2020-Aug-19, Added processing code to write_file function
# PBandy, 2020-Aug-19, Added initiate_cd_inventory function
# PBandy, 2020-Aug-19, Added ask_user_for_input function
# PBandy, 2020-Aug-19, Added generate_new_id function
# PBandy, 2020-Aug-19, Updated ask_user_for_input function to accept one argument
# PBandy, 2020-Aug-19, Updated delete_row_from_table function
# PBandy, 2020-Aug-26, Updated write_file function
# PBandy, 2020-Aug-26, Updated read_file function
# PBandy, 2020-Aug-26, Updated ask_user_for_input function
# PBandy, 2020-Aug-26, Updated append_row_to_table function
# PBandy, 2020-Aug-26, Added request_id_to_delete function
#------------------------------------------#

import pickle
import sys
from os import path

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of dicts to hold data
dictRow = {}  # dict of data row
strFileName = 'CDInventory.dat'  # binary data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:

    @staticmethod
    def append_row_to_table(strID, strTitle, strArtist, lstTbl):
        """Function to append a dictionary to a list

        Args:
            - generated_id (string): The ID of the CD
            - strTitle (string): The Title of the CD
            - strArtist (string): The Artist of the CD
            - lstTble (list): A list of dicts that represents a collection of rows of CD data
        
        Returns:
            - None.
        """
        dictRow = {'id' : strID, 'title' : strTitle, 'artist' : strArtist}
        lstTbl.append(dictRow)

    @staticmethod
    def delete_row_from_table(lstTbl, id_to_delete):
        """Function to delete a row by ID from the in-memory table

        Args: 
            - lstTbl (list): A list of dicts that represents a collection of rows of CD data
            - id_to_delete (string): The numerical ID that represents the row of CD data to delete
        
        Returns: 
            - None.
        """
        
        # There shouldn't be any duplicate entries in the file unless it has been
        # modified outside of this program, which I am not trying to handle at this stage
        # of the program, so this delete function will not delete duplicates reliably.
        for count, row in enumerate(lstTbl):
            if str(row['id']) == str(id_to_delete):
                del lstTbl[count]
                print('Deleted ID #{}'.format(id_to_delete))
                break

    @staticmethod
    def generate_new_id(lstTbl):
        """Function to automatically generate a new ID for CD entries.
        Prevents duplicate IDs to enable simpler processing when deleting entries.
        This only prevents duplicates and therefore assumes there are no existing duplicates.

        Args:
            - lstTbl (list): A list of dicts that represents a collection of rows of CD data

        Returns: 
            - generated_id (string): A newly generated, unique ID
        """
        current_ids = []
        # Check if there's anything in lstTble
        if lstTbl:
            # If there are values in lstTbl, iterate through them
            for row in lstTbl:
                # We're only interested in the ID of each row here. Let's store it in a variable.
                row_id = int(row['id'])
                # Now append each ID into a list of 'current_ids'
                current_ids.append(row_id)
            # Once we have the list of current_ids, let's grab the max ID
            max_id = max(current_ids)
            # ...and add 1 to the max_id to get our next ID.
            generated_id = max_id + 1
        # If lstTbl was empty, we can just start with '1' as the ID.
        else: 
            generated_id = 1
        return generated_id


class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def initiate_cd_inventory():
        """ Function to create the CDInventory.dat file if it doesn't exist.

        Args: 
            - None

        Returns: 
            - None
        """
        if not path.exists(strFileName):
            objFile = open(strFileName, 'wb')
            objFile.close()

    @staticmethod
    def read_file_into_memory(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            - file_name (string): name of file used to read the data from
            - table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            - None.
        """
        table.clear()  # this clears existing data and allows to load data from file
        try:
            # Approach for loading pickled data adapted from 
            # https://stackoverflow.com/questions/20716812/saving-and-loading-multiple-objects-in-pickle-file
            with open(strFileName, 'rb') as objFile:
                while True:
                    try:
                        unpickledLine = pickle.load(objFile)
                        data = unpickledLine.strip().split(',')
                        dictRow = {'id': data[0], 'title': data[1], 'artist': data[2]}
                        table.append(dictRow)
                    except EOFError:
                        break
        except FileNotFoundError as e:
            print(f'No file named {strFileName} was found.\n', e)
        return table

    @staticmethod
    def write_file(file_name, table):
        """Function to write data from a list of dictionaries to a file

        Reads in data from 2D table (list of dicts) identified by 'table' argument.

        Args:
            - file_name (string): name of file to which to write the data
            - table (list of dicts): 2D data structure (list of dicts) that holds the data during runtime
        
        Returns:
            - None.
        """
        try:
            with open(file_name, 'wb') as objFile:
                for row in table:
                    strId = str(row['id'])
                    strTitle = str(row['title'])
                    strArtist = str(row['artist'])
                    strRow = '{},{},{}\n'.format(strId, strTitle, strArtist)
                    pickle.dump(strRow, objFile)
        except PermissionError as e:
            print('Insufficient permissions to write to file:\n', e)
        except IOError as e:
            print('Error writing to file:\n', e)


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            - None.

        Returns:
            - None.
        """
        print('Menu\n\n[l] Load Inventory from File\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] Delete CD from Inventory\n[s] Save Inventory to File\n[x] Exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            - None.

        Returns:
            - choice (string): a lower case string of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            - table (list of dicts): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            - None.

        """
        print()
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by: {})'.format(*row.values()))
        print('======================================')
        print()

    @staticmethod
    def ask_user_for_input():
        """Function to ask user for inputs, validate them, and return them.

        Args: 
            - None

        Returns: 
            - strTitle (string): The Title of the CD
            - strArtist (string): The Artist of the CD
        """
        invalidCharacters = ['"',',']
        try:
            strTitle = input('What is the CD\'s title? ').strip()
            for i in strTitle:
                if i in invalidCharacters:
                    raise ValueError
            strArtist = input('What is the Artist\'s name? ').strip()
            for i in strArtist:
                if i in invalidCharacters:
                    raise ValueError
            return strTitle, strArtist
        except KeyboardInterrupt as e:
            print('Program Manually Exited', e)
        except ValueError as e:
            print('The following characters are not allowed: {}{}'.format(invalidCharacters[0], invalidCharacters[1]))
            sys.exit()

    @staticmethod
    def request_id_to_delete():
        """Function to ask user which CD ID to delete. It also validates
        whether the ID is valid for deletion by confirming that it is an integer.

        Args:
            - None

        Returns:
            - id_to_delete (string): The ID of the CD to delete.
        """
        try:
            # Nested conversion to int validates the input is an integer.
            id_to_delete = int(input('Which ID would you like to delete? ').strip())
            # But I prefer that this be a string, so convert it back
            id_to_delete = str(id_to_delete)
            return id_to_delete
        # If input is not an integer, catch and handle the ValueError
        except ValueError as e:
            print('Uh-oh! Please enter an integer for the ID.')
            input('Press [ENTER] to return to menu:')

# 1. When program starts, read in the currently saved Inventory
FileProcessor.initiate_cd_inventory()
FileProcessor.read_file_into_memory(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection

    # 3.1 Process exit first
    if strChoice == 'x':
        break
    # 3.2 Process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('Type \'yes\' to continue and reload from file. Otherwise, reload will be canceled: ')
        if strYesNo.lower().strip() == 'yes':
            print('Reloading...')
            lstTbl = FileProcessor.read_file_into_memory(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('Canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # Start loop back at top.
    # 3.3 Process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new CD Title and Artist
        
        # Using this ensures that executing this block will always add a unique ID,
        # so we don't need to ask the user for one
        generated_id = DataProcessor.generate_new_id(lstTbl)
        
        strTitle, strArtist = IO.ask_user_for_input()
        
        # 3.3.2 Add item to the table
        DataProcessor.append_row_to_table(generated_id, strTitle, strArtist, lstTbl)
        print()
        IO.show_inventory(lstTbl)
        print()
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        strIdDel = IO.request_id_to_delete()
        # 3.5.2 search thru table and delete CD
        DataProcessor.delete_row_from_table(lstTbl, strIdDel)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')
