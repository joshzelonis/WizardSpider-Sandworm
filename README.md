# WizardSpider-Sandworm
This code base is tested and working, check out my blog for thoughts on this years' evaluation https://medium.com/the-recovering-analyst/the-mitre-att-ck-evaluation-needs-to-evolve-6bf2074138e4

## Installation

chmod +x pull_scores.sh
./pull_scores.sh
pip3 install -r requirements.txt

The output of the WizardSpider-Sandworm.py script will output an XLSX workbook that will allow you to parse and play with vendor scores based on the analysis I've performed for the past 4 years. 

I'm including the XLSX in the source tree to save trouble running the code if that's all you care about. If you don't like the decisions I've made above, the code is yours to modify.

## Requirements
python3

pip3 install -r requirements.txt

curl (to download the json data)


## Thanks
I want to thank MITRE for the ATT&CK Framework and for performing these open and transparent evaluations.

I also want to thank the vendors who participated in this evaluation for providing transparency into the efficacy of their products. 

You are all making the world more secure.
