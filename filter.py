# This script filters the cord19 data into the following format
# | cord_uid | title | passage | 
# ------------------------------
# | 123      | 123   | Covid19 | 
# NOTE: Data folder should be created and stored like this 
# QA-BERT-like-language-models\data\2021-03-08
# |-- QA-BERT-like-language-models\
#     |-- data\
#         |-- 20201-03-08\
#             |-- document_parses
#             |-- changelog
#             |-- cord_19_embeddings.tar.gz
#             |-- document_parses.tar.gz
#             |-- metadata.csv

# Import libs
import csv
import os
import json
from collections import defaultdict

cord_uid_to_text = defaultdict(list)

# open the file
date = '2021-03-08'
with open('./data/' + date + '/metadata.csv') as f_in:
    reader = csv.DictReader(f_in)
    for row in reader:
    
        # access some metadata
        cord_uid = row['cord_uid']
        title = row['title']
        # abstract = row['abstract']
        # authors = row['authors'].split('; ')

        # access the full text (if available) for Intro
        # introduction = []
        if row['pdf_json_files']:
            for json_path in row['pdf_json_files'].split('; '):
                with open(json_path) as f_json:
                    full_text_dict = json.load(f_json)
                    
                    # grab introduction section from *some* version of the full text
                    for paragraph_dict in full_text_dict['body_text']:
                        paragraph_text = paragraph_dict['text']
                        cord_uid_to_text[cord_uid].append({
                            'title': title,
                            'passage': paragraph_text,
                        })
                        # section_name = paragraph_dict['section']
                        # if 'intro' in section_name.lower():
                        #     introduction.append(paragraph_text)

                    # stop searching other copies of full text if already got introduction
                    # if introduction:
                    #     break

        # save for later usage
        # cord_uid_to_text[cord_uid].append({
        #     'title': title,
        #     'abstract': abstract,
        #     'introduction': introduction
        # })

with open('./data/' + date + '/passagefied.csv', mode='w') as f_out:
    writer = csv.writer(f_out, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
    writer.writerow(['cord_uid', 'title', 'passage'])
    for key in cord_uid_to_text.keys():
        writer.writerow([key, cord_uid_to_text[key]['title'], cord_uid_to_text[key]['passage']])