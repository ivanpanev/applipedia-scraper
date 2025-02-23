# Applipedia scraper
A simple python script that scrapes the list of Palo Alto "applipedia" applications and their details, outputting them in a .csv file.   

Palo Alto Applipedia (https://applipedia.paloaltonetworks.com/) is a public knowledge base maintained by Palo Alto Networks that catalogs detailed technical and security attributes of Applications recognized by their Next-Generation Firewalls. As the website lacks a public API, there is no convenient way to programmatically access, filter or reference the list of up to date applicaitons and their properties. This script aims to solve this by scraping the table of applications and retreiving their attributes ('Name', 'Category', 'Subcategory', 'Evasive', 'ExcessiveBandwidth', 'Risk', 'Prone to Misuse', 'Capable of File Transfer', 'Technology', 'Tunnels Other Applications', 'Used by Malware', 'Has Known Vulnerabilities', 'Widely Used', 'SaaS', 'Standard Ports'), and outputting them in a .csv table file.

# Usage instructions
Run the script. It will save the output to a file named "applepedia_data_{date_time_stamp}.csv" in it's local directory. Execution takes ~15 minutes as each of the ~5000 currently defined applications require a POST request to fetch their details, and we apply a courtesy rate limit of 0.1 seconds between requests.

# License and Palo Alto Networks' Terms of Use
All content of this github repository is under MIT License. However, all data processed by and resulting from the execution of the script is owned by Palo Alto Networks and falls under their terms of use: https://www.paloaltonetworks.com/legal-notices/terms-of-use

"Palo Alto Networks grants you a limited, revocable, non-transferable license under its and other applicable copyrights to (1) download or use one copy of Site Content to a single computer, if applicable, solely for your personal and non-commercial internal use, except as otherwise may be indicated on this Site or (2) if you have an existing business relationship with Palo Alto Networks, you may download Site Content for use in furtherance of, and subject to the terms and conditions of, the provisions of your separate written agreement with Palo Alto Networks. If software, executable files or programs are not accompanied by their own terms and conditions, our End User Agreement shall govern their use."
