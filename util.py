__author__ = 'hitanjan'

from urlparse import urlparse
import csv
import input
import search
import itertools
import os

class csv_reader():
    def __init__(self, file):
        self.file = file


    def record_gen(self, max_records=None):
        with open(self.file, 'rU') as csv_file:
                reader = csv.reader(csv_file, delimiter=',')

                for record_count, row in enumerate(reader, 1):
                    if(not max_records is None and record_count > max_records):
                        break

                    # Deal with comma separated 'Inc.' and other such occurrences in csv file. Remove the index of the term. Deals with rogue commas in a csv row
                    if(len(row) > 2):
                        element = row[1].strip()
                        valid_url = urlparse(element)
                        if(not valid_url.netloc):
                            # Not a url, a plain string
                            row[0] += " " + element
                            del row[1]

                    yield row



class csv_dataset():

    def __init__(self, company_list_csv_file, positive_csv_file, negative_csv_file):
        self.company_list_csv_file = company_list_csv_file
        self.positive_csv_file = positive_csv_file
        self.negative_csv_file = negative_csv_file


    def _negative_data_gen(self):

        csv_file = csv_reader(self.company_list_csv_file)
        search_handle = search.bing()

        # Get maximum size of csv
        csv_record_count = sum(1 for _ in csv_file.record_gen())

        # Use half of the total csv record count to create negative dataset
        for record in csv_file.record_gen(csv_record_count/2):
            input_model = input.model(record[1], record[0])
            company_name = input_model.company_name

            # Search google for 50th index. Random search offset
            resultset = search_handle.search(company_name, offset=50)

            for potential_url in resultset:
                try:
                    potential_url_object = input.url(potential_url)
                except BaseException, ex:
                    print ex
                    continue

                if(not potential_url_object is None):
                    break

            yield [company_name, potential_url_object.url]


    def create_files(self):
        # Create positive csv dataset by excluding negative csv dataset from the input set
        if(not os.path.exists(self.negative_csv_file)):
            with open(self.negative_csv_file, 'w', 1) as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=',')
                for row in self._negative_data_gen():
                    csv_writer.writerow(row)


        negative_csv = csv_reader(self.negative_csv_file)
        input_csv = csv_reader(self.company_list_csv_file)

        positive_csv_file = open(self.positive_csv_file, 'w', 1)
        positive_csv_writer = csv.writer(positive_csv_file, delimiter=',')

        for a,b in itertools.izip_longest(negative_csv.record_gen(), input_csv.record_gen(), fillvalue = None):

            input_model_b = input.model(b[1], b[0])
            if(not a is None):
                input_model_a = input.model(a[1], a[0])
                if(input_model_a.company_name == input_model_b.company_name):
                    continue
                else:
                    positive_csv_writer.writerow(b)
            else:
                positive_csv_writer.writerow(b)





