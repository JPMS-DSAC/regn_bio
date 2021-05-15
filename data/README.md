**ALL_REGULATIONS_JSON_FLATTENED** - Each regulation, with split regulations, by date (These are the Pdfs converted into text from ALL_REGULATIONS_SPLIT)
----------------------------
**ALL_REGULATIONS_JSON_FLATTENED_SPLIT_SUBREG** - Each regulation, with split sub-regulations, by date (These are the Pdfs converted into text from ALL_REGULATIONS_SPLIT, and slight modifications of ALL_REGULATIONS_JSON_FLATTENED)
----------------------------
**ALL_REGULATIONS_JSONIFIED** - Each pdf, converted to text (ALL_REGULATIONS_SPLIT_TEXT) and jsonified using the Split into Sections code 
----------------------------
**ALL_REGULATIONS_SPLIT** - Documents from SEBI website, downloaded and grouped by regulation, name of each pdf is the date of release . Names were annotated manually
----------------------------
**ALL_REGULATIONS_SPLIT_TEXT** - ALL_REGULATIONS_SPLIT pdfs converted to text
----------------------------
**COMMENTS** - All matches from comment documents for certain regex patterns

all_amend_rational.match.txt --> 
`grep amendment .* rationale | rationale .* annotation` (-R text_output)

all_rational.match.txt -> 
`grep "rationale"`

all_reg_amend_match.txt -> 
`grep regulation .* amendment | amendment .* regulation` 

all_regs_match.txt ->
`grep SEBI \(.*?\) Regulations`

all_regulation_word_match.txt
`grep regulation`
----------------------------
**REGULATION_ANNOTATION** - Contains dumps of information pertaining to amendment annotation task (Annotating regulations)

All_annotation*.csv - CSV of pairwise matches of regulations with *generated tags* using Code
----------------------------
**regulation_rationale_match.json** - Dump of regulations and rationale matches 

List of [Regulation_Name, Date Identifier, Index of the matching regulation (with given name and date), Rationale Match]
----------------------------

**annual_reports_rationale_text** - folder with all text files of annual reports, that have rationale information, checked manually

**latest_regulations** - All latest regulations SEBI downloaded using the scraper


**RATIONALE_REGULATION_MATCH** -Contains a csv
    - [Text match Score, Regulation, Rationale text]
    - It is a dump of matches between different regulation and rationale
