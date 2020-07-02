import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage

laptop_links = ["https://www.epey.com/laptop/hp-probook-440-g6-7df56ea.html", \
                "https://www.epey.com/laptop/hp-pavilion-x360-14-dh1005nt-8xh01ea.html", \
                "https://www.epey.com/laptop/asus-um431da-am024t.html", \
                "https://www.epey.com/laptop/hp-14-ce3003nt-3h905ea.html", \
                "https://www.epey.com/laptop/acer-swift-3-sf314-58g-53hn.html", \
                "https://www.epey.com/laptop/huawei-matebook-13-8plus512-gb.html", \
                "https://www.epey.com/laptop/huawei-matebook-d-14-amd.html", \
                "https://www.epey.com/laptop/lenovo-s540-81nd003utx.html", \
                "https://www.epey.com/laptop/hp-14-cf2005nt-9cp83ea.html", \
                "https://www.epey.com/laptop/hp-340s-g7-10r29ea.html", \
                "https://www.epey.com/laptop/hp-14-cf2004nt-9cn08ea.html", \
                "https://www.epey.com/laptop/hp-14-cf1018nt-8bw26ea.html", \
                "https://www.epey.com/laptop/dell-inspiron-5490-s510f82n.html", \
                "https://www.epey.com/laptop/monster-huma-h4-v3-2.html"] 

laptop_names = ["HP ProBook 440 G6 (7DF56EA) Notebook", \
                "HP Pavilion x360 14-dh1005nt (8XH01EA) 2'si 1 Arada", \
                "Asus UM431DA-AM024T Ultrabook", \
                "HP 14-ce3003nt (3H905EA) Notebook", \
                "Acer Swift 3 SF314-58G-53HN Ultrabook (NX.HPKEY.002)", \
                "Huawei MateBook 13 8+512 GB Notebook", \
                "Huawei MateBook D 14 AMD Notebook (53010WPX)", \
                "Lenovo S540 81ND003UTX Notebook", \
                "HP 14-cf2005nt (9CP83EA) Notebook", \
                "HP 340S G7 (10R29EA) Notebook", \
                "HP 14-cf2004nt (9CN08EA) Notebook", \
                "HP 14-cf1018nt (8BW26EA) Notebook", \
                "Dell Inspiron 5490", \
                "Monster Huma H4 V3.2"]

#SetUp Email information. Body will be filled throughout the code
msg = EmailMessage()
msg['Subject'] = "Laptop Discount Information"
msg['From'] = "yourbotmail@gmail.com"
msg['To'] = "yourownmail@gmail.com"
messageBody = ""
anyChanges = False  #If even there is a single discount, we'll set this to True (to send mail)

#Opening min file and accessing all min values of laptops
f = open("min.txt", "r")
lines = f.readlines()

for i in range(len(laptop_names)):
	laptopName = lines[i*2]
	oldPrice = float(lines[i*2 + 1])

	#Getting new html object
	r = requests.get(laptop_links[i])
	html_doc = r.content
	soup = BeautifulSoup(html_doc, 'html.parser')

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
		messageBody += laptop_names[i] + " Notebook Discount!\nOld Price = " + str(oldPrice) + "\nNew Price = " + \
		              str(priceFloat) + "\n\n"
		anyChanges = True

	# and write everything back
	with open('min.txt', 'w') as file:
	    file.writelines( lines )
	f.close()
	

if anyChanges:
	msg.set_content(messageBody)
	with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
		smtp.ehlo()
		smtp.starttls()
		smtp.ehlo()

		smtp.login("yourbotmail@gmail.com", "PasswordOfBotMail")
		
		smtp.send_message(msg)