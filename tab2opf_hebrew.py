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
import subprocess
from csv2html import SimpleCSV2HTML


class CreateOPF:

    def __init__(self, title: str = 'Dictionary_Name', book_name: str = 'Dictionary Kindle', input_lang: str = 'he',
                 output_lang: str = 'en', cover_name: str = "cover", image_name: str = "design2.jpg"):
        if sys.platform.lower() == 'darwin':
            os.chdir("/Users/calvin/Documents/hebrew_dictionary/")
        else:
            os.chdir("C:/Users/Calvin/PycharmProjects/hebrew_dictionary_git/hebrew_dictionary")

        self.title = title
        self.book_name = book_name
        self.input_lang = input_lang
        self.output_lang = output_lang
        self.csv2html = SimpleCSV2HTML("pealim_database.csv")
        self.htmlfiles = []
        self.cover_name = cover_name
        self.image_name = image_name

    def runCSV2HTML(self):

        # databases
        self.csv2html.extractForm()
        self.csv2html.extractPattern()
        self.csv2html.hebrewWordsClean('word')

        # nouns
        self.csv2html.importNounPluralDb()
        self.csv2html.hebrewPluralClean()
        # adjectives
        self.csv2html.importAdjectivesDb()

        # pronomial nouns
        self.csv2html.importPronomialNoun()
        # verbs
        self.csv2html.importVerbConjPresent_ver2()
        self.csv2html.importVerbConjPast_ver2()
        self.csv2html.importVerbConjFut_ver()
        self.csv2html.importImperativeVerb()
        self.csv2html.importPassivePresentVerb()
        self.csv2html.importPassivePastVerb()
        self.csv2html.importPassiveFutureVerb()
        self.csv2html.cleanVerbWord()
        self.csv2html.inflectVerbs()

        self.csv2html.mergeNounPlurals()

        self.csv2html.createDefInflection()

        self.csv2html.createSimpleDf()
        self.csv2html.writeHTML(str(self.title), 10000)
        self.htmlfiles = self.csv2html.list_file_names


    def alephbet(self):
        alephbetpage = 'alephbet.html'

        with open(alephbetpage, 'w', encoding='utf-8') as alephbet:
            alephbet.write("""
<html dir="rtl" lang="he">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<style>
table, th, td {
  border: 0.5px solid;
  font-size: 0.3em;
}
</style>
    </head> 
    <body>
        <table style="width:30%">
            <tr>
                <td>א</td>
                <td>בּ</td>
                <td>ג</td>
                <td>ד</td>
                <td>ה</td>
                <td>ו</td>
            </tr>
            <tr>
                <td>aleph</td>
                <td>bet(B/V)</td>
                <td>gimmel(G)</td>
                <td>dalet(D)</td>
                <td>hey(H)</td>
                <td>vav(V)</td>
            </tr>
        </table>    
        <table style="width:30%">
            <tr>        
                <td>ז</td>
                <td>ח</td>
                <td>ט</td>
                <td>י</td>
                <td>כּ</td>
                <td>ך</td>
                <td>ל</td>
            </tr>
            <tr>
                <td>zayin(Z)</td>
                <td>chet(Ch)</td>
                <td>tet(T)</td>
                <td>yod(Y)</td>
                <td>kaf(K/Kh)</td>
                <td>khaf sofit(Kh)</td>
                <td>lamed(L)</td>
            </tr>    
        </table>        
        <table style="width:30%">
        <tr>        
                <td>מ</td>
                <td>ם</td>
                <td>נ</td>
                <td>ן</td>
                <td>ס</td>
                <td>ע</td>
                <td>פ</td>
        </tr>
        <tr>
                <td>mem(M)</td>
                <td>mem sofit(M)</td>
                <td>nun(N)</td>
                <td>nun sofit(N)</td>
                <td>samech(S)</td>
                <td>ayin</td>
                <td>peh(P/F)</td>
        </tr>
        </table>
        <table style="width:30%">
        <tr>        
                <td>ף</td>
                <td>צ</td>
                <td>ץ</td>
                <td>ק</td>
                <td>ר</td>
                <td>ש</td>
                <td>ת</td>
            </tr>
            <tr>
                <td>feh sofit(F)</td>
                <td>tsadech(Ts)</td>
                <td>tsadech sofit(Ts)</td>
                <td>qof(Q)</td>
                <td>resh(R)</td>
                <td>shin(sh/s)</td>
                <td>tav(T)</td>
            </tr>  
        </table>       
  </body>
</html>              
            """
            )
    def createFrontPage(self):
        introPage = 'introPage.html'

        with open(introPage, 'w', encoding='utf-8') as intro:
            intro.write("""
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<style>
table, th, td {
  border: 0.5px solid;
  font-size: 0.3em;
}
</style>
  </head>
  <body>
    <table style="width:30%">
        <tr>
            <th>Mark</th>
            <th>Name</th>
            <th>Sound</th>
            <th>Hebrew</th>
            <th>Trans.</th>
            <th>Class</th>
            <th>Type</th>
        </tr>
        <tr>
            <td>אָ</td>
            <td>Qamets</td>
            <td>"a" as in <b>a</b>qua</td>
            <td>קַמֵּץ</td>
            <td>a/ah</td>
            <td>Long</td>
            <td>A-Type</td>
        </tr>
        <tr>
            <td>אַ</td>
            <td>Patach</td>
            <td>"a" as in <b>a</b>qua</td>
            <td>פַּתַח</td>
            <td>a</td>
            <td>Short</td>
            <td>A-Type</td>
        </tr>
        <tr>
            <td>אֳ</td>
            <td>Chateph Patach</td>
            <td>"a" as in <b>a</b>qua</td>
            <td>חָטֵף פַּתַח</td>
            <td>a</td>
            <td>Reduced</td>
            <td>A-Type</td>
        </tr>
        <tr>
            <td>אָה</td>
            <td>Qamets Hey</td>
            <td>"a" as in <b>a</b>qua</td>
            <td>קַמֵּץ הַא</td>
            <td>a</td>
            <td>Long</td>
            <td>A-Type</td>
        </tr>        

        <tr>
            <td>אֵ</td>
            <td>Tsere</td>
            <td>"ei" as in <b>ei</b>ght <br>
                "e" in th<b>e</b>y</td>
            <td>צֵרֵי</td>
            <td>ei/e</td>
            <td>Long</td>
            <td>E-Type</td>
        </tr>
        <tr>
            <td>אֶ</td>
            <td>Segol</td>
            <td>r<b>e</b>d</td>
            <td>סֶגוֹל</td>
            <td>ei/e</td>
            <td>Short</td>
            <td>E-Type</td>
        </tr>
        <tr>
            <td>אֱ</td>
            <td>Chateph Segol</td>
            <td>r<b>e</b>d</td>
            <td>חָטֵף סֶגוֹל</td>
            <td>e</td>
            <td>Reduced</td>
            <td>E-Type</td>
        </tr>               
        <tr>
            <td>אֵי</td>
            <td>Tsere Yod</td>
            <td>"ei" as in <b>ei</b>ght</td>
            <td>צֵרֵי יוֹד</td>
            <td>ei</td>
            <td>Long</td>
            <td>E-Type</td>
        </tr>
        <tr>
            <td>אֶי</td>
            <td>Segol Yod</td>
            <td>"ey" as in ob<b>ey</b></td>
            <td>סֶגוֹל יוֹד</td>
            <td>ey</td>
            <td>Long</td>
            <td>E-Type</td>
        </tr>
        <tr>
            <td>אִ</td>
            <td>Chireq</td>
            <td>"ee" as in gr<b>ee</b>n</td>
            <td>חִירֶק</td>
            <td>i/ee</td>
            <td>Short</td>
            <td>I-Type</td>
        </tr>
        <tr>
            <td>אִי</td>
            <td>Chireq</td>
            <td>"ee" as in gr<b>ee</b>n</td>
            <td>חִירֶק יוֹד</td>
            <td>i/ee</td>
            <td>Long</td>
            <td>I-Type</td>
        </tr>
        <tr>
            <td>אֹ</td>
            <td>Cholem</td>
            <td>"o" as in yell<b>o</b>w</td>
            <td>חוֹלֶם</td>
            <td>o/oh</td>
            <td>Long</td>
            <td>O-Type</td>
        </tr>
        <tr>
            <td>אֳ</td>
            <td>Chateph Qamets</td>
            <td>"o" as in yell<b>o</b>w</td>
            <td>חָטֵף קָמֵץ</td>
            <td>o/oh</td>
            <td>Reduced</td>
            <td>O-Type</td>
        </tr>
        <tr>
            <td>אָ</td>
            <td>Qamets Chatuph</td>
            <td>"o" as in yell<b>o</b>w</td>
            <td>קָמֵץ חָטוּף</td>
            <td>o/oh</td>
            <td>Short</td>
            <td>O-Type</td>
        </tr>
        <tr>
            <td>אוֹ</td>
            <td>Choelm Vav</td>
            <td>"o" as in yell<b>o</b>w</td>
            <td>חוֹלֶם וָו</td>
            <td>o/oh</td>
            <td>Long</td>
            <td>O-Type</td>
        </tr>
        <tr>
            <td>אֻ</td>
            <td>Qibbuts</td>
            <td>"u" as in bl<b>u</b>e</td>
            <td>קִבּוּץ</td>
            <td>u/oo</td>
            <td>Short</td>
            <td>U-Type</td>
        </tr>
        <tr>
            <td>אוּ</td>
            <td>Shureq</td>
            <td>"u" as in bl<b>u</b>e</td>
            <td>שׁוּרֶק</td>
            <td>u/oo</td>
            <td>Long</td>
            <td>U-Type</td>
        </tr>
        <tr>
            <td>אְ</td>
            <td>Sheva'</td>
            <td><i>Vocal</i>: short "e"<br>
                <i>Silent</i>: no sound</td>
            <td>שְׁוָא</td>
            <td>e or '</td>
            <td>(vocal) Short</td>
            <td> - </td>
        </tr> 
        </table>       
  </body>
</html>
""")

    @contextmanager
    def openOPF(self):
        print('Starting OPF')
        self.createFrontPage()
        self.alephbet()
        fname = "%s.opf" % self.title

        with open(fname, 'w', encoding='utf-8') as f:
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
		<meta: name ="{cover_name}" content="my-cover-image" /> 
	</dc-metadata>
	<x-metadata>
	    <output encoding="utf-8" flatten-dynamic-dir="yes"/>
		<DictionaryInLanguage>{source}</DictionaryInLanguage>
		<DictionaryOutLanguage>{target}</DictionaryOutLanguage>
	</x-metadata>
</metadata>

<!-- list of all the files needed to produce the .prc file -->
<manifest>
        <item id="{cover_name}" properties="cover-image" href="{imagename}" media-type="image/jpeg"  />
        <item id="alephbet" href="alephbet.html" media-type="application/xhtml+xml" />
        <item id="intro_page" href="introPage.html" media-type="application/xhtml+xml" />
            """.format(name=self.book_name, source=self.input_lang, target=self.output_lang,
                       cover_name=self.cover_name, imagename=self.image_name))

            for z in range(len(self.htmlfiles)):
                f.write("""
                <item id="dictionary{id}" href="{html_file}" media-type="text/x-oeb1-document"/>
                """.format(id=z, html_file=str(self.htmlfiles[z])))

            f.write("""</manifest>
            
            <spine>
            <itemref idref="{cover_name}" />
            <itemref idref="alephbet" />
            <itemref idref="intro_page" />
""".format(cover_name=self.cover_name))
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

title = 'hebrew2english_dict'
test = CreateOPF(title=title, book_name='Hebrew English Dictionary')
test.runCSV2HTML()
test.openOPF()

print('end')

print("Beginning Kindlegen")
subprocess.Popen([f"kindlegen.exe, {title}+'.opf' -verbose -c2 -o Hebrew2English_Mobi.mobi"])

# if __name__ == "__main__":
#

