# CFContestSpider

CFContestSpider is a scraper that helps you during contests in codeforces .

### Uses :

1) This scraper downloads all the inputs and outputs for the contest .

2) Creates folders for the contest and for each problem .

3) Creates program file , Actual output file and respective input and Expected output files for each problem .

4) Also downloads complete Problemset for the contest and stores it in pdf format .


### Requirements :

1) python3

2) python - scrapy

3) python - requests

4) python - os

5) python - pdfkit


### Steps :

1) Copy 'main.py' file to your codeforces folder

2) Run the spider by command ->  scrapy runspider main.py

3) Then this prompts for contest link ->  (Copy contest link and paste) Eg: http://codeforces.com/contest/772
           
4) Make sure that given link is valid .

5) Then this prompts for contest name -> Eg: 772

6) Then folder with given name is created

7) Thats it ! You can run this and read your first problem . Contest gets downloaded in mean time .
