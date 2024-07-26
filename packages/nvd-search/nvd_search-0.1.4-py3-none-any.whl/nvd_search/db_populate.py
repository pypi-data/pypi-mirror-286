import requests
import time
from pymongo import MongoClient

class NvdDatabase():
    def __init__(self, api_key:str):
        self.nvd_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        self.results_per_page = 2000
        self.start_index = 0
        self.api_key = api_key

    def init_database(self):
        # Provide the mongodb url 
        CONNECTION_STRING = "mongodb://localhost:27017/"
        
        # Create a connection using MongoClient
        client = MongoClient(CONNECTION_STRING)
        
        # Create the database 
        return client['nvd']

    def retry_request(self, headers, params=None, time_sleep=2, total=2, status_forcelist=503):
        # Make number of requests required
        for _ in range(total):
            try:
                response = requests.get(self.nvd_url, headers=headers, params=params)
                if response.status_code == status_forcelist:
                    # Retry request 
                    time.sleep(time_sleep)
                    continue
                return response
            except requests.exceptions.ConnectionError:
                pass
        return None

    def dump_nvd(self):

        #Initialize NVD database and cves collection
        nvd_db = self.init_database()
        cves_collection = nvd_db['cves']

        # Define apiKey header 
        headers = { 'apiKey': self.api_key }

        # Get the total number of the cves at the times of initializing the tool
        responseT = requests.get(self.nvd_url, headers=headers)
        data = responseT.json()
        total_cves = data['totalResults']

        # Define variables for api rate limit (using the api key)
        requests_made = 0
        start_time = time.time()

        # Iterate through the API calls to get the cves
        while (self.start_index < total_cves):

            
            params = { 'resultsPerPage': self.results_per_page, 'startIndex': self.start_index }
            try:
                # Make a GET request to the NVD API
                #response = requests.get(url, headers=headers, params=params)

                #Make request using retry method
                response = self.retry_request(headers=headers, params=params)

                if response == None:
                    continue
                response.raise_for_status()
                
            except requests.exceptions.HTTPError as err:
                break
            
            # Convert the response to JSON
            data = response.json()

            # Get the results per page of the API call
            self.results_per_page = data['resultsPerPage']

            # Save the data to a JSON file
            for item in data['vulnerabilities']:
                    #Avoiding _id mapping
                    CVE_ID = item['cve']['id']
                    item['cve']['_id'] = CVE_ID

                    # Insert the documents 
                    cves_collection.insert_one(item['cve'])

            # Increment the requests made
            requests_made += 1

            #Recommended by NVD workflow
            time.sleep(6)

            # The rate limit with an api key is 50 requests in a rolling 30 seconds window.
            # If we've made 50 requests, the calls sleeps a range so that we assure that we don't surpass the 30 seconds window
            if requests_made >= 50:
                end_time = time.time()
                requests_time_windows = end_time - start_time
                if requests_time_windows < 30:
                    time.sleep(30 - requests_time_windows)
                    
                # Reset request counter and start_time
                requests_made = 0
                start_time = time.time()
            
            # Increment startIndex for the next batch
            self.start_index += self.results_per_page
        
        return cves_collection.count_documents({})