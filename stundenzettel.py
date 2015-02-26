# -*- coding: utf-8 -*-

#The MIT License (MIT)
#
#Copyright (c) <2015> <Patrick Spengler>
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

import random
import calendar
import collections
import datetime
import math


def getInt(inputstr,errorstr,low,high):
    while True:
        try:
            tmpInput = int(raw_input(inputstr))    
        except ValueError:
            print(errorstr)
            continue
        if tmpInput >= low and tmpInput <= high:
            break
        else:
            print(errorstr)

    return tmpInput

# returns the name of the month
def getMonth(month):
    if month == 1: return "Januar"
    elif month == 2: return "Februar"
    elif month == 3: return r"M\"arz"
    elif month == 4: return "April"
    elif month == 5: return "Mai"
    elif month == 6: return "Juni"
    elif month == 7: return "Juli"
    elif month == 8: return "August"
    elif month == 9: return "September"
    elif month == 10: return "Oktober"
    elif month == 11: return "November"
    elif month == 12: return "Dezember"

# returns the date of eastern sunday
def eastern_greg(year):
    a = year%19
    b,c = divmod(year,100)
    d,e = divmod(b,4)
    f = (b+8)//25
    g = (b-f+1)//3
    h = (19*a+b-d-g+15)%30
    i,j = divmod(c,4)
    k = (32+2*e+2*i-h-j)%7
    l = (a+11*h+22*k)//451
    x = h+k-7*l+114
    mon,day = divmod(x,31)
    
    return datetime.date(year,mon,day+1)

def isHolyday(date):


    eastern_sun = eastern_greg(date.year)
    eastern_fri = eastern_sun - datetime.timedelta(2) 
    eastern_mon = eastern_sun + datetime.timedelta(1) 
    himmelfahrt = eastern_sun + datetime.timedelta(39)
    pfingstmon = eastern_sun + datetime.timedelta(50)
    fronleichnam = eastern_sun + datetime.timedelta(60)
    holyday = []
    holyday.append(datetime.date(date.year,1,1))
    holyday.append(datetime.date(date.year,1,6))
    holyday.append(eastern_fri)
    holyday.append(eastern_mon)
    holyday.append(datetime.date(date.year,5,1))
    holyday.append(himmelfahrt)
    holyday.append(pfingstmon)
    holyday.append(fronleichnam)
    holyday.append(datetime.date(date.year,10,3))
    holyday.append(datetime.date(date.year,11,1))
    holyday.append(datetime.date(date.year,12,24))
    holyday.append(datetime.date(date.year,12,25))
    holyday.append(datetime.date(date.year,12,26))
    holyday.append(datetime.date(date.year,12,31))


    return date in holyday
    

def buildHoursList(date, workHours):

    HoursTimeDay = collections.namedtuple("Hours",("day","time","hours"))

    high = int(math.ceil(workHours / 6 + 2))
    
    maxday = calendar.monthrange(date.year,date.month)[1]
    daylist = list(range(1,maxday+1))
    hoursList = []
    while workHours > 0:
        dayIndex = random.randrange(1,len(daylist))
        day = daylist.pop(dayIndex)
        weekday = calendar.weekday(date.year, date.month, day)
        if weekday < 5 and not isHolyday(datetime.date(date.year, date.month, day)):
            dayHours = random.randrange(1,high)
            if dayHours > workHours:
                dayHours = workHours
            timeStart = random.randrange(8, 19 - dayHours)
            timeEnd = timeStart + dayHours
            workHours = workHours - dayHours
            h = HoursTimeDay(day,str(timeStart)+r":00 - "+str(timeEnd)+r":00",dayHours)
            hoursList.append(h)
    hoursList.sort()
    return hoursList

def vaccationTime(hours):

    vacDay = math.ceil(hours - (hours * 0.929))
    return vacDay

def build(name, supervisor, project, work, date, hours):
    
    vacHours = int(vaccationTime(hours))
    workHours = hours - vacHours
    hoursList = buildHoursList(date, workHours)
    maxday = calendar.monthrange(date.year,date.month)[1]
    
    f = open("stundenzettel.tex","a")
    f.write(r"\begin{table}[ht]"+"\n")
    f.write(r"\begin{tabularx}{\textwidth}{|l|X|l|X|}"+"\n")
    f.write(r"\hline"+"\n")
    f.write(r"Monat & "+getMonth(date.month)+r" & & Betreuer: " + supervisor
            + r" \\" + "\n")
    f.write(r"\hline"+"\n")
    f.write(r"Name des Hiwis & "+name+r" & &\\"+"\n")
    f.write(r"\hline"+"\n")
    f.write(r"h/m & " +str(workHours)+ r"& & Projekt: "+project+r" \\"+"\n")
    f.write(r"\hline"+"\n")
    f.write(r"von & "+date.strftime("%d.%m.%Y")+r" & & \\"+"\n")
    f.write(r"\hline"+"\n")
    date = date.replace(day = maxday)
    f.write(r"bis & "+date.strftime("%d.%m.%Y")+r" & & \\"+"\n")
    f.write(r"\hline"+"\n")
    f.write(r"& & & \\"+"\n")
    f.write(r"\hline"+"\n")
    f.write(r"Urlaub-h & " + str(vacHours) + r" & & \\"+"\n")
    f.write(r"\hline"+"\n")
    f.write(r"Tag: & Uhrzeit von-bis: & Std.: & " + r"T\"atigkeit:"
            + r" Stichwort oder Beschreibung\\"+"\n")
    f.write(r"\hline"+"\n")
    d = 1
    while d < maxday + 1:
        if len(hoursList) > 0:
            if hoursList[0].day == d:
                f.write(str(d)+r" & "+ hoursList[0].time + r" & "
                        + str(hoursList[0].hours) + r" & " + work + r" \\" + "\n")
                hoursList.pop(0)
            else:
                f.write(str(d) + r" & & & \\" + "\n")
        else:
            f.write(str(d) + r" & & & \\" + "\n")
        f.write(r"\hline" + "\n")
        d = d + 1
    while d < 32:
        f.write(r" & & & \\" + "\n")
        f.write(r"\hline" + "\n")
        d = d + 1
    
    f.write(r" & Urlaub & " + str(vacHours) + r"& \\" + "\n")
    f.write(r"\hline" + "\n")
    f.write(r" & Arbeitsstunden & " + str(workHours) + r" & \\" + "\n")
    f.write(r"\hline" + "\n")
    f.write(r" & Konto lfd. Monat & " + str(hours) + r" & \\" + "\n")
    f.write(r"\hline" + "\n")
    f.write(r"\end{tabularx}" + "\n")
    f.write(r"\end{table}" + "\n")
    f.write(r"\vspace{4ex}" + "\n")
    f.write(r"{\Large Unterschrift:} \hspace{0.5cm} Betreuer:\hspace{0.5cm}\makebox[2in]"
            + r"{\hrulefill} \hspace{0.5cm} Student:\hspace{0.5cm}\makebox[2in]"
            + r"{\hrulefill}"+"\n")
    f.write(r"\newpage" + "\n")
    f.close()
    
def userinput():

    
    name = raw_input("Name(Hiwi)? ")
    project = raw_input("Projekt? ")
    work = raw_input("Tätigkeit? ")
    year1 = getInt("Jahr von ","Nur Zahlen von 1900-2100",1900,2100)

    year2 = getInt("Jahr bis ","Nur Zahlen von 1900-2100",1900,2100)
    month1 = getInt("Monat von ","Nur Zahlen von 1-12",1,12)
    month2 = getInt("Monat bis ","Nur Zahlen von 1-12",1,12)
    hours = getInt("Stundenzahl? ","Nur positive Zahlen",0,200)
    supervisor = raw_input("Betreuer? ")

    date1 = datetime.date(year1,month1,1)
    date2 = datetime.date(year2,month2,1)
    if date1 > date2:
        tmp = date2
        date2 = date1
        date1 = tmp
    
    f = open("stundenzettel.tex","w")
    f.close()
    f = open("stundenzettel.tex","a")
    f.write(r"\documentclass[11pt,a4paper]{article}"+"\n")
    f.write(r"\usepackage[ngerman]{babel}"+"\n")
    f.write(r"\usepackage[a4paper,margin=1cm,footskip=.5cm]{geometry}" + "\n")
    f.write(r"\usepackage{tabularx}" + "\n")
    f.write(r"\begin{document}"+"\n")
    f.write(r"\pagenumbering{gobble}"+"\n")
    f.close()
    
    while date1 <= date2:
        build(name, supervisor, project, work, date1, hours)
        m = date1.month + 1
        y = date1.year
        if m == 13:
            m = 1
            y = y + 1
        date1 = date1.replace(month = m, year = y)
        print(date1)
        
    f = open("stundenzettel.tex","a")
    f.write(r"\end{document}"+"\n")
    f.close()

userinput()

