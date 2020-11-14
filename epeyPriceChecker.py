import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage

product_links = ["https://www.epey.com/monitor/james-donkey-jd27fg1ms144.html", \
				"https://www.epey.com/monitor/gamepower-gpr27c1ms144.html", \
				"https://www.epey.com/monitor/acer-kg271pbmidpx.html", \
                "https://www.epey.com/monitor/aoc-g2790px.html", \
                "https://www.epey.com/monitor/gamebooster-gb-2709ff.html", \
                "https://www.epey.com/monitor/acer-nitro-vg270sbmiipx.html", \
                "https://www.epey.com/monitor/rampage-bright-rm-68.html", \
                "https://www.epey.com/monitor/asus-tuf-gaming-vg279q1r.html", \
                "https://www.epey.com/monitor/acer-nitro-xv270p.html", \
                "https://www.epey.com/monitor/gamepower-gpr27c144.html", \
                "https://www.epey.com/monitor/acer-kg241qsbiip.html", \
                "https://www.epey.com/monitor/philips-242e1gaj.html", \
                "https://www.epey.com/monitor/rampage-rm-344.html",\
                "https://www.epey.com/monitor/gamepower-gpr24c1ms144.html", \
                "https://www.epey.com/monitor/rampage-bright-rm-61.html", \
                "https://www.epey.com/monitor/lg-ultragear-24gl650-b.html", \
                "https://www.epey.com/monitor/hp-x24c-9fm22aa.html", \
                "https://www.epey.com/monitor/aoc-g2490vxa.html", \
                "https://www.epey.com/monitor/acer-xf240qs.html",\
                "https://www.epey.com/monitor/acer-nitro-vg240ysbmiipx.html", \
                "https://www.epey.com/monitor/asus-vp249qgr.html", \
                "https://www.epey.com/monitor/acer-kg251qjbmidpx.html", \
                "https://www.epey.com/monitor/viewsonic-vx2458-c-mhd.html"]

product_names = ["James Donkey JD27FG1MS144 Monitör", \
    			"GamePower GPR27C1MS144 Monitör", \
    			"Acer KG271Pbmidpx Monitör (UM.HX1EE.P01)", \
                "AOC G2790PX Monitör", \
                "GameBooster GB-2709FF Monitör", \
                "Acer Nitro VG270Sbmiipx Monitör (UM.HV0EE.S01)", \
                "Rampage Bright RM-68 Monitör", \
                "Asus TUF Gaming VG279Q1R Monitör", \
                "Acer Nitro XV270P Monitör (UM.HX0EE.P04)", \
                "GamePower GPR27C144 Monitör", \
                "Acer KG241QSbiip Monitör (UM.UX1EE.S01)", \
                "Philips 242E1GAJ/01 Monitör", \
                "Rampage RM-344 Monitör",\
                "GamePower GPR24C1MS144 Monitör", \
                "Rampage Bright RM-61 Monitör", \
                "LG UltraGear 24GL650-B Monitör", \
                "HP X24c (9FM22AA) Monitör", \
                "AOC G2490VXA Monitör", \
                "Acer XF240QS Monitör (UM.UX0EE.S01)",\
                "Acer Nitro VG240YSbmiipx Monitör (UM.QV0EE.S01)", \
                "Asus VP249QGR Monitör", \
                "Acer KG251QJbmidpx Monitör", \
                "ViewSonic VX2458-C-mhd Monitör"]

#SetUp Email information. Body will be filled throughout the code
msg = EmailMessage()
msg['Subject'] = "Ürün İndirim Bilgisi"
msg['From'] = "exampleSender@gmail.com"
msg['To'] = "exampleReciever@gmail.com"
messageBody = ""
anyChanges = False  #If even there is a single discount, we'll set this to True (to send mail)

#Opening min file and accessing all min values of laptops
f = open("min.txt", "r")
lines = f.readlines()

for i in range(len(product_names)):
	productName = lines[i*2]
	oldPrice = float(lines[i*2 + 1])

	#Getting new html object
	r = requests.get(product_links[i])
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
	if priceFloat < oldPrice - 200:
		messageBody += product_names[i] + " Ürün İndirimi\nEski Fiyat = " + str(oldPrice) + "\nYeni Fiyat = " + \
		              str(priceFloat) + "\n" + product_links[i] + "\n\n"
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

		smtp.login("exampleSender@gmail.com", "password")
		
		smtp.send_message(msg)