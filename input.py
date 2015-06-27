__author__ = 'hitanjan'

import urllib2
from bs4 import BeautifulSoup
import shutil
import os
import sklearn.datasets
import util

class url():
    def __init__(self, url):
        self.url = url.strip()
        request = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0'})  # Masquerade as firefox to bypass checks to stop python agents
        response = urllib2.urlopen(request)  # TODO - Use retries and timeout options

        # Filter out directly by content type for html. TODO - maybe later add support for parsing pdf/docs ?
        # TODO Add support for parsing dynamic webpages, use a library that runs js to load webpages
        response_content_type = response.headers.getheader("Content-Type")

        if(not 'text/html' in  response_content_type):
            raise BaseException("URL contains non-html data. This tool does not support other content types except 'html'")

        response_content = response.read()

        self.soup = BeautifulSoup(response_content)
        [tag.decompose() for tag in self.soup.find_all(['style', 'script', '[document]', 'span'])]


    def get_text(self):
        return self.soup.get_text()


    def get_embedded_links(self):
        links = [(link.text, link['href']) for link in self.soup.find_all('a') if
                 link is not None and link.has_attr('href')]
        return links


class model():
    def __init__(self, potential_url, company_name=None):
        self.company_name = company_name.strip()
        self.company_name = self.company_name.replace("/", " ")
        self.potential_url = potential_url.strip()


    def load_raw_data(self):
        self.potential_url_object = url(self.potential_url)
        self.text = self.potential_url_object.get_text()
        if(isinstance(self.text, unicode)):
            self.text = self.text.encode("utf-8")
        if(self.text == ""):
            raise BaseException("No data found in URL - %s" % self.potential_url)
        self.descendant_links = self.potential_url_object.get_embedded_links()  # TODO - Use this feature later and Incorporate link structure too ?? Use a separate feature_set dir in dataset object
        del self.potential_url_object

        # TODO Pre-process ? Convert to lower ? Trim spaces ? special chars ?

    def __str__(self):
        return "model(potential_url=%s, company_name=%s)" % (self.potential_url, self.company_name)

class dataset():
    __positive__ = "positive"
    __negative__ = "negative"
    __feature_set_1__ = "url_contents"
    __cache_dir__ = 'dataset_cache'
    __feature_set1_dir_positive__ = os.path.join(__cache_dir__,__feature_set_1__,__positive__)
    __feature_set1_dir_negative__ = os.path.join(__cache_dir__,__feature_set_1__,__negative__)
    __feature_set1_dir__ = os.path.join(__cache_dir__, __feature_set_1__)

    def __init__(self, positive_csv_data, negative_csv_data):
        self.positive_file = positive_csv_data
        self.negative_file = negative_csv_data

    def _create_cache_dir(self):
        if(not self._check_if_cache_exists()):
            print "Building cache... This may take some time.."
            os.makedirs(self.__cache_dir__)
            os.makedirs(self.__feature_set1_dir_positive__)
            os.makedirs(self.__feature_set1_dir_negative__)

    def _check_if_cache_exists(self):
        if(os.path.exists(self.__cache_dir__)):
           return True

    def _build_dataset_cache_from_csv_file(self, file, classifier_dir):

        csv_file = util.csv_reader(file)
        for record in csv_file.record_gen():

            input_model = model(record[1], record[0])
            print("Processing model - %s in file - %s" % (input_model, file))
            if(os.path.exists(os.path.join(classifier_dir, input_model.company_name))):
                continue
            else:
                try:
                    input_model.load_raw_data()
                except BaseException as ex:
                    print("Error in loading dataset from model(potential_url=%s, company_name=%s) found in file : %s..Skipping") % (input_model.potential_url, input_model.company_name, file)
                    print ex
                    continue
                text = input_model.text
                text_file = open(os.path.join(classifier_dir, input_model.company_name), 'w')
                text_file.write(text)
                text_file.close()



    def load(self, build_cache=False, shuffle=True):
        """
            Returns a dictionary of sklearn Bunch data

        :param build_cache: attempt to build cache (i.e. url contents) or reuse existing
        :return: Returns a dictionary of sklearn Bunch data
        """
        if(not self._check_if_cache_exists() or build_cache):
            self._build_data_set_cache()

        # TODO utf-8 ??
        dataset = {}
        dataset[self.__feature_set_1__] = sklearn.datasets.load_files(self.__feature_set1_dir__, shuffle=shuffle)

        return dataset


    def rebuild_data_set_cache(self):
        self.clear_data_set_cache()
        self._build_data_set_cache()


    def clear_data_set_cache(self):
        if(self._check_if_cache_exists()):
            shutil.rmtree(self.__cache_dir__)


    def _build_data_set_cache(self):
        self._create_cache_dir()
        self._build_dataset_cache_from_csv_file(self.positive_file, self.__feature_set1_dir_positive__)
        self._build_dataset_cache_from_csv_file(self.negative_file, self.__feature_set1_dir_negative__)



