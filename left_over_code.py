#
#         if pospeech is False and pd.isnull(row['hebrew_word_present_singular_masculine']) is False:
#             fname.write("""
# <idx:entry name="hebrew" scriptable="yes" spell="yes">
# <idx:short><a id="{id}"></a>
# <idx:orth value="{word}"><p><b>{word}</b>   |   <i>{pronunciation}</i></p>
# <idx:infl inflgrp="{inflgrp}">""".format(id=row['id'], word=row['word'], meaning=row['meaning'], inflgrp=row['part_of_speech_simplified'],
#             pronunciation=row['hebrew_pronunciation']))
#
#             for key in self.allverbs.keys():
#                 try:
#                     for inflection in self.allverbs[str(key)][row['id']]:
#                         fname.write(
# """{inflection}
# """.format(inflection=inflection))
#                 except KeyError:
#                     continue
#
#             fname.write("""
#             </idx:infl >
#             </idx:orth>
#             <p>{meaning}</p>
#             </idx:short>
#             </idx:entry>
#             <hr style="width:50%", size="3", color=black>
#             """.format(meaning=row['meaning']))
#
#
# #             fname.write(
# #                 """
# # <idx:entry name="hebrew" scriptable="yes" spell="yes">
# # <idx:short><a id="{id}"></a>
# # <idx:orth value="{word}"><p><b>{word}</b>&nbsp;<hr class="vertical" />&nbsp;<i>{pronunciation}</i></p>
# # <idx:infl inflgrp="{inflgrp}">
# # <idx:iform value="{hebrew_word_present_singular_masculine}"></idx:iform>
# # <idx:iform value="{hebrew_word_present_singular_feminine}"></idx:iform>
# # <idx:iform value="{hebrew_word_present_plural_masculine}"></idx:iform>
# # <idx:iform value="{hebrew_word_present_plural_feminine}"></idx:iform>
# #
# # <idx:iform value="{hebrew_word_past_1_singular_masculine}"></idx:iform>
# # <idx:iform value="{hebrew_word_past_1_singular_feminine}"></idx:iform>
# # <idx:iform value="{hebrew_word_past_1_plural_masculine}"></idx:iform>
# # <idx:iform value="{hebrew_word_past_1_plural_feminine}"></idx:iform>
# #
# # <idx:iform value="{hebrew_word_past_2_singular_masculine}"></idx:iform>
# # <idx:iform value="{hebrew_word_past_2_singular_feminine}"></idx:iform>
# # <idx:iform value="{hebrew_word_past_2_plural_masculine}"></idx:iform>
# # <idx:iform value="{hebrew_word_past_2_plural_feminine}"></idx:iform>
# #
# # <idx:iform value="{hebrew_word_past_3_singular_masculine}"></idx:iform>
# # <idx:iform value="{hebrew_word_past_3_singular_feminine}"></idx:iform>
# # <idx:iform value="{hebrew_word_past_3_plural_masculine}"></idx:iform>
# # <idx:iform value="{hebrew_word_past_3_plural_feminine}"></idx:iform>
# #
# # <idx:iform value="{hebrew_word_present_singular_masculine_andform}"></idx:iform>
# # <idx:iform value="{hebrew_word_present_singular_feminine_andform}"></idx:iform>
# # <idx:iform value="{hebrew_word_present_plural_masculine_andform}"></idx:iform>
# # <idx:iform value="{hebrew_word_present_plural_feminine_andform}"></idx:iform>
# #
# # <idx:iform value="{hebrew_word_past_1_singular_masculine_andform}"></idx:iform>
# # <idx:iform value="{hebrew_word_past_1_singular_feminine_andform}"></idx:iform>
# # <idx:iform value="{hebrew_word_past_1_plural_masculine_andform}"></idx:iform>
# # <idx:iform value="{hebrew_word_past_1_plural_feminine_andform}"></idx:iform>
# #
# # <idx:iform value="{hebrew_word_past_2_singular_masculine_andform}"></idx:iform>
# # <idx:iform value="{hebrew_word_past_2_singular_feminine_andform}"></idx:iform>
# # <idx:iform value="{hebrew_word_past_2_plural_masculine_andform}"></idx:iform>
# # <idx:iform value="{hebrew_word_past_2_plural_feminine_andform}"></idx:iform>
# #
# # <idx:iform value="{hebrew_word_past_3_singular_masculine_andform}"></idx:iform>
# # <idx:iform value="{hebrew_word_past_3_singular_feminine_andform}"></idx:iform>
# # <idx:iform value="{hebrew_word_past_3_plural_masculine_andform}"></idx:iform>
# # <idx:iform value="{hebrew_word_past_3_plural_feminine_andform}"></idx:iform>
# #
# #
# # <idx:iform value="{hebrew_word_present_singular_masculine_thatform}"></idx:iform>
# # <idx:iform value="{hebrew_word_present_singular_feminine_thatform}"></idx:iform>
# # <idx:iform value="{hebrew_word_present_plural_masculine_thatform}"></idx:iform>
# # <idx:iform value="{hebrew_word_present_plural_feminine_thatform}"></idx:iform>
# #
# # <idx:iform value="{hebrew_word_past_1_singular_masculine_thatform}"></idx:iform>
# # <idx:iform value="{hebrew_word_past_1_singular_feminine_thatform}"></idx:iform>
# # <idx:iform value="{hebrew_word_past_1_plural_masculine_thatform}"></idx:iform>
# # <idx:iform value="{hebrew_word_past_1_plural_feminine_thatform}"></idx:iform>
# #
# # <idx:iform value="{hebrew_word_past_2_singular_masculine_thatform}"></idx:iform>
# # <idx:iform value="{hebrew_word_past_2_singular_feminine_thatform}"></idx:iform>
# # <idx:iform value="{hebrew_word_past_2_plural_masculine_thatform}"></idx:iform>
# # <idx:iform value="{hebrew_word_past_2_plural_feminine_thatform}"></idx:iform>
# #
# # <idx:iform value="{hebrew_word_past_3_singular_masculine_thatform}"></idx:iform>
# # <idx:iform value="{hebrew_word_past_3_singular_feminine_thatform}"></idx:iform>
# # <idx:iform value="{hebrew_word_past_3_plural_masculine_thatform}"></idx:iform>
# # <idx:iform value="{hebrew_word_past_3_plural_feminine_thatform}"></idx:iform>
# #
# #
# # </idx:infl>
# # </idx:orth>
# # <p>{meaning}</p>
# # </idx:short>
# # </idx:entry>
# # <hr style="width:50%", size="3", color=black>
# # """.format(id=row['id'], word=row['word'], meaning=row['meaning'], inflgrp=row['part_of_speech_simplified'],
# #            pronunciation=row['hebrew_pronunciation'],
# #
# #            hebrew_word_present_singular_masculine=row['hebrew_word_present_singular_masculine'],
# #            hebrew_word_present_singular_feminine=row['hebrew_word_present_singular_feminine'],
# #            hebrew_word_present_plural_masculine=row['hebrew_word_present_plural_masculine'],
# #            hebrew_word_present_plural_feminine=row['hebrew_word_present_plural_feminine'],
# #
# #            hebrew_word_past_1_singular_masculine=row['hebrew_word_past_1_singular_masculine'],
# #            hebrew_word_past_1_singular_feminine=row['hebrew_word_past_1_singular_feminine'],
# #            hebrew_word_past_1_plural_masculine=row['hebrew_word_past_1_plural_masculine'],
# #            hebrew_word_past_1_plural_feminine=row['hebrew_word_past_1_plural_feminine'],
# #
# #            hebrew_word_past_2_singular_masculine=row['hebrew_word_past_2_singular_masculine'],
# #            hebrew_word_past_2_singular_feminine=row['hebrew_word_past_2_singular_feminine'],
# #            hebrew_word_past_2_plural_masculine=row['hebrew_word_past_2_plural_masculine'],
# #            hebrew_word_past_2_plural_feminine=row['hebrew_word_past_2_plural_feminine'],
# #
# #            hebrew_word_past_3_singular_masculine=row['hebrew_word_past_3_singular_masculine'],
# #            hebrew_word_past_3_singular_feminine=row['hebrew_word_past_3_singular_feminine'],
# #            hebrew_word_past_3_plural_masculine=row['hebrew_word_past_3_plural_masculine'],
# #            hebrew_word_past_3_plural_feminine=row['hebrew_word_past_3_plural_feminine'],
# #
# #            hebrew_word_present_singular_masculine_andform=row['hebrew_word_present_singular_masculine_andform'],
# #            hebrew_word_present_singular_feminine_andform=row['hebrew_word_present_singular_feminine_andform'],
# #            hebrew_word_present_plural_masculine_andform=row['hebrew_word_present_plural_masculine_andform'],
# #            hebrew_word_present_plural_feminine_andform=row['hebrew_word_present_plural_feminine_andform'],
# #
# #            hebrew_word_past_1_singular_masculine_andform=row['hebrew_word_past_1_singular_masculine_andform'],
# #            hebrew_word_past_1_singular_feminine_andform=row['hebrew_word_past_1_singular_feminine_andform'],
# #            hebrew_word_past_1_plural_masculine_andform=row['hebrew_word_past_1_plural_masculine_andform'],
# #            hebrew_word_past_1_plural_feminine_andform=row['hebrew_word_past_1_plural_feminine_andform'],
# #
# #            hebrew_word_past_2_singular_masculine_andform=row['hebrew_word_past_2_singular_masculine_andform'],
# #            hebrew_word_past_2_singular_feminine_andform=row['hebrew_word_past_2_singular_feminine_andform'],
# #            hebrew_word_past_2_plural_masculine_andform=row['hebrew_word_past_2_plural_masculine_andform'],
# #            hebrew_word_past_2_plural_feminine_andform=row['hebrew_word_past_2_plural_feminine_andform'],
# #
# #            hebrew_word_past_3_singular_masculine_andform=row['hebrew_word_past_3_singular_masculine_andform'],
# #            hebrew_word_past_3_singular_feminine_andform=row['hebrew_word_past_3_singular_feminine_andform'],
# #            hebrew_word_past_3_plural_masculine_andform=row['hebrew_word_past_3_plural_masculine_andform'],
# #            hebrew_word_past_3_plural_feminine_andform=row['hebrew_word_past_3_plural_feminine_andform'],
# #
# #            hebrew_word_present_singular_masculine_thatform=row['hebrew_word_present_singular_masculine_thatform'],
# #            hebrew_word_present_singular_feminine_thatform=row['hebrew_word_present_singular_feminine_thatform'],
# #            hebrew_word_present_plural_masculine_thatform=row['hebrew_word_present_plural_masculine_thatform'],
# #            hebrew_word_present_plural_feminine_thatform=row['hebrew_word_present_plural_feminine_thatform'],
# #
# #            hebrew_word_past_1_singular_masculine_thatform=row['hebrew_word_past_1_singular_masculine_thatform'],
# #            hebrew_word_past_1_singular_feminine_thatform=row['hebrew_word_past_1_singular_feminine_thatform'],
# #            hebrew_word_past_1_plural_masculine_thatform=row['hebrew_word_past_1_plural_masculine_thatform'],
# #            hebrew_word_past_1_plural_feminine_thatform=row['hebrew_word_past_1_plural_feminine_thatform'],
# #
# #            hebrew_word_past_2_singular_masculine_thatform=row['hebrew_word_past_2_singular_masculine_thatform'],
# #            hebrew_word_past_2_singular_feminine_thatform=row['hebrew_word_past_2_singular_feminine_thatform'],
# #            hebrew_word_past_2_plural_masculine_thatform=row['hebrew_word_past_2_plural_masculine_thatform'],
# #            hebrew_word_past_2_plural_feminine_thatform=row['hebrew_word_past_2_plural_feminine_thatform'],
# #
# #            hebrew_word_past_3_singular_masculine_thatform=row['hebrew_word_past_3_singular_masculine_thatform'],
# #            hebrew_word_past_3_singular_feminine_thatform=row['hebrew_word_past_3_singular_feminine_thatform'],
# #            hebrew_word_past_3_plural_masculine_thatform=row['hebrew_word_past_3_plural_masculine_thatform'],
# #            hebrew_word_past_3_plural_feminine_thatform=row['hebrew_word_past_3_plural_feminine_thatform']
# #
# #            )
# #             )
#
#
#     def dictVerbCreat(self, table, dictionary):
#         table = table.reset_index()
#         for index, rows in table.iterrows():
#             for i in list(table.columns.difference(['id'])):
#                 if pd.isnull(rows[(i)]) == False:
#                     self._createChaserDict(dictionary, rows['id'], rows[str(i)])
#
#     def verbs_dictionary(self):
#         self.dictVerbCreat(self.verb_conj_present,self.verb_conj_present_chaser)
#         self.dictVerbCreat(self.verb_conj_present_and, self.verb_conj_present_and_chaser)
#         self.dictVerbCreat(self.verb_conj_present_that, self.verb_conj_present_that_chaser)
#
#         self.dictVerbCreat(self.verb_conj_past,self.verb_conj_past_chaser)
#         self.dictVerbCreat(self.verb_conj_past_and, self.verb_conj_past_and_chaser)
#         self.dictVerbCreat(self.verb_conj_past_that, self.verb_conj_past_that_chaser)
#
#         self.dictVerbCreat(self.verb_conj_future, self.verb_conj_future_chaser)
#         self.dictVerbCreat(self.verb_conj_future_and, self.verb_conj_future_and_chaser)
#         self.dictVerbCreat(self.verb_conj_future_that, self.verb_conj_future_that_chaser)
#
#         list_dict = [self.verb_conj_present_chaser, self.verb_conj_present_and_chaser,
#                      self.verb_conj_present_that_chaser, self.verb_conj_past_chaser,
#                      self.verb_conj_past_and_chaser, self.verb_conj_past_that_chaser,
#                      self.verb_conj_future_chaser, self.verb_conj_future_and_chaser,
#                      self.verb_conj_present_that_chaser]
#         self.allverbs = {}
#
#         for i in range(len(list_dict)):
#             self.allverbs['dict_' + str(i)] = list_dict[i]
#
#
#
#     def importVerbConjPresent(self):
#         self.verb_conj_present = pd.read_csv(self.verb_conj_present_file)
#         print(self.verb_conj_present.head())
#         self.verb_conj_present.drop(columns=['person', 'english_word'], inplace=True)
#         self.verb_conj_present = self.verb_conj_present.pivot(index=['id'], columns=['verb_form', 'form', 'gender'])
#         self.verb_conj_present.columns = ['_'.join(col) for col in self.verb_conj_present.columns.values]
#         self.list_present_verb_columns = list(self.verb_conj_present.columns)
#
#         self.verb_conj_present_and_columns = [s + '_andform' for s in self.list_present_verb_columns]
#         self.verb_conj_present_and = self.verb_conj_present.copy()
#         self.verb_conj_present_and.columns = self.verb_conj_present_and_columns
#         self.verb_conj_present_and = self.verb_conj_present_and.applymap(lambda x: "{}{}".format('ו', x) if pd.isnull(x) == False else x)
#         print(self.verb_conj_present_and.head())
#
#         self.verb_conj_present_that_columns = [s + '_thatform' for s in self.list_present_verb_columns]
#         self.verb_conj_present_that = self.verb_conj_present.copy()
#         self.verb_conj_present_that.columns = self.verb_conj_present_that_columns
#         self.verb_conj_present_that = self.verb_conj_present_that.applymap(lambda x: "{}{}".format('ש', x) if pd.isnull(x) == False else x)
#         print(self.verb_conj_present_that.head())
#
#         # TODO Find a better method
#
#     def importVerbConjPast(self):
#         self.verb_conj_past = pd.read_csv(self.verb_conj_past_file)
#         print(self.verb_conj_past.head())
#         self.verb_conj_past.drop(columns=['english_word'], inplace=True)
#
#         self.verb_conj_past = self.verb_conj_past.pivot(index=['id'], columns=['verb_form', 'person', 'form', 'gender'])
#         data = [tuple(str(x) for x in tup) for tup in self.verb_conj_past.columns.values]
#         self.verb_conj_past.columns = ['_'.join(col) for col in data]
#         self.list_past_verb_columns = list(self.verb_conj_past.columns)
#
#         self.verb_conj_past_and_columns = [s + '_andform' for s in self.list_past_verb_columns]
#         self.verb_conj_past_and = self.verb_conj_past.copy()
#         self.verb_conj_past_and.columns = self.verb_conj_past_and_columns
#         self.verb_conj_past_and = self.verb_conj_past_and.applymap(lambda x: "{}{}".format('ו', x) if pd.isnull(x) == False else x)
#         print(self.verb_conj_past_and.head())
#
#         self.verb_conj_past_that_columns = [s + '_thatform' for s in self.list_past_verb_columns]
#         self.verb_conj_past_that = self.verb_conj_past.copy()
#         self.verb_conj_past_that.columns = self.verb_conj_past_that_columns
#         self.verb_conj_past_that = self.verb_conj_past_that.applymap(lambda x: "{}{}".format('ש', x) if pd.isnull(x) == False else x)
#         print(self.verb_conj_past_that.head())
#
#     def importVerbConjFut(self):
#         self.verb_conj_future = pd.read_csv(self.verb_conj_future_file)
#         self.verb_conj_future.drop(columns=['english_word'], inplace=True)
#
#         self.verb_conj_future = self.verb_conj_future.pivot(index=['id'], columns=['verb_form', 'person', 'form', 'gender'])
#         data = [tuple(str(x) for x in tup) for tup in self.verb_conj_future.columns.values]
#         self.verb_conj_future.columns = ['_'.join(col) for col in data]
#         self.list_verb_future_columns = list(self.verb_conj_future.columns)
#
#         self.verb_conj_future_and_columns = [s + '_andform' for s in self.list_verb_future_columns]
#         self.verb_conj_future_and = self.verb_conj_future.copy()
#         self.verb_conj_future_and.columns = self.verb_conj_future_and_columns
#         self.verb_conj_future_and = self.verb_conj_future_and.applymap(lambda x: "{}{}".format('ו', x) if pd.isnull(x) == False else x)
#         print(self.verb_conj_future_and.head())
#
#         self.verb_conj_future_that_columns = [s + '_thatform' for s in self.list_verb_future_columns]
#         self.verb_conj_future_that = self.verb_conj_future.copy()
#         self.verb_conj_future_that.columns = self.verb_conj_future_that_columns
#         self.verb_conj_future_that = self.verb_conj_future_that.applymap(lambda x: "{}{}".format('ש', x) if pd.isnull(x) == False else x)
#         print(self.verb_conj_future_that.head())
#
#
# """.format(id=index, word=row['hebrew_word'], meaning=row['meaning'], inflgrp=row['part_of_speech_simplified'],
#            pronunciation=row['hebrew_pronunciation'],
#
#            inflection_the=row['inflection_the'],
#            inflection_from=row['inflection_from'],
#            inflection_to=row['inflection_to'],
#            inflection_in=row['inflection_in'],
#            inflection_that=row['inflection_that'],
#            inflection_the_plural=row['inflection_the_plural'],
#            inflection_from_plural=row['inflection_from_plural'],
#            inflection_to_plural=row['inflection_to_plural'],
#            inflection_in_plural=row['inflection_in_plural'],
#            inflection_that_plural=row['inflection_that_plural']
#            ))
#
# <idx:iform value="{inflection_the}"></idx:iform>
# <idx:iform value="{inflection_from}"></idx:iform>
# <idx:iform value="{inflection_to}"></idx:iform>
# <idx:iform value="{inflection_in}"></idx:iform>
# <idx:iform value="{inflection_that}"></idx:iform>
# <idx:iform value="{inflection_the_plural}"></idx:iform>
# <idx:iform value="{inflection_from_plural}"></idx:iform>
# <idx:iform value="{inflection_to_plural}"></idx:iform>
# <idx:iform value="{inflection_in_plural}"></idx:iform>
# <idx:iform value="{inflection_that_plural}"></idx:iform>