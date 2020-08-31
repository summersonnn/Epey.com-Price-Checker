import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage

product_links = ["https://www.epey.com/laptop/hp-probook-440-g6-7df56ea.html", \
				"https://www.epey.com/laptop/hp-15-dw2009nt-3h813ea.html", \
				"https://www.epey.com/laptop/monster-huma-h4-v3-1.html"] 

product_names = ["HP ProBook 440 G6 (7DF56EA) Notebook", \
				"HP 15-dw2009nt (3H813EA) Notebook", \
				"Monster Huma H4 V3.1 Notebook"]

#SetUp Email information. Body will be filled throughout the code
msg = EmailMessage()
msg['Subject'] = "Ürün İndirim Bilgisi"
msg['From'] = "yourbotmail@gmail.com"
msg['To'] = "yourownmail@gmail.com"
messageBody = ""
anyChanges = False  #If even there is a single discount, we'll set this to True (to send mail)

#Opening min file and accessing all min values of products
f = open("min.txt", "r")
lines = f.readlines()

for i in range(len(product_names)):
	productName = lines[i*2]
	oldPrice = float(lines[i*2 + 1])

	#Getting new html object
	r = requests.get(product_links[i])
	html_doc = r.content
	soup = BeautifulSoup(html_doc, 'html.parser')

	try:
		#Accessing the first price
		priceText = soup.find("span",attrs={"class":"urun_fiyat"}).text

		#Chopping string after TL
		sep = 'TL'
		onlyPrice = priceText.split(sep, 1)[0]

		#Remove . from string
		onlyPrice = onlyPrice.replace('.', '')
		onlyPrice = onlyPrice.replace(',', '.')

		#Convert to Float
		priceFloat = float(onlyPrice)

		lines[i*2 + 1] = str(priceFloat) + '\n'
		#If new price is lower, edit corresponding line
		if priceFloat < oldPrice:
			messageBody += product_names[i] + " Ürün İndirimde\nEski Fiyat = " + str(oldPrice) + "\nYeni Fiyat = " + \
			              str(priceFloat) + "\n" + product_links[i] + "\n\n"
			anyChanges = True

		# and write everything back
		with open('min.txt', 'w') as file:
		    file.writelines( lines )
		f.close()
	except:
		continue

if anyChanges:
	msg.set_content(messageBody)
	with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
		smtp.ehlo()
		smtp.starttls()
		smtp.ehlo()

		smtp.login("yourbotmail@gmail.com", "PasswordOfBotMail")
		
		smtp.send_message(msg)