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

        self.verb_conj_future_that_chaser = {}
        self.verb_conj_future_and_chaser = {}
        self.verb_conj_future_chaser = {}
        self.verb_conj_past_that_chaser = {}
        self.verb_conj_past_and_chaser = {}
        self.verb_conj_past_chaser = {}
        self.verb_conj_present_that_chaser = {}
        self.verb_conj_present_and_chaser = {}
        self.database_fname = database_fname
        self.database = None
        self.csv_noun_plural = r"/Users/calvin/Documents/hebrew_dictionary/pealim_noun_db.csv"
        self.list_file_names = []
        self.verb_conj_present_file = r"/Users/calvin/Documents/hebrew_dictionary/pealim_verb_present_table_db.csv"
        self.verb_conj_past_file = r"/Users/calvin/Documents/hebrew_dictionary/pealim_verb_past_table_db.csv"
        self.verb_conj_present = None
        self.verb_conj_present_chaser = {}
        self.verb_conj_future_file = r"/Users/calvin/Documents" \
                                     r"/hebrew_dictionary/pealim_verb_future_table_db.csv"
        # Automatic Functions to Run
        self.importDbFile()

    def importDbFile(self):
        self.database = pd.read_csv(self.database_fname)  # encoding="ISO-8859-8", error_bad_lines=)
        print(self.database.head())

    def importNounPluralDb(self):
        self.noun_plural_db = pd.read_csv(self.csv_noun_plural)
        # self.noun_plural_db = self.noun_plural_db.where(pd.notnull(self.noun_plural_db), "NaN")
        # TODO add inflections onto nouns

    def importVerbConjPresent_ver2(self):
        self.verb_conj_present_ = pd.read_csv(self.verb_conj_present_file)
        self.verb_conj_present_ = self.verb_conj_present_.merge(self.database, left_on='id', right_on='id')

        self.verb_conj_present_filtered = self.verb_conj_present_[['id', 'hebrew_word', 'english_word', 'chaser', 'word', 'hebrew_pronunciation', 'part_of_speech', 'meaning']]
    def importVerbConjPresent(self):
        self.verb_conj_present = pd.read_csv(self.verb_conj_present_file)
        print(self.verb_conj_present.head())
        self.verb_conj_present.drop(columns=['person', 'english_word'], inplace=True)
        self.verb_conj_present = self.verb_conj_present.pivot(index=['id'], columns=['verb_form', 'form', 'gender'])
        self.verb_conj_present.columns = ['_'.join(col) for col in self.verb_conj_present.columns.values]
        self.list_present_verb_columns = list(self.verb_conj_present.columns)

        self.verb_conj_present_and_columns = [s + '_andform' for s in self.list_present_verb_columns]
        self.verb_conj_present_and = self.verb_conj_present.copy()
        self.verb_conj_present_and.columns = self.verb_conj_present_and_columns
        self.verb_conj_present_and = self.verb_conj_present_and.applymap(lambda x: "{}{}".format('ו', x) if pd.isnull(x) == False else x)
        print(self.verb_conj_present_and.head())

        self.verb_conj_present_that_columns = [s + '_thatform' for s in self.list_present_verb_columns]
        self.verb_conj_present_that = self.verb_conj_present.copy()
        self.verb_conj_present_that.columns = self.verb_conj_present_that_columns
        self.verb_conj_present_that = self.verb_conj_present_that.applymap(lambda x: "{}{}".format('ש', x) if pd.isnull(x) == False else x)
        print(self.verb_conj_present_that.head())

        # TODO Find a better method

    def importVerbConjPast(self):
        self.verb_conj_past = pd.read_csv(self.verb_conj_past_file)
        print(self.verb_conj_past.head())
        self.verb_conj_past.drop(columns=['english_word'], inplace=True)

        self.verb_conj_past = self.verb_conj_past.pivot(index=['id'], columns=['verb_form', 'person', 'form', 'gender'])
        data = [tuple(str(x) for x in tup) for tup in self.verb_conj_past.columns.values]
        self.verb_conj_past.columns = ['_'.join(col) for col in data]
        self.list_past_verb_columns = list(self.verb_conj_past.columns)

        self.verb_conj_past_and_columns = [s + '_andform' for s in self.list_past_verb_columns]
        self.verb_conj_past_and = self.verb_conj_past.copy()
        self.verb_conj_past_and.columns = self.verb_conj_past_and_columns
        self.verb_conj_past_and = self.verb_conj_past_and.applymap(lambda x: "{}{}".format('ו', x) if pd.isnull(x) == False else x)
        print(self.verb_conj_past_and.head())

        self.verb_conj_past_that_columns = [s + '_thatform' for s in self.list_past_verb_columns]
        self.verb_conj_past_that = self.verb_conj_past.copy()
        self.verb_conj_past_that.columns = self.verb_conj_past_that_columns
        self.verb_conj_past_that = self.verb_conj_past_that.applymap(lambda x: "{}{}".format('ש', x) if pd.isnull(x) == False else x)
        print(self.verb_conj_past_that.head())

    def importVerbConjFut(self):
        self.verb_conj_future = pd.read_csv(self.verb_conj_future_file)
        self.verb_conj_future.drop(columns=['english_word'], inplace=True)

        self.verb_conj_future = self.verb_conj_future.pivot(index=['id'], columns=['verb_form', 'person', 'form', 'gender'])
        data = [tuple(str(x) for x in tup) for tup in self.verb_conj_future.columns.values]
        self.verb_conj_future.columns = ['_'.join(col) for col in data]
        self.list_verb_future_columns = list(self.verb_conj_future.columns)

        self.verb_conj_future_and_columns = [s + '_andform' for s in self.list_verb_future_columns]
        self.verb_conj_future_and = self.verb_conj_future.copy()
        self.verb_conj_future_and.columns = self.verb_conj_future_and_columns
        self.verb_conj_future_and = self.verb_conj_future_and.applymap(lambda x: "{}{}".format('ו', x) if pd.isnull(x) == False else x)
        print(self.verb_conj_future_and.head())

        self.verb_conj_future_that_columns = [s + '_thatform' for s in self.list_verb_future_columns]
        self.verb_conj_future_that = self.verb_conj_future.copy()
        self.verb_conj_future_that.columns = self.verb_conj_future_that_columns
        self.verb_conj_future_that = self.verb_conj_future_that.applymap(lambda x: "{}{}".format('ש', x) if pd.isnull(x) == False else x)
        print(self.verb_conj_future_that.head())



    def _cleanNiqqudChars(self, my_string):
        return ''.join(['' if 1456 <= ord(c) <= 1479 else c for c in my_string])

    def hebrewWordsClean(self, column_name: str = 'word'):
        self.database[str(column_name)] = self.database[str(column_name)].apply(self._cleanNiqqudChars)
        print(self.database.head())

    def hebrewPluralClean(self):
        self.noun_plural_db['plural_state'] = self.noun_plural_db['plural_state'].apply(
            lambda x: self._cleanNiqqudChars(x) if not pd.isnull(x) else x)

    def hebrewVerbsPresClean(self):
        self.verb_conj_present = self.verb_conj_present.applymap(
            lambda x: self._cleanNiqqudChars(x) if (pd.isnull(x)) == False else x)
        self.verb_conj_present_and = self.verb_conj_present_and.applymap(
            lambda x: self._cleanNiqqudChars(x) if (pd.isnull(x)) == False else x)
        self.verb_conj_present_that = self.verb_conj_present_that.applymap(
            lambda x: self._cleanNiqqudChars(x) if (pd.isnull(x)) == False else x)

    def hebrewVerbsPastClean(self):
        self.verb_conj_past = self.verb_conj_past.applymap(
            lambda x: self._cleanNiqqudChars(x) if (pd.isnull(x)) == False else x)
        self.verb_conj_past_and = self.verb_conj_past_and.applymap(
            lambda x: self._cleanNiqqudChars(x) if (pd.isnull(x)) == False else x)
        self.verb_conj_past_that = self.verb_conj_past_that.applymap(
            lambda x: self._cleanNiqqudChars(x) if (pd.isnull(x)) == False else x)

    def hebrewVerbsFutureClean(self):
        self.verb_conj_future = self.verb_conj_future.applymap(
            lambda x: self._cleanNiqqudChars(x) if (pd.isnull(x)) == False else x)
        self.verb_conj_future_and = self.verb_conj_future_and.applymap(
            lambda x: self._cleanNiqqudChars(x) if (pd.isnull(x)) == False else x)
        self.verb_conj_future_that = self.verb_conj_future_that.applymap(
            lambda x: self._cleanNiqqudChars(x) if (pd.isnull(x)) == False else x)

    def mergeVerbPresent(self):
        self.database = self.database.merge(self.verb_conj_present, left_on=['id'], right_index=True, how='outer')
        self.database = self.database.merge(self.verb_conj_present_and, left_on=['id'], right_index=True, how='outer')
        self.database = self.database.merge(self.verb_conj_present_that, left_on=['id'], right_index=True, how='outer')

    def mergeVerbPast(self):
        self.database = self.database.merge(self.verb_conj_past, left_on=['id'], right_index=True, how='outer')
        self.database = self.database.merge(self.verb_conj_past_and, left_on=['id'], right_index=True, how='outer')
        self.database = self.database.merge(self.verb_conj_past_that, left_on=['id'], right_index=True, how='outer')
    def mergeVerbFuture(self):
        self.database = self.database.merge(self.verb_conj_future, left_on=['id'], right_index=True, how='outer')
        self.database = self.database.merge(self.verb_conj_future_and, left_on=['id'], right_index=True, how='outer')
        self.database = self.database.merge(self.verb_conj_future_that, left_on=['id'], right_index=True, how='outer')

    def mergeNounPlurals(self):
        self.database = self.database.merge(self.noun_plural_db[['id', 'plural_state']], on=['id'], how='outer')

        print(self.database.head())

    def _createChaserDict(self, sel_dict: dict, key, value):
        # Creating a function that creates a dictionary key and then adding in all the chasers relevant to that dict key
        sel_dict.setdefault(key, []).append('<idx:iform value="' + str(value) + '" />')

    def extractForm(self):
        self.database['part_of_speech_simplified'] = self.database['part_of_speech'].apply(
            lambda x: re.match(r"(\w+)", x)[0] if re.match(r"(\w+)", x) is not None else '-')

    def createDefInflection(self):
        from_value = str('מ')
        the_value = str('ה')
        to_value = str('ל')
        in_value = str('ב')
        that_value = str('ש')
        self.database['inflection_the'] = self.database[['word', 'part_of_speech_simplified']].apply(
            lambda x: str(the_value + str(x['word'])) if x['part_of_speech_simplified'] == 'Noun' else np.nan,
            axis=1)
        self.database['inflection_from'] = self.database[['word', 'part_of_speech_simplified']].apply(
            lambda x: str(from_value + the_value + str(x['word'])) if x['part_of_speech_simplified'] == 'Noun' else
            np.nan,
            axis=1)
        self.database['inflection_to'] = self.database[['word', 'part_of_speech_simplified']].apply(
            lambda x: str(to_value + str(x['word'])) if x['part_of_speech_simplified'] == 'Noun' else np.nan,
            axis=1)
        self.database['inflection_in'] = self.database[['word', 'part_of_speech_simplified']].apply(
            lambda x: str(in_value + str(x['word'])) if x['part_of_speech_simplified'] == 'Noun' else np.nan,
            axis=1)
        self.database['inflection_that'] = self.database[['word', 'part_of_speech_simplified']].apply(
            lambda x: str(that_value + the_value + str(x['word'])) if x['part_of_speech_simplified'] == 'Noun' else
            np.nan,
            axis=1)

        self.database['inflection_the_plural'] = self.database[['plural_state', 'part_of_speech_simplified']].apply(
            lambda x: str(the_value + str(x['plural_state'])) if (x['part_of_speech_simplified'] == 'Noun'
                                                                  and pd.isnull(
                        x['plural_state']) == False) else np.nan,
            axis=1)
        self.database['inflection_from_plural'] = self.database[['plural_state', 'part_of_speech_simplified']].apply(
            lambda x: str(from_value + the_value + str(x['plural_state'])) if (x['part_of_speech_simplified'] == 'Noun'
                                                                               and pd.isnull(
                        x['plural_state']) == False)
            else np.nan,
            axis=1)
        self.database['inflection_to_plural'] = self.database[['plural_state', 'part_of_speech_simplified']].apply(
            lambda x: str(to_value + str(x['plural_state'])) if (x['part_of_speech_simplified'] == 'Noun'
                                                                 and pd.isnull(x['plural_state']) == False) else np.nan,
            axis=1)
        self.database['inflection_in_plural'] = self.database[['plural_state', 'part_of_speech_simplified']].apply(
            lambda x: str(in_value + str(x['plural_state'])) if (
                    x['part_of_speech_simplified'] == 'Noun' and pd.isnull(x['plural_state']) == False) else np.nan,
            axis=1)
        self.database['inflection_that_plural'] = self.database[['plural_state', 'part_of_speech_simplified']].apply(
            lambda x: str(that_value + the_value + str(x['plural_state'])) if (x['part_of_speech_simplified'] == 'Noun'
                                                                               and pd.isnull(
                        x['plural_state']) == False) else np.nan, axis=1)

        print(self.database['inflection_the'])



    def dictVerbCreat(self, table, dictionary):
        table = table.reset_index()
        for index, rows in table.iterrows():
            for i in list(table.columns.difference(['id'])):
                if pd.isnull(rows[(i)]) == False:
                    self._createChaserDict(dictionary, rows['id'], rows[str(i)])

    def verbs_dictionary(self):
        self.dictVerbCreat(self.verb_conj_present,self.verb_conj_present_chaser)
        self.dictVerbCreat(self.verb_conj_present_and, self.verb_conj_present_and_chaser)
        self.dictVerbCreat(self.verb_conj_present_that, self.verb_conj_present_that_chaser)

        self.dictVerbCreat(self.verb_conj_past,self.verb_conj_past_chaser)
        self.dictVerbCreat(self.verb_conj_past_and, self.verb_conj_past_and_chaser)
        self.dictVerbCreat(self.verb_conj_past_that, self.verb_conj_past_that_chaser)

        self.dictVerbCreat(self.verb_conj_future, self.verb_conj_future_chaser)
        self.dictVerbCreat(self.verb_conj_future_and, self.verb_conj_future_and_chaser)
        self.dictVerbCreat(self.verb_conj_future_that, self.verb_conj_future_that_chaser)

        list_dict = [self.verb_conj_present_chaser, self.verb_conj_present_and_chaser,
                     self.verb_conj_present_that_chaser, self.verb_conj_past_chaser,
                     self.verb_conj_past_and_chaser, self.verb_conj_past_that_chaser,
                     self.verb_conj_future_chaser, self.verb_conj_future_and_chaser,
                     self.verb_conj_present_that_chaser]
        self.allverbs = {}

        for i in range(len(list_dict)):
            self.allverbs['dict_' + str(i)] = list_dict[i]




    def createSimpleDf(self):
        self.simplifiedDf_list = list(
            ['id', 'word', 'hebrew_pronunciation', 'part_of_speech_simplified', 'meaning', 'inflection_the',
             'inflection_to', 'inflection_from'
                , 'inflection_in', 'inflection_that',
             'plural_state', 'inflection_the_plural', 'inflection_to_plural',
             'inflection_from_plural'
                , 'inflection_in_plural', 'inflection_that_plural']) + self.list_present_verb_columns + \
                                 self.list_past_verb_columns \
                                 + self.verb_conj_past_and_columns + self.verb_conj_past_that_columns + \
                                 self.verb_conj_present_and_columns + self.verb_conj_present_that_columns + \
                                self.verb_conj_present_that_columns + self.verb_conj_future_and_columns + \
                                 self.list_verb_future_columns
        self.csv2html_df = self.database[self.simplifiedDf_list].copy()
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

        if pospeech is False and pd.isnull(row['hebrew_word_present_singular_masculine']) is False:
            fname.write("""
<idx:entry name="hebrew" scriptable="yes" spell="yes">
<idx:short><a id="{id}"></a>
<idx:orth value="{word}"><p><b>{word}</b>   |   <i>{pronunciation}</i></p>
<idx:infl inflgrp="{inflgrp}">""".format(id=row['id'], word=row['word'], meaning=row['meaning'], inflgrp=row['part_of_speech_simplified'],
            pronunciation=row['hebrew_pronunciation']))

            for key in self.allverbs.keys():
                try:
                    for inflection in self.allverbs[str(key)][row['id']]:
                        fname.write(
"""{inflection}
""".format(inflection=inflection))
                except KeyError:
                    continue

            fname.write("""
            </idx:infl >
            </idx:orth>
            <p>{meaning}</p>
            </idx:short>
            </idx:entry>
            <hr style="width:50%", size="3", color=black>
            """.format(meaning=row['meaning']))


#             fname.write(
#                 """
# <idx:entry name="hebrew" scriptable="yes" spell="yes">
# <idx:short><a id="{id}"></a>
# <idx:orth value="{word}"><p><b>{word}</b>&nbsp;<hr class="vertical" />&nbsp;<i>{pronunciation}</i></p>
# <idx:infl inflgrp="{inflgrp}">
# <idx:iform value="{hebrew_word_present_singular_masculine}"></idx:iform>
# <idx:iform value="{hebrew_word_present_singular_feminine}"></idx:iform>
# <idx:iform value="{hebrew_word_present_plural_masculine}"></idx:iform>
# <idx:iform value="{hebrew_word_present_plural_feminine}"></idx:iform>
#
# <idx:iform value="{hebrew_word_past_1_singular_masculine}"></idx:iform>
# <idx:iform value="{hebrew_word_past_1_singular_feminine}"></idx:iform>
# <idx:iform value="{hebrew_word_past_1_plural_masculine}"></idx:iform>
# <idx:iform value="{hebrew_word_past_1_plural_feminine}"></idx:iform>
#
# <idx:iform value="{hebrew_word_past_2_singular_masculine}"></idx:iform>
# <idx:iform value="{hebrew_word_past_2_singular_feminine}"></idx:iform>
# <idx:iform value="{hebrew_word_past_2_plural_masculine}"></idx:iform>
# <idx:iform value="{hebrew_word_past_2_plural_feminine}"></idx:iform>
#
# <idx:iform value="{hebrew_word_past_3_singular_masculine}"></idx:iform>
# <idx:iform value="{hebrew_word_past_3_singular_feminine}"></idx:iform>
# <idx:iform value="{hebrew_word_past_3_plural_masculine}"></idx:iform>
# <idx:iform value="{hebrew_word_past_3_plural_feminine}"></idx:iform>
#
# <idx:iform value="{hebrew_word_present_singular_masculine_andform}"></idx:iform>
# <idx:iform value="{hebrew_word_present_singular_feminine_andform}"></idx:iform>
# <idx:iform value="{hebrew_word_present_plural_masculine_andform}"></idx:iform>
# <idx:iform value="{hebrew_word_present_plural_feminine_andform}"></idx:iform>
#
# <idx:iform value="{hebrew_word_past_1_singular_masculine_andform}"></idx:iform>
# <idx:iform value="{hebrew_word_past_1_singular_feminine_andform}"></idx:iform>
# <idx:iform value="{hebrew_word_past_1_plural_masculine_andform}"></idx:iform>
# <idx:iform value="{hebrew_word_past_1_plural_feminine_andform}"></idx:iform>
#
# <idx:iform value="{hebrew_word_past_2_singular_masculine_andform}"></idx:iform>
# <idx:iform value="{hebrew_word_past_2_singular_feminine_andform}"></idx:iform>
# <idx:iform value="{hebrew_word_past_2_plural_masculine_andform}"></idx:iform>
# <idx:iform value="{hebrew_word_past_2_plural_feminine_andform}"></idx:iform>
#
# <idx:iform value="{hebrew_word_past_3_singular_masculine_andform}"></idx:iform>
# <idx:iform value="{hebrew_word_past_3_singular_feminine_andform}"></idx:iform>
# <idx:iform value="{hebrew_word_past_3_plural_masculine_andform}"></idx:iform>
# <idx:iform value="{hebrew_word_past_3_plural_feminine_andform}"></idx:iform>
#
#
# <idx:iform value="{hebrew_word_present_singular_masculine_thatform}"></idx:iform>
# <idx:iform value="{hebrew_word_present_singular_feminine_thatform}"></idx:iform>
# <idx:iform value="{hebrew_word_present_plural_masculine_thatform}"></idx:iform>
# <idx:iform value="{hebrew_word_present_plural_feminine_thatform}"></idx:iform>
#
# <idx:iform value="{hebrew_word_past_1_singular_masculine_thatform}"></idx:iform>
# <idx:iform value="{hebrew_word_past_1_singular_feminine_thatform}"></idx:iform>
# <idx:iform value="{hebrew_word_past_1_plural_masculine_thatform}"></idx:iform>
# <idx:iform value="{hebrew_word_past_1_plural_feminine_thatform}"></idx:iform>
#
# <idx:iform value="{hebrew_word_past_2_singular_masculine_thatform}"></idx:iform>
# <idx:iform value="{hebrew_word_past_2_singular_feminine_thatform}"></idx:iform>
# <idx:iform value="{hebrew_word_past_2_plural_masculine_thatform}"></idx:iform>
# <idx:iform value="{hebrew_word_past_2_plural_feminine_thatform}"></idx:iform>
#
# <idx:iform value="{hebrew_word_past_3_singular_masculine_thatform}"></idx:iform>
# <idx:iform value="{hebrew_word_past_3_singular_feminine_thatform}"></idx:iform>
# <idx:iform value="{hebrew_word_past_3_plural_masculine_thatform}"></idx:iform>
# <idx:iform value="{hebrew_word_past_3_plural_feminine_thatform}"></idx:iform>
#
#
# </idx:infl>
# </idx:orth>
# <p>{meaning}</p>
# </idx:short>
# </idx:entry>
# <hr style="width:50%", size="3", color=black>
# """.format(id=row['id'], word=row['word'], meaning=row['meaning'], inflgrp=row['part_of_speech_simplified'],
#            pronunciation=row['hebrew_pronunciation'],
#
#            hebrew_word_present_singular_masculine=row['hebrew_word_present_singular_masculine'],
#            hebrew_word_present_singular_feminine=row['hebrew_word_present_singular_feminine'],
#            hebrew_word_present_plural_masculine=row['hebrew_word_present_plural_masculine'],
#            hebrew_word_present_plural_feminine=row['hebrew_word_present_plural_feminine'],
#
#            hebrew_word_past_1_singular_masculine=row['hebrew_word_past_1_singular_masculine'],
#            hebrew_word_past_1_singular_feminine=row['hebrew_word_past_1_singular_feminine'],
#            hebrew_word_past_1_plural_masculine=row['hebrew_word_past_1_plural_masculine'],
#            hebrew_word_past_1_plural_feminine=row['hebrew_word_past_1_plural_feminine'],
#
#            hebrew_word_past_2_singular_masculine=row['hebrew_word_past_2_singular_masculine'],
#            hebrew_word_past_2_singular_feminine=row['hebrew_word_past_2_singular_feminine'],
#            hebrew_word_past_2_plural_masculine=row['hebrew_word_past_2_plural_masculine'],
#            hebrew_word_past_2_plural_feminine=row['hebrew_word_past_2_plural_feminine'],
#
#            hebrew_word_past_3_singular_masculine=row['hebrew_word_past_3_singular_masculine'],
#            hebrew_word_past_3_singular_feminine=row['hebrew_word_past_3_singular_feminine'],
#            hebrew_word_past_3_plural_masculine=row['hebrew_word_past_3_plural_masculine'],
#            hebrew_word_past_3_plural_feminine=row['hebrew_word_past_3_plural_feminine'],
#
#            hebrew_word_present_singular_masculine_andform=row['hebrew_word_present_singular_masculine_andform'],
#            hebrew_word_present_singular_feminine_andform=row['hebrew_word_present_singular_feminine_andform'],
#            hebrew_word_present_plural_masculine_andform=row['hebrew_word_present_plural_masculine_andform'],
#            hebrew_word_present_plural_feminine_andform=row['hebrew_word_present_plural_feminine_andform'],
#
#            hebrew_word_past_1_singular_masculine_andform=row['hebrew_word_past_1_singular_masculine_andform'],
#            hebrew_word_past_1_singular_feminine_andform=row['hebrew_word_past_1_singular_feminine_andform'],
#            hebrew_word_past_1_plural_masculine_andform=row['hebrew_word_past_1_plural_masculine_andform'],
#            hebrew_word_past_1_plural_feminine_andform=row['hebrew_word_past_1_plural_feminine_andform'],
#
#            hebrew_word_past_2_singular_masculine_andform=row['hebrew_word_past_2_singular_masculine_andform'],
#            hebrew_word_past_2_singular_feminine_andform=row['hebrew_word_past_2_singular_feminine_andform'],
#            hebrew_word_past_2_plural_masculine_andform=row['hebrew_word_past_2_plural_masculine_andform'],
#            hebrew_word_past_2_plural_feminine_andform=row['hebrew_word_past_2_plural_feminine_andform'],
#
#            hebrew_word_past_3_singular_masculine_andform=row['hebrew_word_past_3_singular_masculine_andform'],
#            hebrew_word_past_3_singular_feminine_andform=row['hebrew_word_past_3_singular_feminine_andform'],
#            hebrew_word_past_3_plural_masculine_andform=row['hebrew_word_past_3_plural_masculine_andform'],
#            hebrew_word_past_3_plural_feminine_andform=row['hebrew_word_past_3_plural_feminine_andform'],
#
#            hebrew_word_present_singular_masculine_thatform=row['hebrew_word_present_singular_masculine_thatform'],
#            hebrew_word_present_singular_feminine_thatform=row['hebrew_word_present_singular_feminine_thatform'],
#            hebrew_word_present_plural_masculine_thatform=row['hebrew_word_present_plural_masculine_thatform'],
#            hebrew_word_present_plural_feminine_thatform=row['hebrew_word_present_plural_feminine_thatform'],
#
#            hebrew_word_past_1_singular_masculine_thatform=row['hebrew_word_past_1_singular_masculine_thatform'],
#            hebrew_word_past_1_singular_feminine_thatform=row['hebrew_word_past_1_singular_feminine_thatform'],
#            hebrew_word_past_1_plural_masculine_thatform=row['hebrew_word_past_1_plural_masculine_thatform'],
#            hebrew_word_past_1_plural_feminine_thatform=row['hebrew_word_past_1_plural_feminine_thatform'],
#
#            hebrew_word_past_2_singular_masculine_thatform=row['hebrew_word_past_2_singular_masculine_thatform'],
#            hebrew_word_past_2_singular_feminine_thatform=row['hebrew_word_past_2_singular_feminine_thatform'],
#            hebrew_word_past_2_plural_masculine_thatform=row['hebrew_word_past_2_plural_masculine_thatform'],
#            hebrew_word_past_2_plural_feminine_thatform=row['hebrew_word_past_2_plural_feminine_thatform'],
#
#            hebrew_word_past_3_singular_masculine_thatform=row['hebrew_word_past_3_singular_masculine_thatform'],
#            hebrew_word_past_3_singular_feminine_thatform=row['hebrew_word_past_3_singular_feminine_thatform'],
#            hebrew_word_past_3_plural_masculine_thatform=row['hebrew_word_past_3_plural_masculine_thatform'],
#            hebrew_word_past_3_plural_feminine_thatform=row['hebrew_word_past_3_plural_feminine_thatform']
#
#            )
#             )
        elif pospeech is True:
            fname.write(
                """
<idx:entry name="hebrew" scriptable="yes" spell="yes">
<idx:short><a id="{id}"></a>
<idx:orth value="{word}"><p><b>{word}</b>   |   <i>{pronunciation}</i></p>
<idx:infl inflgrp="{inflgrp}"> 
<idx:iform value="{inflection_the}"></idx:iform>
<idx:iform value="{inflection_from}"></idx:iform>
<idx:iform value="{inflection_to}"></idx:iform>
<idx:iform value="{inflection_in}"></idx:iform>
<idx:iform value="{inflection_that}"></idx:iform>
<idx:iform value="{inflection_the_plural}"></idx:iform>
<idx:iform value="{inflection_from_plural}"></idx:iform>
<idx:iform value="{inflection_to_plural}"></idx:iform>
<idx:iform value="{inflection_in_plural}"></idx:iform>
<idx:iform value="{inflection_that_plural}"></idx:iform>
</idx:infl> 
</idx:orth>
<p>{meaning}</p>
</idx:short>
</idx:entry>
<hr style="width:50%", size="3", color=black> 
""".format(id=row['id'], word=row['word'], meaning=row['meaning'], inflgrp=row['part_of_speech_simplified'],
           pronunciation=row['hebrew_pronunciation'],

           inflection_the=row['inflection_the'],
           inflection_from=row['inflection_from'],
           inflection_to=row['inflection_to'],
           inflection_in=row['inflection_in'],
           inflection_that=row['inflection_that'],
           inflection_the_plural=row['inflection_the_plural'],
           inflection_from_plural=row['inflection_from_plural'],
           inflection_to_plural=row['inflection_to_plural'],
           inflection_in_plural=row['inflection_in_plural'],
           inflection_that_plural=row['inflection_that_plural']
           ))
        elif pospeech is False:
            fname.write(
                """
<idx:entry name="hebrew" scriptable="yes" spell="yes">
<idx:short><a id="{id}"></a>
<idx:orth value="{word}"><p><b>{word}</b>   |   <i>{pronunciation}</i></p>

<idx:infl inflgrp="{inflgrp}">
</idx:infl>
</idx:orth> 
<p>{meaning}</p>
</idx:short>
</idx:entry>
<hr style="width:50%", size="3", color=black> 
""".format(id=row['id'], word=row['word'], meaning=row['meaning'], inflgrp=row['part_of_speech_simplified'],
           pronunciation=row['hebrew_pronunciation'])
            )

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
            with open(fname, 'w', encoding="utf-8") as f:
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
