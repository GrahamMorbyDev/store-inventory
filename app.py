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
        month = int(split_date[1])
        day = int(split_date[0])
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


def add_csv_data():
    with open('inventory.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            product_in_db = session.query(Product).filter(Product.product_name == row[0]).one_or_none()
            if product_in_db is None:
                print(row[1])
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
            for item in session.query(Product):
                print(f'Name: {item.product_name}, Quantity: {item.product_quantity}, Price: {item.product_price}')
            input('Press ENTER to continue...')
        elif choice == 'a':
            pass
        elif choice == 'b':
            pass
        else:
            print('Goodbye and thanks for using this tool')
            exit()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv_data()
    app()
