import requests
import smtplib
import shutil
import config

from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

#  Daily xkcd dose  - Pulls a random xkcd comic and sends it to by mail.


def get_image():

    # Finds and loads the image
    header = "xkcd"
    r = requests.get("https://c.xkcd.com/random/comic/", header)
    soup = BeautifulSoup(r.text, features="html.parser")
    comic_div = soup.find(id="comic")
    img = comic_div.find("img")
    img_url = img.get("src")
    fixed_img_url = "https:" + img_url
    get_image.image_title = img.get("alt")
    request_img = requests.get(fixed_img_url, header, stream="True")
    get_image.png_title = get_image.image_title + ".png"
    local_image = open(get_image.png_title, "wb")
    request_img.raw.decode_content = True

    # Saves image locally
    shutil.copyfileobj(request_img.raw, local_image)
    del request_img


def send_mail():

    # Message config
    msgRoot = MIMEMultipart("related")
    msgRoot["Subject"] = "Your daily xkcd dose - " + get_image.image_title
    msgRoot["From"] = config.send_from
    msgRoot["To"] = config.send_to

    # Loads image to mail
    fp = open(get_image.png_title, "rb")
    msgImage = MIMEImage(fp.read())
    fp.close()
    msgImage.add_header("Content-ID", "<image1>")
    msgRoot.attach(msgImage)

    # Starts SMTP connection and sends the mail
    server = smtplib.SMTP_SSL(config.host)
    server.connect(config.host, config.port)
    server.login(config.send_from, config.password)
    server.sendmail(config.send_from, config.send_to, msgRoot.as_string())


get_image()
send_mail()
