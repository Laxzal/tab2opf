'''
1. Create the OPF File
    Example: (Bilingual Dictionary Metadata)
            <x-metadata>

            <DictionaryInLanguage>es</DictionaryInLanguage>

            <DictionaryOutLanguage>fr</DictionaryOutLanguage>

            <DefaultLookupIndex>Spanish</DefaultLookupIndex>

            ...

            </x-metadata>


https://gist.github.com/carlopires/1262033 --ISO Codes for langauges to implement


2. Write Frameset Element


'''
import os
import sys
from contextlib import contextmanager

from csv2html import SimpleCSV2HTML


class CreateOPF:

    def __init__(self, title: str = 'Dictionary_Name', book_name: str = 'Dictionary Kindle', input_lang: str = 'he',
                 output_lang: str = 'en'):
        if sys.platform.lower() == 'darwin':
            os.chdir("/Users/calvin/Documents/hebrew_dictionary/")


        self.title = title
        self.book_name = book_name
        self.input_lang = input_lang
        self.output_lang = output_lang
        self.csv2html = SimpleCSV2HTML("pealim_database.csv")
        self.htmlfiles = []

    def runCSV2HTML(self):

        # databases
        self.csv2html.extractForm()
        self.csv2html.extractPattern()
        self.csv2html.hebrewWordsClean('word')

        # nouns
        self.csv2html.importNounPluralDb()
        self.csv2html.hebrewPluralClean()
        # verbs
        self.csv2html.importVerbConjPresent_ver2()
        self.csv2html.importVerbConjPast_ver2()
        self.csv2html.importVerbConjFut_ver()
        self.csv2html.cleanVerbWord()
        self.csv2html.inflectVerbs()

        self.csv2html.mergeNounPlurals()

        self.csv2html.createDefInflection()

        self.csv2html.createSimpleDf()
        self.csv2html.writeHTML(str(self.title), 10000)
        self.htmlfiles = self.csv2html.list_file_names

    @contextmanager
    def openOPF(self):
        print('Starting OPF')
        fname = "%s.opf" % self.title

        with open(fname, 'w') as f:
            f.write("""<?xml version="1.0"?><!DOCTYPE package SYSTEM "oeb1.ent">

<!-- the command line instruction 'prcgen dictionary.opf' will produce the dictionary.prc file in the same folder-->
<!-- the command line instruction 'mobigen dictionary.opf' will produce the dictionary.mobi file in the same folder-->

<package unique-identifier="uid" xmlns:dc="Dublin Core">

<metadata>
	<dc-metadata>
		<dc:Identifier id="uid">{name}</dc:Identifier>
		<!-- Title of the document -->
		<dc:Title><h2>{name}</h2></dc:Title>
		<dc:Language>EN</dc:Language>
	</dc-metadata>
	<x-metadata>
	        <output encoding="utf-8" flatten-dynamic-dir="yes"/>
		<DictionaryInLanguage>{source}</DictionaryInLanguage>
		<DictionaryOutLanguage>{target}</DictionaryOutLanguage>
	</x-metadata>
</metadata>

<!-- list of all the files needed to produce the .prc file -->
<manifest>
            """.format(name=self.book_name, source=self.input_lang, target=self.output_lang))

            for z in range(len(self.htmlfiles)):
                f.write("""
                <item id="dictionary{id}" href="{html_file}" media-type="text/x-oeb1-document"/>
                """.format(id=z, html_file=str(self.htmlfiles[z])))

            f.write("""</manifest>
            
            <spine>""")
            for y in range(len(self.htmlfiles)):
                f.write("""
                    <itemref idref="dictionary{y}"/>
                """.format(y=str(y)))

            f.write("""
</spine>            
<tours/>
<guide> <reference type="search" title="Dictionary Search" onclick= "index_search()"/> </guide>
</package>
"""
                    )

        assert f.closed is True


test = CreateOPF(title='hebrew2english_dict', book_name='Hebrew English Dictionary')
test.runCSV2HTML()
test.openOPF()

print('end')
