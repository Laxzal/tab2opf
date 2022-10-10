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
from contextlib import contextmanager


class CreateOPF:

    def __init__(self, title: str = 'Dictionary_Name', input_lang: str = 'he', output_lang: str = 'en'):
        self.title = title
        self.input_lang = input_lang
        self.output_lang = output_lang

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
""".format(name=self.title, source=self.input_lang, target=self.output_lang))

            f.write("""
<tours/>
<guide> <reference type="search" title="Dictionary Search" onclick= "index_search()"/> </guide>
</package>
"""
                    )



        assert f.closed is True


test = CreateOPF(title='Test_Dict')
test.openOPF()

print('end')
