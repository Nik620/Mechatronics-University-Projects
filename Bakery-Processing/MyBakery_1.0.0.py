"""***************************************************************************
Title:          Bakery Inventory Management
File:           MyBakery.py
Version:        1.0.0
Release Notes:  First Release

Author:         Nik Paulic

Purpose:        Generates a typical bakery inventory, with pricing for a user
                to buy bread, bakers to slice bread, and many other typical
                bakery activities.
Description:    This file implements several data structures in order to
                support typical operations of a bakery in sales and several
                operations.
***************************************************************************"""
"""*********************Libraries******************************************"""
from queue import Queue
from queue import LifoQueue


"""*********************Functions******************************************"""
'========================================='
def demo_bakery():
    """
    Develops a test scenario for the inventory and bread availability of a
    bakery.
    """
    # Breads
    sourdough = Breads("Sourdough", 1.12, 3.12, 40, 450,
                       ["flour", "sourdough starter", "water", "salt"])
    rye = Breads("Rye", .52, 1.80, 50, 350,
                 ["flour", "yeast", "water", "salt", "honey", "sugar"])
    pita = Breads("Pita", .3, 2.80, 10, 450,
                  ["flour", "yeast", "water", "salt", "olive oil"])
    whole_wheat = Breads("Whole Wheat", .11, 1.30, 35, 350)
    baguette = Breads("Baguette", .92, 3.80, 30, 450,
                      ["flour", "yeast", "water", "salt", "olive oil"])
    ciabatta = Breads("Ciabatta", .31, 1.87, 35, 400,
                      ["flour", "yeast", "water", "salt", "olive oil"])
    focaccia = Breads("Focaccia", .32, 2.10, 25, 400,
                      ["flour", "yeast", "water", "salt", "olive oil", 
                       "herbs"])
    cheesey = Breads("Cheese Bread", 1.34, 4.59, 30, 350,
                     ["flour", "yeast", "water", "salt", "cheese"])
    
    # General Inventory
    apple_juice = Inventory("Apple Juice", .80, 1.90)
    milk = Inventory("Milk", 1.22, 3.23)
    peanut_butter = Inventory("Peanut Butter", 2.50, 6.30)
    
    # 1. Lists Example
    print("Scenario 1: Purchasing items at the bakery")
    shopping_bag = Inventory.shopping(sourdough, rye, rye, cheesey, cheesey, 
                                   peanut_butter, milk, apple_juice)
    print("\nTaking an item from the shopping bag: ", shopping_bag[2])
    
    # 2. Queue
    print("\n\nScenario 2: Running bread through a bread slicer")
    slicing_order = Breads.bread_slicer(sourdough, cheesey, baguette)
    print("\nThe first bread out of the slicer is: ", slicing_order.get())
    
    # 3. Stack
    print("\n\nScenario 3: Baking breads at 350F, we will put in order from ",
          "longest time to shortest time to leave the first baking longer")
    baking_350 = Breads.bake_bread(rye, whole_wheat, cheesey)
    print("\nWith the minimum time leaving first, the first bread out is: ",
          baking_350.get())

    # 4. Linked Lists
    print("\n\nScenario 4: Customer order management - items to prepare")
    customer_1 = [baguette, milk]
    customer_2 = [whole_wheat, peanut_butter]
    customer_3 = [focaccia, cheesey, apple_juice]
    customer_4 = [pita, pita, pita]
    orders = Inventory.customer_handling(customer_1, customer_2, 
                                         customer_3, customer_4)
    print("\nOrder of items to prepare for customers: ", orders.nodes_list())
    print("The third item to prepare is: ", orders.search_index(2))
    print("Checking for pita indices: ", orders.search_value(pita))
    print("Checking for ciabatta indices: ", orders.search_value(ciabatta))
    
    # 5. Dictionary
    print("\n\nScenario 5: Creating a cookbook")
    recipe_list = Breads.cook_book(whole_wheat, rye, focaccia, pita, ciabatta)
    print("\nTo bake some rye and whole wheat, the ingredients are:",
          recipe_list[rye], "for Rye and ", recipe_list[whole_wheat], 
          "for whole wheat")
    

"""*********************Classes********************************************"""
'========================================='
class Inventory():
    """
    Develops an inventory for the bakery
    """
    '====================================='
    def __init__(self, item, cost, value):
        """
        Initiates the inventory item, cost, and value
        
        Arguments: the inventory item (str), cost (float), and value (float)
        """
        try:
            if not(isinstance(item, str)):
                print("Error with entry: ", item)
                raise TypeError # Error 2
            elif not(isinstance(cost, (float, int)) or
                     isinstance(value, (float, int))):
                print("Error with entry: ", value, " or ", cost)
                raise ValueError # Error 1
            else:
                self.__item = item
                self.__cost = round(cost, 2)
                self.__value = round(value, 2)
        except ValueError:
            Inventory._error_codes(1) 
        except TypeError:
            Inventory._error_codes(2) 
        except:
            Inventory._error_codes(3) # Error 3, any other error
            
            
    '====================================='
    def __str__(self):
        """
        Returns: the item (string)
        """
        return self.__item
    
    
    '====================================='
    @staticmethod
    def _error_codes(error_code):
        """
        Identifies typical error issues.
        
        Arguments: Any integer from 0 to 9
        """
        errors = {
            0 : ("Error 0: Please enter the items as a list," + 
                 " ex. [entry1, entry2...]"),
            1 : ("Error 1: Please enter the cost and value as a float," + 
                 " ex. Breads('Rye', .52, 1.80,...)"),
            2 : "Error 2: Please enter the value as a string",
            3 : "Error 3: Please enter a string and two floats",
            4 : ("Error 4: Enter bake time in minutes (int) and " +
                    "temperature in fahrenheit (int)"),
            5 : "Error 5: Enter a valid bread (object)",
            6 : "Error 6: Enter a valid inventory item (object)"
            }
        print(errors[error_code])
        
        if error_code == 0: return False
        else: return None
    
    
    '====================================='     
    @property
    def value(self):
        """       
        Returns: the price for the bread (float)
        """
        return self.__value
    
    
    '====================================='
    @property
    def cost(self):
        """       
        Returns: the price for the bread (float)
        """
        return self.__cost
    
        
    '====================================='  
    @staticmethod
    def shopping(*items):
        """
        Creates a shopping list receipt for the user
        
        Arguments: Inputs an undefined list of breads (list)
        Returns: A list of items in the shopping bag (list)
        """
        total = 0
        valid_items = Inventory._check_inventory(items)
        print("------------", "\nBakery Receipt\n")
        
        for item in valid_items:
            print(item, " $", item.value)
            total += item.value
            
        total = round(total,2)
        print("\nTotal payment: $", total, "\n")
        print("------------")
        
        return items
    
    
    '====================================='  
    @staticmethod
    def customer_handling(*orders):
        """
        Creates a linked list of customer orders
        
        Arguments: Inputs an undefined list of breads (list)
        Returns: A list of customer purchases (linked list)
        """
        prepare_order = Inventory.LinkedList()
        
        for order in orders:
            if Inventory._check_list(order) == False: next

            valid_order = Inventory._check_inventory(order)
            
            for item in valid_order: prepare_order.append(item) 
                
        return prepare_order
    

    '=====================================' 
    @staticmethod
    def _check_list(items):
        """
        Returns: True/false if the input is a list (Bool)
        """
        valid_list = []

        try:
            if not(isinstance(items, list)):
                print("Error with entry: ", items)
                raise ValueError # Error 0
            else:
                valid_list.append(items)
        except:
            Inventory._error_codes(0)  
        
        return True
    
    
    '=====================================' 
    @staticmethod
    def _check_inventory(items):
        """
        Returns: A list of valid inventory objects (Inventory)
        """
        valid_items = []
        
        for item in items:
            try:
                if not(isinstance(item, Inventory)):
                    print("Error with entry: ", item)
                    raise ValueError # Error 6
                else:
                    valid_items.append(item)
            except:
                Inventory._error_codes(6)  
        
        return valid_items
    
    
    '====================================='
    class LinkedList:
        """
        Generates an embedded class for linked lists for use within Inventory
        
        Source: Architecture and noted functions/classes supported by ChatGTP
        """         
        '================================='
        class Node:
            """
            Creates each node within the linked list
            """
            '============================='
            def __init__(self, value):
                """
                Initializes the node variable
                
                Arguments: value (any)
                Source: ChatGTP
                """
                self.value = value
                self.next = None
                
                
        '================================='
        def __init__(self):
            """
            Initializes the head of the linked list
            
            Source: ChatGTP
            """
            self.head = None
            
            
        '================================='
        def append(self, value):
            """
            Appends the previous node with the next
            
            Source: ChatGTP
            """
            new_node = self.Node(value)
            
            if not self.head:
                self.head = new_node
                return
            
            current = self.head
            
            while current.next:
                current = current.next
                
            current.next = new_node
            
            
        '================================='
        def search_index(self, index):
            """
            Arguments: The index position (int)
            Returns: The value at the specified index (value)
            """
            node = self.head
            position = 0
            
            while node.value != None:
                if position == index:
                    return node.value
                elif position != index:
                    node = node.next
                    position += 1
                else:
                    print("Index not found")
                    return None
        
        
        '================================='
        def search_value(self, value):
            """
            Arguments: A value to search through the list (any)
            Returns: A list of indices with the specified value (list)
            """
            node = self.head
            position = 0
            positions = []
            
            while node is not None:
                if node.value == value:
                    positions.append(position)
                node = node.next
                position += 1
            if len(positions) == 0: positions.append(None)
            
            return positions
                
        
        '================================='
        def nodes_list(self):
            """
            Prints the linked list values
            
            Returns: A string of all the nodes in the linked list
            """
            node = self.head
            nodes = ''
            
            while node != None:
                nodes += str(node.value)
                if node.next != None: nodes += " -> "
                node = node.next
                
            return nodes


'========================================='
class Breads(Inventory):
    """
    Creates a class for breads
    """    
    '====================================='
    def __init__(self, bread_type, cost, value, bake_time, bake_temp,
                 ingredients = ["flour", "yeast", "water", "salt"]):
        """
        Initiates the bread inventory with ingredients
        
        Arguments: the inventory item (str), cost (float), value (float), and
                    the ingredients of the bread (list)  
        """
        try:
            if Inventory._check_list(ingredients): 
                if isinstance(bake_time, int) and isinstance(bake_temp, int):
                    super().__init__(bread_type, cost, value)
                    self.__time = bake_time
                    self.__temp = bake_temp
                    self.__ingredients = ingredients
                else:
                    print("Error with entry: ", bake_time, " or ", bake_temp)
                    raise ValueError # Error 4
        except ValueError:
            Inventory._error_codes(4) 
            
            
    '====================================='     
    @property
    def ingredients(self):
        """       
        Returns: the ingredients (list)
        """
        return self.__ingredients
    
    
    '====================================='      
    @property
    def bake_time(self):
        """       
        Returns: the bake time (int)
        """
        return self.__time
        
    
    '====================================='      
    @property
    def bake_temp(self):
        """       
        Returns: the bake temperature (int)
        """
        print("The baking temp of ", self.__item, " is ", self.__temp, "F")
        return self.__temp
    
    
    '====================================='     
    def instructions(self):
        """       
        Prints the instructions to bake the bread
        """
        print("The ingredients for ", self.__item, " are:\n")
        for ingredient in self.__ingredients: 
            print(ingredient)
        print("\nBake the bread at ", self.bake_temp, "F for ", 
              self.bake_time, " min")
    
    
    '====================================='  
    @staticmethod
    def bread_slicer(*breads):
        """
        Ordered FIFO of breads going into a bread slicer
        
        Arguments: Inputs an undefined list of breads (list)
        Returns: A queue of breads in order of the slicing (queue)
        """
        slicer = Queue()
        valid_breads = Breads.check_breads(breads)
        
        for bread in valid_breads: slicer.put(bread)
                
        return slicer
    
    
    '=====================================' 
    @staticmethod
    def bake_bread(*breads):
        """
        Ordered LIFO of breads going into a bread slicer based on time
        
        Arguments: Inputs an undefined list of breads (list)
        Returns: A stack of breads in order of the highest bake time (stack)
        Note: sorted_baking_time and LifoQueue process sourced from chatGTP
        """
        valid_breads = Breads.check_breads(breads)
                
        sorted_baking_time = sorted(valid_breads, 
                                    key = lambda bread: bread.bake_time,
                                    reverse = True)
        baking_stack = LifoQueue(maxsize = len(sorted_baking_time))
        
        for bread in sorted_baking_time: baking_stack.put(bread)
        
        return baking_stack
    
    
    '=====================================' 
    @staticmethod
    def cook_book(*breads):
        """
        Creates a dictionary recipe book of all unique input breads
        
        Arguments: Inputs an undefined list of breads (list)
        Returns: A queue of breads in order of the slicing (queue)
        """
        recipes = {}
        valid_breads = Breads.check_breads(breads)
        
        for bread in valid_breads: recipes[bread] = bread.ingredients
                
        return recipes
    
    
    '=====================================' 
    @staticmethod
    def check_breads(breads):
        valid_breads = []
        
        for bread in breads:
            try:
                if not(isinstance(bread, Breads)):
                    print("Error with entry: ", bread)
                    raise ValueError # Error 5
                else:
                    valid_breads.append(bread)
            except:
                Inventory._error_codes(5)  
        
        return valid_breads
        
        
    
"""*********************Main Routine***************************************"""
# Runs the main routine
if __name__ == "__main__":

    demo_bakery()
