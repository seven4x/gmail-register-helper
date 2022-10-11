import requests
from pyquery import PyQuery  
import time   
f = open("names.txt", "a")
for page in range(234,461):
    r = requests.get(f"https://babynames.net/boy?page={page}")
    time.sleep(3)
    pq = PyQuery(r.text)
    tag = pq('span.result-name') 
    line = tag.text()
    line = line.replace(' ','\n')
    print(line +"\n") 
    f.write(line +'\n')
print('done!!!')