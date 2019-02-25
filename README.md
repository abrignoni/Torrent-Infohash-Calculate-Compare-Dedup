# Torrent-Infohash-Calculate-Compare

Python 3 script used to recursively calculate infohashes on files ending with the .torrent extension.  
It can also take a list of known infohash values (list.txt) and find matching torrents recursively.  
After calculation and/or comparison corresponding calculated.txt and matches.txt files are created in the same directory as the script.

Script will create 

Prerequisite:
- Pip install beconding .whl file. (https://pypi.org/project/bencoding/)   
- If doing comparisons have a file named list.txt with one infohash per line in the same directory as the script.  
- Enclose paths in quotations if any blank spaces in it. Ex: "C:\Program Files\"

Usage  
![alt text](/images/Usage.PNG "Usage example")  

Calculate infohash example:  
![alt text](/images/Calculated_infohashes.PNG "Usage example")

Compared infohash example:
![alt text](/images/Compared.PNG "Usage example")
