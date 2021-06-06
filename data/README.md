Documents from SEBI have been collected, and have been transformed for our tasks. This README explains the available data.

**ALL_REGULATIONS_SPLIT** - 
Regulatory documents from SEBI website, downloaded and grouped by the type of regulation, name of each pdf is the date of release of the . Names were annotated manually

Example : 
|- Alternative Investment Funds
| -- Jan08_2021.pdf
| -- Sep16_2013.pdf

Jan08_2021 version of the regulatory document Alternative Investment Funds

* Certain older versions of the regulatory documents are present in text form, and present as .txt files in their corresponding folders. 
  
----------------------------

**ALL_REGULATIONS_SPLIT_TEXT** - All the pdfs of regulatory documents in ALL_REGULATIONS_SPLIT folder are converted to text.
Each pdf document has been converted into the corresponding text document with the same name, using a pdf to text converter tool.

Example : 
|- Alternative Investment Funds
| -- Jan08_2021.txt
| -- Sep16_2013.txt

Jan08_2021.txt is the text form of the Jan08_2021.pdf document in the previous section

* Certain older versions of the regulatory documents are alreay in text files, and have just been copied to their corresponding folders in ALL_REGULATIONS_SPLIT_TEXT as is. 

----------------------------

**ALL_REGULATIONS_JSONIFIED** - There are two transformations happening from ALL_REGULATIONS_SPLIT_TEXT. 

First is that each text document has been split into its constituent chapters and sections (Each section has a small number of regulations).
Second is that all versions of a given regulatory document have been clubbed into a single json.

`JSON format : 
 {
     "VERSION_DATE" : {
         "CHAPTER TITLE" : 
            {
                "SECTION TITLE": 
                "CONTENT OF THE SECTION" 
            }
         }
 }`

Example `Substantial_Acquisition_of_Shares_and_Takeovers.json`

`   "May25_2016": {
        "CHAPTER -II": {
            "chap_title": "SUBSTANTIAL ACQUISITION OF SHARES, VOTING RIGHTS OR CONTROL",
            "3": {
                "title": "Acquisition of control.",
                "content": [
                    "3.(1)  No acquirer shall acquire shares or voting rights in a target company which takentogether with shares or voting rights, if any, held by him and by persons acting inconcert with him in such target company, entitle them to exercise twenty-five percent  or  more  of  the  voting  rights  in  such  target  company  unless  the  acquirermakes  a  public  announcement  of  an  open  offer  for  acquiring  shares  of  suchtarget company in accordance with these regulations.2016, w.e.f. 25-05-2016.6 Clause  (ze)  renumbered  as  clause  \u2015(zf)\u2016  by  the  SEBI  (Substantial  Acquisition  of  Shares  and  Takeovers)(Second Amendment) Regulations, 2016, w.e.f. 25-05-2016.(2)  No acquirer, who together with persons acting in concert with him, has acquiredand holds in accordance with these regulations shares or voting rights in a targetcompany  entitling  them  to  exercise  twenty-five  per  cent  or  more  of  the  votingrights  in  the target  company but  less than the maximum  permissible non-publicshareholding, shall acquire within any financial year additional shares or votingrights in such target company entitling them to exercise more than five per centof the voting rights, unless the acquirer makes a public announcement of an openoffer  for  acquiring  shares  of  such  target  company  in  accordance  with  theseregulations:Provided that such acquirer shall not be entitled to acquire or enter into anyagreement to acquire shares or voting rights exceeding such number of shares aswould  take  the  aggregate  shareholding  pursuant  to  the  acquisition  above  themaximum permissible non-public shareholding.additional voting rights under this sub-regulation,\u2014(i) gross  acquisitions  alone  shall  be  taken  into  account  regardless  of  anyintermittent fall in shareholding or voting rights whether owing to disposalof shares held or dilution of voting rights owing to fresh issue of shares bythe target company.(ii) in the case of acquisition of shares by way of issue of new shares by thetarget  company  or  where  the  target  company  has  made  an  issue  of  newshares  in  any  given  financial  year,  the  difference  between  the  pre-allotment and the post-allotment percentage voting rights shall be regardedas the quantum of additional acquisition .(3)  For  the  purposes  of  sub-regulation  (1)  and  sub-regulation  (2),  acquisition  ofshares  by  any  person,such  that  the  individual  shareholding  of  such  personacquiring  shares  exceeds  the  stipulated  thresholds,  shall  also  be  attracting  theobligation  to  make  an  open  offer  for  acquiring  shares  of  the  target  companyirrespective  of  whether  there  is  a  change  in  the  aggregate  shareholding  withpersons acting in concert.7[(4)  Nothing  contained  in  this  regulation  shall  apply  to  acquisition  of  shares  orvoting rights of a company by the promoters or shareholders in control, in termsof  the  provisions  of  Chapter  VI-A  of  Securities  and  Exchange  Board  of  India"
                ]
            },
            "4": {
                "title": "Indirect acquisition of shares or control.",
                "content": [
                    "4.",
                    "Irrespective of acquisition or holding of shares or voting rights in a target company,",
                    "no acquirer shall acquire, directly or indirectly, control over such target company",
                    "unless  the  acquirer  makes  a  public  announcement  of  an  open  offer  for  acquiring",
                    "shares of such target company in accordance with these regulations."
                ]`

Here, May25_2016 is one of the versions of the SAST regulations, with CHAPTER-II having sections 3 and 4, which have one regulation each.

  * Note that the regulations in the sections have not been grouped yet, they exist as seperate lines, because of the text conversion. 
----------------------------

**ALL_REGULATIONS_JSON_FLATTENED** - Each section of each version of the regulatory document from ALL_REGULATIONS_JSONIFIED, have been neatly spliced into the corresponging regulations.

`JSON format : 
 {
     "VERSION_DATE" : [
         [[REGULATION_NUMBER], [""], [REGULATION_TEXT]]
     ]
 }`

` "May25_2016": [ [..], 
                ["4", "", "Irrespective of acquisition or holding of shares or voting rights in a target company, no acquirer shall acquire, directly or indirectly, control over such target company unless  the  acquirer  makes  a  public  announcement  of  an  open  offer  for  acquiring shares of such target company in accordance with these regulations."],
                 [..] ] 
` 

Here "4" is the number of the regulation, and "Irrespective of  ..." is the content of regulation 4. This regulation is part of the May25_2016 version of SAST regulations
Regulation number can be a combination of int and string eg : "4B".

Note : The middle row is always `[""]` and is just present for easier code writing where this data is used, and doesnt have any other significance

----------------------------

**ALL_REGULATIONS_JSON_FLATTENED_SPLIT_SUBREG** - Each regulation text in ALL_REGULATIONS_JSON_FLATTENED has been split into subregulations. 
The format remains the same, except that `REGULATION_TEXT` has been split into its corresponding subregulations.


`JSON format : 
 {
     "VERSION_DATE" : [
         [[REGULATION_NUMBER], [""], [REGULATION_TEXT - SPLIT INTO SUBREGULATIONS]]
     ]
 }`

`[
    "May25_2016": 
            [
            
            "5A",
            "",
            [
                "(1) Notwithstanding anything contained in these regulations, in the event the acquirer makes a public announcement of an open offer for acquiring shares of a target company in terms of regulations 3, 4 or 5, he may delist the company in accordance with provisions of the Securities and Exchange Board of India (Delisting of Equity Shares) Regulations, 2009: Provided that the acquirer shall have declared upfront his intention to so delist at the time of making the detailed public statement.w.e.f. 24-03-2015.",
                "(2) Where an offer made under sub-regulation (1) is not successful,-(i) on account of non\u2013receipt of prior approval of shareholders in terms of clause (b) ofsub-regulation (1) of regulation 8 of Securities and Exchange Board of India (Delistingof Equity Shares) Regulations, 2009; or(ii) in  terms  of regulation  17 of Securities  and Exchange Board of  India  (Delisting ofEquity Shares) Regulations, 2009; or(iii)  on  account  of  the  acquirer  rejecting  the  discovered  price  determined  by  the  bookbuilding  process  in  terms  of  sub-regulation  (1)  of  regulation  16  of  Securities  andExchange Board of India (Delisting of Equity Shares) Regulations, 2009,the acquirer shall make  an announcement within two working  days in  respect  of suchfailure in all the newspapers in which the detailed public statement was made and shallcomply with all applicable provisions of these regulations.",
                "(3)  In  the  event  of  the  failure  of  the  delisting  offer  made  under  sub-regulation(1),  the acquirer,  through  the  manager  to  the  open  offer,  shallwithin  five  working  days  from  the date of the announcement under sub-regulation(2), file with the Board, a draft of the letter of offer as specified insub-regulation  (1) of regulation  16 and shall comply with  all other applicableprovisions of these regulations: Provided  that  the  offer  price  shall  stand  enhanced  by  an  amount  equal  to  asum determined at the rate of ten per cent per annum for the period betweenthe scheduled date of  payment  of  consideration  to  the  shareholders  and  theactual  date  of  payment  of consideration to the shareholders which the payment of consideration ought to have been made tothe shareholders in terms of the timelines in these regulations.",
                "(4) Where a competing offer is made in terms of sub-regulation (1) ofregulation 20,-(a) the acquirer shall not be entitled to delist the company;(b) the acquirer shall not be liable to pay interest to the shareholders onaccount of delaydue to competing offer;(c) the acquirer shall comply with all the applicable provisions of theseregulations andmake an announcement in this regard, within twoworking days from the date of publicannouncement  made  in  terms  ofsub-regulation  (1)  of  regulation  20,  in  all  thenewspapers in which thedetailed public statement was made.",
                "(5)  Shareholders  who  have  tendered  shares  in  acceptance  of  the  offer  madeunder  sub- regulation  (1),  shall  be  entitled  to  withdraw  such  shares  tendered,within 10  working  days from the date of the announcement under sub-regulation(2) .",
                "(6) Shareholders who have not tendered their shares in acceptance of theoffer made under sub-regulation  (1)  shall  be  entitled  to  tender  their  shares  inacceptance  of  the  offer  made"
            ]

        ],

        [... Other Regulations]
`
Here "5A" is the number of the regulation, and has been split into 6 sub-regulations. This regulation is part of the May25_2016 version of SAST regulations
Regulation number can be a combination of int and string eg : "4B".

Note : The middle row is always `[""]` and is just present for easier code writing where this data is used, and doesnt have any other significance

----------------------------

**SEBI_DOCUMENTS_TEXT** - Folder consisting of all documents downloaded from SEBI, grouped by document type in text form. 

Example : 

SEBI_DOCUMENTS_TEXT 
|- annual_reports 
|-- ar01024_p.txt

----------------------------

**COMMENTS** - Using grep and pattern matching, pattern matched text was extracted from SEBI_DOCUMENTS_TEXT.
For example, all_rational_match.txt has matches for all lines in these documents where the word rationale has been mentioned. This data has been pushed
to a text file.

The grep command used for genetating each of these filess have been mentioned below 

all_amend_rational_match.txt --> 
`grep amendment .* rationale | rationale .* annotation` (-R SEBI_DOCUMENTS_TEXT) -C 2

all_rational_match.txt -> 
`grep "rationale"`

all_reg_amend_match.txt -> 
`grep regulation .* amendment | amendment .* regulation` 

all_regs_match.txt ->
`grep SEBI \(.*?\) Regulations`

all_regulation_word_match.txt
`grep regulation`

Example : 

Format : Refer to grep for better understanding of the format.
In brief, each file has rows of this nature 

`--

FILE NAME : (lines containing the matched text)

FILE NAME - (adjacent lines to the match)

-- (Delimiters that seperate the matches)`

`all_amend_rational_match.txt :

--
press_releases/cef84d39a84bc838057416351dcfd8b1.txt:   SEBI seeks public comments on Report submitted by the Committee on Fair Market ConductSEBI constituted a Committee on Fair Market Conduct in August, 2017 under the Chairmanship of Shri T.K. Viswanathan, Ex-Secretary General, Lok Sabha and Ex- Law Secretary. The Committee was mandated to review the existing legal framework to deal with market abuse to ensure fair market conduct in the securities market. The Committee was also mandated to review the surveillance, investigation and enforcement mechanisms being undertaken by SEBI to make them more effective in protecting market integrity and the interest of investors from market abuse. The Committee comprised of representatives of law firms, mutual funds, brokers, forensic auditing firms, stock exchanges, chambers of commerce, data analytics firms and SEBI.The committee has submitted its report to SEBI on August 08, 2018 wherein it has recommended amendments to SEBI Act,1992, SEBI (Prohibition of Insider Trading) Regulations, 2015 and SEBI (Prohibition of Fraudulent and Unfair Trade Practices relating to Securities Markets) Regulations, 2003.  A copy of the report is placed on the SEBI website at the following link: https://www.sebi.gov.in/reports/reports/aug-2018/report-of-committee-on-fair-market-conduct-for-public-comments_39884.html Comments from public are invited on the recommendations contained in the aforesaid report in the following format:Chapter and sub-heading to which the comment pertainsRecommendations of Committee Suggestions / CommentsRationale for Suggestions / CommentsComments may be sent by email to Ms. Maninder Cheema, General Manager at maninderc@sebi.gov.in and Mr. Nitesh Bhati, Assistant General Manager at niteshb@sebi.gov.in latest by August 24, 2018. 
press_releases/cef84d39a84bc838057416351dcfd8b1.txt-

`
----------------------------

**REGULATION_ANNOTATION** - Contains dumps of information pertaining to amendment annotation task. Each row compares a regulation with the older version of the regulation. This comparision uses some information such as the regulation numbers, date of the corresponding version of the regulation document and the o


All_annotation_latest.csv - CSV of pairwise matches of regulations with *generated tags* using Code

CSV file, with the following rows and a brief explanation


*Input* : 
Regulation - Regulation text

Text of last amendment - Older version of this regulation

footnoted - Edits that have happened between Regulation and Text of last amendment,

cleaned regulation - Regulation text cleaned off of footnote numbers

Document Name - Name of the regulation document where the regulation is from 

Old num - Regulation Number of the older version of regulation

New num - Regulation Number of the new version of regulation,

Old date - Date of the version of the regulation document which the old regulation belongs to ,

New date - Date of the version of the regulation document which the new regulation belongs to

*Output* : 
Amendment type  : Insertion/Substitution etc. 

Amendment Document : Same as amendment type

Amendment Effect : Update, Proviso, Meaning Assigned etc.

Amendment Function : Declaration , Cross Reference etc. 
 
These output tags are generated by the rule based tagger.

----------------------------
**regulation_rationale_match.json** - Dump of regulations and rationale matches 

Using text similarity each rationale has been matched to the corresponding regulation

Format :  `List of [Regulation_Name, Date Identifier, Index of the matching regulation (with given name and date), Rationale Match]`

`[
    [
        "Mutual Funds",
        "May06_2014",
        46,
        "vi.  amendment  to  the  sebi  (mutual funds) regulations, 1996 sebi  (mutual  funds)  regulations,  1996  were amended on april 8, 2009 to:- a)  make listing of close ended schemes mandatory.1. 136\fpart four: regulatory changesc) crore rupees. for  issuers  making  fast  track  issue,  whose  public  shareholding  is less than 15 percent of its issued  equity  capital,  eligibility  regarding  the  annualised  trading  turnover  of  issuers  equity  shares  has  been  changed and it has to be calculated  as  at  least  two  percent  of  the  weighted average number of equity  shares available as free float during  six  months  immediately  preceding  the reference date.d)  for issuers making fast track issue,  eligibility  regarding  compliance  with  equity  listing  agreement  has  been  changed  to  provide  that  if  the  issuer  has  not  complied  with  the  provision  of ..."
    ]
]`  

The above example is matching regulation 46 of May 06 2014 version of Mutual Funds regulations to the rationale text "vi. amendment to ...."

----------------------------
**RATIONALE_REGULATION_MATCH** - Dump of regulation and rationale matches

Using text similarity each rationale has been matched to the corresponding regulation. It is a json containing a row of lists.

Format : `[Text match Score, Regulation, Rationale text]`

Regulation - Regulation text 

Rationale text - The matched rationale text

Text match score - The text similarity score