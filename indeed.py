#!c:\python\python.exe

#to include download time in the file name
import datetime
x = datetime.datetime.now()
y = x.strftime("%b%d%Y%H%M%S")

#to send response as a csv file
print("Content-Disposition: attachment; filename = \"indeed{}.csv\"\r\n".format(y))

#to send response as html
#print("Content-type:text/html\n\n")

import cgi
formData = cgi.FieldStorage()

from urllib.request import urlopen
from bs4 import BeautifulSoup

# to save the file in the server
#file = open("indeed.csv","w")
#file.write("Job-title, Company Name, Location, Salary, Posting Date, Job-Link\n")

all_jobs = " "

#collect search parameters from the HTML
job = formData.getvalue("searchjob")
Search_job = job.replace(" ","+").strip()
loc = formData.getvalue("location")
Search_loc = loc.replace(" ","+").strip()
pages = [0, 10, 20, 30, 40, 50, 60]

#get data from first 7 pages
for page in pages:
    #Create the url using search parameters
    url = ("https://ca.indeed.com/jobs?q={}&l={}&start={}".format(Search_job, Search_loc, page))
    
    uREQ = urlopen(url)
    pageC = uREQ.read()
    uREQ.close()
    soup = BeautifulSoup(pageC,"html.parser")

    #get all job sections
    job_info = soup.find_all("div",{"class":"jobsearch-SerpJobCard"})

    for job in job_info:        
        #get jobTitle and company name
        job_title = job.find("a",{"class":"jobtitle"}).text.strip().replace(",","-")
        com_name = job.find("span",{"class":"company"}).text.strip().replace(",","")
        
        #get location 
        try:
           loc = job.find("div",{"class":"location"}).text
        except:
           loc = job.find("span",{"class":"location"}).text
        
        #get salary range
        try:
           salary = job.find("span",{"class":"salaryText"}).text.replace(",", "").strip()
        except:
           salary =" "
    
        #get job posting time
        date = job.find("span",{"class":"date"}).text

        #get job link
        job_link = job.h2.find("a",href = True)
        link = (job_link["href"])
        link = "https://ca.indeed.com" + link
        
        all_jobs = all_jobs+(job_title + "," + com_name + "," + loc.replace(",","-") + "," + salary + ","
                + date +"," + link+"\n")
      
print("Job-title, Company Name, Location, Salary, Posting Date, Job-Link")        
print(all_jobs)

# to save the file in the server
#file.write(all_jobs) 
#file.close()

