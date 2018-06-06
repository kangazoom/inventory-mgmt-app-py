# michelle cronin
import csv
import os

#TODO welcome the user by name??
def menu(username, products_count):
    # this is a multi-line string, also using preceding `f` for string interpolation
    menu = f"""
    -----------------------------------
    INVENTORY MANAGEMENT APPLICATION
    -----------------------------------
    Welcome, {username}!
    There are {products_count} products in the database.\n
        operation | description
        --------- | ------------------
        'List'    | Display a list of product identifiers and names.
        'Show'    | Show information about a product.
        'Create'  | Add a new product.
        'Update'  | Edit an existing product.
        'Destroy' | Delete an existing product.
        'Reset'   | Reset CSV file.
    Please select an operation: """ # end of multi- line string. also using string interpolation

    return menu

def read_products_from_file(filename="products.csv"):
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
    print(f"READING PRODUCTS FROM FILE: '{filepath}'")
    products = []

    with open(filepath, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            products.append(dict(row))
    # returns a list of dictionary items
    return products


def write_products_to_file(filename="products.csv", products=[]):
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
    print(f"OVERWRITING CONTENTS OF FILE: '{filepath}' \n ... WITH {len(products)} PRODUCTS")
    #TODO: open the file and write a list of dictionaries. each dict should represent a product.
    with open(filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["id", "name", "aisle", "department", "price"])
        writer.writeheader()
# p --> dictionary
        for p in products:
            writer.writerow(p)

def reset_products_file(products, from_filename="products_default.csv", filename="products.csv"):
    print("RESETTING DEFAULTS")
    products = read_products_from_file(from_filename)
    write_products_to_file(filename, products)
    # for some reason, products variable is not reassigned in this reset function outside of the function
    # so it's rewritten a second time at the bottom of the run function; but without the products_default.csv items
    # ultimately, i elected to exit the program... there's got to be a better way!
    # return products
    exit()



# available CRUD actions
def list(products):
    print("Current Inventory:")
    return [print(f'#{p["id"]}: {p["name"]}') for p in products]

def show(products):
    #TODO: create validation here
    id_input = input("Please enter the product's identifier: ")
    #list of product identifiers
    pid_list = [int(p["id"]) for p in products]

    # it has got to be a number and also exit in the product identifier list to match
    if id_input.isnumeric() == True and int(id_input) in pid_list:
        matching = [p for p in products if int(p["id"])==int(id_input)]
        print(matching[0])
    else:
        print(f"Please enter a valid product identifier number. There are {len(products)} items for you to choose from.")

def create(products):
    create_name = input("Please insert the new product's name: ")
    create_aisle = input("Please input the new product's aisle: ")
    create_department = input("Please input the new product's department: ")
    # TODO: add validation here:
    create_price = input("Please input the new product's price: ")

    if create_price.isnumeric() == True or create_price.replace('.','').isnumeric()==True:
        create_price = format(float(create_price), '.2f')
        # find maximum id
        # TODO - make IDs int earlier?
        all_ids = [int(p["id"]) for p in products]
        max_id = max(all_ids)
        # create new id for new item
        create_id = max_id + 1

        create_new_dict = {
        "id": create_id,
        "name": create_name,
        "aisle": create_aisle,
        "department": create_department,
        "price": create_price
        }
        print(f"You have just created the following item: {create_new_dict}")

        # add new dictionary item to products list
        products.append(create_new_dict)
        return products
    else:
        print("Please input a price formatted as a number with two decimal places. Creation abandoned.")



def update(products):
    id_input = input("Please enter the product's identifier: ")
    pid_list = [int(p["id"]) for p in products]

        # it has got to be a number and also exit in the product identifier list to match
    if id_input.isnumeric() == True and int(id_input) in pid_list:
        matching_product = [p for p in products if int(p["id"])==int(id_input)][0]
        print(f"You are updating: {matching_product}")

        update_name = input("Please insert the updated product's name: ")
        update_aisle = input("Please input the updated product's aisle: ")
        update_department = input("Please input the updated product's department: ")
        update_price = input("Please input the updated product's price: ")


        if update_price.isnumeric() == True or update_price.replace('.','').isnumeric()==True:
            update_price = format(float(update_price), '.2f')

            matching_product["name"] = update_name
            matching_product["aisle"] = update_aisle
            matching_product["department"] = update_department
            matching_product["price"] = update_price

            print(f"Your updated product: {matching_product}")

            # replace old item with new item
            [matching_product for p in products if int(p["id"])==int(id_input)][0]

            return products

        else:
            print("Please input a price formatted as a number with two decimal places. Update abandoned")
    else:
        print(f"Please enter a valid product identifier number. There are {len(products)} items for you to choose from.")


# TODO: give option for no update?

def destroy(products):
    id_input = input("Please enter the product's identifier: ")
    pid_list = [int(p["id"]) for p in products]

        # it has got to be a number and also exit in the product identifier list to match
    if id_input.isnumeric() == True and int(id_input) in pid_list:
        matching_product = [p for p in products if int(p["id"])==int(id_input)][0]
        # delete item with index that matches the product user wants to delete
        del products[products.index(matching_product)]
        print(f"You've just deleted: {matching_product}")

        return products

    else:
        print(f"Please enter a valid product identifier number. There are {len(products)} items for you to choose from.")

def run():
    # read files
    products = read_products_from_file()
    number_of_products = len(products)

    #capture username
    username = input("What is your username? ").title()

    # print menu
    print(menu(username=username, products_count=number_of_products))
    user_selection = input().upper()
    print(f"You chose {user_selection}. \n")

    # TODO: add a while loop to keep prompting user until done??
    # all possible operations
    if user_selection == "LIST":
        list(products=products)
    elif user_selection == "SHOW":
        show(products=products)
    elif user_selection == "CREATE":
        create(products=products)
    elif user_selection == "UPDATE":
        update(products=products)
    elif user_selection == "DESTROY":
        destroy(products=products)
    elif user_selection == "RESET":
        reset_products_file(products=products)
    else:
        print("Your selection is not valid. Please choose from among the following: 'List', 'Show', 'Create', 'Update', or 'Destroy'.")

    # Finally, save products to file so they persist after script is done...
    write_products_to_file(products=products)

# only prompt the user for input if this script is run from the command-line [??]
if __name__ == "__main__":
    run()
