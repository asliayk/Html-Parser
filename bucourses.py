
from bs4 import BeautifulSoup
from lxml import html
import requests
import sys
import time

argList=sys.argv
summer= False

# The start and finish dates of the program written to console.
startDate = argList[1]
finishDate = argList[2]

# The list of all department codes and their names based on 2019-Spring term in alphabetical order.
Departments = ["AD (MANAGEMENT)", "ASIA (ASIAN STUDIES)", "ASIA (ASIAN STUDIES WITH THESIS)", "ATA (ATATURK INSTITUTE FOR MODERN TURKISH HISTORY)", "AUTO (AUTOMOTIVE ENGINEERING)", 
"BIO (MOLECULAR BIOLOGY & GENETICS)", "BIS (BUSINESS INFORMATION SYSTEMS)", "BM (BIOMEDICAL ENGINEERING)", "CCS (CRITICAL AND CULTURAL STUDIES)", 
"CE (CIVIL ENGINEERING)", "CEM (CONSTRUCTION ENGINEERING AND MANAGEMENT)", "CET (COMPUTER EDUCATION & EDUCATIONAL TECHNOLOGY)",  "CET (EDUCATIONAL TECHNOLOGY)","CHE (CHEMICAL ENGINEERING)", 
"CHEM (CHEMISTRY)", "CMPE (COMPUTER ENGINEERING)", "COGS (COGNITIVE SCIENCE)", "CSE (COMPUTATIONAL SCIENCE & ENGINEERING)", "EC (ECONOMICS)", 
"ED (EDUCATIONAL SCIENCES)", "EE (ELECTRICAL & ELECTRONICS ENGINEERING)", "EF (ECONOMICS AND FINANCE)", "ENV (ENVIRONMENTAL SCIENCES)", "ENVT (ENVIRONMENTAL TECHNOLOGY)",
"EQE (EARTHQUAKE ENGINEERING", "ETM (ENGINEERING AND TECHNOLOGY MANAGEMENT)", "FE (FINANCIAL ENGINEERING)", "FLED (FOREIGN LANGUAGE EDUCATION)", 
"GED (GEODESY)", "GPH (GEOPHYSICS)", "GUID (GUIDANCE & PSYCHOLOGICAL COUNSELING)", "HIST (HISTORY)", "HUM (HUMANITIES COURSES COORDINATOR)", 
"IE (INDUSTRIAL ENGINEERING)", "INCT (INTERNATIONAL COMPETITION AND TRADE)", "INT (CONFERENCE INTERPRETING)",  "INTT (INTERNATIONAL TRADE)", "INTT (INTERNATIONAL TRADE MANAGEMENT)",
"LING (LINGUISTICS)", "LL (WESTERN LANGUAGES & LITERATURES)",  "LS (LEARNING SCIENCES)", "MATH (MATHEMATICS)", "ME (MECHANICAL ENGINEERING)", "MECA (MECHATRONICS ENGINEERING)",
"MIR (INTERNATIONAL RELATIONS:TURKEY,EUROPE AND THE MIDDLE EAST)", "MIR (INTERNATIONAL RELATIONS:TURKEY,EUROPE AND THE MIDDLE EAST WITH THESIS)",
"MIS (MANAGEMENT INFORMATION SYSTEMS)", "PA (FINE ARTS)", "PE (PHYSICAL EDUCATION)", "PHIL (PHILOSOPHY)", "PHYS (PHYSICS)", "POLS (POLITICAL SCIENCE&INTERNATIONAL RELATIONS)",
"PRED (PRIMARY EDUCATION)", "PSY (PSYCHOLOGY)", "SCED (MATHEMATICS AND SCIENCE EDUCATION)", "SCED (SECONDARY SCHOOL SCIENCE AND MATHEMATICS EDUCATION)",
"SCO(SYSTEMS & CONTROL ENGINEERING)", "SOC (SOCIOLOGY)", "SPL (SOCIAL POLICY WITH THESIS)", "SWE (SOFTWARE ENGINEERING)", "SWE (SOFTWARE ENGINEERING WITH THESIS)",
"TK (TURKISH COURSES COORDINATOR)", "TKL (TURKISH LANGUAGE & LITERATURE)", "TR (TRANSLATION AND INTERPRETING STUDIES)", "TRM (SUSTAINABLE TOURISM MANAGEMENT)",
"TRM (TOURISM ADMINISTRATION)", "WTR(TRANSLATION)",  "XMBA (EXECUTIVE MBA)",  "YADYOK (SCHOOL OF FOREIGN LANGUAGES)" ]  

# Common substring of all URLs needed.
head = "https://registration.boun.edu.tr/scripts/sch.asp?donem="
fall = False

# This function returns a list which contains the numbers of undergraduate and graduate lessons in a given lessons list.
def findUG(lessons):
    UGList = []
    U=0
    G=0
    for d in lessons:
        if not d[-3].isdigit():
            U+=1
        else:
            if d[-3]=="5" or d[-3]=="6" or d[-3]=="7":
                G+=1
            else:
                U+=1
    UGList.append(U)
    UGList.append(G)
    return UGList

# This function returns the sum of the elements of the given list.    
def listSum(list):
    sum=0
    for x in list:
        sum+=x
    return sum    
            
# This function returns the indexes of all elements which contain a spesific substring.    
def findIndex(list, substring):
    indexList = []
    for i, s in enumerate(list):
        if substring in s:
            indexList.append(i)
    return indexList

# This function returns the elements in a given list with spesific indexes which are in indexList.  
def findElements(indexList, list):
    findList = []
    for index in indexList:
        findList.append(list[index])
    return findList
     
# This function removes the given val. from the list.     
def removeValues(list, val):
   return [value for value in list if value != val]

# This if-else statements decides from which season the program starts taking data.
if startDate.find("Fall")!= -1:
 s=1
 w=1
 fall=True
elif startDate.find("Spring")!= -1:
 s=2
 w=2
else:
 s=3
 w=3

# This if-else statements decides at which season the program finishes taking data. 
if finishDate.find("Fall")!= -1:
 f=1
elif finishDate.find("Spring")!= -1:
 f=2
else:
 f=3
 summer = True

# Taking only the years from the entered arguments.
startYear=startDate[:4]
finishYear=finishDate[:4]

# List that keeps all terms with their String versions.
dates=[]
start=False

b = int(finishYear)
i = int(startYear)

# This while loop appends elements to the dates list by looking at the given date-ranges and adds the correct terms. 
while i<b+1:
    q=False
    if i==b:
         if w==1 and f==1:
           dates.append(str(i)+"-Fall") 
         elif w==2 and f==1:
           dates.append(str(i)+"-Spring")
           dates.append(str(i)+"-Summer")
           dates.append(str(i)+"-Fall")
         elif w==2 and f==2:
           dates.append(str(i)+"-Spring")
         elif w==2 and f==3:
           dates.append(str(i)+"-Spring")
           dates.append(str(i)+"-Summer")
         elif w==3 and f==1:
           dates.append(str(i)+"-Summer")
           dates.append(str(i)+"-Fall")
         elif w==3 and f==3:
           dates.append(str(i)+"-Summer")
           
    elif w==1 and i!=b and not q:
        dates.append(str(i)+"-Fall")
        w=2
        q = True
    elif w==2 and i!=b and not q:
        dates.append(str(i)+"-Spring")
        i-=1
        w=3
        q = True
    elif w==3 and i!=b and not q:
        dates.append(str(i)+"-Summer") 
        i-=1
        q = True
        w=1
    
    i+=1         
           
            
i = int(startYear)            

# Lists that keep all URLs of all terms in a given date range.
asiaStudies, asiaStudiesT, ata, auto, bm, bis, che, chem, ce, cogs, cse, ceet, cmpe, int, cem, ccs, eqe, ec, ef, ed, cet, ee, etm, env, envt, xmba, fe, pa, fled, ged, gph, guid, hist, hum, ie, inct, mir, mirT, intt, inttM, ls, ling, ad, mis, math, sced, me, meca, bio, phil, pe, phys, pols, pred, psy, yadyok, sceds, spl, soc, swe, sweT, trm, sco, ttrm, wtr, tr, tk, tkl, ll = ([] for k in range(69))

# List that stores lists of all departments above.
allDepartments = []

# While loop that adds all the URLs in a given date range and appends them to the corresponding department list.
while i<b+1: 
  a=False
  if not start and not fall:
   i-=1
   start=True
  x=i+1
  ad.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=AD&bolum=MANAGEMENT")
  asiaStudies.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=ASIA&bolum=ASIAN+STUDIES")
  asiaStudiesT.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=ASIA&bolum=ASIAN+STUDIES+WITH+THESIS")
  ata.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=ATA&bolum=ATATURK+INSTITUTE+FOR+MODERN+TURKISH+HISTORY")
  auto.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=AUTO&bolum=AUTOMOTIVE+ENGINEERING")
  bio.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=BIO&bolum=MOLECULAR+BIOLOGY+%26+GENETICS")
  bis.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=BIS&bolum=BUSINESS+INFORMATION+SYSTEMS")
  bm.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=BM&bolum=BIOMEDICAL+ENGINEERING")
  ccs.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=CCS&bolum=CRITICAL+AND+CULTURAL+STUDIES")
  ce.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=CE&bolum=CIVIL+ENGINEERING")
  cem.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=CEM&bolum=CONSTRUCTION+ENGINEERING+AND+MANAGEMENT")
  ceet.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=CET&bolum=COMPUTER+EDUCATION+%26+EDUCATIONAL+TECHNOLOGY")
  cet.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=CET&bolum=EDUCATIONAL+TECHNOLOGY")
  che.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=CHE&bolum=CHEMICAL+ENGINEERING")
  chem.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=CHEM&bolum=CHEMISTRY")
  cmpe.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=CMPE&bolum=COMPUTER+ENGINEERING")
  cogs.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=COGS&bolum=COGNITIVE+SCIENCE")
  cse.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=CSE&bolum=COMPUTATIONAL+SCIENCE+%26+ENGINEERING")
  ec.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=EC&bolum=ECONOMICS")
  ed.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=ED&bolum=EDUCATIONAL+SCIENCES")
  ee.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=EE&bolum=ELECTRICAL+%26+ELECTRONICS+ENGINEERING")
  ef.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=EF&bolum=ECONOMICS+AND+FINANCE")
  env.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=ENV&bolum=ENVIRONMENTAL+SCIENCES")
  envt.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=ENVT&bolum=ENVIRONMENTAL+TECHNOLOGY")
  eqe.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=EQE&bolum=EARTHQUAKE+ENGINEERING")
  etm.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=ETM&bolum=ENGINEERING+AND+TECHNOLOGY+MANAGEMENT")
  fe.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=FE&bolum=FINANCIAL+ENGINEERING")
  fled.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=FLED&bolum=FOREIGN+LANGUAGE+EDUCATION")
  ged.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=GED&bolum=GEODESY")
  gph.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=GPH&bolum=GEOPHYSICS")
  guid.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=GUID&bolum=GUIDANCE+%26+PSYCHOLOGICAL+COUNSELING")
  hist.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=HIST&bolum=HISTORY")
  hum.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=HUM&bolum=HUMANITIES+COURSES+COORDINATOR")
  ie.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=IE&bolum=INDUSTRIAL+ENGINEERING")
  inct.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=INCT&bolum=INTERNATIONAL+COMPETITION+AND+TRADE")
  int.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=INT&bolum=CONFERENCE+INTERPRETING")
  intt.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=INTT&bolum=INTERNATIONAL+TRADE")
  inttM.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=INTT&bolum=INTERNATIONAL+TRADE+MANAGEMENT")
  ling.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=LING&bolum=LINGUISTICS")
  ll.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=LL&bolum=WESTERN+LANGUAGES+%26+LITERATURES")
  ls.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=LS&bolum=LEARNING+SCIENCES")
  math.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=MATH&bolum=MATHEMATICS")
  me.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=ME&bolum=MECHANICAL+ENGINEERING")
  meca.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=MECA&bolum=MECHATRONICS+ENGINEERING")
  mir.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=MIR&bolum=INTERNATIONAL+RELATIONS%3aTURKEY%2cEUROPE+AND+THE+MIDDLE+EAST")
  mirT.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=MIR&bolum=INTERNATIONAL+RELATIONS%3aTURKEY%2cEUROPE+AND+THE+MIDDLE+EAST+WITH+THESIS")
  mis.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=MIS&bolum=MANAGEMENT+INFORMATION+SYSTEMS")
  pa.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=PA&bolum=FINE+ARTS")
  pe.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=PE&bolum=PHYSICAL+EDUCATION")
  phil.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=PHIL&bolum=PHILOSOPHY")
  phys.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=PHYS&bolum=PHYSICS")
  pols.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=POLS&bolum=POLITICAL+SCIENCE%26INTERNATIONAL+RELATIONS")
  pred.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=PRED&bolum=PRIMARY+EDUCATION")
  psy.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=PSY&bolum=PSYCHOLOGY")
  sced.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=SCED&bolum=MATHEMATICS+AND+SCIENCE+EDUCATION")
  sceds.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=SCED&bolum=SECONDARY+SCHOOL+SCIENCE+AND+MATHEMATICS+EDUCATION")
  sco.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=SCO&bolum=SYSTEMS+%26+CONTROL+ENGINEERING")
  soc.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=SOC&bolum=SOCIOLOGY")
  spl.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=SPL&bolum=SOCIAL+POLICY+WITH+THESIS")
  swe.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=SWE&bolum=SOFTWARE+ENGINEERING")
  sweT.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=SWE&bolum=SOFTWARE+ENGINEERING+WITH+THESIS")
  tk.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=TK&bolum=TURKISH+COURSES+COORDINATOR")
  tkl.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=TKL&bolum=TURKISH+LANGUAGE+%26+LITERATURE")
  tr.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=TR&bolum=TRANSLATION+AND+INTERPRETING+STUDIES")
  trm.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=TRM&bolum=SUSTAINABLE+TOURISM+MANAGEMENT")
  ttrm.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=TRM&bolum=TOURISM+ADMINISTRATION")
  wtr.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=WTR&bolum=TRANSLATION")
  xmba.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=XMBA&bolum=EXECUTIVE+MBA")
  yadyok.append(head+str(i)+"/"+str(x)+"-"+str(s)+"&kisaadi=YADYOK&bolum=SCHOOL+OF+FOREIGN+LANGUAGES")
  
  # Part that decides for the while loop to terminate or continue.
  if i==b and s==1 and f==1:
   break
  elif x==b and ((s==2 and f==2) or (s==3 and f ==3)):
   break
    
   
  if s==3 and not a:
   s=1
   a=True
  if s==1 and not a:
   s=2
   a=True
   i-=1
  if s==2 and not a:
   s=3
   i-=1
   a=True
  
  i+=1
  
allDepartments.append(ad)  
allDepartments.append(asiaStudies)
allDepartments.append(asiaStudiesT)
allDepartments.append(ata)
allDepartments.append(auto)
allDepartments.append(bio)
allDepartments.append(bis)
allDepartments.append(bm)
allDepartments.append(ccs)
allDepartments.append(ce)
allDepartments.append(cem)
allDepartments.append(ceet)
allDepartments.append(cet)
allDepartments.append(che)
allDepartments.append(chem)
allDepartments.append(cmpe)
allDepartments.append(cogs)
allDepartments.append(cse)
allDepartments.append(ec)
allDepartments.append(ed)
allDepartments.append(ee)
allDepartments.append(ef)
allDepartments.append(env)
allDepartments.append(envt)
allDepartments.append(eqe)
allDepartments.append(etm)
allDepartments.append(fe)
allDepartments.append(fled)
allDepartments.append(ged)
allDepartments.append(gph)
allDepartments.append(guid)
allDepartments.append(hist)
allDepartments.append(hum)
allDepartments.append(ie)
allDepartments.append(inct)
allDepartments.append(int)
allDepartments.append(intt)
allDepartments.append(inttM)
allDepartments.append(ling)
allDepartments.append(ll)
allDepartments.append(ls)
allDepartments.append(math)
allDepartments.append(me)
allDepartments.append(meca)
allDepartments.append(mir)
allDepartments.append(mirT)
allDepartments.append(mis)
allDepartments.append(pa)
allDepartments.append(pe)
allDepartments.append(phil)
allDepartments.append(phys)
allDepartments.append(pols)
allDepartments.append(pred)
allDepartments.append(psy)
allDepartments.append(sced)
allDepartments.append(sceds)
allDepartments.append(sco)
allDepartments.append(soc)
allDepartments.append(spl)
allDepartments.append(swe)
allDepartments.append(sweT)
allDepartments.append(tk)
allDepartments.append(tkl)
allDepartments.append(tr)
allDepartments.append(trm)
allDepartments.append(ttrm)
allDepartments.append(wtr)
allDepartments.append(xmba)
allDepartments.append(yadyok)

# List of lists of all lessons for all departments without duplication.
allLessonsNoDup=[]
# List of lists of all lessons for all departments keeping their lessons in each term in separate lists inside, without duplication.
allLessonsNoDupTermTerm=[]
# List of lists of all numbers of different teachers for all departments in each term.
teacherNumberTermTerm = []
# List of lists of all lessons with their different sections for all departments.
allLessonCodesWithSections=[]
# List of lists of names of all lessons for all departments with duplicates.
allLessonNameWithDup = []
# List of lists of names of all teachers of all lessons for all departments with duplicates. 
allTeachersWithDup= []
# List of lists of all numbers of Undergraduate and graduate lessons of all departments in each term in separate lists inside.
allTermUGs = []

# For all URLs in all specific department lists in allDepartments, it takes the required data and fill the lists with them.
for dep in allDepartments:
    # List of all lessons for a department without duplication.
    allLessonsofaDepNoDup=[]
    # List of all lessons for a department keeping their lessons in each term in separate lists inside, without duplication.
    allLessonsofaDepNoDupTermTerm = []
    # List of all numbers of different teachers for a department in each term.
    teacherNumberofaDepTermTerm = []
    # List of all lessons with their different sections for a department.
    allLessonCodesofaDepWithSections = []
    # List of names of all lessons for a department with duplicates.
    allLessonNameofaDepWithDup = []
    # List of names of all teachers of all lessons for a department with duplicates. 
    allTeachersofaDepWithDup= []
    # List of all numbers of Undergraduate and graduate lessons of a department in each term in separate lists inside.
    allTermUGsofaDep = []
    for x in dep: 
        # List of lessons for a department in a single term without duplicates.
        lessonsTermNoDup = []
        # List of teachers for a department in a single term without duplicates.
        teachersTermNoDup =[]
        # Taking the URL and converting it to the HTML part.
        response = ''
        while response =='':
            try:
                response = requests.get(x)
                break
            except:
                time.sleep(1)
                continue
        soup = BeautifulSoup(response.text, "lxml")
        # Searching for all tables in order to get the correct one in HTML. 
        table_body=soup.findAll("table")
        if len(table_body)!=0:
            rows = table_body[len(table_body)-1].find_all('tr') 
            for k, row in enumerate(rows):
                cols=row.find_all('td')
                cols=[x.text.strip() for x in cols]
                # Finding the column indexes of lesson codes, lesson names and teachers from the first row in table. 
                if k==0:
                    for i, col in enumerate(cols):
                        if "Instr." in cols[i]:
                            teacherIndex = i
                        elif "Name" in cols[i]:
                            nameIndex = i
                        elif "Code.Sec" in cols[i] or "Code." in cols[i]:
                            codeIndex = i
                lesson=cols[codeIndex]
                allLessonCodesofaDepWithSections.append(lesson)
                lesson=lesson[:-3]
                lessonsTermNoDup.append(lesson)
                allLessonsofaDepNoDup.append(lesson)
                if cols[nameIndex]!="LAB" and cols[nameIndex]!="P.S.":
                    allLessonNameofaDepWithDup.append(cols[nameIndex])
                    a=len(dates)
                    allTeachersofaDepWithDup.append(cols[teacherIndex])
                    teachersTermNoDup.append(cols[teacherIndex])
        
        # Removing unnecessary values and duplicates from corresponding lists.
        lessonsTermNoDup = removeValues(lessonsTermNoDup, "Code.Sec")
        lessonsTermNoDup = removeValues(lessonsTermNoDup, "Code.")
        lessonsTermNoDup = removeValues(lessonsTermNoDup, "") 
        teachersTermNoDup = removeValues(teachersTermNoDup, "Instr.")  
        teachersTermNoDup = removeValues(teachersTermNoDup, "STAFF STAFF")
        lessonsTermNoDup = list(dict.fromkeys(lessonsTermNoDup))
        teachersTermNoDup = list(dict.fromkeys(teachersTermNoDup))
        teacherNumberofaDepTermTerm.append(len(teachersTermNoDup))
        allTermUGsofaDep.append(findUG(lessonsTermNoDup))
        allLessonsofaDepNoDupTermTerm.append(lessonsTermNoDup)
        
    # Removing unnecessary values and duplicates from corresponding lists.    
    allLessonsofaDepNoDup = removeValues(allLessonsofaDepNoDup, "Code.Sec")
    allLessonsofaDepNoDup = removeValues(allLessonsofaDepNoDup, "Code.")
    allLessonsofaDepNoDup = removeValues(allLessonsofaDepNoDup, "")
    allLessonsofaDepNoDup = list(dict.fromkeys(allLessonsofaDepNoDup))
    allLessonsofaDepNoDup.sort(key = lambda item: ([str,int].index(type(item)), item))    
    allLessonCodesofaDepWithSections = removeValues(allLessonCodesofaDepWithSections, "Code.Sec")
    allLessonCodesofaDepWithSections = removeValues(allLessonCodesofaDepWithSections, "Code.")
    allLessonCodesofaDepWithSections = removeValues(allLessonCodesofaDepWithSections, "") 
    allLessonNameofaDepWithDup = removeValues(allLessonNameofaDepWithDup, "Name")
    allTeachersofaDepWithDup = removeValues(allTeachersofaDepWithDup, "Instr.")  
    
    # Appending lists for each department to lists that stores the data of all departments.
    allLessonsNoDup.append(allLessonsofaDepNoDup)
    allLessonsNoDupTermTerm.append(allLessonsofaDepNoDupTermTerm)
    teacherNumberTermTerm.append(teacherNumberofaDepTermTerm)
    allLessonCodesWithSections.append(allLessonCodesofaDepWithSections)
    allLessonNameWithDup.append(allLessonNameofaDepWithDup)
    allTermUGs.append(allTermUGsofaDep)
    allTeachersWithDup.append(allTeachersofaDepWithDup)
   
# Printing the desired data in CSV form to the standard output.
print("Dept./Prog. (name), Course Code, Course Name, ", end = '')
for date in dates:
    print(date + " , ", end = '')   
print("Total Offerings")
# Part for printing the data for each department separately.  
for i, department in enumerate(allDepartments):    
    if len(allLessonsNoDup[i])!=0:
        print("\""+Departments[i] +"\""+ ", ", end = '')
        UGlist = findUG(allLessonsNoDup[i])
        print("U" + str(UGlist[0]) + " G" + str(UGlist[1]) + ", , ", end = '')
        # Since U and G values in Total Off. part are the sums of all term values of U and G, these lists get all U and G's 
        # in order to sum them separately.
        Ulist=[]
        Glist=[]
        # Determines the U,G and I values for each term.
        for k, date in enumerate(dates):
            if len(allLessonsNoDupTermTerm[i][k])==0:
                print("U0 G0 I0, ", end = '')
            else:    
                UGlist = findUG(allLessonsNoDupTermTerm[i][k])
                print("U" + str(UGlist[0]) + " ", end = '')
                Ulist.append(UGlist[0])
                print("G" + str(UGlist[1]) + " ", end = '')
                Glist.append(UGlist[1])
                print("I" + str(teacherNumberTermTerm[i][k]) + ", ", end = '')
                U=listSum(Ulist)
                G=listSum(Glist)  
                teachersoftheDepNoDup = list(dict.fromkeys(allTeachersWithDup[i]))
                teachersoftheDepNoDup = removeValues(teachersoftheDepNoDup, "STAFF STAFF")
                I = len(teachersoftheDepNoDup)      
        print("U" + str(U) + " G" + str(G) + " I" + str(I))
        # Printing the lesson information under each department for each term.
        for lesson in allLessonsNoDup[i]:
            print(" ," + lesson +",", end = '')
            listindex = findIndex(allLessonCodesWithSections[i], lesson)
            courseName = allLessonNameWithDup[i][listindex[0]]
            print("\"" + courseName +"\"" + ", ", end = '')
            counter = 0;
            # If a lesson exists in a term, it puts a mark(x), otherwise prints space.
            for k, date in enumerate(dates):
                if lesson in allLessonsNoDupTermTerm[i][k]:
                    print("x, ", end = '')
                    # The counter is to determine how many times a lesson is offered in given date range.
                    counter+=1
                else:
                    print(", ", end = '')
            print(str(counter) + "/", end = '')
            # To find number of distinct instructors for a lesson in all terms, it finds the indexes of lesson codes with sections,
            # finds the corresponding teachers in those indexes and remove duplicates to get correct number.
            listindex2 = findIndex(allLessonCodesWithSections[i], lesson)
            teachers = findElements(listindex2, allTeachersWithDup[i])       
            teachers = list(dict.fromkeys(teachers))
            l = len(teachers)
            # Ignoring the STAFF STAFF.
            if "STAFF STAFF" in teachers:
                l-=1    
            print(l)
          


