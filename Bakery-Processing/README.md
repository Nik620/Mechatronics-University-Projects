==============================================================================
			BAKERY INVENTORY MANAGEMENT (VERSION 1.0.0)
==============================================================================

The following documentation is to be used to support the operation of: 
MyBakery.exe and MyBakery.py

The software MyBakery.exe is used to manage your bakery sales and operational
needs: from purchasing, documenting sliced breads, baking order, based on 
time, and tracking customer orders.

Running the software itself will run through a demonstration case to manage
several operations.

==============================================================================

Version: 	1.0.0 released 2024-11-01
Release Notes:	Initial Release

Created by Nik Paulic. 

==============================================================================

CONTENTS
========

1. Requirements

2. Installation

3. Getting Started

4. How to Use

4.1 Inventory Management

4.2 Bread Operations

5. Acknowledgements

==============================================================================

1. Requirements
===============

This software was designed to be run with Windows 7, 8, 10, and 11 as an
x-64 operating system. 

The software uses the requirements of:
Python version 3.10 or later (required libraries: queue and collections)


2. Installation
===============

Unzip the folder to ensure all of the files are available. 


3. Getting Started
==================

Relocate the file to desired directory. To run the application, double-click
to launch.

Optionally, the executable may be run from the command line (navigate first to
the correct directory) and run: MyBakery.exe

No additional requirements are needed to execute, no parameters required to be 
passed.


4. How to use
===============

4.1 Sales Management
========================

With this software, you can manage sales easily with individual items or as a
collective of several orders.


Purchasing multiple items:

Using Inventory.Shopping(item_1, item_2...) (a <list>), the software can run 
through all customer purchases to tabulate a total, receipt, and more. If
desired to confirm if an item is there, it may be searched for by the index
it was placed. 

This function can ensure that multiple items are handled and tabulated in the
total cost. Refer to the demo's Scenario 1 for more details.


Preparation of Group orders:

For those difficult times with multiple orders coming in at the same time, you
can rest assured that by using Inventory.customer_handling() (running a 
<linked-list>) that we can easily navigate through all of the orders to 
prepare. Refer to the demo's Scenario 4.


4.2 Bread Operations
====================

Several operations are supported by this bakery software including: baking, 
slicing bread, and easily accessing ingredients.

Baking:
When using your oven, ensure that the breads of the same baking temperature
are being baked at the same time. To ensure that they are in for the 
appropriate amount of time, you can use Breads.bake_bread(bread_1, bread_2...)
(using a <stack>) to ensure the last one in takes the shortest amount of time
to be retrieved first.

Slicing Bread:
For slicing the bread, we understand that the bread cutting machine will take
in the first one and process it first, which is why we have available the
function Breads.breas_slicer(bread_1, bread_2...) (using a <queue>).

Creating a Cookbook:
Finally, when your baker requires a list of the ingredients to bake the bread,
we have created the function Breads.cook_book(bread_1, bread_2...) (using a
<dictionary>) to ensure that they don't have to waste time with breads that
aren't on their work scope. 


5. Acknowledgements
===================

Thank you to ChatGTP for the support in the areas of development of this
software, as well as the communities who've supported in creating a substitute
to Linked Lists in the Python Language.


==============================================================================
End