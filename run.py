import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT =  gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

# sales = SHEET.worksheet('sales')

# data = sales.get_all_values()

# print(data)

def get_sales_data():
    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers separated
    by commas. The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("Please enter sales data from last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: \n")
        
        sales_data = data_str.split(",")
        
        if validate_data(sales_data):
            print("Data is valid!")
            break
            # breaks while loop if condition is met

    return sales_data

def validate_data(values):
    # print(values)
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again. \n")
        return False

    return True

# def update_sales_worksheet(data):
#     """
#     Update sales worksheet, add new row with the list data provided.
#     """
#     print("Updating sales worksheet...\n")
#     sales_worksheet = SHEET.worksheet("sales")
#     sales_worksheet.append_row(data)
#     print("Sales worksheet updated successfully.\n")

# def update_surplus_worksheet(data):
#     """
#     Update surplus worksheet, add new row with the list data provided.
#     """
#     print("Updating surplus worksheet...\n")
#     surplus_worksheet = SHEET.worksheet("surplus")
#     surplus_worksheet.append_row(data)
#     print("Surplus worksheet updated successfully.\n")

def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully.\n")

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    
    The surplus is defined as the sales figure substracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus inficates extra made when stock was sold out."""
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    # pprint(stock)
    stock_row = stock[-1]
    # print(stock_row)
    # print(F"stock row: {stock_row}") 
    # print(F"sales row: {sales_row}")
    # prints them individually, but we need to read them together. Use of zip instead
    
    surplus_data = []
    
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    # print(surplus_data)
    return surplus_data


def get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet, collecting 
    the last 5 entries for each sandwich and returns the data 
    as a list of lists.
    """
    sales = SHEET.worksheet("sales")
    # column = sales.col_values(3)
    # print(column)
    columns = []
    for ind in range(1, 7):
        # print(ind)
        column = sales.col_values(ind)
        columns.append(column[-5:])
    # pprint(columns)
    return columns

def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print("Calculating stock data...\n")
    new_stock_data = []
    for column in data:
        int_column = [int(num) for num in column]
        average =  sum(int_column)/ len(int_column)
        # average = sum(int_column)/5 - could use this instead as our stock columns will always have 5 items 
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    # print(new_stock_data)
    return new_stock_data

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data =  [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")

    
print("Welcome to Love Sandwiches Data Automation")
stock_data = main() 

def get_stock_values(data):
    """
    Return message to user with suggested stock numbers for next market formatted as a dictionnary
    """
    headings = SHEET.worksheet("stock").get_all_values()[0]
    suggested_stock = SHEET.worksheet("stock").get_all_values()[-1]
    # headings = SHEET.worksheet('stock').row_values(1)
    print(f'Make the following numbers of sandwiches for the next market:\n')
    return {headings[i]: suggested_stock[i] for i in range(len(headings))}
    
stock_values = get_stock_values(stock_data)
print(stock_values)