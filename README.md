# Intro

This, **English to Narsese, beta 1.0**, is a Python script by Tangrui Li (tuo90515@temple.edu) translating English to Narsese, which is the formal language used in the non-axiomatic reasoning system (NARS, https://www.opennars.org). This script will translate your input English sentence (including possible punctuations) to several Narsese judgments, so that you may use the strong capability of reasoning of NARS on your NLP tasks. Here are some examples of a Q&A problem.

---

Q: I am studying Chinese diligently. I am studying English. What I am studying diligently?

A: Chinese.

Q: I am studying Chinese. I am studying English diligently. What I am studying diligently?

A: English.

---

Note that this script does not include an OpenNARS agent; it is only for translation. Therefore, you cannot get the answer by this program merely. And it is suggested to translate sentences one by one, although it is okay to process a long paragraph.



# Prerequisites

- Python 3.
- stanfordcorenlp (a package on Github, https://github.com/Lynten/stanford-corenlp)
- CoreNLP for English 4.2.2 (the latest version is 4.3.2, https://stanfordnlp.github.io/CoreNLP/download.html)
- other necessary general packages.



# Usage

English to Narsese beta 1.0 is an IDLE (e.g. Spyder) based script for debugging purposes. It is not currently suitable to run on terminals. 



# Appendix

Terms used in the program are largely consistent with CoreNLP's handbook (https://downloads.cs.stanford.edu/nlp/software/dependencies_manual.pdf) and PennTreeBanks (https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html). You can visualize the result of CoreNlP at here (https://corenlp.run).
