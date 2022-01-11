#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 18:26:39 2021

@author: Tangrui Li (tuo90515@temple.edu, litangrui.tori@gmail.com)
@author: Hongzheng Wang (tuf78197@temple.edu, hongzheng.wang@temple.edu)
"""

import re
import copy
import random
from stanfordcorenlp import StanfordCoreNLP

# Please change the address of Stanford CoreNLP as yours
nlp = StanfordCoreNLP(r"/External_Library/stanford-corenlp-4.3.2")


class semi_concept:

    def __init__(self, name):
        self.name = name
        self.subj = "$"
        self.obj = "$"
        self.case = "$"
        self.cop = False
        self.cc = None

    def subj_complex(self):
        if self.subj != "$":
            return self.subj
        else:
            return None

    def obj_complex(self):
        if self.obj != "$":
            return self.obj
        else:
            return None

    def motion_complex(self):
        if self.subj != "$" and self.obj != "$":
            return "(*," + self.subj + "," + self.obj + ")"
        else:
            return None

    def self_complex(self):
        return self.name


class EtN:

    def __init__(self, nlp):
        self.instant_translation = []
        self.nlp = nlp
        self.semi_cpt_dict = {}
        self.ID = 0

    def internal_concept(self):
        self.ID += 1
        return "ID" + str(self.ID - 1)

    def token_complex(self, semi_cpt):
        if semi_cpt.motion_complex():
            self.instant_translation.append("<" + semi_cpt.motion_complex() + "-->" + semi_cpt.name + "_complex" + ">.")
            self.instant_translation.append(
                "<" + semi_cpt.subj + "-->(/," + semi_cpt.name + "_complex,_," + semi_cpt.obj + ")>.")
            self.instant_translation.append(
                "<" + semi_cpt.obj + "-->(/," + semi_cpt.name + "_complex," + semi_cpt.subj + ",_)>.")
        self.instant_translation.append("<" + semi_cpt.self_complex() + "-->" + semi_cpt.name + "_complex" + ">.")
        return semi_cpt.name + "_complex"

    def advmod(self, A, B):
        if B.name == "When":
            self.instant_translation.append("<?-->" + A.name + ">?")
        else:
            self.instant_translation.append("<" + A.name + "-->" + A.name + "_complex>.")
            self.instant_translation.append("<" + A.name + "_complex-->" + B.name + ">.")

    def nummod(self, A, B):
        # nummod(AM,8:00)
        self.instant_translation.append("<" + A.name + "-->" + A.name + "_complex>.")
        self.instant_translation.append("<" + A.name + "_complex-->" + B.name + ">.")

    def amod(self, A, B):
        # amod(identity,distinct)
        self.instant_translation.append("<" + A.name + "-->" + A.name + "_complex>.")
        self.instant_translation.append("<" + A.name + "_complex-->" + B.name + ">.")

    def case(self, A, B):
        # case(half,in)
        if A.cop:
            A.name = A.name + "_" + B.name
        A.case = B.name

    def det(self, A, B):
        # det(half,the)
        # det(centry,what)
        if B.name != "the" and B.name != "The" and B.name != "a" and B.name != "A":
            self.instant_translation.append("<" + A.name + "<->" + B.name + ">.")

    def nmod(self, A, B):
        # nmod(half,century)
        self.instant_translation.append("<" + A.name + "-->" + A.name + "_complex>.")
        self.instant_translation.append("<" + A.name + "_complex-->" + B.case + "_" + B.name + ">.")
        self.instant_translation.append("<" + B.case + "_" + B.name + "-->" + B.name + ">.")

    def nsubj(self, A, B):
        # nusbj(happen,it)
        A.subj = self.token_complex(B)
        if A.cop:
            self.instant_translation.append("<" + B.name + "-->" + A.name + ">.")
        if A.subj != "$" and A.obj != "$":
            self.token_complex(A)

    def obl(self, A, B):
        # obl(engage,half)
        self.instant_translation.append("<" + A.name + "_" + B.case + "-->" + A.name + ">.")
        A.name = A.name + "_" + B.case
        A.obj = self.token_complex(B)
        if A.subj != "$" and A.obj != "$":
            self.token_complex(A)

    def obj(self, A, B):
        # obj(have,it)
        A.obj = self.token_complex(B)
        if A.subj != "$" and A.obj != "$":
            self.token_complex(A)

    def cop(self, A, B):
        # cop(branch,is)
        A.cop = True

    def compound(self, A, B):
        # compound(science,computer)
        self.instant_translation.append("<" + B.name + "_" + A.name + "-->" + A.name + ">.")
        A.name = B.name + "_" + A.name

    def fixed(self, A, B):
        # fixed(according,to)
        self.instant_translation.append("<" + A.name + "_" + B.name + "-->" + A.name + ">.")
        A.name = A.name + "_" + B.name

    def nmod_poss(self, A, B):
        # nmod:poss(difficult,their)
        self.instant_translation.append("<" + A.name + "-->" + A.name + "_complex>.")
        self.instant_translation.append("<" + A.name + "_complex-->of_" + B.name + ">.")
        self.instant_translation.append("<of_" + B.name + "-->" + B.name + ">.")

    def acl_relcl(self, A, B):
        # acl:relcl(theory,focus)
        B.subj = self.token_complex(A)
        self.token_complex(B)

    def mark(self, A, B):
        # mark(want,that)
        pass

    def ccomp(self, A, B):
        # ccomp(say,want)
        A.obj = self.token_complex(B)
        if A.subj != "$" and A.obj != "$":
            self.token_complex(A)

    def aux(self, A, B):
        # aux(emerged,did)
        pass

    def xcomp(self, A, B):
        # xcomp(want,say)
        if A.obj != "$":
            B.subj = A.obj
        A.obj = self.token_complex(B)
        if A.subj != "$" and A.obj != "$":
            self.token_complex(A)

    def punct(self, A, B):
        # punct(apple,;)
        pass

    def dep(self, A, B):
        pass

    def cc(self, A, B):
        # cc(11th,and)
        A.cc = B.name

    def conj(self, A, B):
        # conj(10th,11th)
        if A.cc:
            cc = A.cc
        elif B.cc:
            cc = B.cc
        else:
            cc = "CC"
        self.instant_translation.append("<" + A.name + "_" + cc + "_" + B.name + "<->" + A.name + ">.")
        self.instant_translation.append("<" + A.name + "_" + cc + "_" + B.name + "<->" + B.name + ">.")

    def appos(self, A, B):
        # appos(Normandy,region)
        self.instant_translation.append("<" + A.name + "_" + B.name + "-->" + A.name + ">.")
        self.instant_translation.append("<" + A.name + "_" + B.name + "-->" + B.name + ">.")

    def csubj(self, A, B):
        # csubj(makes,said)
        # the second word's motion complex is the subject of the first word
        if not A.cop:
            if A.subj == "$":
                A.subj = self.token_complex(B)
                if A.subj != "$" and A.obj != "$":
                    self.token_complex(A)
            else:
                self.instant_translation.append("<" + A.subj + "<->" + self.token_complex(B) + ">.")
        else:
            if B.subj == "$":
                B.subj = self.token_complex(A)
                if B.subj != "$" and B.obj != "$":
                    self.token_complex(B)
            else:
                self.instant_translation.append("<" + B.subj + "<->" + self.token_complex(A) + ">.")

    def advcl(self, A, B):
        # advcl(talk,know)
        # if the first verb needs an object, B is its subject
        if A.obj == "$":
            A.obj = self.token_complex(B)
        if A.subj != "$" and A.obj != "$":
            self.token_complex(A)

    def acl(self, A, B):
        # acl(problem,classified)
        # B's object is A
        if B.obj == "$":
            B.obj = self.token_complex(A)
        if B.subj != "$" and B.obj != "$":
            self.token_complex(B)

    def split(self, s):
        return self.nlp.word_tokenize(s)

    def sentence_preProcessing(self, s, dep_replacing=False, replacing_num=0):
        Q = None
        if "?" in s:
            PT = self.nlp.pos_tag(s)
            for each in PT:
                if each[1] == "WP" or each[1] == "WDT":
                    Q = "<" + each[0] + "_complex<->?>?"
                    break
        dp = self.nlp.dependency_parse(s)
        s = self.split(s)
        for i in range(len(dp)):
            if dp[i][0] != "ROOT":
                if s[dp[i][1] - 1] + "_" + str(dp[i][1]) not in self.semi_cpt_dict:
                    self.semi_cpt_dict.update({s[dp[i][1] - 1] + "_" + str(dp[i][1]): semi_concept(s[dp[i][1] - 1])})
                if s[dp[i][2] - 1] + "_" + str(dp[i][2]) not in self.semi_cpt_dict:
                    self.semi_cpt_dict.update({s[dp[i][2] - 1] + "_" + str(dp[i][2]): semi_concept(s[dp[i][2] - 1])})
                dp[i] = [dp[i][0],
                         dp[i][1],
                         dp[i][2],
                         self.semi_cpt_dict[s[dp[i][1] - 1] + "_" + str(dp[i][1])],
                         self.semi_cpt_dict[s[dp[i][2] - 1] + "_" + str(dp[i][2])]]
        dp_cpy = copy.deepcopy(dp)
        if dep_replacing:
            tmp = [i for i in range(len(dp)) if dp[i][0] == "punct" or dp[i][0] == "mark" or dp[i][0] == "aux"]
            replacing_pos = random.sample(set(range(1, len(dp))) - set(tmp), replacing_num)
            for each in replacing_pos:
                dp_cpy[each][0] = "dep"
        return dp, dp_cpy, Q

    def relation_sequence_util(self, dp):
        ret = []
        new_dp = []
        OUT = [x[1] for x in dp]
        for each in dp:
            if each[2] not in OUT:
                ret.append(each)
            else:
                new_dp.append(each)
        return ret, new_dp

    def relation_sequence(self, dp):
        RET = []
        while len(dp) != 0:
            ret, dp = self.relation_sequence_util(dp)
            RET.append(ret)
        return RET

    def translate_util(self, single_rs):
        for each_relation in single_rs:
            if each_relation[0] == "ROOT":
                pass
            elif each_relation[0] == "advmod":
                self.advmod(each_relation[3], each_relation[4])
            elif each_relation[0] == "nummod":
                self.nummod(each_relation[3], each_relation[4])
            elif each_relation[0] == "amod":
                self.amod(each_relation[3], each_relation[4])
            elif each_relation[0] == "case":
                self.case(each_relation[3], each_relation[4])
            elif each_relation[0] == "det":
                self.det(each_relation[3], each_relation[4])
            elif each_relation[0] == "nmod":
                self.nmod(each_relation[3], each_relation[4])
            elif each_relation[0] == "nsubj":
                self.nsubj(each_relation[3], each_relation[4])
            elif each_relation[0] == "obl":
                self.obl(each_relation[3], each_relation[4])
            elif each_relation[0] == "obj":
                self.obj(each_relation[3], each_relation[4])
            elif each_relation[0] == "cop":
                self.cop(each_relation[3], each_relation[4])
            elif each_relation[0] == "compound":
                self.compound(each_relation[3], each_relation[4])
            elif each_relation[0] == "fixed":
                self.fixed(each_relation[3], each_relation[4])
            elif each_relation[0] == "nmod:poss":
                self.nmod_poss(each_relation[3], each_relation[4])
            elif each_relation[0] == "acl:relcl":
                self.acl_relcl(each_relation[3], each_relation[4])
            elif each_relation[0] == "mark":
                self.mark(each_relation[3], each_relation[4])
            elif each_relation[0] == "ccomp":
                self.ccomp(each_relation[3], each_relation[4])
            elif each_relation[0] == "aux":
                self.aux(each_relation[3], each_relation[4])
            elif each_relation[0] == "xcomp":
                self.xcomp(each_relation[3], each_relation[4])
            elif each_relation[0] == "punct":
                self.punct(each_relation[3], each_relation[4])
            elif each_relation[0] == "dep":
                self.dep(each_relation[3], each_relation[4])
            elif each_relation[0] == "cc":
                self.cc(each_relation[3], each_relation[4])
            elif each_relation[0] == "conj":
                self.conj(each_relation[3], each_relation[4])
            elif each_relation[0] == "appos":
                self.appos(each_relation[3], each_relation[4])
            elif each_relation[0] == "nsubj:pass":
                self.nsubj(each_relation[3], each_relation[4])
            elif each_relation[0] == "aux:pass":
                self.aux(each_relation[3], each_relation[4])
            elif each_relation[0] == "csubj":
                self.csubj(each_relation[3], each_relation[4])
            elif each_relation[0] == "advcl":
                self.advcl(each_relation[3], each_relation[4])
            elif each_relation[0] == "acl":
                self.acl(each_relation[3], each_relation[4])
            else:
                print("currently unknown:", each_relation[0])

    def translate(self, rs, show=True):
        for each_rs in rs:
            self.translate_util(each_rs)
        for each in self.semi_cpt_dict:
            if "_" + str(each_rs[0][-1]) in each:
                self.token_complex(self.semi_cpt_dict[each])  # for the root
                break
        if show:
            for each in set(self.instant_translation):
                print(each)
        return list(set(self.instant_translation))

    def tape_util(self, s, dep_replacing=False, replacing_num=0):
        self.instant_translation = []
        self.semi_cpt_dict = {}
        tmp = []
        for each in self.nlp.pos_tag(s):
            if each[0].isalpha():
                tmp.append("<" + each[0] + "-->" + each[1] + ">.")
        dp, dp_cpy, _ = self.sentence_preProcessing(s, dep_replacing, replacing_num)
        rs = self.relation_sequence(dp)
        _ = self.translate(rs, False)
        RET_NOADEP = self.instant_translation
        self.instant_translation = []
        rs_cpy = self.relation_sequence(dp_cpy)
        _ = self.translate(rs_cpy, False)
        RET_ADEP = self.instant_translation
        return tmp, list(set(RET_NOADEP)), list(set(RET_ADEP))

    def split2(self, s):
        return re.split("<|>|--|\.|,|\(|\)|\?", s)


def no_translate(s_temp):
    if s_temp.startswith('*'):
        return True
    else:
        return False


def bubble_sort(dp):
    # sort the dp according to the increasing distance between two words
    # a temporary fix to avoid missing translate like "A is B"
    for i in range(len(dp)):
        for j in range(len(dp) - 1):
            if abs(dp[j][2] - dp[j][1]) > abs(dp[j + 1][2] - dp[j + 1][1]):
                dp[j], dp[j + 1] = dp[j + 1], dp[j]

    return dp


while True:
    # s = input("Please input the sentence: ")
    s = input()

    if no_translate(s):
        print(s.strip('*').strip())
        continue

    W = EtN(nlp)
    dp, dp_dep, Q = W.sentence_preProcessing(s, dep_replacing=False, replacing_num=0)
    dp = bubble_sort(dp)
    rs = W.relation_sequence(dp)
    T = W.translate(rs, False)
    if Q:
        T.append(Q)
    for each in T:
        print(each)

    print('\n')
