from results import Results 
from partner import Partner
import requests
import json
from collections import defaultdict

GET_URL = 'https://candidate.hubteam.com/candidateTest/v3/problem/dataset?userKey=5512d5c24e712202822a815d9880'
POST_URL = 'https://candidate.hubteam.com/candidateTest/v3/problem/result?userKey=5512d5c24e712202822a815d9880'

def get_json():
    """
    Submits a GET request to URL to access data 
    """
    return requests.get(GET_URL).json()

def post_json(results_dic):
    """
    Refactors the results variable into the appropriate json format and sends a POST request to submit data
    """
    data = {"countries":[]}
    for country in results_dic: 
        data["countries"].append(results_dic[country].json_results())
    res = requests.post(POST_URL, data=json.dumps(data))
    return res

def process_data(json_file):
    """
    Processes the JSON file returned from the GET request, finds the minimum most consecutive dates for each country, and manipulates the data into a format ready for submission
    """
    #dictionary with the keys set as countries and the values set as the "Results" class
    results_dic = {}
    
    #dictionary with keys set as countries and the values as partners from the respective country
    country_dic = defaultdict(list)
    for p in json_file['partners']:
        p = Partner(p)
        country_dic[p.country].append(p)
        
    for country in country_dic: 
        available_dic = defaultdict(list)
        for partner in country_dic[country]:
            #finds consecutive dates of each individual partner and uses those dates as keys for a dictionary 
            available_date = partner.get_consecutive()
            for dates in available_date: 
                available_dic[dates].append(partner.email)
        #first sort maintains the minimum order of dates 
        res = sorted(available_dic.items(), key=lambda item: item[0][0])
        #second sort finds the maximum amount of attendees respective to minimum date
        res.sort(key=lambda item: len(item[1]), reverse=True)
        #adds result to "Results" class
        results_dic[country] = Results(res, country)  
    return results_dic 

if __name__ == "__main__":
    json_file = get_json()
    results_dic = process_data(json_file)
    res = post_json(results_dic)
    print(res.status_code == 200)