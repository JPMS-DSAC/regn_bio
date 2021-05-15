from collections import deque
import pandas as pd
import re
import nltk
from nltk.stem import PorterStemmer
from nltk import word_tokenize, pos_tag
import json


def footnote(row):
    regtext = row['Regulation']
    searchobj = re.search('[1-9][0-9]*\ *\[(.*?)\]', regtext)
    if searchobj is not None:
        return searchobj.group(1)
    else:
        return ""


def clean_regulation(row):
    regtext = row['Regulation']
    cleaned_regtext = re.sub('[1-9][0-9]*\ *\[(.*?)\]', r"\1", regtext)
    return cleaned_regtext


def clean_regulation_for_comparision(regtext):
    cleaned_regtext = re.sub('[1-9][0-9]*\ *\[(.*?)\]', r"\1", regtext)
    return cleaned_regtext


def detect_acts(text, CURRENT_AMENDMENT):
    reg_list = """Alternative Investment Funds
    Collective Investment Scheme
    Substantial Acquisition of Shares and Takeovers
    Buy Back Of Securities
    Share Based Employee Benefits
    Foreign Venture Capital Investor
    Central Database of Market Participants
    Mutual Funds
    Certification of Associated Persons in the Securities Markets
    Depositories and Participants
    Stock Exchanges and Clearing Corporations
    Settlement of Administrative and Civil Proceedings
    Stock Brokers
    Credit Rating Agencies
    Issue and Listing of Securities Debt Instruments and Security Receipts
    Issue and Listing of Debt Securities
    Investment Advisers
    Investor Protection and Education Fund
    Regulatory Fee on Stock Exchanges
    Issue of Capital and Disclosure Requirements
    SEBI Know Your Client
    Issues and Listing of Muncipal Debt Securities
    Issue of Sweat Equity
    Delisting of Equity Shares
    Merchant Bankers
    Prohibition of Insider Trading
    Procedure of Search and Seizure
    Issue and Listing of Non Convertible Redeemable Preference Shares
    Portfolio Managers
    Listing of Specified Securities on Institutional Trading Platform
    Listing Obligations and Disclosure
    Companies Act
    Securities Contracts (Regulation) Act
    Securities and Exchange Board of India Act
    Depositories Act
    Fugitive Economic Offenders Act
    Insolvency and Bankruptcy Code"""
    reg_array = [reg_name.strip().lower() for reg_name in reg_list.split("\n")]
#     print(reg_array)
    for reg_name in reg_array:
        if (CURRENT_AMENDMENT.lower() not in reg_name) and (reg_name in text):
            return reg_name
    return None


def printc(text, color):
    CRED = '\033[91m'
    CEND = '\033[0m'
    return CRED + text + CEND


def get_amendment_type(amendment_document):
    cleaned_line = amendment_document.strip().lower()
    list_of_words = cleaned_line.split(' ')
    ps = PorterStemmer()

    first_word_stemmed = ps.stem(list_of_words[0])
    if first_word_stemmed == 'substitut':
        return "Substitution"
    elif first_word_stemmed == 'insert':
        return 'Insertion'
    elif first_word_stemmed == 'omit':
        return 'Omission'

    if list_of_words[0] == "proviso" and ps.stem(list_of_words[1]) == "substitut":
        return "Substitution"

    if 'renumb' in [ps.stem(ele) for ele in list_of_words[:4]]:
        return "Renumbered"


def get_amendment_function(row, amendment_type, CURRENT_AMENDMENT="Substantial Acquisition of Shares and Takeovers"):
    if amendment_type == "Renumbered":
        return "Re-numbering"
    if amendment_type == "Insertion" or amendment_type == "Substitution":
        any_match = detect_acts(
            row["Amendment Document"].lower(), CURRENT_AMENDMENT)
        if any_match is not None:
            return "Cross Reference"

        any_match = detect_acts(row["footnoted"].lower(), CURRENT_AMENDMENT)
        if any_match is not None:
            return "Cross Reference"

    if amendment_type == "Omission":
        return "Repeal"

    return "Declaration"


def get_amendment_effect(row, amendment_type):
    def_regex = re.compile(
        """(\"|\“|“|‘|‘)\ *(.*)\ *(\"|\”|”|’|’)\ *? (shall have the same meaning.*|shall have\ +?the meaning.*|means.*|includes.*|shall be defined|)""")

    squared_regulation = row['footnoted'].lower()
    proviso_list = ["provided that", "notwithstanding", "nothing contained in"]

    match = def_regex.search(row["footnoted"].lower())
    if match is not None:
        return "Meaning Assigned"
    if amendment_type == "Renumbered":
        return "None"
    if amendment_type == "Omission":
        return "Exclusion"
    if any([word in squared_regulation for word in proviso_list]):
        return "Proviso"
    if amendment_type == "Substitution":
        return "Update"
    if amendment_type == "Insertion":
        if len(word_tokenize(squared_regulation)) == 1:
            list_of_pos_tags = pos_tag(word_tokenize(
                row["Amendment Document"].lower()))
            for word in list_of_pos_tags:
                if squared_regulation.strip() == word[0] and word[1] == "JJ":
                    return "Strict"
        return "Inclusion"
    else:
        return ""


def lcs(a, b):
    """
    Word level LCS
    a : array of words
    b : array of words
    """
    # generate matrix of length of longest common subsequence for substrings of both words
    lengths = [[0] * (len(b)+1) for _ in range(len(a)+1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if x == y:
                lengths[i+1][j+1] = lengths[i][j] + 1
            else:
                lengths[i+1][j+1] = max(lengths[i+1][j], lengths[i][j+1])

    # read a substring from the matrix

    result = []
    j = len(b)
    for i in range(1, len(a)+1):
        if lengths[i][j] != lengths[i-1][j]:
            result.append(a[i-1])

    qa = deque(a)
    qb = deque(b)
    rq = deque(result)

    ansa = []
    ansb = []
    new_text = []
    while rq:
        common_ele = rq.popleft()
        while len(qa) >= 1 and qa[0] != common_ele:
            ansa.append((qa.popleft()))
        while len(qb) >= 1 and qb[0] != common_ele:
            ala = qb.popleft()
            ansb.append((ala))
            new_text.append(ala)

        ansa.append((common_ele))
        ansb.append((common_ele))

        if len(qa) >= 1:
            qa.popleft()
        if len(qb) >= 1:
            qb.popleft()

    while len(qa) >= 1:
        ansa.append((qa.popleft()))
    while len(qb) >= 1:
        ansb.append((qb.popleft()))

    return ' '.join(new_text)


def get_amendment_type_from_comparision(new_text, old_text, new_t_num, old_t_num, ):
    if new_text == "":
        return "Omission"
    if old_text == "":
        return "Insertion"
    if new_t_num != old_t_num and new_text == old_text:
        return "Renumbering"
    elif old_text == new_text:
        return "Nochange"
    else:
        return "Substitution"


def get_footnoted_text(new_text, old_text):
    return lcs(old_text.split(' '), new_text.split(' '))

# S.N. 	Regulation 	Amendment type 	Amendment Function 	Amendment Effect 	Amendment Document 	Text of last amendment 	footnoted 	cleaned regulation


def process_comparision_text(old_text, new_text, document_name, old_t_num, new_t_num, old_reg_date, new_reg_date):
    row_elem = {}
    row_elem["Regulation"] = new_text

    row_elem["Text of last amendment"] = old_text
    row_elem["footnoted"] = get_footnoted_text(new_text, old_text)
    row_elem["cleaned regulation"] = clean_regulation_for_comparision(new_text)
    row_elem["Amendment type"] = get_amendment_type_from_comparision(
        new_text, old_text, new_t_num, old_t_num)
    row_elem["Amendment Document"] = row_elem["Amendment type"]
    row_elem["Document Name"] = document_name
    row_elem["Old num"] = old_t_num
    row_elem["New num"] = new_t_num
    row_elem["Old date"] = old_reg_date
    row_elem["New date"] = new_reg_date

    row = row_elem
    amendment_text = row['Amendment type']
    
    amtx = amendment_text
    ameff = get_amendment_effect(row, amtx)
    amfun = get_amendment_function(
        row, amtx, CURRENT_AMENDMENT=row['Document Name'])

    return [amtx if amtx != "Nochange" else "", ameff, amfun]


def get_tags_l1(ele, key1, key2, fol_name):
    od, nd = key1, key2
    return [ele[0], ele[1], fol_name, ele[2], ele[3], od, nd]


def get_tags(ele, key1, key2, fol_name):
    ele = get_tags_l1(ele, key1, key2, fol_name)

    ot = ""
    nt = ""
    if type(ele[0]) == list:
        ot = ele[0][0]
    else:
        ot = ele[0]

    if type(ele[1]) == list:
        nt = ele[1][0]
    else:
        nt = ele[1]

    return process_comparision_text(ot, nt, ele[2], ele[3], ele[4], ele[5], ele[6])
