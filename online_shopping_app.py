
#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#    Student no: N10282653
#    Student name: JACOB MATTHEW KRAUT
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  Submitted files will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Assignment Description-----------------------------------------#
#
#  Online Shopping Application
#
#  In this assignment you will combine your knowledge of HTMl/XML
#  mark-up languages with your skills in Python scripting, pattern
#  matching, and Graphical User Interface design to produce a useful
#  application for simulating an online shopping experience.  See
#  the instruction sheet accompanying this file for full details.
#
#--------------------------------------------------------------------#



#-----Imported Functions---------------------------------------------#
#
# Below are various import statements for helpful functions.  You
# should be able to complete this assignment using these
# functions only.  Note that not all of these functions are
# needed to successfully complete this assignment.
#

# The function for opening a web document given its URL.
# (You WILL need to use this function in your solution,
# either directly or via our "download" function.)
from urllib.request import urlopen

# Import the standard Tkinter functions. (You WILL need to use
# these functions in your solution.)
from tkinter import *

# Functions for finding all occurrences of a pattern
# defined via a regular expression, as well as
# the "multiline" and "dotall" flags.  (You do NOT need to
# use these functions in your solution, because the problem
# can be solved with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.)
from re import findall, finditer, MULTILINE, DOTALL

# Import the standard SQLite functions (just in case they're
# needed).
from sqlite3 import *
import webbrowser
#
#--------------------------------------------------------------------#



#-----Downloader Function--------------------------------------------#
#
# This is our function for downloading a web page's content and both
# saving it on a local file and returning its source code
# as a Unicode string. The function tries to produce
# a meaningful error message if the attempt fails.  WARNING: This
# function will silently overwrite the target file if it
# already exists!  NB: You should change the filename extension to
# "xhtml" when downloading an XML document.  (You do NOT need to use
# this function in your solution if you choose to call "urlopen"
# directly, but it is provided for your convenience.)
#
def download(url,target_filename,filename_extension):

    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    # Open the web document for reading
    try:
        web_page = urlopen(url)
    except ValueError:
        raise Exception("Download error - Cannot find document at URL '" + url + "'")
    except HTTPError:
        raise Exception("Download error - Access denied to document at URL '" + url + "'")
    except:
        raise Exception("Download error - Something went wrong when trying to download " + \
                        "the document at URL '" + url + "'")

    # Read its contents as a Unicode string
    try:
        web_page_contents = web_page.read().decode('UTF-8')
    except UnicodeDecodeError:
        raise Exception("Download error - Unable to decode document at URL '" + \
                        url + "' as Unicode text")

    # Write the contents to a local text file as Unicode
    # characters (overwriting the file if it
    # already exists!)
    try:
        text_file = open(target_filename + '.' + filename_extension,
                         'w', encoding = 'UTF-8')
        text_file.write(web_page_contents)
        text_file.close()
    except:
        raise Exception("Download error - Unable to write to file '" + \
                        target_file + "'")

    # Return the downloaded document to the caller
    return web_page_contents

#
#--------------------------------------------------------------------#



#-----Student's Solution---------------------------------------------#
#
# Put your solution at the end of this file.
#
#############################################
### DOGES PROCURED GOODS SHOPPING PROGRAM ###
#############################################


####################################
### GENERATE INVOICE FUNCTION    ###
### INCLUDES WRITING TO DATABASE ###
####################################


#Function to generate a html document with their purchase items, pictures,
#prices and their total cost
def generate_invoice():

    #Connects to the database and deletes the content
    sales_db = connect('shopping_cart.db')
    sales_view = sales_db.cursor()
    sales_view.execute("DELETE FROM ShoppingCart")
    #Loop over the amount of items in the cart and write to database
    for sale in range(len(cart_titles)):
        sales_view.execute("""INSERT INTO ShoppingCart (Item, Price)
                           VALUES (?,?)""",(cart_titles[sale],cart_prices[sale]))
    #Write changes to database and close the connections
    sales_db.commit()
    sales_view.close()
    sales_db.close()
        
        
                      
        

    invoice = open('invoice.html', 'w', encoding = 'UTF-8')

    #Converts items to a float, adds them together and then rounds the decimal out
    total_cost = round(sum([float(dollars) for dollars in cart_prices]), 2)

    #Declares the document a html file and then writes
    #the first part of the invoice in html
    invoice.write('''
    <!DOCTYPE html>
    <html>
    <head>
    <body>
    <title>Doges Procured Goods!</title>
    <div align="center">
    <h1><i>Doges Procured Goods!</i></h1><br>
    </head>

    <h2>"Doge is impressed with your cart!"</h1>
    <img src="https://i.imgur.com/74tQpTa.gif">
    <h1>Your Purchase Invoice</h1>
                ''')
    #Writes in the total cost of the cart by calling the previous floats
    #and then converting them back to a string to be written
    cart_total = ('<h2>The Total Cost For Your Cart Is: $TOTAL AUD<br><br><br>')
    cart_total = cart_total.replace('TOTAL', str(total_cost))
    invoice.write(cart_total)
    
    #Small if statement to check if the cart is empty,
    #if so it tells the user that the cart is empty
    if cart_titles == []:
        invoice.write('<h2> Your Cart Is Empty!</h2>')

    #Iterate over the number of items in the cart and write
    #and replace a html line to generate the invoice
    for purchases in range(len(cart_titles)):
        titlewrite = ('<h4>TITLE</h4>')
        titlewrite = titlewrite.replace('TITLE', cart_titles[purchases])
        invoice.write(titlewrite)

        imagewrite = ('<img src="IMAGE" height="200" width="200">')
        imagewrite = imagewrite.replace('IMAGE', cart_images[purchases])
        invoice.write(imagewrite)
        
        pricewrite = ('<h4>$PRICE AUD</h4><br><br><br>')
        pricewrite =  pricewrite.replace('PRICE', cart_prices[purchases])
        invoice.write(pricewrite)


   #Finish off writing the html document
    invoice.write('''
    <br><br><br>

    <p>Old Procures were stocked from:<br>

    <a href="https://www.fishingtackleshop.com.au/pages/RSS.html">Tackle Shop RSS Feed</a>
    <a href="https://www.fishingtackleshop.com.au/">Tackle Shop Products</a>
    <a href="https://www.amazon.com.au/new-releases/electronics?tag=assoc-tag">Amazon Electronics</a>

    <p>Fresh Procures were stocked from:<br>

    <a href="https://www.amazon.com.au/new-releases/books?tag=assoc-tag">Amazon Books</a>
    <a href="https://www.amazon.com.au/new-releases/videogames?tag=assoc-tag">Amazon Games</a>

    </div>
    </body>  
    </head>
    </html>
    ''')
    #Close the document to allow the invoice to be opened
    invoice.close()

    #Save the user searching his documents by auto-opening
    webbrowser.open('invoice.html')


##########################
### TACKLE SHOP WINDOW ###
##########################



def tackle_purchase_window():

    #Open file for use
    tackle_shop = open(file = 'tackle_shop.xhtml', encoding = 'UTF-8').read()



    #Scrape the webpage for title names
    tackle_titles = []
    tackle_title_list = findall(r'<title><!\[CDATA\[(.+)]]></title>', tackle_shop)
    tackle_titles.append(tackle_title_list)
    tackle_titles = tackle_titles[0]


    #Scrape the webpage for images
    tackle_images = []
    tackle_image_list = findall(r'<isc:image><!\[CDATA\[(.+)\?c=2]]', tackle_shop)
    tackle_images.append(tackle_image_list)
    tackle_images = tackle_images[0]

    #Scrape the webpage for prices
    tackle_prices = []
    tackle_prices_list = findall(r'<isc:price><!\[CDATA\[\$(.+)]]></isc:price>', tackle_shop)
    tackle_prices.append(tackle_prices_list)
    tackle_prices = tackle_prices[0]
    
    #Setup the slave window
    tackle_window = Toplevel()
    tackle_window['bg'] = 'dodgerblue4'
    tackle_window.title("Fishing Tackle For Sale")
    tackle_window.focus_force()

    #Declare variables for checkbuttons
    tackle1 = IntVar()
    tackle2 = IntVar()
    tackle3 = IntVar()
    tackle4 = IntVar()
    tackle5 = IntVar()
    tackle6 = IntVar()
    tackle7 = IntVar()
    tackle8 = IntVar()
    tackle9 = IntVar()
    tackle10 = IntVar()
    
    #Nested function for adding things to the cart
    def add_tackle_to_cart():
        if tackle1.get() == 1:
            cart_titles.append(tackle_titles[1])
            cart_images.append(tackle_images[0])
            cart_prices.append(tackle_prices[0])
            
        if tackle2.get() == 1:
            cart_titles.append(tackle_titles[2])
            cart_images.append(tackle_images[1])
            cart_prices.append(tackle_prices[1])
            
        if tackle3.get() == 1:
            cart_titles.append(tackle_titles[3])
            cart_images.append(tackle_images[2])
            cart_prices.append(tackle_prices[2])
            
        if tackle4.get() == 1:
            cart_titles.append(tackle_titles[4])
            cart_images.append(tackle_images[3])
            cart_prices.append(tackle_prices[3])
            
        if tackle5.get() == 1:
            cart_titles.append(tackle_titles[5])
            cart_images.append(tackle_images[4])
            cart_prices.append(tackle_prices[4])
            
        if tackle6.get() == 1:
            cart_titles.append(tackle_titles[6])
            cart_images.append(tackle_images[5])
            cart_prices.append(tackle_prices[5])
            
        if tackle7.get() == 1:
            cart_titles.append(tackle_titles[7])
            cart_images.append(tackle_images[6])
            cart_prices.append(tackle_prices[6])
            
        if tackle8.get() == 1:
            cart_titles.append(tackle_titles[8])
            cart_images.append(tackle_images[7])
            cart_prices.append(tackle_prices[7])
            
        if tackle9.get() == 1:
            cart_titles.append(tackle_titles[9])
            cart_images.append(tackle_images[8])
            cart_prices.append(tackle_prices[8])
            
        if tackle10.get() == 1:
            cart_titles.append(tackle_titles[10])
            cart_images.append(tackle_images[9])
            cart_prices.append(tackle_prices[9])
            


    #Setup all of the widgets
    frame_for_tackle_list = LabelFrame(tackle_window,relief = SOLID, borderwidth = 2, fg = "#00C957", bg = 'dodgerblue4', width = 450, height = 750, text = "Select Items, Then Click Add To Cart", font = ('Helvetica' , '14', 'bold'))

    #Here was a for loop I made to create the 10 checkbuttons unforunately I was
    #unable to figure out how to create then iterate
    #over IntVar() and had to abandon it
    ##        for x in range(9):
    ##              tackle_b = Checkbutton(frame_for_tackle_list, text = tackle_titles[x +1] + '\n $' + tackle_prices[x], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = tackle[x])

    #Create the checkbuttons 
    tackle_b1 = Checkbutton(frame_for_tackle_list, text = tackle_titles[1] + '\n $' + tackle_prices[0], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = tackle1)
    tackle_b2 = Checkbutton(frame_for_tackle_list, text = tackle_titles[2] + '\n $' + tackle_prices[1], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = tackle2)
    tackle_b3 = Checkbutton(frame_for_tackle_list, text = tackle_titles[3] + '\n $' + tackle_prices[2], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = tackle3)
    tackle_b4 = Checkbutton(frame_for_tackle_list, text = tackle_titles[4] + '\n $' + tackle_prices[3], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = tackle4)
    tackle_b5 = Checkbutton(frame_for_tackle_list, text = tackle_titles[5] + '\n $' + tackle_prices[4], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = tackle5)
    tackle_b6 = Checkbutton(frame_for_tackle_list, text = tackle_titles[6] + '\n $' + tackle_prices[5], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = tackle6)
    tackle_b7 = Checkbutton(frame_for_tackle_list, text = tackle_titles[7] + '\n $' + tackle_prices[6], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = tackle7)
    tackle_b8 = Checkbutton(frame_for_tackle_list, text = tackle_titles[8] + '\n $' + tackle_prices[7], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = tackle8)
    tackle_b9 = Checkbutton(frame_for_tackle_list, text = tackle_titles[9] + '\n $' + tackle_prices[8], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = tackle9)
    tackle_b10 = Checkbutton(frame_for_tackle_list, text = tackle_titles[10] + '\n $' + tackle_prices[9], width = 100, bg = 'deepskyblue1',fg = 'black', font = ('Helvetica' , '14', 'bold'), variable = tackle10)

    #Add to cart button
    add_tackle_to_cart_button = Button(tackle_window, width = 100, text = "Add To Cart", bg = 'deepskyblue1', fg = 'white', font = ('Helvetica' , '14', 'bold'), command = add_tackle_to_cart)

    #Pack everything into the window
    tackle_b1.pack()
    tackle_b2.pack()
    tackle_b3.pack()
    tackle_b4.pack()
    tackle_b5.pack()
    tackle_b6.pack()
    tackle_b7.pack()
    tackle_b8.pack()
    tackle_b9.pack()
    tackle_b10.pack()
    frame_for_tackle_list.pack(side = 'top')
    add_tackle_to_cart_button.pack(side = 'bottom')


###############################
### ELECTRONICS SHOP WINDOW ###
###############################


    
def electronics_purchase_window():

    #Open the file for use
    electronics_shop = open(file = 'electronics_shop.xhtml', encoding = 'UTF-8').read()


    #Scrape the webpage for title names
    electronics_titles = []
    electronics_title_list = findall(r'<title>\s*\#[0-9]+[0-9]*:(.*?)\s*<\/title>', electronics_shop)
    electronics_titles.append(electronics_title_list)
    electronics_titles = electronics_titles[0]
    

    #Scrape the webpage for image sources
    electronics_images = []
    electronics_image_list = findall(r'<img src="(https://images-fe\..*?)"', electronics_shop)
    electronics_images.append(electronics_image_list)
    electronics_images = electronics_images[0]


    #Scrape the webpage for prices
    electronics_prices = []
    electronics_prices_list = findall(r'<b>\$(.*?)</b>', electronics_shop)
    electronics_prices.append(electronics_prices_list)
    electronics_prices = electronics_prices[0]

   
    #Setup the slave window
    electronics_window = Toplevel()
    electronics_window['bg'] = 'dodgerblue4'
    electronics_window.title("electronicss For Sale")
    electronics_window.focus_force()

    #Declare variables for the checkbuttons
    electronics1 = IntVar()
    electronics2 = IntVar()
    electronics3 = IntVar()
    electronics4 = IntVar()
    electronics5 = IntVar()
    electronics6 = IntVar()
    electronics7 = IntVar()
    electronics8 = IntVar()
    electronics9 = IntVar()
    electronics10 = IntVar()
    
    #Nested function for adding things to cart
    def add_electronics_to_cart():
        if electronics1.get() == 1:
            cart_titles.append(electronics_titles[0])
            cart_images.append(electronics_images[0])
            cart_prices.append(electronics_prices[0])
            
        if electronics2.get() == 1:
            cart_titles.append(electronics_titles[1])
            cart_images.append(electronics_images[1])
            cart_prices.append(electronics_prices[1])
            
        if electronics3.get() == 1:
            cart_titles.append(electronics_titles[2])
            cart_images.append(electronics_images[2])
            cart_prices.append(electronics_prices[2])
            
        if electronics4.get() == 1:
            cart_titles.append(electronics_titles[3])
            cart_images.append(electronics_images[3])
            cart_prices.append(electronics_prices[3])
            
        if electronics5.get() == 1:
            cart_titles.append(electronics_titles[4])
            cart_images.append(electronics_images[4])
            cart_prices.append(electronics_prices[4])
            
        if electronics6.get() == 1:
            cart_titles.append(electronics_titles[5])
            cart_images.append(electronics_images[5])
            cart_prices.append(electronics_prices[5])
            
        if electronics7.get() == 1:
            cart_titles.append(electronics_titles[6])
            cart_images.append(electronics_images[6])
            cart_prices.append(electronics_prices[6])
            
        if electronics8.get() == 1:
            cart_titles.append(electronics_titles[7])
            cart_images.append(electronics_images[7])
            cart_prices.append(electronics_prices[7])
            
        if electronics9.get() == 1:
            cart_titles.append(electronics_titles[8])
            cart_images.append(electronics_images[8])
            cart_prices.append(electronics_prices[8])
            
        if electronics10.get() == 1:
            cart_titles.append(electronics_titles[9])
            cart_images.append(electronics_images[9])
            cart_prices.append(electronics_prices[9])
            


    

    #Setup all of the widgets
    frame_for_electronics_list = LabelFrame(electronics_window,relief = SOLID, borderwidth = 2, fg = "#00C957", bg = 'dodgerblue4', width = 450, height = 750, text = "Select Items, Then Click Add To Cart", font = ('Helvetica' , '14', 'bold'))
    electronics_b1 = Checkbutton(frame_for_electronics_list, text = electronics_titles[0] + '\n $' + electronics_prices[0], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = electronics1)
    electronics_b2 = Checkbutton(frame_for_electronics_list, text = electronics_titles[1] + '\n $' + electronics_prices[1], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = electronics2)
    electronics_b3 = Checkbutton(frame_for_electronics_list, text = electronics_titles[2] + '\n $' + electronics_prices[2], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = electronics3)
    electronics_b4 = Checkbutton(frame_for_electronics_list, text = electronics_titles[3] + '\n $' + electronics_prices[3], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = electronics4)
    electronics_b5 = Checkbutton(frame_for_electronics_list, text = electronics_titles[4] + '\n $' + electronics_prices[4], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = electronics5)
    electronics_b6 = Checkbutton(frame_for_electronics_list, text = electronics_titles[5] + '\n $' + electronics_prices[5], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = electronics6)
    electronics_b7 = Checkbutton(frame_for_electronics_list, text = electronics_titles[6] + '\n $' + electronics_prices[6], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = electronics7)
    electronics_b8 = Checkbutton(frame_for_electronics_list, text = electronics_titles[7] + '\n $' + electronics_prices[7], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = electronics8)
    electronics_b9 = Checkbutton(frame_for_electronics_list, text = electronics_titles[8] + '\n $' + electronics_prices[8], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = electronics9)
    electronics_b10 = Checkbutton(frame_for_electronics_list, text = electronics_titles[9] + '\n $' + electronics_prices[9], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = electronics10)

    #Add to cart button
    add_electronics_to_cart_button = Button(electronics_window, width = 100, text = "Add To Cart", bg = 'deepskyblue1', fg = 'white', font = ('Helvetica' , '14', 'bold'), command = add_electronics_to_cart)

    #Pack everything into the window
    electronics_b1.pack()
    electronics_b2.pack()
    electronics_b3.pack()
    electronics_b4.pack()
    electronics_b5.pack()
    electronics_b6.pack()
    electronics_b7.pack()
    electronics_b8.pack()
    electronics_b9.pack()
    electronics_b10.pack()
    frame_for_electronics_list.pack(side = 'top')
    add_electronics_to_cart_button.pack(side = 'bottom')



#########################
### GAMES SHOP WINDOW ###
#########################


    
def games_purchase_window():

    #Download the webpage for scraping
    download('https://www.amazon.com.au/rss/new-releases/videogames?tag=assoc-tag','game_shop', 'xhtml')


    #Open the webpage for use
    game_shop = open(file = 'game_shop.xhtml', encoding = 'UTF-8').read()


         
    #Scrape the webpage for title names
    game_titles = []
    game_title_list = findall(r'<title>\s*\#[0-9]+[0-9]*:(.*?)\s*<\/title>', game_shop)
    game_titles.append(game_title_list)
    game_titles = game_titles[0]


    #Scrape the webpage for image sources
    game_images = []
    game_image_list = findall(r'<img src="(https://images-fe\..*?)"', game_shop)
    game_images.append(game_image_list)
    game_images = game_images[0]


    #Scrape the webpage for prices
    game_prices = []
    game_price_list = findall(r'<b>\$(.*?)</b>', game_shop)
    game_prices.append(game_price_list)
    game_prices = game_prices[0]
    
    #Setup the slave window
    games_window = Toplevel()
    games_window['bg'] = 'dodgerblue4'
    games_window.title("games For Sale")
    games_window.focus_force()

    #Declare variables for the checkbuttons
    game1 = IntVar()
    game2 = IntVar()
    game3 = IntVar()
    game4 = IntVar()
    game5 = IntVar()
    game6 = IntVar()
    game7 = IntVar()
    game8 = IntVar()
    game9 = IntVar()
    game10 = IntVar()
    
    #Nested function for adding things to cart
    def add_game_to_cart():
        if game1.get() == 1:
            cart_titles.append(game_titles[0])
            cart_images.append(game_images[0])
            cart_prices.append(game_prices[0])
            
        if game2.get() == 1:
            cart_titles.append(game_titles[1])
            cart_images.append(game_images[1])
            cart_prices.append(game_prices[1])
            
        if game3.get() == 1:
            cart_titles.append(game_titles[2])
            cart_images.append(game_images[2])
            cart_prices.append(game_prices[2])
            
        if game4.get() == 1:
            cart_titles.append(game_titles[3])
            cart_images.append(game_images[3])
            cart_prices.append(game_prices[3])
            
        if game5.get() == 1:
            cart_titles.append(game_titles[4])
            cart_images.append(game_images[4])
            cart_prices.append(game_prices[4])

        if game6.get() == 1:
            cart_titles.append(game_titles[5])
            cart_images.append(game_images[5])
            cart_prices.append(game_prices[5])

        if game7.get() == 1:
            cart_titles.append(game_titles[6])
            cart_images.append(game_images[6])
            cart_prices.append(game_prices[6])

        if game8.get() == 1:
            cart_titles.append(game_titles[7])
            cart_images.append(game_images[7])
            cart_prices.append(game_prices[7])

        if game9.get() == 1:
            cart_titles.append(game_titles[8])
            cart_images.append(game_images[8])
            cart_prices.append(game_prices[8])

        if game10.get() == 1:
            cart_titles.append(game_titles[9])
            cart_images.append(game_images[9])
            cart_prices.append(game_prices[9])



    

    #Setup all of the widgets
    frame_for_games_list = LabelFrame(games_window,relief = SOLID, borderwidth = 2, fg = "#00C957", bg = 'dodgerblue4', width = 450, height = 750, text = "Select Items, Then Click Add To Cart", font = ('Helvetica' , '14', 'bold'))
    games_b1 = Checkbutton(frame_for_games_list, text = game_titles[0] + '\n $' + game_prices[0], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = game1)
    games_b2 = Checkbutton(frame_for_games_list, text = game_titles[1] + '\n $' + game_prices[1], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = game2)
    games_b3 = Checkbutton(frame_for_games_list, text = game_titles[2] + '\n $' + game_prices[2], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = game3)
    games_b4 = Checkbutton(frame_for_games_list, text = game_titles[3] + '\n $' + game_prices[3], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = game4)
    games_b5 = Checkbutton(frame_for_games_list, text = game_titles[4] + '\n $' + game_prices[4], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = game5)
    games_b6 = Checkbutton(frame_for_games_list, text = game_titles[5] + '\n $' + game_prices[5], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = game6)
    games_b7 = Checkbutton(frame_for_games_list, text = game_titles[6] + '\n $' + game_prices[6], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = game7)
    games_b8 = Checkbutton(frame_for_games_list, text = game_titles[7] + '\n $' + game_prices[7], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = game8)
    games_b9 = Checkbutton(frame_for_games_list, text = game_titles[8] + '\n $' + game_prices[8], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = game9)
    games_b10 = Checkbutton(frame_for_games_list, text = game_titles[9] + '\n $' + game_prices[9], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = game10)
    
    #Add to cart button
    add_game_to_cart_button = Button(games_window, width = 100, text = "Add To Cart", bg = 'deepskyblue1', fg = 'white', font = ('Helvetica' , '14', 'bold'), command = add_game_to_cart)

    #Pack everything into the window
    games_b1.pack()
    games_b2.pack()
    games_b3.pack()
    games_b4.pack()
    games_b5.pack()
    games_b6.pack()
    games_b7.pack()
    games_b8.pack()
    games_b9.pack()
    games_b10.pack()
    frame_for_games_list.pack(side = 'top')
    add_game_to_cart_button.pack(side = 'bottom')


#########################
### BOOKS SHOP WINDOW ###
#########################



def books_purchase_window():

    #Download the webpage for scraping
    download('https://www.amazon.com.au/rss/new-releases/books?tag=assoc-tag', 'book_shop', 'xhtml')

    #Open the webpage for use
    book_shop = open(file = 'book_shop.xhtml', encoding = 'UTF-8').read()



    #Scrape the webpage for title names
    book_titles = []
    book_title_list = findall(r'<title>\#[0-9]+[0-9]*:(.*?)<\/title>',book_shop)
    book_titles.append(book_title_list)
    book_titles = book_titles[0]


    #Scrape webpage for image sources
    book_images = []
    book_image_list = findall(r'<img src="(https://images-fe\..*?)"', book_shop)
    book_images.append(book_image_list)
    book_images = book_images[0]
    

    #Scrape webpage for prices
    book_prices = []
    book_price_list = findall(r'<b>\$([0-9]*\.[0-9]*)</b>', book_shop)
    book_prices.append(book_price_list)
    book_prices = book_prices[0]
    
    #Setup the slave window
    books_window = Toplevel()
    books_window['bg'] = 'dodgerblue4'
    books_window.title("Books For Sale")
    books_window.focus_force()

    #Declare variables for checkbuttons
    book1 = IntVar()
    book2 = IntVar()
    book3 = IntVar()
    book4 = IntVar()
    book5 = IntVar()
    book6 = IntVar()
    book7 = IntVar()
    book8 = IntVar()
    book9 = IntVar()
    book10 = IntVar()

    #Nested function for adding things to cart
    def add_book_to_cart():
        if book1.get() == 1:
            cart_titles.append(book_titles[0])
            cart_images.append(book_images[0])
            cart_prices.append(book_prices[0])
            
        if book2.get() == 1:
            cart_titles.append(book_titles[1])
            cart_images.append(book_images[1])
            cart_prices.append(book_prices[1])
            
        if book3.get() == 1:
            cart_titles.append(book_titles[2])
            cart_images.append(book_images[2])
            cart_prices.append(book_prices[2])
            
        if book4.get() == 1:
            cart_titles.append(book_titles[3])
            cart_images.append(book_images[3])
            cart_prices.append(book_prices[3])
            
        if book5.get() == 1:
            cart_titles.append(book_titles[4])
            cart_images.append(book_images[4])
            cart_prices.append(book_prices[4])
           
        if book6.get() == 1:
            cart_titles.append(book_titles[5])
            cart_images.append(book_images[5])
            cart_prices.append(book_prices[5])
           
        if book7.get() == 1:
            cart_titles.append(book_titles[6])
            cart_images.append(book_images[6])
            cart_prices.append(book_prices[6])
            
        if book8.get() == 1:
            cart_titles.append(book_titles[7])
            cart_images.append(book_images[7])
            cart_prices.append(book_prices[7])
           
        if book9.get() == 1:
            cart_titles.append(book_titles[8])
            cart_images.append(book_images[8])
            cart_prices.append(book_prices[8])
            
        if book10.get() == 1:
            cart_titles.append(book_titles[9])
            cart_images.append(book_images[9])
            cart_prices.append(book_prices[9])
           


    


    #Setup all of the widgets
    frame_for_books_list = LabelFrame(books_window,relief = SOLID, borderwidth = 2, fg = "#00C957", bg = 'dodgerblue4', width = 450, height = 750, text = "Select Items, Then Click Add To Cart", font = ('Helvetica' , '14', 'bold'))
    books_b1 = Checkbutton(frame_for_books_list, text = book_titles[0] + '\n $' + book_prices[0], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = book1)
    books_b2 = Checkbutton(frame_for_books_list, text = book_titles[1] + '\n $' + book_prices[1], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = book2)
    books_b3 = Checkbutton(frame_for_books_list, text = book_titles[2] + '\n $' + book_prices[2], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = book3)
    books_b4 = Checkbutton(frame_for_books_list, text = book_titles[3] + '\n $' + book_prices[3], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = book4)
    books_b5 = Checkbutton(frame_for_books_list, text = book_titles[4] + '\n $' + book_prices[4], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = book5)
    books_b6 = Checkbutton(frame_for_books_list, text = book_titles[5] + '\n $' + book_prices[5], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = book6)
    books_b7 = Checkbutton(frame_for_books_list, text = book_titles[6] + '\n $' + book_prices[6], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = book7)
    books_b8 = Checkbutton(frame_for_books_list, text = book_titles[7] + '\n $' + book_prices[7], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = book8)
    books_b9 = Checkbutton(frame_for_books_list, text = book_titles[8] + '\n $' + book_prices[8], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100, font = ('Helvetica' , '14', 'bold'), variable = book9)
    books_b10 = Checkbutton(frame_for_books_list, text = book_titles[9] + '\n $' + book_prices[9], width = 100, height = 4, bg = 'deepskyblue1',fg = 'black', wraplength = 1100,  font = ('Helvetica' , '14', 'bold'), variable = book10)

    #Add to cart button
    add_book_to_cart_button = Button(books_window, width = 100, text = "Add To Cart", bg = 'deepskyblue1', fg = 'white', font = ('Helvetica' , '14', 'bold'), command = add_book_to_cart)

    #Pack everything into the window
    books_b1.pack()
    books_b2.pack()
    books_b3.pack()
    books_b4.pack()
    books_b5.pack()
    books_b6.pack()
    books_b7.pack()
    books_b8.pack()
    books_b9.pack()
    books_b10.pack()
    frame_for_books_list.pack(side = 'top')
    add_book_to_cart_button.pack(side = 'bottom', pady = 10)


################################
### GRAPHICAL USER INTERFACE ###
################################



#Construct GUI main window
main_window = Tk()
main_window['bg'] = 'dodgerblue4'
main_window.title("Doges Procured Goods")
main_window.geometry("500x750")

#Give the main window a snazzy title
main_window_text = Label(main_window, height = 2, width = 50, text = 'Welcome To \n Doges Procured Goods', bg = 'dodgerblue4', font = ('Helvetica' , '30', 'bold italic'), relief = FLAT, fg = 'white')
main_window_text.pack(side = 'top')


#Add an image to the GUI main window
img = PhotoImage(file = 'doge.gif')
main_window_image = Label(main_window, image = img, bg = 'dodgerblue4')
main_window_image.pack(side = 'top')


#Place in a frame to hold static widgets
frame_for_static_pages = LabelFrame(main_window, bg = 'dodgerblue4', bd = 5, fg = 'white', text = "Old Procures", font = ('Helvetica' , '14', 'bold italic'))
frame_for_static_pages.pack(side = 'top')


#Place in a frame to hold live widgets
frame_for_live_pages = LabelFrame(main_window, bg = 'dodgerblue4', fg = 'white', bd = 5, text = "Fresh Procures", font = ('Helvetica' , '14', 'bold italic'))
frame_for_live_pages.pack(side = 'top')

#Add in some buttons for the slave windows
Tackle_Button = Button(frame_for_static_pages, width = 20, text = "Buy Fishing Tackle", bg = 'deepskyblue1',fg = 'white', command = tackle_purchase_window, font = ('Helvetica' , '14', 'bold'))
electronics_Button = Button(frame_for_static_pages, width = 20, text = "Buy Electronics", bg = 'deepskyblue1',fg = 'white', command = electronics_purchase_window, font = ('Helvetica' , '14', 'bold'))
games_Button = Button(frame_for_live_pages, width = 20, text = "Buy Games", bg = 'deepskyblue1',fg = 'white', command = games_purchase_window, font = ('Helvetica' , '14', 'bold'))
Books_Button = Button(frame_for_live_pages, width = 20, text = "Buy Books", bg = 'deepskyblue1',fg = 'white', command = books_purchase_window, font = ('Helvetica' , '14', 'bold'))
Generate_invoice = Button(main_window, width = 20, height = 10, text = "Generate Invoice", bg = 'deepskyblue1', fg = 'white', font = ('Helvetica' , '14', 'bold'), command = generate_invoice)

#Pack all the widgets into the window
Tackle_Button.pack()
electronics_Button.pack()
games_Button.pack()
Books_Button.pack()
Generate_invoice.pack(pady = 20)

#Empty lists for adding to the cart and generating an invoice
cart_titles = []
cart_images = []
cart_prices = []

#Run the main window
main_window.mainloop()

