import json
import urllib, urllib2


def run_query(search_terms):
    # Specify the base
    root_url = 'https://api.datamarket.azure.com/Bing/Search/'
    source = 'Web'

    # Specify how many results we wish to be returned per page.
    # Offset specified where in the result list to start from.
    # With results_per_page = 10 and offset = 11, this would start form page 2.
    results_per_page = 10
    offset = 0

    # Wrap quotes around a query (required by bing api).
    # The query we will use is stored in variable query

    query = "'{0}'".format(search_terms)
    query = urllib.quote(query)

    # Construct the latter part of the request URL
    # Sets the format of the response to JSON and sets other properties
    search_url = "{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(
        root_url, source, results_per_page, offset, query)

    # Setup authentication with Bing servers
    # Username must be blank, get your API key from Bing API site
    username = ''
    bingapikey = 'XXXpWlIbCrtd45Tief5Y1dopOm2bgUCKhBukj5kFWfA'

    # Create a 'password manager' to handle authentication
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, search_url, username, bingapikey)

    # Create our results list which we'll populate
    results = []

    try:
        # Prepare connection to Bing servers
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)

        # Connect to the server and get the response
        response = urllib2.urlopen(search_url).read()

        # Convert response to JSON dictionary object
        json_response = json.loads(response)

        # Loop through each page and constructing results list
        for result in json_response['d']['results']:
            results.append({
                'title': result['Title'],
                'link': result['Url'],
                'summary': result['Description']})

    # Catch exceptions
    except urllib2.URLError, e:
        print 'Error querying the Bing API: ', e

    # Return results list
    return results


if __name__ == "__main__":
    print("Enter query string: ")
    query = raw_input().strip()
    result_list = []
    result_list = run_query(query)
    i = 1
    if result_list:
        for result in result_list:
            print i, result["title"]
            i+=1