import urllib2
from time import sleep, localtime
from datetime import date, timedelta
from BeautifulSoup import BeautifulSoup
from random import randrange
#from random import shuffle
from win32com import client


to = ["me@gmail.com"]

#####################################
#
#  Sends email
#
#####################################
def SendMail(subj, msg):
    rcpts = ''
    olMailItem = 0x0
    obj = client.Dispatch("Outlook.Application")
    newMail = obj.CreateItem(olMailItem)
    newMail.Subject = subj
    newMail.Body = msg
    
    for ppl in to:
        rcpts += ppl + ";"
    newMail.To = rcpts
    print "\nSending:  " + newMail.Subject + "\n" + msg
    newMail.Send()


#####################################
#
#  Processes a webpage, finding gift card values
#
#####################################
def grab_junk(URL, opener, avg, discount):
   ## Grab the page
   try:
      page = opener.open(URL)
   except urllib2.URLError, e:
      print "\nReceived error:"
      print e
      sleep(240)
      return
      
   ## Grab relevant blocks
   content = page.read()
   soup = BeautifulSoup(content)
   
   html_blocks = soup.findAll('tr', attrs = {'class' : 'toggle-details'})

   count = 0
   card_list = []
   for block in html_blocks:
      temp = block.findAll('td', attrs = {'class' : 'right'})
      
      price = str(temp[0])
      price = float(price[price.find("$")+1:price[1:].find("<")+1])

      prcnt = str(temp[1])
      prcnt = float(prcnt[prcnt.find(">")+1:prcnt.find("%")])

      card_list.append((price, prcnt))
      
      count += 1
      if count > 8:
         break

   avg_prcnt = 0
   interesting = False
   # Check each card for interesting discount
   for card in card_list:
      #print card[0], "%.02f" % (card[0] * (100-card[1])/100)
      avg_prcnt += card[1]
      if card[1] > discount:
         interesting = True
         print URL
         print URL
         print "Looks good..."

    # See if discount level in general is getting interesting
   avg_prcnt /= len(card_list)
   if avg_prcnt >= avg:
      interesting = True
      
   return interesting, card_list

   
   
#####################################
#
#  Logic that sends an email if criteria met, also records information
#
#####################################
def watch(URL, opener, average, disc, end):
    interesting = False
    cards = []
    # Grab card info
    try:
        (interesting, cards) = grab_junk(URL, opener, average, disc)
    except:
        print "Card Read Error", end
        sleep(60*4)
        return

    #Send email if there's anything interesting
    if interesting:
        body = URL + '\n'
        print "Sending " + body
        for card in cards:
            body += str(card) + '\n'
        SendMail("Check " + end + " Cards", body)

    # Gather and Format Info
    high = [0,0]
    avg = []
    for c in cards:
        if c[1] >= high[1]:
            if c[0] > high[0]:
                high = c
        avg.append(c[0])
    avg = "%.2f" % float(sum(avg)/len(avg))
    time = "%d:%02d" % (localtime().tm_hour, localtime().tm_min)

    # Record information found
    print "%s\tAvg:%s\tHighest Disc: (%.2f, %.2f)" % (end, avg, high[0], high[1])
    try: 
        f = open("raise_records_" + end + ".txt", 'a')
    except IOError: 
        pass
    if high[1] > disc*0.95:
        uno = disc / 5
        dos = disc / 4
        temp = "\t%s\t%s\t(%.2f, %.1f) " % (time, avg, high[0], high[1])
        for x in range(0, int(high[1]) - disc):
            if x < uno:
                temp += '-'
            elif x < dos:
                temp += '+'
            else:
                temp += 'x'
        temp += '\n'
    else:
        temp = "\t%s\t%s\t(%.2f, %.1f)\n" % (time, avg, high[0], high[1])
    f.write(temp)
    f.close()



#####################################
#
#  Watches for gift cards at specified URLs, sending email if specified criterea are met
#
#####################################
def main():
    URLs = ["https://www.raise.com/buy-t-j-maxx-gift-cards"]#,
            #"https://www.raise.com/buy-home-depot-in-store-only-gift-cards",
            #"https://www.raise.com/buy-autozone-gift-cards",
            #"https://www.raise.com/buy-macaroni-grill-gift-cards",
            #"https://www.raise.com/buy-cirque-du-soleil-gift-cards",
            #"https://www.raise.com/buy-advance-auto-parts-gift-cards",
            #"https://www.raise.com/buy-lowe-s-in-store-only-gift-cards",
            #"https://www.raise.com/buy-hancock-fabrics-gift-cards",
            #"https://www.raise.com/buy-chick-fil-a-gift-cards",
            #"https://www.raise.com/buy-gordmans-gift-cards"]
    avgs = [21]#, # tjmaxx
            #45, # hd
            #45, # autozone
            #45, # macgrill
            #45, # cirque
            #45, # advance
            #45, # lowes
            #45, # hancock
            #23, # cfila
            #45] # gordmans
    discs = [22]#, # tjmaxx
            #45, # hd
            #45, # autozone
            #45, # macgrill
            #45, # cirque
            #45, # advance
            #15, # lowes
            #45, # hancock
            #20, # cfila
            #45] # gordmans
    ends = ["tjmaxx"]#,
           #"hd",
           #"autozone",
           #"macgrill",
           #"cirque",
           #"advance",
           #"lowes",
           #"hancock",
           #"cfila",
           #"gordmans"]
    daily_trigger = [False]#, # tjmaxx
                     #False, # hd
                     #False, # autozone
                     #False, # macgrill
                     #False, # cirque
                     #False, # advance
                     #False, # lowes
                     #False, # hancock
                     #False, # cfila
                     #False] # gordmans

    indices = []
    for idx in range(0,len(URLs)):
        indices.append(idx)
    
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]

    while True:
        #shuffle(indices)
        for idx in indices:
            # Record date as necessary
            if daily_trigger[idx] and localtime().tm_hour == 0:
                # 'Writing info to file...\n'
                try: 
                    f = open("raise_records_" + ends[idx] + ".txt", 'a')
                except IOError: 
                    pass
                day = date.today() # - timedelta(days=1)
                f.write(str(day)+'\n')
                f.close()

                daily_trigger[idx] = False
            elif localtime().tm_hour > 5:
                daily_trigger[idx] = True

            # Call watch() function
            watch(URLs[idx], opener, avgs[idx], discs[idx], ends[idx])
                    
            # Sleep
            skew = randrange(60*2, 60*6)
            sleep(60*1 + skew)


      
if __name__ == '__main__':
   main()
