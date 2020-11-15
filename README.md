# Epey.com-Price-Checker
Script that checks prices of desired products and sends e-mail whenever there is a discount.

* pip install -r requirements.txt
* List the link of the products that you want to follow in **product_links** list
* List the name of the products that you want to follow in **product_names** list
* Put your botmail and real mail in **EmailMessage()** object. (**msg**)
* At the end of the code, enter your botmail and its password for **smtp login.**
* Change the min.txt so that it stores the starting prices of the products you want to follow along with their names . Make sure the price is in "floatable" format. (No comma, space etc.)
* Set up a scheduler in your own machine, you're good to go!

Whenever there is a discount in one of the products, an e-mail will be sent to your mail.



