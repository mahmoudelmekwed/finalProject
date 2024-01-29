# MY FINAL PROJECT
WatchStore is an e-commerce platform dedicated to the world of watches. This online store provides a rich collection of timepieces, catering to diverse tastes and preferences. With user-friendly features like product details, an add-to-cart system, seamless checkout, and order confirmation, WatchStore aims to deliver a superior shopping experience for watch enthusiasts.

One-Page Checkout: A simplified one-page checkout process that reduces the time and complexity of completing a purchase. All necessary information is collected on a single page, leading to higher conversion rates.

## Prerequisites
Did you add any additional modules that someone needs to install (for instance anything in Python that you `pip install-ed`)? 
List those here (if any).
Clone the Repository:
    git clone https://github.com/mahmoudelmekwed/finalProject.git
Navigate to the Project Directory:
    cd finalProject
Install Python Dependencies:
    pip install Flask
Run the Flask Application:
    flask --app app.py run

## Project Checklist
- [x] It is available on GitHub.
- [x] It uses the Flask web framework.
- [x] It uses at least one module from the Python Standard Library other than the random module.
  Please provide the name of the module you are using in your app.
  - Module name: - json module
                 - secrets module
- [x] It contains at least one class written by you that has both properties and methods. It uses `__init__()` to let the class initialize the object's attributes (note that  `__init__()` doesn't count as a method). This includes instantiating the class and using the methods in your app. Please provide below the file name and the line number(s) of at least one example of a class definition in your code as well as the names of two properties and two methods.
  - File name for the class definition: models.py
  - Line number(s) for the class definition: 4 , 18
  - Name of two properties: id , image , name , username , password , email
  - Name of two methods:  calculate_cart_total , calculate_cart_quantity , clear_cart
  - File name and line numbers where the methods are used: 
         - product.py   13 , 145 , 146
         - user.py 38
- [x] It makes use of JavaScript in the front end and uses the localStorage of the web browser.
- [x] It uses modern JavaScript (for example, let and const rather than var).
- [x] It makes use of the reading and writing to the same file feature.
- [x] It contains conditional statements. Please provide below the file name and the line number(s) of at least
  one example of a conditional statement in your code.
  - File name: product.py
  - Line number(s):   11 , 26 , 31 , 44 
- [x] It contains loops. Please provide below the file name and the line number(s) of at least
  one example of a loop in your code.
  - File name: product.py
  - Line number(s): 25 , 43 , 120
- [x] It lets the user enter a value in a text box at some point.
  This value is received and processed by your back end Python code.
- [x] It doesn't generate any error message even if the user enters a wrong input.
- [x] It is styled using CSS.
- [x] The code follows the code and style conventions as introduced in the course, is fully documented using comments and doesn't contain unused or experimental code. 
  In particular, the code should not use `print()` or `console.log()` for any information the app user should see. Instead, all user feedback needs to be visible in the browser.  
- [x] All exercises have been completed as per the requirements and pushed to the respective GitHub repository.