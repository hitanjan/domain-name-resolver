__author__ = 'hitanjan'

from googleapiclient.discovery import build
from py_bing_search import PyBingSearch

class google():

    # This code is largely copied from the code written by Joe Gregorio
    # Original code may be found here - https://github.com/google/google-api-python-client/tree/master/samples/customsearch


    __auth__ = "AIzaSyCQkiO-7Rj4fnFRRYViGPluyJzxnd6hQCE"
    __cse_id__ = '000176173689670368806:gp5yn6rybga'

    def __init__(self, auth=__auth__, cse_id=__cse_id__):
        self.auth = auth
        self.cse_id = cse_id


    def search_by_page_rank(self, search_query, num_results=20):

        cse = self._get_cse()

        it = [(int(b*10 +1),10) for b in range(num_results/10)]
        it += [((num_results/10)*10 +1, num_results%10)] if num_results%10!=0 else []

        url_list = [cse.list(q=search_query,
                       cx=self.cse_id,
                       start = a,
                       num = b
                       ).execute()['items'][c]['link'] for (a,b) in it for c in range(b)]


        return url_list

    def _get_cse(self):
        # Build a service object for interacting with the API. Visit
        # the Google APIs Console <http://code.google.com/apis/console>
        # to get an API key for your own application.

        #print num_results
        service = build("customsearch", "v1",
                        developerKey=self.auth)

        cse = service.cse()
        return cse


    def search_by_index(self, search_key, start):

        cse = self._get_cse()

        # List contains bactch of 10 results.
        url_list = [cse.list(q=search_key,
                       cx=self.cse_id,
                       start = start,
                       num = 10
                       ).execute()['items'][c]['link'] for c in range(10)]

        return url_list


class bing():

    __API_KEY__ = 'S1zUX0tftHn+JWVkJ6c2b8RNsjbZUh6xZY+b4pmQ6m4'

    def __init__(self, API_KEY = __API_KEY__):
        self.API_KEY = API_KEY

    def search(self, search_query, offset=0, limit=50):
        # TODO - Deal with SSL errors

        bing = PyBingSearch(self.__API_KEY__)
        result_list, next_uri = bing.search(search_query, limit=limit, offset=offset, format='json')
        url_list = [element.url for element in result_list]
        return url_list