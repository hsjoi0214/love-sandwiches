import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS=Credentials.from_service_account_file('creds.json')
SCOPED_CREDS=CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT=gspread.authorize(SCOPED_CREDS)
SHEET=GSPREAD_CLIENT.open('love_sandwiches')

#It just takes input from user and convert it into list, nothing more
def get_sales_data():
    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal,which must be a string of 6 numbers separated by commas.
    The loop will repeatedly request data,until it is valid
    """
    while True:
        print("Please enter sales data from the last market")
        print("Data should be six numbers,separated by commas.")
        print("Example:10,20,30,40,50,60\n")
    
        data_str=input("Enter your data here:")
    
        sales_data=data_str.split(",")    #takes the string came from input and converts it into list item but still string, so we convert it to int later
        validate_data(sales_data)
        
        if validate_data(sales_data):
            print("Data is valid!")
            break
        
    return sales_data
    
#here we are converting the argument into integer and check for length validity  
def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises value error if strings cannot be converted into int,
    0r if there arent exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values)!=6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    return True
        
# just append the data we got from user in get_data funtion        
def update_sales_worksheet(data):
    """
    Update sales worksheet,add new row with the list data provided.
    """    
    print("Updating sales worksheet...\n")
    sales_worksheet=SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("sales worksheet updated successfully.\n")
    
def update_surplus_worksheet(data):
    """
    Update surplus worksheet,add new row with the list data provided.
    """    
    print("Updating surplus worksheet...\n")
    surplus_worksheet=SHEET.worksheet("surplus")
    surplus_worksheet.append_row(data)
    print("surplus worksheet updated successfully.\n")
    
# here we are getting the last row of the data in the stock sheet in google docs   
def calculate_surplus_data(sales_row): 
    """
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is defines as the sales figure strubtracted from the stock:
    -postibe indicates waste
    -negative indicates extra made when stock was sold out.
    """
    print("calculating surplus data...\n")
    stock=SHEET.worksheet("stock").get_all_values()
    stock_row=stock[-1]
    print(f"stock row: {stock_row}")
    print(f"sales row: {sales_row}")
    
    surplus_data=[]
    for stock,sales in zip(stock,sales):
        surplus=int(stock)-sales
        surplus_data.append(surplus)
    return surplus_data
    
   

#here we are converting the list data from get_sales_data to integer and passing that result in update_sales_worksheet
def main():
    """
    Run all program functions
    """
    data=get_sales_data()
    sales_data=[int(num) for num in data] 
    update_sales_worksheet(sales_data)
    new_surplus_data=calculate_surplus_data(sales_data)
    update_surplus_worksheet(new_surplus_data)

print("Welcome to love sandwiches data automation")
main() 
    







