from re import findall
import subprocess
import urllib.request
import os

print("""
\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
\t\tFireship Course Downloader
\t\t\t\t\t- @manish
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~""")

while(True):
    try:
        userMenuChoice=int(input("""
1. Download Course Here
2. Download Course in Seperate Folder
Enter Your Choice: """))
        if userMenuChoice != 1 and userMenuChoice != 2:
            raise ValueError
        break
    except (ValueError):
        print("Enter a Valid Choice")
    except (KeyboardInterrupt):
        print("\nExiting.....")
        exit()

while(True):
    try:
        courseLinkInput = input("""
Enter the Fireship Course Link (Multiple links are Supported Eg. link1 link2 ): """)
        # Spliting the links if multiple links are given
        courseLinkList = courseLinkInput.split(" ")
        for courseLink in courseLinkList:
            courseLink = courseLink.strip()
            # Checking if the given links are from fireship.io
            if "fireship.io" not in courseLink:
                raise ValueError
            # Checking if the given links are valid
            fireshipResponse = urllib.request.urlopen(courseLink).read().decode("utf-8")
        break
    except (ValueError):
        print("\nEnter a Valid Fireship.io link")
    except (KeyboardInterrupt):
        print("\nExiting.....")
        exit()
# Looping through the provided links
for courseLink in courseLinkList:
    # Striping the link incase if there's duplicated whitespace
    courseLink = courseLink.strip()
    # Connecting to the url and fetching the HTML
    fireshipResponse = urllib.request.urlopen(courseLink).read().decode("utf-8")
    # Parsing and Formatting the obtained HTML response
    fireshipResponse = fireshipResponse.split("\n")
    stripedResponse=[]
    for element in fireshipResponse:
        element = element.strip()
        stripedResponse.append(element)

    # Parsing through the <header> tag to fetch the course title
    courseHeader = findall('<header>(.*?)</header>', str(stripedResponse))
    courseTitle = findall('id="(.*?)"', str(courseHeader))
    courseTitle = courseTitle[0].capitalize()
    
    # Fetching all the video links in the course 
    url=[]
    for line in stripedResponse:
        line=line.strip()
        if line.startswith('<a href="/courses/'):
            line=findall(r'"(.*?)"', line)
            url.append(line)
    linkList=[]
    for line in url:
        for link in line:
            link="https://fireship.io/"+link
            linkList.append(link)
    
    # Storing the Links in a Textfile to make batch process with yt-dlp
    fireshipLinkOut=open(courseTitle+".txt", "w")
    
    for link in linkList:
        fireshipLinkOut.write(link+"\n")
    fireshipLinkOut.close()
    
    # Downloading the Lessons with yt-dlp according to the users choice
    if userMenuChoice==1:
        subprocess.run(["yt-dlp","-f","mp4","-a",courseTitle+".txt"])
    if userMenuChoice==2:
        os.makedirs(courseTitle,exist_ok=True)
        subprocess.run(["yt-dlp","-f","mp4","-a",courseTitle+".txt","-P",courseTitle])

# Cleaning up text files created for batch operations
for fileName in os.listdir():
    if fileName.endswith(".txt"):
        os.remove(fileName)