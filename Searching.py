import requests
from bs4 import BeautifulSoup
from collections import deque
import urllib.parse as url
def finding_corrupted_links(link, max_depth):
    queue_for_links = deque()
    visited = []
    visited = dict()       
    list_of_links = []
    number_of_corrupted_links = 0 
    queue_for_links.appendleft(link) 
    last_link = link 
    hloubka = 0 
    while hloubka <= max_depth: 
        if len(queue_for_links) == 0: break 
        current_link = queue_for_links.pop() 
        try:
            responce = requests.get(current_link)
        except:
            if "https" in current_link or "http" in current_link:
                print(f"{current_link} + responce code: -1")
                number_of_corrupted_links+=1
            continue
        parsing = BeautifulSoup(responce.text, features="xml") 
        if responce.status_code == 400 or responce.status_code == 404 or responce.status_code == 403 or responce.status_code == -1 or "redlink=1" in current_link:
            number_of_corrupted_links+=1
            list_of_links.append(current_link)
            print(current_link, "responce code "+ str(responce.status_code))
            continue
        if hloubka < max_depth:
            for i in parsing.find_all("a"):
                c = url.urljoin(current_link, i.get("href"))
                b = url.urlparse(c).scheme+"://"+url.urlparse(c).netloc
                if url.urljoin(b, i.get("href")) not in visited:
                    queue_for_links.appendleft(url.urljoin(b, i.get("href"))) 
                    visited[(url.urljoin(b, i.get("href")))] = True
        if current_link == last_link:
            hloubka+=1
            if len(queue_for_links) != 0:
                last_link = queue_for_links.popleft()
                queue_for_links.appendleft(last_link)
    if number_of_corrupted_links == 0: print("\nEnd of program\nNo corrupted links were found") 
    else: print(f"\nEnd of program\n{number_of_corrupted_links} corrupted links were found")
    return list_of_links
link = input("Enter your URL: ") 
print("Aware! Working time is growing exponentialy due to the depth")
max_depth = int(input("Enter depth of searching: "))
print("Started searching, wait until program ends...")
finding_corrupted_links(link, max_depth)