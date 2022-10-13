'''

Simple one
id  |   word    |   meaning

'''
import contextlib
import re

import numpy as np
import pandas as pd


# /Users/calvin/Library/CloudStorage/OneDrive-Personal/Documents/hebrew_dict

class SimpleCSV2HTML:

    def __init__(self, database_fname):
        self.database_fname = database_fname
        self.database = None
        self.csv_noun_plural = r"/Users/calvin/Library/CloudStorage/OneDrive-Personal/Documents/hebrew_dict" \
                               r"/pealim_noun_db.csv"
        self.list_file_names = []
        # Automatic Functions to Run
        self.importDbFile()

    def importDbFile(self):
        self.database = pd.read_csv(self.database_fname)  # encoding="ISO-8859-8", error_bad_lines=)
        print(self.database.head())

    def importNounPluralDb(self):
        self.noun_plural_db = pd.read_csv(self.csv_noun_plural)
        # self.noun_plural_db = self.noun_plural_db.where(pd.notnull(self.noun_plural_db), "NaN")

    def _cleanNiqqudChars(self, my_string):
        return ''.join(['' if 1456 <= ord(c) <= 1479 else c for c in my_string])

    def hebrewWordsClean(self, column_name: str = 'word'):
        self.database[str(column_name)] = self.database[str(column_name)].apply(self._cleanNiqqudChars)
        print(self.database.head())

    def hebrewPluralClean(self):
        self.noun_plural_db['plural_state'] = self.noun_plural_db['plural_state'].apply(
            lambda x: self._cleanNiqqudChars(x) if not pd.isnull(x) else x)

    def mergeNounPlurals(self):
        self.database = self.database.merge(self.noun_plural_db[['id', 'plural_state']], on=['id'], how='outer')

        print(self.database.head())

    def extractForm(self):
        self.database['part_of_speech_simplified'] = self.database['part_of_speech'].apply(
            lambda x: re.match(r"(\w+)", x)[0] if re.match(r"(\w+)", x) is not None else '-')

    def createDefInflection(self):
        from_value = str('מ')
        the_value = str('ה')
        to_value = str('ל')
        self.database['inflection_the'] = self.database[['word', 'part_of_speech_simplified']].apply(
            lambda x: str(the_value + str(x['word'])) if x['part_of_speech_simplified'] == 'Noun' else str('NaN'),
            axis=1)
        self.database['inflection_from'] = self.database[['word', 'part_of_speech_simplified']].apply(
            lambda x: str(from_value + the_value + str(x['word'])) if x['part_of_speech_simplified'] == 'Noun' else str(
                'NaN'),
            axis=1)
        self.database['inflection_to'] = self.database[['word', 'part_of_speech_simplified']].apply(
            lambda x: str(to_value + str(x['word'])) if x['part_of_speech_simplified'] == 'Noun' else str('NaN'),
            axis=1)
        print(self.database['inflection_the'])

    def createSimpleDf(self):
        self.csv2html_df = self.database[
            ['id', 'word', 'part_of_speech_simplified', 'meaning', 'inflection_the','inflection_to', 'inflection_from', 'plural_state']].copy()
        print(self.csv2html_df.head())

    @contextlib.contextmanager
    def writeKeys(self, title_name):
        self.fname = f'{title_name}.html'
        with open(self.fname, 'w') as f:
            f.write("""
            <html xmlns:math="http://exslt.org/math" xmlns:svg="http://www.w3.org/2000/svg" xmlns:tl="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf"

xmlns:saxon="http://saxon.sf.net/" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xmlns:cx="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf" xmlns:dc="http://purl.org/dc/elements/1.1/"

xmlns:mbp="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf" xmlns:mmc="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf" xmlns:idx="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf">

<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head>

<body>

<mbp:frameset> 
            """)
            for index, row in self.csv2html_df.iterrows():
                f.write(
                    """
<idx:entry name="hebrew" scriptable="yes" spell="yes">
<idx:short><a id="{id}"></a>
<idx:orth value="{word}">
</idx:orth>
<p>{meaning}</p>
</idx:short>
</idx:entry>
""".format(id=row['id'], word=row['word'], meaning=row['meaning'])
                )
            f.write("""
        </mbp:frameset>

</body>

</html> 
        """)
        assert f.closed is True

    def _writekeysLoop(self, fname, index, row, pospeech: bool):

        if pospeech is False:
            fname.write(
                """
<idx:entry name="hebrew" scriptable="yes" spell="yes">
<idx:short><a id="{id}"></a>
<idx:orth value="{word}"><b>{word}</b>
</idx:orth>
<idx:infl inflgrp="{inflgrp}"> 
</idx:infl> 
<p>{meaning}</p>
</idx:short>
</idx:entry>
<hr style="width:50%", size="3", color=black> 
""".format(id=row['id'], word=row['word'], meaning=row['meaning'], inflgrp=row['part_of_speech_simplified'])
            )
        elif pospeech is True:
            fname.write(
                """
<idx:entry name="hebrew" scriptable="yes" spell="yes">
<idx:short><a id="{id}"></a>
<idx:orth value="{word}"><b>{word}</b>
<idx:infl inflgrp="{inflgrp}"> 
<idx:iform value="{inflection_the}"></idx:iform>
<idx:iform value="{inflection_from}"></idx:iform>
<idx:iform value="{inflection_to}"></idx:iform>
</idx:infl> 
</idx:orth>
<p>{meaning}</p>
</idx:short>
</idx:entry>
<hr style="width:50%", size="3", color=black> 
""".format(id=row['id'], word=row['word'], meaning=row['meaning'], inflgrp=row['part_of_speech_simplified'],
           inflection_the=row['inflection_the'],
           inflection_from=row['inflection_from'],
           inflection_to=row['inflection_to']))

    @contextlib.contextmanager
    def writeHTML(self, title_name, max_file_line: int = 1000):

        count_start = 0
        file_line_max = max_file_line
        if file_line_max > self.csv2html_df.shape[0]:
            file_line_max = self.csv2html_df.shape[0]
        noHTMLfiles = int(np.ceil(self.csv2html_df.shape[0] / file_line_max))

        for i in range(noHTMLfiles):
            fname = f'{title_name}_{i}.html'
            self.list_file_names.append(fname)
            with open(fname, 'w') as f:
                f.write("""
            <html xmlns:math="http://exslt.org/math" xmlns:svg="http://www.w3.org/2000/svg" xmlns:tl="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf"

xmlns:saxon="http://saxon.sf.net/" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"

xmlns:cx="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf" xmlns:dc="http://purl.org/dc/elements/1.1/"

xmlns:mbp="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf" xmlns:mmc="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf" xmlns:idx="https://kindlegen.s3.amazonaws.com/AmazonKindlePublishingGuidelines.pdf">

<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head>

<body>

<mbp:frameset>""")
                # while count_start < file_line_max:
                for index, row in self.csv2html_df.iloc[count_start:file_line_max].iterrows():
                    if row['part_of_speech_simplified'] == 'Noun':
                        self._writekeysLoop(f, index, row, pospeech=True)
                    else:
                        self._writekeysLoop(f, index, row, pospeech=False)
                count_start = file_line_max
                file_line_max += max_file_line
                f.write("""
                <tours/>
                <guide> <reference type="search" title="Dictionary Search" onclick= "index_search()"/> </guide>
                </package>
                """
                        )

            assert f.closed is True

    def returnHtmlName(self):
        return str(self.fname)

# test = SimpleCSV2HTML("/Users/calvin/Library/CloudStorage/OneDrive-Personal/Documents/hebrew_dict/pealim_database.csv")
# test.hebrewWordsClean('word')
# test.createSimpleDf()
# test.writeHTML('split_test_html')
# test.writeKeys('test_html_file')
