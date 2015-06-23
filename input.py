__author__ = 'hitanjan'

import csv
import urllib2
from bs4 import BeautifulSoup
import numpy
import os
import shelve



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
        self.descendant_links = self.potential_url_object.get_embedded_links()  # TODO - Use this feature later and Incorporate link structure too ??
        del self.potential_url_object

        # TODO Pre-process ? Convert to lower ? Trim spaces ? special chars ?


class dataset():
    def __init__(self, positive_csv_data, negative_csv_data):
        self.positive_file = positive_csv_data
        self.negative_file = negative_csv_data
        self.__cache_dir__ = 'dataset_cache'


    def _load_data_from_csv(self, file):
        if(not os.path.exists(self.__cache_dir__)):
            print "Loading data for the first time... This may take some time.."
            os.makedirs(self.__cache_dir__)

        cache = shelve.open(os.path.join(self.__cache_dir__, os.path.basename(file)))

        with open(file, 'rU') as csv_file:
                reader = csv.reader(csv_file, delimiter=',')
                data, data_class = [], []

                for row in reader:

                    # TODO : Deal with comma separated 'Inc.' and other occurrences in csv file. Remove the index of the term. Refine Logic
                    for (i,index) in [('Inc.' == element.strip(),row.index(element)) for element in row]:
                        if(i == True):
                            del row[index]

                    input_model = model(row[1], row[0])
                    if(cache.has_key(input_model.company_name)):
                        text = cache[input_model.company_name]
                    else:
                        try:
                            input_model.load_raw_data()
                        except BaseException as ex:
                            print("Error in loading dataset from model(potential_url=%s, company_name=%s) found in file : %s..Skipping") % (input_model.potential_url, input_model.company_name, file)
                            print ex
                            continue
                        text = cache[input_model.company_name] = input_model.text

                    data += [(input_model.company_name, text)]


        cache.close()
        return data


    def load(self):

        positive_data = self._load_data_from_csv(self.positive_file)
        data_positive = numpy.array(positive_data)
        class_positive = numpy.array([1 for r in range(len(positive_data))])


        negative_data = self._load_data_from_csv(self.negative_file)
        data_negative = numpy.array(negative_data)
        class_negative = numpy.array([0 for r in range(len(negative_data))])



        # Equal sizes of positive and negative training data
        # TODO - Shrink one list on basis of the other to make them equal before shuffle
        if (len(class_negative) != len(class_positive)):
            raise Exception("Positive and Negative Dataset Sizes don't match")

        data = numpy.concatenate((data_positive, data_negative))
        classification = numpy.concatenate((class_positive, class_negative))

        # shuffle
        shuffle_binder = numpy.c_[data.reshape(len(data), -1), classification.reshape(len(classification), -1)]
        newdata = shuffle_binder[:, :data.size // len(data)].reshape(data.shape)
        newclassification = shuffle_binder[:, data.size // len(data):].reshape(classification.shape)
        numpy.random.shuffle(shuffle_binder)


        dataset.data = newdata
        dataset.classification = newclassification
        return dataset





