# PySciScrapping

PySciScrapping is a Python program to gather data from CSV files in the Publish and Perish (PoP) CSV format. 

If you want to evaluate abstracts or keywords before goes downloading the pdf paper, you can use PySciScrapping to obtain just those information.

Users of the tool [Publish or Perish](https://harzing.com/resources/publish-or-perish) (PoP) can export their searches to Comma Separated Values (CSV) files. Those files have a URL for the publisher's page where information about the article can be readed. PySciScrapping will analyse the HTML file, going for the abstract and keywords. If additional information could be obtained, it will be saved in a output CSV file.

The file [Test.csv](https://github.com/charlesANC/PySciScrapping/blob/master/Test.csv) is a example of input file and [Output_Test.csv](https://github.com/charlesANC/PySciScrapping/blob/master/Output_Test.csv) is for the file you will obtain after running the program.

But, in this version, information can be gathered from publishers IEEE, Springer and ACM only.

# How to use it

use: 'python scrapping.py input [output]'.

Where:

- input: A CSV file exported from PoP.

- output: Optional, a name for the output file. Will be used 'Output_'+input if omited.

