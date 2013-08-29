pyfun
=====
This repo was created to hold various Python scripts I'm working on after a friend said he wanted to contribute.
As of the beginning of August, I'm somewhat new to writing in Python, so feel free to offer suggestions on my
style if you feel it is lacking.  Also, please note that I don't really expect anybody else to use these so they
may have customizations specific to me which you could easily change.  
For reference, I primarily use Python 2.7.
Amazon Watch
=====
Enter Amazon product URLs that you are interested in.  Currently, it checks one product every 2-3 minutes.  
By default, it will track the lowest new item price with shipping on the New Items page.
If supplied a URL to used listings, it will track Amazon Warehous Deal inventory.  
When a noteworthy change is made, an email notification is sent.  A price reduction of 5 cents is not noteworthy.

To Do List
* With used listing, offer to watch new prices also.
* When Amazon says, "Add to cart to see product details," go to main page and grab the price from there.

Phrase-based Password
=====
My first script which takes a phrase and a number then generates a secure password.

Random URLs
=====
The wifi at UIUC will slow downloads significantly unless your computer is also making http requests, so I gathered 
the top websites into a list for this script to randomly load pages every five seconds.

Traffic Flow
=====
Polls current traffic info between two points from Gmaps so that you can plan your commute accordingly.  The user may 
specify a route and a time to start polling.
The display_flow.py script will show a graph of travel times if you get the right modules installed.

To Do List
* Add scheduling functionality to take input such as: '6-9 mon-fri'
* Possibly add an end time, as a stepping stone to the above functionality.
* Potentially reverse a route to work around 1:30 p.m. or offer an afternoon return route if a morning 6-9 a.m. route is scheduled.
* Somehow smooth data points in the graph so it isn't so jumpy (digital samping to analog).
* Best:  Notify is route is busier than usual.
