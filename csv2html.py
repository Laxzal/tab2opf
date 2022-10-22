'''

Simple one
id  |   word    |   meaning

'''
import contextlib
import os
import re
import sys

import emoji
import numpy as np
import pandas as pd


# /Users/calvin/Library/CloudStorage/OneDrive-Personal/Documents/hebrew_dict

class SimpleCSV2HTML:

    def __init__(self, database_fname):

        self.database_fname = database_fname
        self.database = None
        self.csv_noun_plural = r"/Users/calvin/Documents/hebrew_dictionary/pealim_noun_db.csv"
        self.list_file_names = []
        self.verb_conj_present_file = r"/Users/calvin/Documents/hebrew_dictionary/pealim_verb_present_table_db.csv"
        self.verb_conj_past_file = r"/Users/calvin/Documents/hebrew_dictionary/pealim_verb_past_table_db.csv"
        self.verb_conj_future_file = r"/Users/calvin/Documents" \
                                     r"/hebrew_dictionary/pealim_verb_future_table_db.csv"
        self.adjective_db = "pealim_adjective_table_db.csv"
        self.pronomial_file = "pealim_pronomial_db.csv"
        self.noun_inflection_group = ['plural_state', 'infl_from', 'infl_to', 'infl_in', 'infl_that', 'infl_the_plural',
                                      'infl_from_plural', 'infl_to_plural', 'infl_in_plural', 'infl_that_plural',
                                      'plural_construct_state',
                                      'single_construct_state']
        self.verb_inflection_group = ['chaser', 'infl_when_cond', 'infl_that', 'infl_and', 'infl_when_cond_chaser',
                                      'infl_that_chaser', 'infl_and_chaser']
        self.from_value = str('מ')
        self.the_value = str('ה')
        self.to_value = str('ל')
        self.in_value = str('ב')
        self.that_value = str('ש')
        self.as_value = str('כ')
        self.and_value = str('ו')
        self.verb_conj_present_filtered = None
        self.verb_conj_past_filtered = None
        self.verb_conj_future_filtered = None

        self.remove_conv_emoji = r"(:)(.*?)(:)"
        # Automatic Functions to Run
        self.importDbFile()

    def importDbFile(self):
        self.database = pd.read_csv(self.database_fname)  # encoding="ISO-8859-8", error_bad_lines=)
        self.database['meaning'] = self.database['meaning'].apply(
            lambda x: emoji.demojize(x).strip())
        self.database['meaning'] = self.database['meaning'].apply(
            lambda x: re.sub(self.remove_conv_emoji, "", x).strip())
        print(self.database.head())

    def importNounPluralDb(self):
        self.noun_plural_db = pd.read_csv(self.csv_noun_plural)
        # self.noun_plural_db = self.noun_plural_db.where(pd.notnull(self.noun_plural_db), "NaN")
        # TODO add inflections onto nouns
    def importAdjectivesDb(self):
        self.adjectives_df = pd.read_csv(self.adjective_db)
        #Need to clean the niqqud
        self.adjectives_df['hebrew_word'] = self.adjectives_df['hebrew_word'].apply(lambda x: self._cleanNiqqudChars(x)
                                                                                   if not pd.isnull(x) else x)
        self.adjectives_df['gender'] = np.where(
            self.adjectives_df[['id', 'form', 'hebrew_word', 'english_word', 'chaser']].duplicated(
                keep=False), str('both'), self.adjectives_df['gender'])
        self.adjectives_df = self.adjectives_df.drop_duplicates(
            ['id', 'form', 'hebrew_word', 'english_word', 'chaser'])
        self.adjectives_df.drop(columns=['pronunciation','english_word'], inplace=True)
        self.adjectives_df_pivot = self.adjectives_df.pivot(index=['id'], columns=['gender', 'form'])
        self.adjective_columns = ['_'.join(tup) for tup in self.adjectives_df_pivot.columns.values]
        self.adjectives_df_pivot.columns = self.adjective_columns
        for heading in list(self.adjectives_df_pivot.columns):
            self.adjectives_df_pivot['theinfl_' +str(heading)] = self.adjectives_df_pivot[heading].apply(lambda x: "{}{}".format(self.the_value,
                                                                                         x) if not pd.isnull(x) else np.nan)

        self.database = self.database.merge(self.adjectives_df_pivot, left_on='id', right_index=True, how='outer')
        self.adj_infl = list(self.adjectives_df_pivot.columns)

    def importVerbConjPresent_ver2(self):
        self.verb_conj_present_ = pd.read_csv(self.verb_conj_present_file)
        self.verb_conj_present_['english_word'] = self.verb_conj_present_['english_word'].apply(
            lambda x: emoji.demojize(x).strip())
        self.verb_conj_present_['english_word'] = self.verb_conj_present_['english_word'].apply(
            lambda x: re.sub(self.remove_conv_emoji, "", x).strip())

        self.verb_conj_present_['gender'] = np.where(
            self.verb_conj_present_[['id', 'verb_form', 'person', 'hebrew_word', 'english_word', 'chaser']].duplicated(
                keep=False), str('both'), self.verb_conj_present_['gender'])
        self.verb_conj_present_ = self.verb_conj_present_.drop_duplicates(
            ['id', 'verb_form', 'person', 'hebrew_word', 'english_word', 'chaser'])

        self.verb_conj_present_ = self.verb_conj_present_.merge(self.database, left_on='id', right_on='id')
        self.verb_conj_present_filtered = self.verb_conj_present_[['id', 'hebrew_word', 'english_word', 'chaser',
                                                                   'word', 'hebrew_pronunciation',
                                                                   'part_of_speech_simplified', 'meaning', 'gender',
                                                                   'pattern']]
        self.verb_conj_present_filtered['niqqud'] = self.verb_conj_present_filtered['hebrew_word'].copy()
        self.verb_conj_present_filtered.rename(columns={'word': 'infinitive'}, inplace=True)

    def importVerbConjPast_ver2(self):
        self.verb_conj_past_ = pd.read_csv(self.verb_conj_past_file)
        self.verb_conj_past_['english_word'] = self.verb_conj_past_['english_word'].apply(
            lambda x: emoji.demojize(x).strip())
        self.verb_conj_past_['english_word'] = self.verb_conj_past_['english_word'].apply(
            lambda x: re.sub(self.remove_conv_emoji, "", x).strip())

        self.verb_conj_past_['gender'] = np.where(
            self.verb_conj_past_[['id', 'verb_form', 'person', 'hebrew_word', 'english_word', 'chaser']].duplicated(
                keep=False), str('both'), self.verb_conj_past_['gender'])
        self.verb_conj_past_ = self.verb_conj_past_.drop_duplicates(
            ['id', 'verb_form', 'person', 'hebrew_word', 'english_word', 'chaser'])

        self.verb_conj_past_ = self.verb_conj_past_.merge(self.database, left_on='id', right_on='id')
        self.verb_conj_past_filtered = self.verb_conj_past_[['id', 'hebrew_word', 'english_word', 'chaser', 'word',
                                                             'hebrew_pronunciation', 'part_of_speech_simplified',
                                                             'meaning',
                                                             'gender', 'pattern']]
        self.verb_conj_past_filtered['niqqud'] = self.verb_conj_past_filtered['hebrew_word'].copy()
        self.verb_conj_past_filtered.rename(columns={'word': 'infinitive'}, inplace=True)

    def importVerbConjFut_ver(self):
        self.verb_conj_future_ = pd.read_csv(self.verb_conj_future_file)
        self.verb_conj_future_['english_word'] = self.verb_conj_future_['english_word'].apply(
            lambda x: emoji.demojize(x).strip())
        self.verb_conj_future_['english_word'] = self.verb_conj_future_['english_word'].apply(
            lambda x: re.sub(self.remove_conv_emoji, "", x).strip())

        self.verb_conj_future_['gender'] = np.where(
            self.verb_conj_future_[['id', 'verb_form', 'person', 'hebrew_word', 'english_word', 'chaser']].duplicated(
                keep=False), str('both'), self.verb_conj_future_['gender'])
        self.verb_conj_future_ = self.verb_conj_future_.drop_duplicates(
            ['id', 'verb_form', 'person', 'hebrew_word', 'english_word', 'chaser'])

        self.verb_conj_future_ = self.verb_conj_future_.merge(self.database, left_on='id', right_on='id')
        self.verb_conj_future_filtered = self.verb_conj_future_[
            ['id', 'hebrew_word', 'english_word', 'chaser', 'word', 'hebrew_pronunciation', 'part_of_speech_simplified',
             'meaning',
             'gender', 'pattern']]
        self.verb_conj_future_filtered['niqqud'] = self.verb_conj_future_filtered['hebrew_word'].copy()
        self.verb_conj_future_filtered.rename(columns={'word': 'infinitive'}, inplace=True)

    def importPronomialNoun(self):
        self.pronomial_df = pd.read_csv(self.pronomial_file)
        self.pronomial_df['hebrew_word'] = self.pronomial_df['hebrew_word'].apply(self._cleanNiqqudChars)
        self.pronomial_df['english_word'] = self.pronomial_df['english_word'].apply(
            lambda x: emoji.demojize(x).strip())
        self.pronomial_df['english_word'] = self.pronomial_df['english_word'].apply(
            lambda x: re.sub(self.remove_conv_emoji, "", x).strip())


        self.pronomial_df['gender'] = np.where(
            self.pronomial_df[['id', 'noun_form', 'person', 'hebrew_word', 'english_word', 'chaser']].duplicated(
                keep=False), str('both'), self.pronomial_df['gender'])
        self.pronomial_df = self.pronomial_df.drop_duplicates(
            ['id', 'noun_form', 'person', 'hebrew_word', 'english_word', 'chaser'])

        self.pronomial_df['part_of_speech_simplified'] = "Pronomial Noun"



    def cleanVerbWord(self):
        self.verb_conj_present_filtered['hebrew_word'] = self.verb_conj_present_filtered['hebrew_word'].apply(
            self._cleanNiqqudChars)
        self.verb_conj_past_filtered['hebrew_word'] = self.verb_conj_past_['hebrew_word'].apply(
            self._cleanNiqqudChars)
        self.verb_conj_future_filtered['hebrew_word'] = self.verb_conj_future_filtered['hebrew_word'].apply(
            self._cleanNiqqudChars)

    def _inflectionVerbs(self, dataframe):

        dataframe['infl_and'] = dataframe['hebrew_word'].apply(lambda x: "{}{}".format(self.and_value,
                                                                                       x))
        dataframe['infl_that'] = dataframe['hebrew_word'].apply(lambda x: "{}{}".format(self.that_value,
                                                                                        x))
        dataframe['infl_when_cond'] = dataframe['hebrew_word'].apply(lambda x: "{}{}{}".format(self.as_value,
                                                                                               self.that_value,
                                                                                               x))
        dataframe['infl_and_chaser'] = dataframe['chaser'].apply(lambda x: "{}{}".format(self.and_value,
                                                                                         x) if pd.isnull(
            x) == False else np.nan)
        dataframe['infl_that_chaser'] = dataframe['chaser'].apply(lambda x: "{}{}".format(self.that_value,
                                                                                          x) if pd.isnull(
            x) == False else np.nan)
        dataframe['infl_when_cond_chaser'] = dataframe['chaser'].apply(lambda x: "{}{}{}".format(self.as_value,
                                                                                                 self.that_value,
                                                                                                 x) if pd.isnull(
            x) == False else np.nan)

    def inflectVerbs(self):
        self.list_of_verb_databases = [self.verb_conj_present_filtered, self.verb_conj_past_filtered,
                                       self.verb_conj_future_filtered]
        for verb_file in self.list_of_verb_databases:
            self._inflectionVerbs(verb_file)



    def _cleanNiqqudChars(self, my_string):
        return ''.join(['' if 1456 <= ord(c) <= 1479 else c for c in my_string])

    def hebrewWordsClean(self, column_name: str = 'word'):
        self.database[str(column_name)] = self.database[str(column_name)].apply(self._cleanNiqqudChars)
        print(self.database.head())

    def hebrewPluralClean(self):
        self.noun_plural_db['plural_state'] = self.noun_plural_db['plural_state'].apply(
            lambda x: self._cleanNiqqudChars(x) if not pd.isnull(x) else x)
        self.noun_plural_db['single_construct_state'] = self.noun_plural_db['single_construct_state'].apply(
            lambda x: self._cleanNiqqudChars(x) if not pd.isnull(x) else x)
        self.noun_plural_db['plural_construct_state'] = self.noun_plural_db['plural_construct_state'].apply(
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
        self.database = self.database.merge(self.noun_plural_db[['id', 'plural_state','plural_construct_state',
                                                                 'single_construct_state']], on=['id'], how='outer')

        print(self.database.head())

    def _createChaserDict(self, sel_dict: dict, key, value):
        # Creating a function that creates a dictionary key and then adding in all the chasers relevant to that dict key
        sel_dict.setdefault(key, []).append('<idx:iform value="' + str(value) + '" />')

    def extractPattern(self):
        regex = r"(?<=\s)[^\W\d_]+(?:['.][^\W\d_]+)*(?![^\W\d_])"
        self.database['pattern'] = self.database['part_of_speech'].apply(
            lambda x: re.search(regex, x)[0] if
            re.search(regex, x) is not None else np.nan
        )
        self.database['pattern'].mask(
            (self.database['pattern'] == 'feminine') | (self.database['pattern'] == 'masculine'), np.nan, inplace=True)

    def extractForm(self):
        self.database['part_of_speech_simplified'] = self.database['part_of_speech'].apply(
            lambda x: re.match(r"(\w+)", x)[0] if re.match(r"(\w+)", x) is not None else np.nan)

    def createDefInflection(self):
        from_value = str('מ')
        the_value = str('ה')
        to_value = str('ל')
        in_value = str('ב')
        that_value = str('ש')
        self.database['infl_the'] = self.database[['word', 'part_of_speech_simplified']].apply(
            lambda x: str(the_value + str(x['word'])) if x['part_of_speech_simplified'] != 'Verb' else np.nan,
            axis=1)
        self.database['infl_from'] = self.database[['word', 'part_of_speech_simplified']].apply(
            lambda x: str(from_value + the_value + str(x['word'])) if x['part_of_speech_simplified'] != 'Verb' else
            np.nan,
            axis=1)
        self.database['infl_to'] = self.database[['word', 'part_of_speech_simplified']].apply(
            lambda x: str(to_value + str(x['word'])) if x['part_of_speech_simplified'] != 'Verb' else np.nan,
            axis=1)
        self.database['infl_in'] = self.database[['word', 'part_of_speech_simplified']].apply(
            lambda x: str(in_value + str(x['word'])) if x['part_of_speech_simplified'] != 'Verb' else np.nan,
            axis=1)
        self.database['infl_that'] = self.database[['word', 'part_of_speech_simplified']].apply(
            lambda x: str(that_value + the_value + str(x['word'])) if x['part_of_speech_simplified'] != 'Verb' else
            np.nan,
            axis=1)

        self.database['infl_the_plural'] = self.database[['plural_state', 'part_of_speech_simplified']].apply(
            lambda x: str(the_value + str(x['plural_state'])) if (x['part_of_speech_simplified'] == 'Noun'
                                                                  and pd.isnull(
                        x['plural_state']) == False) else np.nan,
            axis=1)
        self.database['infl_from_plural'] = self.database[['plural_state', 'part_of_speech_simplified']].apply(
            lambda x: str(from_value + the_value + str(x['plural_state'])) if (x['part_of_speech_simplified'] == 'Noun'
                                                                               and pd.isnull(
                        x['plural_state']) == False)
            else np.nan,
            axis=1)
        self.database['infl_to_plural'] = self.database[['plural_state', 'part_of_speech_simplified']].apply(
            lambda x: str(to_value + str(x['plural_state'])) if (x['part_of_speech_simplified'] == 'Noun'
                                                                 and pd.isnull(x['plural_state']) == False) else np.nan,
            axis=1)
        self.database['infl_in_plural'] = self.database[['plural_state', 'part_of_speech_simplified']].apply(
            lambda x: str(in_value + str(x['plural_state'])) if (
                    x['part_of_speech_simplified'] == 'Noun' and pd.isnull(x['plural_state']) == False) else np.nan,
            axis=1)
        self.database['infl_that_plural'] = self.database[['plural_state', 'part_of_speech_simplified']].apply(
            lambda x: str(that_value + the_value + str(x['plural_state'])) if (x['part_of_speech_simplified'] == 'Noun'
                                                                               and pd.isnull(
                        x['plural_state']) == False) else np.nan, axis=1)

        print(self.database['infl_the'])

    def createSimpleDf(self):
        self.simplifiedDf_list = list(
            ['id', 'word', 'hebrew_pronunciation', 'part_of_speech_simplified', 'meaning', 'infl_the',
             'infl_to', 'infl_from'
                , 'infl_in', 'infl_that',
             'plural_state', 'infl_the_plural', 'infl_to_plural',
             'infl_from_plural'
                , 'infl_in_plural', 'infl_that_plural', 'pattern','plural_construct_state','single_construct_state']) + self.adj_infl
        self.csv2html_df = self.database[self.simplifiedDf_list].copy()
        print(self.csv2html_df.head())

    @contextlib.contextmanager


    def _writekeysLoop(self, fname, index, row, pospeech: bool):

        fname.write(
            """
<idx:entry name="hebrew" scriptable="yes" spell="yes">
<idx:short><a id="{id}"></a>
<idx:orth value="{word}"><p><b>{word}</b>&emsp;|&emsp;<i>{pronunciation}</i></p>
""".format(id=index, word=row['hebrew_word'], pronunciation=row['hebrew_pronunciation'],
           inflgrp=row['part_of_speech_simplified']))
        if not pd.isnull(row[self.noun_inflection_group]).all():
            fname.write(
                """<idx:infl>
""")

        for noun_inflection in self.noun_inflection_group:
            if not pd.isnull(row[str(noun_inflection)]):
                        fname.write(
                            """<idx:iform value="{inflgrp}" />
""".format(inflgrp=row[str(noun_inflection)]))

        if not pd.isnull(row[self.noun_inflection_group]).all():
            fname.write(
                """</idx:infl>""")

        fname.write("""
</idx:orth>
<p>{form}</p> 
<p>{meaning}</p>
</idx:short>
</idx:entry>
<hr style="width:50%", size="3", color=black>""".format(meaning=row['meaning'],
                                                        form=row['part_of_speech_simplified']))

    def _writeAdjectiveLoop(self, fname, index, row, pospeech: bool):

        fname.write(
            """
<idx:entry name="hebrew" scriptable="yes" spell="yes">
<idx:short><a id="{id}"></a>
<idx:orth value="{word}"><p><b>{word}</b>&emsp;|&emsp;<i>{pronunciation}</i></p>
""".format(id=index, word=row['hebrew_word'], pronunciation=row['hebrew_pronunciation'],
           inflgrp=row['part_of_speech_simplified']))
        if not pd.isnull(row[self.adj_infl]).all():
            fname.write(
                """<idx:infl>
""")

        for adj_inflection in self.adj_infl:
            if (pd.isnull(row[str(adj_inflection)])) == False:
                        fname.write(
                            """<idx:iform value="{inflgrp}" />
""".format(inflgrp=row[str(adj_inflection)]))

        if not pd.isnull(row[self.adj_infl]).all():
            fname.write(
                """</idx:infl>""")

        fname.write("""
    </idx:orth>
    <p>{form}</p> 
    <p>{meaning}</p>
    </idx:short>
    </idx:entry>
    <hr style="width:50%", size="3", color=black>""".format(meaning=row['meaning'],
                                                            form=row['part_of_speech_simplified']))

    def _writeWordsVerb(self, fname, index, row):
        fname.write("""
<idx:entry name="hebrew" scriptable="yes" spell="yes">
<idx:short><a id="{index}"></a>
<idx:orth value="{word}"><p><b>{word}</b>&emsp;|&emsp;<i>{niqqud}</i></p>
""".format(index=index,
           word=row['hebrew_word'],
           niqqud=row['niqqud']))
        if not pd.isnull(row[self.verb_inflection_group]).all():
            fname.write("""
<idx:infl>
""")

        for x in self.verb_inflection_group:
            if pd.isnull(row[str(x)]) == False:
                fname.write(
                    """<idx:iform value="{inflgrp}" />
""".format(inflgrp=row[str(x)]))
        if not pd.isnull(row[self.verb_inflection_group]).all():
            fname.write("""
</idx:infl>""")

        fname.write("""
</idx:orth> 
<p>{form}&emsp;|&emsp;{gender}</p>
<p><i><b>{infinitive}</b></i>&emsp;|&emsp;{pattern}</p>
<p>1. {meaning}</p>
<p>2. {english_word}</p>
</idx:short>
</idx:entry>
<hr style="width:50%", size="3", color=black>        
        """.format(form=row['part_of_speech_simplified'],
                   gender=row['gender'],
                   infinitive=row['infinitive'],
                   meaning=row['meaning'],
                   english_word=row['english_word'],
                   pattern=row['pattern']))

    def _writeWordsGrammar(self, fname, row, index):
        fname.write("""<idx:entry name="hebrew" scriptable="yes" spell="yes">
<idx:short><a id="{index}"></a>
<idx:orth value="{word}"><p><b>{word}</b>&emsp;|&emsp;<i>{niqqud}</i></p>""".format(index=index,
                                                                                    word=row['hebrew_word'],
                                                                                    niqqud=row['niqqud']))

    def _writePronomialLoop(self, fname, index, row, pospeech: bool):

        fname.write(
            """
<idx:entry name="hebrew" scriptable="yes" spell="yes">
<idx:short><a id="{id}"></a>
<idx:orth value="{word}"><p><b>{word}</b>&emsp;|&emsp;<i>{pronunciation}</i></p>
""".format(id=index, word=row['hebrew_word'], pronunciation=row['hebrew_pronunciation'],
           inflgrp=row['part_of_speech_simplified']))
#             if not pd.isnull(row[self.adj_infl]).all():
#                 fname.write(
#                     """<idx:infl>
#     """)
#
#             for adj_inflection in self.adj_infl:
#                 if (pd.isnull(row[str(adj_inflection)])) == False:
#                     fname.write(
#                         """<idx:iform value="{inflgrp}" />
# """.format(inflgrp=row[str(adj_inflection)]))
#
#             if not pd.isnull(row[self.adj_infl]).all():
#                 fname.write(
#                     """</idx:infl>""")

        fname.write("""
    </idx:orth>
    <p>{form}</p> 
    <p>{meaning}</p>
    </idx:short>
    </idx:entry>
    <hr style="width:50%", size="3", color=black>""".format(meaning=row['meaning'],
                                                            form=row['part_of_speech_simplified']))

    @contextlib.contextmanager
    def writeHTML(self, title_name, max_file_line: int = 1000):
        if sys.platform == "darwin":
            os.chdir("/Users/calvin/PycharmProjects/tab2opf_git")
        else:
            print('chng')
        # Quick switch
        self.csv2html_df['part_of_speech_simplified'] = self.csv2html_df['part_of_speech_simplified'].str.replace(
            'Verb', 'Infinitive Verb')
        # self.csv2html_df['part_of_simplified_speech'] = self.csv2html_df['word', 'part_of_simplified_speech'].apply(
        #     lambda x: 'Infinitive Verb' if (x['part_of_simplified_speech'] == 'Verb')==True else x,axis=1)
        self.csv2html_df.rename(columns={'word': 'hebrew_word'}, inplace=True)
        temp_df = pd.concat([self.csv2html_df,
                             self.verb_conj_present_filtered,
                             self.verb_conj_past_filtered,
                             self.verb_conj_future_filtered,
                             self.pronomial_df])
        temp_df.reset_index(drop=True, inplace=True)

        count_start = 0
        file_line_max = max_file_line
        if file_line_max > temp_df.shape[0]:
            file_line_max = temp_df.shape[0]
        noHTMLfiles = int(np.ceil(temp_df.shape[0] / file_line_max))

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
                for index, row in temp_df.iloc[count_start:file_line_max].iterrows():
                    if row['part_of_speech_simplified'] == 'Noun' or row[
                        'part_of_speech_simplified'] == 'Infinitive Verb':
                        self._writekeysLoop(f, index, row, pospeech=True)
                    elif row['part_of_speech_simplified'] == 'Verb':
                        self._writeWordsVerb(f, index, row)
                    elif row['part_of_speech_simplified'] == 'Adjective':
                        self._writeAdjectiveLoop(f, index, row, pospeech=False)
                    elif row['part_of_speech_simplified'] == 'Pronomial Noun':
                        self._writePronomialLoop(f, index, row, False)
                    else:
                        self._writekeysLoop(f, index, row, False)

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
