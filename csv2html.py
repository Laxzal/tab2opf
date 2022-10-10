'''

Simple one
id  |   word    |   meaning

'''
import contextlib

import numpy as np
import pandas as pd


# /Users/calvin/Library/CloudStorage/OneDrive-Personal/Documents/hebrew_dict

class SimpleCSV2HTML:

    def __init__(self, database_fname):
        self.database_fname = database_fname
        self.database = None
        self.list_file_names = []
        # Automatic Functions to Run
        self.importDbFile()

    def importDbFile(self):
        self.database = pd.read_csv(self.database_fname)  # encoding="ISO-8859-8", error_bad_lines=)
        print(self.database.head())

    def _cleanNiqqudChars(self, my_string):
        return ''.join(['' if 1456 <= ord(c) <= 1479 else c for c in my_string])

    def hebrewWordsClean(self, column_name: str = 'word'):
        self.database[str(column_name)] = self.database[str(column_name)].apply(self._cleanNiqqudChars)

        print(self.database.head())

    def createSimpleDf(self):
        self.csv2html_df = self.database[['id', 'word', 'meaning']].copy()
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
    def _writekeysLoop(self,fname, index, row):

            fname.write(
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

    @contextlib.contextmanager
    def writeHTML(self, title_name):


        count_start = 0
        file_line_max = 1000
        if file_line_max > self.csv2html_df.shape[0]:
            file_line_max = self.csv2html_df.shape[0]
        noHTMLfiles = int(np.ceil(self.csv2html_df.shape[0]/file_line_max))


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
                #while count_start < file_line_max:
                for index, row in self.csv2html_df.iloc[count_start:file_line_max].iterrows():
                    self._writekeysLoop(f, index, row)
                count_start = file_line_max
                file_line_max += 1000
                f.write("""
                <tours/>
                <guide> <reference type="search" title="Dictionary Search" onclick= "index_search()"/> </guide>
                </package>
                """
                        )

            assert f.closed is True

    def returnHtmlName(self):
        return str(self.fname)

test = SimpleCSV2HTML("/Users/calvin/Library/CloudStorage/OneDrive-Personal/Documents/hebrew_dict/pealim_database.csv")
test.hebrewWordsClean('word')
test.createSimpleDf()
test.writeHTML('split_test_html')
#test.writeKeys('test_html_file')
