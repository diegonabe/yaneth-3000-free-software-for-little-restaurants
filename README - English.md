
YANETH 3000 - Small Restaurant Order Management System.

This is an order management system designed for restaurants, aimed to be as simple as possible to implement in the restaurant's internal control. It allows customers to place orders from different tables and enables waiters to efficiently manage these orders.

Key Features

Graphical User Interface (GUI): The system features an easy-to-use graphical user interface, developed using the Python Tkinter library.

Table Management: Customers can select a specific table and place orders from that table.

Adding and Deleting Orders: Waiters can add new orders to selected tables and delete existing orders if necessary.

Data Persistence: Orders are stored in an SQLite database to ensure data persistence even after system restarts.

System Components

The system consists of several main components:

Main Window: This is the main window of the application that displays all available tables for customers.

Table-specific Order Window: Clicking on a specific table opens a new window that displays current orders placed at that table and allows waiters to add or delete orders.

SQLite Database: An SQLite database is used to store information about orders, including ordered dishes, prices, and the associated table.

System Requirements

Python 3.x installed on the system.
Tkinter library for GUI.
SQLite database.
Installation and Execution Instructions

Clone or download this repository to your local machine.
Make sure you have Python 3.x installed.
Install the Tkinter library if it's not already installed:
Copy code
pip install tk
Run the main file main.py to start the application.
An executable will be added in future versions.
Contributions

Contributions are welcome. If you have suggestions for improvements, bug fixes, or new features, feel free to submit a pull request or open an issue on this repository. Your help is greatly appreciated.

Author

This project was developed by Diego Napán. Email me: diegonabe@hotmail.com