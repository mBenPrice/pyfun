
def pass_gen():
  import random
  import math
   
  while(1):
      print("\nAn easy-to-remember password is also easy to guess, but a phrase-based "
            "\npassword is fairly easy to remember while very difficult to crack.\n"
            "Enter a phrase with at least seven words.")
      typed_phrase = ' '.join(input().split())
      lower_phrase = typed_phrase.lower()
      phrase = lower_phrase.split()

      letters = ""
      phrase_index = 0
      for word in phrase:
         if word == "january":
            if bool(random.randint(0, 1)):
               word = "1"
         if word == "february":
            if bool(random.randint(0, 1)):
               word = "2"
         if word == "march":
            if bool(random.randint(0, 1)):
               word = "3"
         if word == "april":
            if bool(random.randint(0, 1)):
               word = "4"
         if word == "may":
            if bool(random.randint(0, 1)):
               word = "5"
         if word == "june":
            if bool(random.randint(0, 1)):
               word = "6"
         if word == "july":
            if bool(random.randint(0, 1)):
               word = "7"
         if word == "august":
            if bool(random.randint(0, 1)):
               word = "8"
         if word == "september":
            if bool(random.randint(0, 1)):
               word = "9"
         if word == "sunday":
            if bool(random.randint(0, 1)):
               word = "1"
         if word == "monday":
            if bool(random.randint(0, 1)):
               word = "2"
         if word == "tuesday":
            if bool(random.randint(0, 1)):
               word = "3"
         if word == "wednesday":
            if bool(random.randint(0, 1)):
               word = "4"
         if word == "thursday":
            if bool(random.randint(0, 1)):
               word = "5"
         if word == "friday":
            if bool(random.randint(0, 1)):
               word = "6"
         if word == "saturday":
            if bool(random.randint(0, 1)):
               word = "7"
               
         if word == "october":
            if bool(random.randint(0, 1)):
               word = "10"
               letters += word
         elif word == "november":
            if bool(random.randint(0, 1)):
               word = "11"
               letters += word
         elif word == "december":
            if bool(random.randint(0, 1)):
               word = "12"
               letters += word
         else:
            letters += word[0]
         

      if(len(letters) < 7):
         print("You failed to provide a sufficiently long phrase.\n\n")
         continue

      suggestion = (13 - len(letters))
      if suggestion < 2:
        suggestion = 2
      print("\nEnter a number sequence with at least %d digits." % suggestion )
      entered_nums = input()

      pie = 8
      numbers = ""
      for num in entered_nums:
         try:
            pie += int(num)
            numbers += num
         except ValueError:
            pie = 0

      while(1):
        nums = 0
        lets = 1
        string_index = 0
        new_string = letters[0]
        li = 0
        ni = 0
        straight_count = 0
        upnum = 0
        uplet = 0
        
        while( (nums + 1 <= len(numbers)) | (lets + 1 <= len(letters)) ):
          fairness = len(letters) - len(numbers) + nums - lets
          antifair = -fairness
          string_index += 1
          if bool(random.randint(0, 1)):
            if fairness < 0:     # there are more numbers
               if random.randint(0, antifair):
                 if nums + 1 <= len(numbers):  # give numbers a better chance
                   new_string += numbers[nums]
                   nums += 1
            else:
               if random.randint(0, 1):
                 if nums + 1 <= len(numbers):
                   new_string += numbers[nums]
                   nums += 1
          else:
            if fairness > 0:     # there are more letters
               if random.randint(0, fairness):
                 if lets + 1 <= len(letters):  # give letters a better chance
                   new_string += letters[lets]
                   lets += 1
            else:
               if random.randint(0, 1):
                 if lets + 1 <= len(letters):
                   new_string += letters[lets]
                   lets += 1

        
        while li < len(letters):
          si = 0
          while si < len(new_string):
            if(letters[li] == new_string[si]):
               while(li + 2 <= len(letters)) & (si + 2 <= len(new_string)):
                 if (letters[li+1] != new_string[si+1]):
                   break
                 straight_count += 1
                 li += 1
                 si += 1
            si += 1
          li += 1
          
        while ni < len(numbers):
          si = 0
          while si < len(new_string):
            if(numbers[ni] == new_string[si]):
               while(ni + 2 <= len(numbers)) & (si + 2 <= len(new_string)):
                 if(numbers[ni+1] != new_string[si+1]):
                   break
                 straight_count += 1
                 ni += 1
                 si += 1
            si += 1
          ni += 1


        final_string = ""
        for c in new_string:
          if random.randint(0, 1) == 0:
             try:
                lower_phrase = int(c)
                upnum += 1
                if lower_phrase == 0:
                   final_string += ")"
                if lower_phrase == 1:
                   final_string += "!"
                if lower_phrase == 2:
                   final_string += "@"
                if lower_phrase == 3:
                   final_string += "#"
                if lower_phrase == 4:
                   final_string += "$"
                if lower_phrase == 5:
                   final_string += "%"
                if lower_phrase == 6:
                   final_string += "^"
                if lower_phrase == 7:
                   final_string += "&"
                if lower_phrase == 8:
                   final_string += "*"
                if lower_phrase == 9:
                   final_string += "("
             except ValueError:
                uplet += 1
                final_string += c.upper()
          else:
             final_string += c

        if(upnum + uplet) == 0:
           continue
          
        floatval = float(len(final_string) / (upnum + uplet))
        if( floatval > 2.5 ) | (floatval < 1.54 ) | (upnum == 0):
           continue

        straight_count = math.fabs(straight_count - math.fabs(len(letters) - len(numbers)))
        if straight_count < 2:
           break

      
      print("\nYour typed phrase and number sequence are:\n%s\n%s\nThey were turned into "
            "%s and %s, then intermingled and " % (typed_phrase,entered_nums,letters,numbers) )
      
      print("manipulated to generate your highly secure password "
            "suggestion:\n\t\t\t%s \n" %  (final_string))

      again = input("If you are satisfied with your password, type \'exit\' to leave.\n").lower()
      if again.find("exit") == 0:
        break
      else:
        print("\n")

pass_gen()
