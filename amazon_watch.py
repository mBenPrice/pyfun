import urllib2, smtplib, re, imaplib, getpass
from time import sleep, localtime, strftime
from bs4 import BeautifulSoup
from random import randrange

    # ## # ## # ## # ##
    #
    #   Grab Junk reads relevant info from based on the type of link
    #   passed in:  prices for products, Warehouse Deals for used listings.
    #
    # ## # ## # ## # ##
def grab_junk(URL, opener):
   ## Grab the page
   try:
      page = opener.open(URL)
   except urllib2.URLError, e:
      print "\nReceived error:"
      print e
      sleep(240)
      
   ## Grab relevant blocks
   content = page.read()
   soup = BeautifulSoup(content)
   html_blocks = soup.findAll('div', attrs = {'class' \
                                    : 'a-row a-spacing-mini olpOffer'})


   sub_blocks = []
   ## Snatch relevant info out of blocks
   if URL.find("used") != -1:
      ## Used Items
      for block in html_blocks:
         detail = block.find(alt="Amazon Warehouse Deals")
         if detail != None:
            ## Item Condition
            temp1 = re.sub("\s+"," ",str(block.findAll('h3', attrs = \
                                    {'class' : 'a-spacing-small olpCondition'})))
            idx1 = temp1.find(">")
            endx1 = temp1.find("</")
            ## Item Description
            temp2 = re.sub("\s+"," ",str(block.findAll('noscript')))
            idx2 = temp2.find("comments\">") + 9
            endx2 = temp2.find(" </")
            sub_blocks.append(temp1[idx1+2:endx1] + "-" + temp2[idx2+2:endx2])
      return sorted(sub_blocks)
   
      ## New Items
   else:
      for block in html_blocks:
         ## Item Cost
         temp1 = re.sub("\s+"," ",str(block.findAll('span', attrs = \
                        {'class' : 'a-size-large a-color-price olpOfferPrice a-text-bold'})))
         idx1 = temp1.find("$")
         endx1 = temp1.find("</")
         ## Shipping Cost
         temp2 = re.sub("\s+"," ",str(block.findAll('span', attrs = {'class' : 'olpShippingPrice'})))
         idx2 = temp2.find("$")
         endx2 = temp2.find("</")
         if len(temp1) < 3: ## Amazon says 'Add to cart to see product details'
            continue
         if len(temp2) > 10:    ## If there is a shipping cost
            sub_blocks.append(float(temp1[idx1+1:endx1]) + float(temp2[idx2+1:endx2]))
         else:
            sub_blocks.append(float(temp1[idx1+1:endx1]))
      return str(min(sub_blocks))
   
   
    # ## # ## # ## # ##
    #
    #   Send Email does exactly what the name says.  Gmail only.
    #
    # ## # ## # ## # ##
def send_email(username, password, new, old, URL):
   fromaddr = username
   toaddrs  = username
#   tempstr = str("From: " + str(old) + "\n\"To: " + str(new) + URL)
   msg = "From: %s\nTo: %s\n" % (username, username)
   msg += "Subject: Amazon Update\n\n"
   msg += "New Value:  " + re.sub(",","\n",str(new)) + "\n"
   msg += "Old Value:  " + re.sub(",","\n",str(old)) + "\n" + URL
   server = smtplib.SMTP('smtp.gmail.com:587')
   server.ehlo()
   server.starttls()
   server.login(username,password)
   server.sendmail(fromaddr, toaddrs, msg)
   server.quit()
   print "Sent notification ~ "
   
   
    # ## # ## # ## # ##
    #
    #   Send Email does exactly what the name says.  Gmail only.
    #
    # ## # ## # ## # ##
def get_info():
    while True:
        username = raw_input("Enter your Gmail username:  ")
        if len(username):
            username += "@gmail.com"
        else:
            username = "sonofdays@gmail.com"

        password = getpass.getpass("Now your password:  ")
           
        obj = imaplib.IMAP4_SSL('imap.gmail.com','993')
        try:
            obj.login(username,password)
            print "Good, you can type.\n"
            break
        except (imaplib.IMAP4.error, urllib2.URLError) as err:
            print err, "\n\n"

    watch_list = []
    while True:
        answer = raw_input("Enter a URL to add it to the watch list or nothing to start watching.\n")
        if len(answer) == 0:
            if len(watch_list) == 0:
                URL1 = "http://www.amazon.com/gp/offer-listing/B00752R4U0/ref=dp_olp_used?ie=UTF8&condition=used"
                URL2 = "http://www.amazon.com/gp/offer-listing/B000ZK5UT6/ref=dp_olp_new?ie=UTF8&condition=new"
                #URL3 = "http://www.amazon.com/gp/offer-listing/B00752R4U0/ref=dp_olp_new?ie=UTF8&condition=new"
                watch_list.append(("", URL1))
                watch_list.append(("", URL2))
                #watch_list.append(("", URL3))
            break
        if answer.find("amazon") == -1:
            print "\nThat doesn't look like a valid URL\n\n"
            continue

        idx1 = answer.find("/")
        ## Find the 10-character-long product ID
        while idx1 > 0:
            idx2 = answer.find("/", idx1 + 1)
            if idx2 < 0:
               print "\nThis shouldn't happen.  Maybe your URL isn't an Amazon product?\n\n"
               continue
            if (idx2 - (idx1+1)) == 10:
               product = answer[idx1+1:idx2]
               break
            idx1 = idx2

        if answer.find("used") == -1:   ## If the URL wasn't for a used item
            URL = "http://www.amazon.com/gp/offer-listing/" + product \
                              + "/ref=dp_olp_new?ie=UTF8&condition=new"
        else:
            URL = "http://www.amazon.com/gp/offer-listing/" + product \
                              + "/ref=dp_olp_used?ie=UTF8&condition=used"
            
        watch_list.append(("", URL))
        
    return (username, password, watch_list)



    # ## # ## # ## # ##
    #
    #   We grab Gmail credentials and some Amazon URLs
    #   then get to business, sending notifications on changes.
    #
    # ## # ## # ## # ##
def main():
    username, password, watch_list = get_info()
    
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
      
    for idx, item in enumerate(watch_list):
        watch_list[idx] = (grab_junk(item[1], opener), item[1])
        print (strftime("%H:%M -", localtime())), \
                       "Found", watch_list[idx][0], "at:\n", item[1], "\n"
        sleep(3)
   
    while True:
        for idx, item in enumerate(watch_list):
            temp = grab_junk(item[1], opener)
            
            if temp != item[0]:
                try:
                    float(str(temp))
                    diff = float(str(item[0])) - float(str(temp))
                    if (diff > 0) & (diff > .05):
                        send_email(username, password, temp, item[0], item[1])
                except ValueError:
                    send_email(username, password, temp, item[0], item[1])
                print (strftime("%H:%M -", localtime())), \
                                     "Changed from", item[0], "to", temp, "\n"
            else:
                print (strftime("%H:%M -", localtime())), \
                                     "Still: ", item[0], "\n"
                    
            watch_list[idx] = (temp, item[1])
            skew = 87
            sleep(110 + skew)
      
      
      

if __name__ == '__main__':
   main()
