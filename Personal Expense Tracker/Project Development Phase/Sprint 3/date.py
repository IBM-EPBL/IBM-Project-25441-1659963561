from datetime import date
  
todays_date = date.today()

dates = [
    "2022-11-19",
    "2021-03-02",
    "2022-06-17",
    "2022-11-16",
    "2023-08-09",
]

year_count = 0
month_count = 0

for date in dates:
    if date[:4] == str(todays_date.year):
        year_count = year_count + 1
    if date[:4] == str(todays_date.year) and date[5:7] == str(todays_date.month):
        month_count += 1
    if date[:4] == str(todays_date.year) and date[5:7] == str(todays_date.month):
        if int(date[-2:])<8:
            print("week 1")
        elif int(date[-2:])<16:
            print("week 2")
        elif int(date[-2:])<24:
            print("week 3")
        elif int(date[-2:])<32:
            print("week 4")
    
print(year_count)
print(month_count)

