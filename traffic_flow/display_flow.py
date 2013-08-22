import matplotlib.pyplot as plt

def see_flow():
    import glob
    import numpy as np

    files = glob.glob('*_to_*')

    while True:
       count = 0
       
       print("Recorded traffic flow files:")
       for idx, line in enumerate(files):
          print("%d.  %s" % (idx, line))
          count += 1

       flow = raw_input("Choose a file number to view:  ")

       try:
           flow = int(flow)
           if flow <= count:
              break
       except ValueError:
           print("Try again.\n\n")

    data = np.genfromtxt(files[flow], dtype=None, names=True)

    days = []
    for row in data:
        if row["Day"] not in days:
            days.append(row["Day"])


    while True:
        print "Data from the following days are available:"
        for idx, day in enumerate(days):
            print "\t%d.  %s" % (idx, day)
    
        answer = raw_input("Enter the number of the day you'd like data for:  ")

        if (len(answer) == 1):
            try:
                answer = int(answer)
                weekday = days[answer]
                break
            except ValueError:
                print "\nNot a valid selection.\n\n"
        else:
            print "\nNot a valid selection.\n\n"

    print "Displaying data for", weekday

    subset = []
    for row in data:
        if row["Day"] == weekday:
            temp = row.tolist()
            subset.append((temp[1], temp[2], temp[3], temp[4], temp[5]))

    subset.sort()
    
    x = []
    y = []
    for row in subset:
        x.append(row[0] + row[1]/float(60) + row[2]/float(60*60) + row[3]/float(60*60*1000))
        y.append(row[4])


    plt.plot(x, y)
    plt.title("Traffic Flow by Hour")
    plt.show()
    

    


















see_flow()
