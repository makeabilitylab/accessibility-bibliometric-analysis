# Accessibility bibliometric analysis
This repo contains scripts and data for reproducing the bibliometric analysis of citation diversity in accessibility and HCI research conducted in Wang LL *et al.*, our CHI LBW 2021 [paper](https://makeabilitylab.cs.washington.edu/media/publications/Wang_ABibliometricAnalysisOfCitationDiversityInAccessibilityAndHciResearch_EXTENDEDABSTRACTSOFCHI2021.pdf). 


This work is a complement to the [Mack *et al.* CHI 2021 paper](https://makeabilitylab.cs.washington.edu/media/publications/Mack_WhatDoWeMeanByAccessibilityResearchALiteratureSurveyOfAccessibilityPapersInChiAndAssetsFrom1994To2019_CHI2021.pdf), which has it's own [GitHub repo here](https://github.com/makeabilitylab/accessibility-literature-survey).

## Data files

Several data files are too large for GitHub. You can download them here:

* [a11y\_bibliometrics\_dataset.jsonl.gz](https://drive.google.com/file/d/1Abp2nTxXHrrVZ48r6dLgNW3qssDMmJof/view?usp=sharing)
* [a11y\_bibliometrics\_mag\_fos.jsonl.gz](https://drive.google.com/file/d/1CYVCbx3xxIBc1faSSsoGsjTwUzeYB-qN/view?usp=sharing)
* [dblp\_papers\_by\_conference.json.gz](https://drive.google.com/file/d/1Fm0D10GcVV6y0eMlTjJfC1MShlkc24n-/view?usp=sharing)

The directory structure for the `data/` subdirectory should be:

```
data
│   a11y_survey_quant_dataset.csv
│   dblp_container_meta.json
|   dblp_papers_by_conference.json.gz*
│
└───analysis
    │   a11y_bibliometrics_dataset.jsonl.gz*
    │   a11y_bibliometrics_mag_fos.jsonl.gz*
    |   lcdi_cits_by_papers_l1.json
    |   lcdi_refs_by_papers_l1.json
```

*Files with an asterisk have to be downloaded.

A brief description of the data files and what they contain:

* [a11y\_survey\_quant\_dataset.csv](https://github.com/makeabilitylab/accessibility-bibliometric-analysis/data/a11y_survey_quant_dataset.csv): The quantitative dataset from the Mack *et al.* paper
* [dblp\_container\_meta.json](https://github.com/makeabilitylab/accessibility-bibliometric-analysis/data/dblp_container_meta.json): Conference metadata extracted from the [DBLP data dump](https://dblp.org/faq/1474679.html)
* [dblp\_papers\_by\_conference.json.gz](https://drive.google.com/file/d/1Fm0D10GcVV6y0eMlTjJfC1MShlkc24n-/view?usp=sharing): Conference paper data extracted from the [DBLP data dump](https://dblp.org/faq/1474679.html)
* [a11y\_bibliometrics\_dataset.jsonl.gz](https://drive.google.com/file/d/1Abp2nTxXHrrVZ48r6dLgNW3qssDMmJof/view?usp=sharing): The main dataset of all papers used in analysis along with metadata, citation, and reference information
* [a11y\_bibliometrics\_mag\_fos.jsonl.gz](https://drive.google.com/file/d/1CYVCbx3xxIBc1faSSsoGsjTwUzeYB-qN/view?usp=sharing): The MAG field of study information corresponding to the papers in the dataset
* [lcdi\_refs\_by\_papers\_l1.json](https://github.com/makeabilitylab/accessibility-bibliometric-analysis/data/analysis/lcdi_refs_by_papers_l1.json): Data for plotting the results of the LCDI analysis for references; generated by running `scripts/get_lcdi_scores.py`
* [lcdi\_cits\_by\_papers\_l1.json](https://github.com/makeabilitylab/accessibility-bibliometric-analysis/data/analysis/lcdi_cits_by_papers_l1.json): Data for plotting the results of the LCDI analysis for citations; generated by running `scripts/get_lcdi_scores.py`

## Analysis

Plots and analysis are available in [this notebook](https://github.com/makeabilitylab/accessibility-bibliometric-analysis/notebooks/accessibility_bibliometrics_analysis.ipynb). This notebook includes:

* Summary statistics
* Top venues among references and citations of accessibility papers from CHI and ASSETS
* Top MAG fields of study among references and citations of accessibility papers from CHI and ASSETS
* Temporal trends of MAG fields of study among references and citations
* LCDI diversity index among the references and citations of 13 comparative HCI conferences

### Set up your environment:

If you are interested in running the code in this repo, you will need to set up a Python environment. 

1. Clone this repository

2. Install an environment manager (recommend [MiniConda3](https://docs.conda.io/en/latest/miniconda.html)). 

3. Go to the base directory for this repo and run the following in your command line:

```bash
conda create -n a11y_bibliometric_analysis python=3.8 ipython jupyter
conda activate a11y_bibliometric_analysis
pip install -r requirements.txt
python setup.py develop
```

You're ready to go!

## Citation

To cite this work:

>Wang LL, Mack K, McDonnell E, Jain D, Findlater L, Froehlich JE. A bibliometric analysis of citation diversity in accessibility and HCI research. In: *Proceedings of the 2021 ACM CHI Virtual Conference on Human Factors in Computing Systems: Extended Abstract*. Online. May 8-13, 2021.

```
@inproceedings{wang-2021-accessibility-bibliometrics,
    title = "A bibliometric analysis of citation diversity in accessibility and {HCI} research",
    author = "Wang, Lucy Lu and Mack, Kelly and McDonnell, Emma and Jain, Dhruv and Findlater, Leah and Froehlich, Jon E.",
    booktitle = "Proceedings of the 2021 ACM CHI Virtual Conference on Human Factors in Computing Systems: Extended Abstract",
    month = may,
    year = "2021",
    address = "Online",
    publisher = "Association for Computing Machinery",
    doi = "10.1145/3411763.3451618"
}
```

Please contact [Lucy Lu Wang](mailto:lucyw@allenai.org) if you have any questions.

