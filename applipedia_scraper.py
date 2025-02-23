import requests
import re
import time
import datetime
import csv
import os

def get_application_data():
    session = requests.Session()
    main_url = "https://applipedia.paloaltonetworks.com/"
    
    # Retrieve initial ASP.NET viewstate parameters
    response = session.get(main_url)
    viewstate = re.search(r'__VIEWSTATE" value="([^"]+)"', response.text).group(1)
    viewstategen = re.search(r'__VIEWSTATEGENERATOR" value="([^"]+)"', response.text).group(1)

    # Using a standard set of HTTP headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://applipedia.paloaltonetworks.com',
        'Referer': main_url,
    }

    # Request the main list of applications
    response = session.post(
        "https://applipedia.paloaltonetworks.com/Home/GetApplicationListView",
        data={
            '__VIEWSTATE': viewstate,
            '__VIEWSTATEGENERATOR': viewstategen,
            'category': '',
            'subcategory': '',
            'technology': '',
            'risk': '',
            'characteristic': '',
            'searchstring': ''
        },
        headers=headers
    )
    
    # Parse out the main applications table from the response
    applications = []
    app_pattern = re.compile(
        r'ShowApplicationDetail\(\'(\d+)\',\s*\'([^\']+)\',\s*\'(\d+)\'\)[^>]*>([^<]+)<',
        re.DOTALL
    )
    for match in app_pattern.findall(response.text):
        applications.append({
            'id': match[0],
            'internal_name': match[1],
            'ottawagroup': match[2],
            'display_name': match[3].strip()
        })

    # Regex to extract properties from the application detailed pop-up
    property_patterns = {
        'Category': r'Category\s*<\/td>\s*<td[^>]*>(.*?)<\/td>',
        'Subcategory': r'Subcategory\s*<\/td>\s*<td[^>]*>(.*?)<\/td>',
        'Evasive': r'Evasive\s*<\/td>\s*<td[^>]*>(.*?)<\/td>',
        'ExcessiveBandwidth': r'Excessive Bandwidth\s*<\/td>\s*<td[^>]*>(.*?)<\/td>',
        'Risk': r'<img[^>]*risklevel/risk_(\d)\.gif',
        'Prone to Misuse': r'Prone to Misuse\s*<\/td>\s*<td[^>]*>(.*?)<\/td>',
        'Capable of File Transfer': r'Capable of File Transfer\s*<\/td>\s*<td[^>]*>(.*?)<\/td>',
        'Technology': r'Technology\s*<\/td>\s*<td[^>]*>(.*?)<\/td>',
        'Tunnels Other Applications': r'Tunnels Other Applications\s*<\/td>\s*<td[^>]*>(.*?)<\/td>',
        'Used by Malware': r'Used by Malware\s*<\/td>\s*<td[^>]*>(.*?)<\/td>',
        'Has Known Vulnerabilities': r'Has Known Vulnerabilities\s*<\/td>\s*<td[^>]*>(.*?)<\/td>',
        'Widely Used': r'Widely Used\s*<\/td>\s*<td[^>]*>(.*?)<\/td>',
        'SaaS': r'SaaS\s*<\/td>\s*<td[^>]*>(.*?)<\/td>',
        'Standard Ports': r'Standard Ports\s*<\/td>\s*<td[^>]*>(.*?)<\/td>'
    }

    result = {}
    detail_url = "https://applipedia.paloaltonetworks.com/Home/GetApplicationDetailView"
    
    for app in applications:
        try:
            # Request detailed application info
            detail_response = session.post(
                detail_url,
                data={
                    'id': app['id'],
                    'ottawagroup': app['ottawagroup'],
                    'appName': app['internal_name']
                },
                headers=headers
            )
            
            app_data = {}
            html = detail_response.text
            
            # Extract each property using regex patterns
            for prop, pattern in property_patterns.items():
                match = re.search(pattern, html, re.DOTALL | re.IGNORECASE)
                if match:
                    value = match.group(1).strip()
                    value = re.sub(r'<[^>]+>', '', value) # Remove HTML tags
                    value = re.sub(r'\s+', ' ', value).strip() # Collapse extra spaces
                    
                    if prop == 'Risk':
                        value = f"{value}"
                    else:
                        lower_val = value.lower()
                        if lower_val in ['yes', 'y', 'true']:
                            value = 'Yes'
                        elif lower_val in ['no', 'n', 'false']:
                            value = 'No'
                    
                    app_data[prop] = value
                else:
                    app_data[prop] = 'N/A'

            result[app['display_name']] = app_data

            time.sleep(0.1) # Rate limit
            
        except Exception as e:
            print(f"Error processing {app['display_name']}: {str(e)}")
            result[app['display_name']] = {'error': str(e)}

    return result

def main():
    print("Getting application data from applipedia.paloaltonetworks.com...")
    app_data = get_application_data()
    
    csv_headers = [
        'Application', 'Category', 'Subcategory', 'Evasive', 'ExcessiveBandwidth',
        'Risk', 'Prone to Misuse', 'Capable of File Transfer', 'Technology',
        'Tunnels Other Applications', 'Used by Malware', 'Has Known Vulnerabilities',
        'Widely Used', 'SaaS', 'Standard Ports'
    ]
    
    date_time_stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    output_filename = f"applipedia_data_{date_time_stamp}.csv"
    
    # Write to CSV
    with open(output_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(csv_headers)
        
        for name, details in app_data.items():
            if 'error' in details:
                print(f"Error in retreiving application data for {name}. Excluding it from .csv output.")
                continue 
            
            row = [name] + [details.get(field, 'N/A') for field in csv_headers[1:]]
            writer.writerow(row)
    
    print(f"Data has been successfully written to '{output_filename}' in {os.getcwd()}")

if __name__ == "__main__":
    main()
