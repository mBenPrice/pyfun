import time, os, urllib2, sched, re
from datetime import datetime as dt
from time import sleep, localtime, strftime
from bs4 import BeautifulSoup
from random import randrange


   # ## # ## # ## # ## #
   #
   #  Define Route will offer previous locations to choose from if they exist
   #  and ultimately a starting and ending location will be chosen.
   #
   #  An interval for polling will also be chosen.
   #
   #  Return:  start, end, interval
   #
   # ## # ## # ## # ## #
def define_route():      
   polling = [999, 730, 595, 475, 370, 280, 205, 145, 100, 70, 55]
   
   while True:
      count = 0
      options = []
      ## Attempt accessing previously saved locations
      try:
         f = open(os.path.abspath("flow_settings.txt"))
         past_searches = f.readlines()
         f.close()
         past_searches.reverse()

         for line in past_searches:
            if line.rstrip() not in options:
               options.append(line.rstrip())
               count += 1
               
            if count == 10:
               break
      except IOError:
         count = 0

      ## If any locations found, offer a list
      if count > 0:
         options.sort()
         print("Recent Locations:")
         for idx, line in enumerate(options):
            print("\t%d.  %s" % (idx, line))
         

         answer = raw_input("Specify your route (e.g. 2 to b) or enter a starting location:  ")

         if (len(answer) < 2):
            print("\nYou'll need at least two characters.\n\n")
            continue

         number = re.sub("\D", "", answer)
         if (len(number) == 2) & (len(answer) <= 7):
            if (int(number[0]) < count ) & (int(number[1]) < count ):
               start = options[int(number[0])]
               end = options[int(number[1])]
            else:
               print("\nTry again.\n\n")
               continue                  
         else:
            start = answer
            end = raw_input("Destination:  ")
            if( len(end) == 1 ):
               if(int(end) < count ):
                  end = options[int(end)]

      ## Else, ask for starting and ending locations
      else:
         start = raw_input("Starting location:  ")
         end = raw_input("Destination:  ")

      while True:   
         answer = raw_input("\nHow quickly do you want to poll (scale of 1-10, slow-fast)?  ")
      
         try:
            interval = int(answer)
            if 1 <= interval <= 10:
               interval = polling[interval]            
               return (start, end, interval)
            else:
               print("\nTry again\n\n")
         except ValueError:
            print("\nTry again\n\n")


   # ## # ## # ## # ## #
   #
   #  Routes will be offered from the requested starting and ending locations.
   #
   #  Return:  desired route, if chosen
   #
   # ## # ## # ## # ## #
def specify_route(start, end, url):
   content = url.read()
   soup = BeautifulSoup(content)
   
   html_blocks = str(soup.findAll('li', attrs = {'class' : 'dir-altroute'}))
   
   travel_options = []
   idx = html_blocks.find("</div> <div>")
   while(idx != -1):
      endx = html_blocks.find("</div>", idx + 10)
      route = html_blocks[idx+12:endx]
      travel_options.append(route)
      idx = html_blocks.find("</div> <div>", idx + 1)
      
   if len(travel_options) <= 1:
      return
   
   while True:
      print("\nThe following routes between your locations are available:")
      routes = 0
      for road in travel_options:
         print("\t%d.  %s" % (routes+1, road))
         routes += 1
      
      print("\t%d.  Any, whichever is fastest at the moment." % (routes+1))
      
      answer = raw_input("Please specify your preference:  ")

      try:
         answer = int(answer)
         if answer <= routes + 1:
            if answer <= routes:
               return travel_options[answer-1]
            else:
               return "not specified"
                  
            print "\nTravel times along", route, "will be recorded."
            break
         else:
            print("\nTry again.\n")
      except ValueError:
         print "\n"
         return


   # ## # ## # ## # ## #
   #
   #  Wait Maybe provides the option for the program to sleep
   #  until a specified time.  
   #
   #  Return:  none
   #
   # ## # ## # ## # ## #
def wait_maybe():
      print("\n\nYou may schedule polling to start at a specific hour, in military time.")
      print("\n\tFor example:  2:15 p.m. = 14:15, midnight = 0, 6 a.m. = 6\n")
      wait_time = raw_input("To enable a delay, enter a starting time.  ")
      
      if (len(wait_time) == 0):
         return
		 
      ## Convert times
      colon = wait_time.find(":")
      if colon != -1:
         minutes = wait_time[colon+1:]
         wait_time = wait_time[:colon]
               
         waitmin = int(re.sub("\D", "", minutes))
               
         if (0 > waitmin) | (waitmin > 60):
            waitmin = 9999
         
      waithour = re.sub("\D", "", wait_time)
      waithour = int(waithour)


      ## With a valid starting time, wait
      if 0 <= waithour < 24:
         print("\nScheduling Enabled")
         while True:
            if dt.now().hour is waithour:
               if waitmin < 60:
                  if dt.now().minute >= waitmin:
                     break
                  else:
                     print("\tSleeping...")
                     sleep(60)
               else:
                  break
            else:
               print("\tSleeping...")
               sleep(180)


   # ## # ## # ## # ## #
   #
   #  Wait Maybe provides the option for the program to sleep
   #  until a specified time.  
   #
   #  Return:  none
   #
   # ## # ## # ## # ## #
def book_keeping(settings, timings, start, end):
   try:
      with open(timings): pass
   except IOError:
      ## If this specific route doesn't already exist, set column names
      with open(timings, "a") as myfile:
         myfile.write("# Day Hour Minute Second Millisecond Travel\n")

   temp_start = re.sub("\s+"," ",start.replace(","," "))
   temp_end = re.sub("\s+"," ",end.replace(","," "))
   
   with open(settings,'r') as f:
      locations = f.read().splitlines()
   
   output = []
   for places in locations:
      if places != temp_start:
         if places != temp_end:
            output.append(places + "\n")
        
   output.append(temp_start + "\n")
   output.append(temp_end + "\n")
   
   transfer = output[-10:]
   
   with open(settings,'w') as f:
      f.writelines(transfer)


   # ## # ## # ## # ## #
   #
   #  Simply makes a usable URL
   #
   #  Return:  URL
   #
   # ## # ## # ## # ## #
def format_url(start, end):
      url_start = ""
      url_end = ""
      
      temp = start
      for n in temp:
         if n == " ":
            url_start += "+"
         elif n == "/":
            url_start += "%2F"
         else:
            url_start += n

      temp = end
      for n in temp:
         if n == " ":
            url_end += "+"
         elif n == "/":
            url_end += "%2F"
         else:
            url_end += n
      
      URL = "https://www.google.com/maps?saddr=" + url_start + "&daddr=" + url_end
      
      return URL


def find_flow(start, end, route, URL, interval, timings):
      ## Grab new page
      route = str(route)
      try:
         page = urllib2.urlopen(URL)
      except urllib2.URLError, e:
         print "\nReceived error:"
         print e
         print "But continuing on in about 5 minutes...\n"
         skew = randrange(120)
         sleep(240 + skew)
         return
         
      content = page.read()

      ## Grab relevant sections
      soup = BeautifulSoup(content)
      html_blocks = soup.findAll('li', attrs = {'class' : 'dir-altroute'})
      
      routes = []

      calc_times = []
      est_times = []
      for item in html_blocks:
         sub_block = str(item)
         idx = sub_block.find(route)
         ## If a route is specified, then only grab times if this is that route
         if ((route == "not specified") | ((idx is not -1) & (sub_block[idx + len(route)] == "<"))):
            ## First search for the theoretical travel times
            idx = sub_block.find("mi</span>, <span>")
            mins = 0
            temp1 = sub_block[idx:]
            temp2 = temp1[17:min(len(temp1) + 17, 17+16)]
            h_idx = temp2.find("hours")
            if h_idx != -1:
               mins = 60 * int(temp2[:2])

            m_idx = temp2.find("mins")
            if m_idx != -1:
               try:
                  mins += int(temp2[m_idx-3:m_idx])
               except ValueError:
                  mins += int(temp2[m_idx-2:m_idx])
                         
            calc_times.append(mins)
            
            ## Next look for travel times in current traffic
            idx = sub_block.find("fic:")
            mins = 0
            temp1 = sub_block[idx + 5:]
            temp2 = temp1[:min(len(temp1), 17)]
            h_idx = temp2.find("hours")
            if h_idx != -1:
               mins = 60 * int(temp2[:2])

            m_idx = temp2.find("mins")
            if m_idx != -1:
               mins += int(temp2[m_idx-3:m_idx])
                         
            est_times.append(mins)


      ## Time of interest is maximum of the minimum of each
      if (len(est_times) > 0) & (len(calc_times) > 0):
         travel_time = max(min(calc_times), min(est_times))
      elif(len(est_times) > 0):
         travel_time = min(est_times)
      elif(len(calc_times) > 0):
         travel_time = min(calc_times)
      else:
         print "Something went wrong when grabbing times"
         print "This usually happens when GMaps \"can't\" find a route,"
         print "so you may want to abort this traffic analysis.\n"
         sleep(5)
         return


      if travel_time < 60:
         print("At %s:  %d minutes" % (strftime("%H:%M %S", localtime()), travel_time))
      else:
         minutes = travel_time % 60
         hours = int(travel_time / 60)
         print("At %s:  %d hours %d minutes" % (strftime("%H:%M %S", localtime()), hours, minutes))

      with open(timings, "a") as myfile:
         millis = ((dt.now()).microsecond)/1000
         myfile.write("%s %d %d\n" % (strftime("%a %H %M %S", localtime()), millis, travel_time))

      ## To hopefully keep Google from booting us
      skew = randrange(35)
      sleep(interval + skew)


   # ## # ## # ## # ## #
   #
   #  Polls travel time in current traffic between two points, 
   #  potentially on a specified route.  
   #
   #  The script will optionally wait until a specified time so as 
   #  not to upset Google's servers.
   #
   # ## # ## # ## # ## #
def main():

   ## Loop until a page is successfully loaded
   while True:
      start, end, interval  = define_route()
      
      URL = format_url(start, end)
      
      try:
         url = urllib2.urlopen(URL)
         route = specify_route(start, end, url)
         break
      except urllib2.URLError, e:
         print e
         print "The URL did not load properly.  Please enter your locations again.\n\n"
         continue
   ## End loop
      
   settings = os.path.abspath("flow_settings.txt")
   if (route == "not specified"):
      timings = os.path.abspath(start[0:6] + "_to_" + end[0:6] + "_flow.txt")
   else:
      timings = os.path.abspath(start[0:6] + "_to_" + end[0:6] + "_thru_" + route[0:6] + "_flow.txt")
   
   wait_maybe()
   print "\n"

   book_keeping(settings, timings, start, end)
   
   ## Read travel time at ~interval until program is closed
   while(True):
      find_flow(start, end, route, URL, interval, timings)


if __name__ == '__main__':
   main()
