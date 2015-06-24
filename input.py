__author__ = 'hitanjan'

import csv
import urllib2
from bs4 import BeautifulSoup
import shutil
import os
from urlparse import urlparse
import sklearn.datasets



class url():
    def __init__(self, url):
        self.url = url.strip()
        req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib2.urlopen(req).read() # TODO - Use retries and timeout options and add https support
        self.soup = BeautifulSoup(html)
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
        self.__create_cache_dir()

    def __create_cache_dir(self):
        if(not os.path.exists(self.__cache_dir__)):
            print "Building cache... This may take some time.."
            os.makedirs(self.__cache_dir__)
            os.makedirs(self.__feature_set1_dir_positive__)
            os.makedirs(self.__feature_set1_dir_negative__)

    def _build_dataset_cache_from_csv_file(self, file, classifier_dir):

        with open(file, 'rU') as csv_file:
                reader = csv.reader(csv_file, delimiter=',')
                data, data_class = [], []

                for row in reader:

                    # Deal with comma separated 'Inc.' and other such occurrences in csv file. Remove the index of the term. Deals with rogue commas in a csv row
                    if(len(row) > 2):
                        element = row[1]
                        valid_url = urlparse(element)
                        if(not valid_url.netloc):
                            # Not a url, a plain string
                            row[0] += element
                            del row[1]

                    input_model = model(row[1], row[0])
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


    def load(self):

        self.build_data_set_cache()

        # TODO utf-8 ??
        dataset = sklearn.datasets.load_files(self.__feature_set1_dir__)

        return dataset


    def rebuild_data_set_cache(self):
        if(os.path.exists(self.__cache_dir__)):
            shutil.rmtree(self.__cache_dir__)


        self.build_data_set_cache()


    def build_data_set_cache(self):
        self._build_dataset_cache_from_csv_file(self.positive_file, self.__feature_set1_dir_positive__)
        self._build_dataset_cache_from_csv_file(self.negative_file, self.__feature_set1_dir_negative__)



