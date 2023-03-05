"""
Program to simulate customer behaviour in a supermarket visually.
Uses random images stored in the images/customers folder.

Returns:
    _cv2 image_: _A gif-like visual tracking average customers at
    each location in a store._
"""

import time
import glob
import random
import numpy as np
import pandas as pd
import cv2


CUSTOMER_IMAGE_PATH = 'images/customers/*'
BACKGROUND_IMAGE_PATH = "images/resized_market.png"
SUPERMARKET_LOGO_PATH = "images/unknown.jpeg"
PRESENCE_PROBABILITIES_PATH = "data/average_cust_per_section.csv"
POSITIONS = pd.read_json("data/positions.json")
START_TIME = "08:00:00"


class Character:
    """
    Customers for supermarket simulation.
    """

    def __init__(self, image, x, y):
        if not isinstance(x, int) or not isinstance(y, int):
            raise TypeError("x and y must be set to an integer")
        if (x < 0) or (y < 0):
            raise ValueError("x and y must be positive integers")
        self.image = image
        self.x = int(x)
        self.y = int(y)

    def __repr__(self):
        return f"<Customer at {self.x}/{self.y}>"

    def draw(self, background_image):
        """Used to draw the background and characters

        Args:
            background_image (_jpeg or png_): _An image to use as a background._
        """

        background_image[
            self.y : self.y + self.image.shape[0], self.x : self.x + self.image.shape[1]
        ] = self.image


class Location:
    """
    Location for supermarket simulation.
    """

    def __init__(self, name, customers_present, revenue_per_minute):
        if not isinstance(name, str):
            raise TypeError("name must be set to a string")
        self.name = str(name)
        self.customers_present = customers_present
        self.revenue_per_minute = int(revenue_per_minute)

    def __repr__(self):
        return f"<{self.customers_present} customers present at section {self.name}.>"



def put_customers_and_revenue(image, sections, dataframe, images_path, revenue):
    """Puts customers and info about revenue on background image.

    Args:
        image (_jpeg or png_): _Background image._
        sections (_non-str list_): _List of names for sections. NO QUOTATION MARKS!_
        dataframe (_DataFrame_): _A DataFrame with info about how many customers visit the store._
        revenue (_int_): _An integer that will increase over time._

    Returns:
        _int_: _The total amount of reveune._
    """

    customers_present = dataframe[dataframe["time"] == current_time][
        "new_id"
    ].values

    for i, section in enumerate(sections):
        section.customers_present = update_customers_present(customers_present, i)
        for j in range(int(section.customers_present)):
            random_path = random.choice(images_path)
            img = cv2.imread(random_path)
            new_img, new_x, new_y = update_customer_values(POSITIONS, img, section, j)
            customers.append(Character(new_img, new_x, new_y))
        revenue += int(section.customers_present * section.revenue_per_minute)

    for customer in customers:
        customer.draw(image)

    write_text(image, f"Total Revenue: {revenue}EUR", 10, 130)

    return revenue


def update_customers_present(updated_list, index):
    """Updates customer count for each location

    Args:
        updated_list (_list_): _Generated in the function 'put_customers_and_revenue'_
        index (_int_): _Generated in the function 'put_customers_and_revenue'_

    Returns:
        _int_: _Number of customers present in each location_
    """

    new_presence = np.random.poisson(updated_list[index])
    new_presence = min(new_presence, 8)

    return new_presence


def update_customer_values(pos_dict, image, location, index):
    """Updates positions for customers present at location

    Args:
        pos_dict (_dict_): _JSON dictionary given in the POSITIONS variable_
        image (_jpeg or png_): _Background image_
        location (_non-string_): _Found in the SECTIONS variable_
        index (_int_): _Generated in the function 'put_customers_and_revenue'_

    Returns:
        _Various_: _Updated values. Look into put_customers_and_revenue'_
    """

    x_update = pos_dict[location.name][int(index)]["x"]
    y_update = pos_dict[location.name][int(index)]["y"] + 136

    if index % 2 == 0:
        img_update = image.copy()
    else:
        img_update = image[:, ::-1, :].copy()

    return img_update, x_update, y_update


def write_customers_text(image):
    """
    Writes info on customers present on image
    """

    customers_screen_text = f"""
        Customers:
        Checkout: {checkout.customers_present}
        Dairy: {dairy.customers_present}
        Drinks: {drinks.customers_present}
        Fruit: {fruit.customers_present}
        Spices: {spices.customers_present}
        """

    x_0 = 450
    y_0, d_y = 0, 40

    for i, line in enumerate(customers_screen_text.split("\n")):
        if i >= 5:
            x_0 = 700
            y_0 = 80
            y_updated = y_0 + (i - 5) * d_y
        else:
            y_updated = y_0 + i * d_y

        write_text(image, line, x_0, y_updated)


def write_text(image, text, x_position, y_position):
    """
    Adds text to background image at x_position, y_position
    """

    if not isinstance(text, str):
        raise TypeError("text must be a string")
    cv2.putText(
        image,
        str(text),
        (x_position, y_position),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 0),
        2,
    )


if __name__ == "__main__":

    cus_imgs_path = glob.glob(CUSTOMER_IMAGE_PATH)

    background = cv2.imread(BACKGROUND_IMAGE_PATH)
    doodl = cv2.imread(SUPERMARKET_LOGO_PATH)

    checkout = Location("checkout", 0, 0)
    dairy = Location("dairy", 0, 5)
    drinks = Location("drinks", 0, 6)
    fruit = Location("fruit", 0, 4)
    spices = Location("spices", 0, 3)
    entrance = Location("entrance", 0, 0)

    locations = [checkout, dairy, drinks, fruit, spices]
    customers = []
    total_revenue = 0
    current_time = pd.to_datetime(START_TIME)

    df_presences = pd.read_csv(PRESENCE_PROBABILITIES_PATH)
    df_presences["time"] = pd.to_datetime(df_presences["time"]).copy()

    while True:
        t = current_time.time()
        time.sleep(1)

        frame = background.copy()
        total_revenue = put_customers_and_revenue(
            frame, locations, df_presences, cus_imgs_path, total_revenue
        )

        write_text(frame, t.strftime("%H:%M:%S"), 10, 30)
        write_customers_text(frame)
        frame[180:230, 500:596] = doodl

        cv2.imshow("frame", frame)
        customers.clear()
        current_time += pd.to_timedelta(1, unit="min")

        if cv2.waitKey(1) & 0xFF == ord("d"):
            cv2.destroyAllWindows()
