from models import (Base, session, Product, engine)
import csv
import datetime


def clean_price(price_str):
    split_price = price_str.split('$')
    try:
        new_price = float(split_price[1])
    except ValueError:
        input('''\nThe amount you entered is not correct, please try again
                 \r Example: $10.99
                 \r Press ENTER to continue''')
    else:
        return int(new_price*100)


def clean_date(date_str):
    split_date = date_str.split('/')
    try:
        month = int(split_date[0])
        day = int(split_date[1])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except ValueError:
        input('''
                \n******* DATE ERROR *******
                \rThe data format should include a valid Day, Month and Year 
                \rExample: 10/07/1982
                \rPress enter to try again
                \r**************************
            ''')
    else:
        return return_date


def clean_id(id_str, options):
    try:
        product_id = int(id_str)
    except ValueError:
        input('''
                    \n******* ID ERROR *******
                    \rThe ID should be a number
                    \rPress enter to try again
                    \r*************************
                ''')
    else:
        if product_id in options:
            return product_id
        else:
            input(f'''
                \n******* ID ERROR *******
                \rOptions: {options}
                \rPress enter to try again
                \r*************************
            ''')
            return


def add_csv_data():
    with open('inventory.csv') as csv_file:
        data = csv.reader(csv_file)
        headers = next(data)
        for row in data:
            product_in_db = session.query(Product).filter(Product.product_name == row[0]).one_or_none()
            if product_in_db is None:
                product_name = row[0]
                product_quantity = row[2]
                product_price = clean_price(row[1])
                date_updated = clean_date(row[3])
                new_product = Product(product_name=product_name,
                                      product_quantity=product_quantity,
                                      product_price=product_price,
                                      date_updated=date_updated)
                session.add(new_product)
        session.commit()


def menu():
    while True:
        print('''
            \nPRODUCTS DATABASE
            \rv: View all products
            \ra: Add a new product
            \rb: Back up database
            \rq: Exit
        ''')
        choice = input('What would you like to do? ')
        if choice.lower() in ['v', 'a', 'b', 'q']:
            return choice.lower()
        else:
            input('''\rPlease choice one the options above
                     \reither v, a, b, or q.
                     \rPress enter to try again  ''')


def app():
    running = True
    while running:
        choice = menu()
        if choice == 'v':
            id_options = []
            for item in session.query(Product):
                id_options.append(item.id)
            id_error = True
            while id_error:
                id_choice = input(f'''
                                \nId Options: {id_options}
                                \rProduct Id: ''')
                id_choice = clean_id(id_choice, id_options)
                if type(id_choice) == int:
                    id_error = False
            item = session.query(Product).filter(Product.id == id_choice).first()
            print(f'Name: {item.product_name}, Quantity: {item.product_quantity}, Price: ${item.product_price/100}')
            input('Press ENTER to continue...')
        elif choice == 'a':
            product_name = input('What is the name of the product?  ')
            product_quantity = input('How many do we have? ')

            price_error = True
            while price_error:
                price = input('''\nHow much is the product? 
                                 \r*price must be in the correct format
                                 \rexample: $10.99    ''')
                price = clean_price(price)
                if type(price) == int:
                    price_error = False

            date = datetime.date.today()
            new_product = Product(product_name=product_name, product_quantity=product_quantity, product_price=price, date_updated=date)

            session.add(new_product)
            session.commit()
            input('''\n***New Product added***
                     \r Press ENTER to continue''')

        elif choice == 'b':
            with open('new_inventory.csv', 'a') as csv_file:
                header = ['name', 'quantity', 'price', 'date updated']
                writer = csv.writer(csv_file)
                writer.writerow(header)
                products = session.query(Product)
                for product in products:
                    data = [product.product_name, product.product_quantity, product.product_price, product.date_updated]
                    writer.writerow(data)
                input('''\n*** New backup CSV file created ***
                         \rPress ENTER to continue ''')
        else:
            print('Goodbye and thanks for using this tool')
            exit()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv_data()
    app()
