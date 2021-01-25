import requests
import bs4
from tkinter import ttk, BOTTOM
from PIL import ImageTk, Image
import webbrowser
try:
    import tkinter
except ImportError:
    import Tkinter as tkinter


"""A program that scrapes the website of Squid Industries to get the latest info on
product prices, names and other information. Utilises the BeautifulSoup library and tkinter
to achieve this.

Author: Aidan Hawkins"""

# Get the URL for Squid Industries's trainer website and turn it into a soup
trainer_data = requests.get("https://www.squidindustries.co/collections/frontpage")
trainer_soup = bs4.BeautifulSoup(trainer_data.text, "html.parser")

# Get the URL for Squid Industries's accessories website and turn it into a soup
accessories_data = requests.get("https://www.squidindustries.co/collections/miscellaneous")
accessories_soup = bs4.BeautifulSoup(accessories_data.text, "html.parser")

# Setup empty lists for information
trainer_names = []
trainer_prices = []
accessories_names = []
accessories_prices = []

trainer_availability_list = []
accessory_availability_list = []

for trainer_availability in trainer_soup.select(".grid-view-item__meta"):
    trainer_availability = str(trainer_availability.text)
    trainer_availability_list.append(trainer_availability)

for accessory_availability in accessories_soup.select(".grid-view-item__meta"):
    accessory_availability = str(accessory_availability.text)
    accessory_availability_list.append(accessory_availability)

# Get the names of the trainers
for name in trainer_soup.findAll('div', attrs={'class': 'h4 grid-view-item__title'}):
    trainer_names.append(name.text)

# Get the prices of the trainers
prices = trainer_soup.select(".product-price__price")
for val in prices:
    trainer_prices.append(val.text)

# Get the names of the accessories
for access_name in accessories_soup.findAll('div', attrs={'class': 'h4 grid-view-item__title'}):
    accessories_names.append(access_name.text)

# Get the prices of the accessories
access_prices = accessories_soup.select(".product-price__price")
for access_price in access_prices:
    accessories_prices.append(access_price.text)


# Set up a dictionary in order to be able to obtain prices from a choice
trainer_dict = {}
accessories_dict = {}
trainer_availability_dict = {}
accessories_availability_dict = {}

for i in range(len(trainer_names)):
    trainer_dict[trainer_names[i]] = trainer_prices[i]

for i in range(len(accessories_names)):
    accessories_dict[accessories_names[i]] = accessories_prices[i]

for i in range(len(trainer_names)):
    if "Sold out" in trainer_availability_list[i]:
        trainer_availability_dict[trainer_names[i]] = "Sold Out"
    else:
        trainer_availability_dict[trainer_names[i]] = "Available"

for i in range(len(accessories_names)):
    if "Sold out" in accessory_availability_list[i]:
        accessories_availability_dict[accessories_names[i]] = "Sold Out"
    else:
        accessories_availability_dict[accessories_names[i]] = "Available"


# Set up tab variable
tab = 0


def open_socials(social):
    """Open the corresponding social media website in correspondence to the
    user's selected button. String references determine this."""

    if social == "facebook":
        webbrowser.open("https://www.facebook.com/squidindustriesco/")
    if social == "instagram":
        webbrowser.open("https://www.instagram.com/squidindustriesco/")
    if social == "twitter":
        webbrowser.open("https://twitter.com/squidindustries")
    if social == "youtube":
        webbrowser.open("https://www.youtube.com/c/squidindustriesco")


def change_tabs():
    """Change the tabs depending on what the current tab variable is"""
    global tab

    if tab == 0:
        change_tab_button.config(text="Trainers")
        tab = 1

        trainer_name_combobox.set("Squid Industries Wrist Lanyard")
        trainer_name_combobox.config(value=accessories_names)

    elif tab == 1:
        change_tab_button.config(text="Accessories")
        trainer_name_combobox.set("Triton")
        tab = 0

        trainer_name_combobox.config(value=trainer_names)


def handle_choice():
    """Take the user's trainer choice, and display the correct info.
    This includes the price, availability and image."""

    # Store the image as a global variable, otherwise it will not display
    global trainer_image
    global accessory_image
    global tab

    # Get the user's choice and display the price
    choice = trainer_name_combobox.get()
    if tab == 0:
        price_label.config(text="Price: " + trainer_dict[choice])
        availability_label.config(text="Availability: " + trainer_availability_dict[choice])

        # Rename the squiddy knives to their appropriate names if they have "restock" in the name somewhere
        # Without this, the squiddy would have an incorrect image path name

        if "Squiddy-B" in trainer_name_combobox.get() and "Re-stocks" in trainer_name_combobox.get():
            image_choice = "Squiddy-B.jpg"

        elif "Squiddy-C" in trainer_name_combobox.get() and "Re-stocks" in trainer_name_combobox.get():
            image_choice = "Squiddy-C.jpg"

        elif "Squiddy-G" in trainer_name_combobox.get() and "Re-stocks" in trainer_name_combobox.get():
            image_choice = "Squiddy-G (Discontinued).jpg"

        elif "Squiddy-B" not in trainer_name_combobox.get() and "Squiddy-C" not in trainer_name_combobox.get() and "Squiddy-G" not in trainer_name_combobox.get() and "Squiddy" in trainer_name_combobox.get():
            image_choice = "Squiddy.jpg"
        else:
            image_choice = trainer_name_combobox.get() + ".jpg"

        trainer_image = ImageTk.PhotoImage(Image.open(image_choice))
        image_label.config(image=trainer_image)

    elif tab == 1:
        price_label.config(text="Price: " + accessories_dict[choice])
        availability_label.config(text="Availability: " + accessories_availability_dict[choice])

        image_choice = trainer_name_combobox.get() + ".jpg"
        accessory_image = ImageTk.PhotoImage(Image.open(image_choice))
        image_label.config(image=accessory_image)


# Setup root tkinter window + frames
root = tkinter.Tk()
root.title("Squid Industries Tracker")
root.geometry("500x530")
root.resizable(0, 0)
root.iconbitmap("butterfly knife.ico")
root.config(bg="grey")

title_frame = tkinter.Frame(root)
title_frame.pack(padx=5, pady=5)

everything_frame = tkinter.Frame(root)
everything_frame.pack(padx=5, pady=5)

choice_frame = tkinter.Frame(root)
choice_frame.pack(padx=5, pady=5)

image_frame = tkinter.Frame(root, bg="grey")
image_frame.pack(padx=5)

button_frame = tkinter.Frame(root, bg="grey")
button_frame.pack(padx=5, pady=5)

credit_frame = tkinter.Frame(root)
credit_frame.pack(side=BOTTOM, pady=5, padx=5)

socials_frame = tkinter.Frame(root)
socials_frame.pack(side=BOTTOM, pady=5, padx=5)


# Create all of the widgets utilized
title = tkinter.Label(title_frame, text="Squid Industries Tracker", font=("SimSun", 25), width=30)
title.pack()

confirm_button = tkinter.Button(button_frame, text="Get Info", font=("SimSun", 15), width=13, command=handle_choice)
confirm_button.grid(row=0, column=0, padx=5, pady=5)

change_tab_button = tkinter.Button(button_frame, text="Accessories", font=("SimSun", 15), width=13, command=change_tabs)
change_tab_button.grid(row=0, column=1, padx=5, pady=5)

quit_button = tkinter.Button(button_frame, text="Quit", font=("SimSun", 15), command=root.destroy, width=13)
quit_button.grid(row=0, column=2, padx=5, pady=5)

trainer_name_combobox = tkinter.ttk.Combobox(choice_frame, value=trainer_names, state="readonly", justify="center", font=("SimSun", 15), width=45)
trainer_name_combobox.grid(row=0, column=0)

image_label = tkinter.Label(image_frame, image=ImageTk.PhotoImage(Image.open("placeholder.jpg")))
image_label.grid(row=0, column=0, padx=5, pady=5)

price_label = tkinter.Label(everything_frame, text="Price: ", font=("SimSun", 25), width=30)
price_label.pack(padx=5, pady=5)

availability_label = tkinter.Label(everything_frame, text="Availability: ", font=("SimSun", 25), width=30)
availability_label.pack(padx=5, pady=5)

credit_label = tkinter.Label(credit_frame, text="Created by AHawky", font=("SimSun", 10))
credit_label.pack()

# Set up social buttons + images
instagram_image = ImageTk.PhotoImage(Image.open("instagram.png"))
instagram_button = tkinter.Button(socials_frame, image=instagram_image, command=lambda: open_socials("instagram"))
instagram_button.grid(row=0, column=0)

facebook_image = ImageTk.PhotoImage(Image.open("facebook.png"))
facebook_button = tkinter.Button(socials_frame, image=facebook_image, command=lambda: open_socials("facebook"))
facebook_button.grid(row=0, column=1)

twitter_image = ImageTk.PhotoImage(Image.open("twitter.png"))
twitter_button = tkinter.Button(socials_frame, image=twitter_image, command=lambda: open_socials("twitter"))
twitter_button.grid(row=0, column=2)

youtube_image = ImageTk.PhotoImage(Image.open("youtube.png"))
youtube_button = tkinter.Button(socials_frame, image=youtube_image, command=lambda: open_socials("youtube"))
youtube_button.grid(row=0, column=3)

trainer_name_combobox.set("Triton")

root.mainloop()
