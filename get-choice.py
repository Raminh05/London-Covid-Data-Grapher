from london import run_program_london
from ontario import run_program_ontario

def get_choice():    
    u_choice = input("What do you want to do?\n (a) Just update and write data to the csv\n (b) Update data AND graph London cases\n (c) Update data AND graph Ontario cases\n")

    if u_choice == 'b':
        run_program_london()

    elif u_choice == 'c':
        run_program_ontario()
        
    else:
        print("Invalid choice!")
        get_choice() # Added so that if the user chooses an invalid option, (s)he will get sent back to the questions again to retry.

get_choice()






   

