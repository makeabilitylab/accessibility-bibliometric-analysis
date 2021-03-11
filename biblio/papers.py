import os, sys
import json
import gzip
import re
from typing import Dict, List, Tuple, Optional
from collections import defaultdict


# load DBLP conference data
print('loading dblp data; this will take a moment...')
DBLP_ALL_FILE = 'data/dblp_papers_by_conference.json.gz'
with gzip.open(DBLP_ALL_FILE, 'r') as f:
    data = json.load(f)

# create mappings between DOIs and DBLP conf identifiers and years
DBLP_DOI_TO_CONF = dict()
DBLP_DOI_TO_YEAR = dict()
for conf_key, papers in data.items():
    for paper in papers:
        if paper['doi']:
            DBLP_DOI_TO_CONF[paper['doi'].lower()] = conf_key
            DBLP_DOI_TO_YEAR[paper['doi'].lower()] = paper['year']

VENUE_2_DIGIT_YEAR_REGEX = r"(\'\d{2})"
VENUE_4_DIGIT_YEAR_REGEX = r"(\d{4})"

S2_VENUE_NORMALIZATION = {
        'HCI': 'conf/hci',
        'Graphics Interface': 'conf/graphicsinterface',
        'ASSETS': 'conf/assets',
        'UIST': 'conf/uist',
        'UbiCOMP': 'conf/huc',
        'UbiComp': 'conf/huc',
        'CSCW': 'conf/cscw',
        'IUI': 'conf/iui',
        'DIS': 'conf/ACMdis',
        'OzCHI': 'conf/ozchi',
        'TEI': 'conf/tei',
        'IDC': 'conf/acmidc',
        'NordiCHI': 'conf/nordichi',
        'Lecture Notes in Computer Science': 'series/lncs',
        'BCS HCI': 'conf/bcshci',
        'INTERSPEECH': 'conf/interspeech',
        'CUU': 'CUU',
        'IEEE transactions on rehabilitation engineering : a publication of the IEEE Engineering in Medicine and Biology Society': 'IEEE Transactions on Rehabilitation Engineering',
        'ACM Trans. Access. Comput.': 'journals/taccess',
        'LREC': 'conf/lrec',
        'Optometry and vision science : official publication of the American Academy of Optometry': 'Optometry and vision science',
        'Universal Access in the Information Society': 'journals/uais',
        'IHC': 'conf/ihc',
        'AMCIS': 'conf/amcis',
        'PervasiveHealth': 'conf/ph',
        'SOUPS': 'conf/soups',
        'ICWSM': 'conf/icwsm',
        'Studies in health technology and informatics': 'series/shti',
        'MIS Q.': 'journals/misq',
        'HCOMP': 'conf/hcomp',
        'IxD&A': 'journals/ixda',
        'ICCHP': 'conf/icchp',
        'NIME': 'conf/nime',
        'Human–Computer Interaction Series': 'series/hci',
        'MM 2003': 'MM',
        'HICSS': 'conf/hicss',
        'ICMC': 'conf/icmc',
        'EMNLP': 'conf/emnlp',
        'International Conference on Internet Computing': 'conf/ic',
        'IEEE Transactions on Biomedical Engineering': 'journals/tbe',
        'SOUPS @ USENIX Security Symposium': 'conf/soups',
        'SLPAT@NAACL': 'conf/slpat',
        'RoCHI': 'conf/rochi',
        'ICEIS': 'conf/iceis',
        'CHI PLAY': 'conf/chiplay',
        'WEBIST': 'conf/webist',
        'Presence: Teleoperators & Virtual Environments': 'journals/presence',
        'USENIX Security Symposium': 'conf/uss',
        'AAAI': 'conf/aaai',
        'SLPAT@HLT-NAACL': 'conf/slpat',
        'ACL': 'conf/acl',
        'AUIC': 'conf/auic',
        'ICAD': 'conf/icad',
        'The American journal of occupational therapy : official publication of the American Occupational Therapy Association': 'The American journal of occupational therapy',
        'PETRA': 'conf/petra',
        'ECIS': 'conf/ecis',
        'First Monday': 'journals/firstmonday',
        'TacTT@ITS': 'TacTT',
        'HLT-NAACL': 'conf/naacl',
        'Inf. Res.': 'journals/ires',
        'CHI': 'conf/chi',
        # Stopped normalizing at 'JMIR rehabilitation and assistive technologies'
    }


def normalize_year(year_str: str) -> Optional[int]:
    """
    Normalize year str
    :param year_str:
    :return:
    """
    if not year_str or not year_str.isdigit():
        return None

    year_num = int(year_str)

    if len(year_str) == 2:
        if year_num < 30:
            return 2000 + year_num
        else:
            return 1900 + year_num
    elif len(year_str) == 4:
        return year_num
    else:
        print(f'Not a year: {year_str}')
        return None


def normalize_venue(venue_str: str) -> Tuple[Optional[str], Optional[int]]:
    """
    Normalize venue string
    :param venue_str:
    :return:
    """
    # just return the conf/journal string if it's a dblp identifier
    if venue_str.startswith('conf/') or venue_str.startswith('journal/'):
        return venue_str, None
    # just return norm name if in dict
    if venue_str in S2_VENUE_NORMALIZATION:
        return S2_VENUE_NORMALIZATION[venue_str], None
    # year match regex
    matches = re.findall(VENUE_2_DIGIT_YEAR_REGEX, venue_str)
    if not matches:
        matches = re.findall(VENUE_4_DIGIT_YEAR_REGEX, venue_str)
    # return match strings as venue and year
    if matches and len(matches) == 1:
        start_ind = venue_str.find(matches[0])
        end_ind = start_ind + len(matches[0])
        before_part = venue_str[:start_ind].strip()
        year_part = venue_str[start_ind:end_ind].strip("'")
        after_part = venue_str[end_ind:].strip()
        if len(before_part) > len(after_part):
            venue_name = S2_VENUE_NORMALIZATION[before_part] \
                if before_part and before_part in S2_VENUE_NORMALIZATION \
                else before_part.lower()
        else:
            venue_name = S2_VENUE_NORMALIZATION[after_part] \
                if after_part and after_part in S2_VENUE_NORMALIZATION \
                else after_part.lower()
        return venue_name, normalize_year(year_part)
    return venue_str, None


class Paper:
    def __init__(
            self,
            pid: int,
            doi: str,
            sha: str,
            venue: Optional[str],
            year: Optional[int],
            fos: Optional[List],
            title: Optional[str],
            refs: List[int],    # references (S2 corpus id)
            cits: List[int]     # citations (S2 corpus id)
    ):
        if not pid and not doi and not sha:
            raise NotImplementedError
        self.pid = pid if pid else None
        self.doi = doi.lower() if doi else None
        self.sha = sha.lower() if sha else None
        if doi and doi.lower() in DBLP_DOI_TO_CONF:
            self.venue = DBLP_DOI_TO_CONF[doi.lower()]
            self.year = DBLP_DOI_TO_YEAR[doi.lower()]
        else:
            # try to get something from S2 venue
            if venue:
                venue_name, venue_year = normalize_venue(venue)
                self.venue = venue_name
                self.year = venue_year
            else:
                self.venue = None
                self.year = None
            # and keep year if there's a year
            if year:
                self.year = year
        self.fos = sorted(fos, key=lambda x: x[1], reverse=True) if fos else None
        self.title = title if title else None
        self.refs = refs if refs else []
        self.cits = cits if cits else []

    def __eq__(self, p2):
        if self.pid and p2.pid and self.pid == p2.pid:
            return True
        if self.doi and p2.doi and self.doi == p2.doi:
            return True
        if self.sha and p2.sha and self.sha == p2.sha:
            return True
        return False

    def __hash__(self):
        return hash((self.pid, self.doi, self.sha))

    def __repr__(self):
        return json.dumps({
            "pid": self.pid,
            "doi": self.doi,
            "sha": self.sha,
            "venue": self.venue,
            "year": self.year,
            "fos": [fos_entry[2] for fos_entry in self.fos] if self.fos else None,
            "title": self.title,
            "references": len(self.refs) if self.refs else 0,
            "citations": len(self.cits) if self.cits else 0
        })

    def as_json(self):
        return {
            "pid": self.pid,
            "doi": self.doi,
            "sha": self.sha,
            "venue": self.venue,
            "year": self.year,
            "fos": self.fos,
            "title": self.title,
            "refs": self.refs,
            "cits": self.cits
        }

    @property
    def l0_fos(self):
        if not self.fos:
            return None
        return [entry for entry in self.fos if entry[-1] == 0]

    @property
    def l1_fos(self):
        if not self.fos:
            return None
        return [entry for entry in self.fos if entry[-1] == 1]

    @property
    def l2_fos(self):
        if not self.fos:
            return None
        return [entry for entry in self.fos if entry[-1] == 2]

    def has_fos(self, fos_str: str) -> bool:
        if not self.fos:
            return False
        for fos_entry in self.fos:
            if fos_str == fos_entry[2]:
                return True
        return False


class PaperLookup:
    def __init__(self, paper_list: List[Paper]):
        self.papers = paper_list
        self.pid_dict = dict()
        self.doi_dict = dict()
        self.sha_dict = dict()
        for paper in paper_list:
            if paper.pid:
                self.pid_dict[paper.pid] = paper
            if paper.doi:
                self.doi_dict[paper.doi] = paper
            if paper.sha:
                self.sha_dict[paper.sha] = paper

    def get_paper_by_pid(self, pid: int):
        if pid in self.pid_dict:
            return self.pid_dict[pid]
        else:
            return None

    def get_paper_by_doi(self, doi: str):
        if doi.lower() in self.doi_dict:
            return self.doi_dict[doi.lower()]
        else:
            return None

    def get_paper_by_sha(self, sha: str):
        if sha.lower() in self.sha_dict:
            return self.sha_dict[sha.lower()]
        else:
            return None

    def get_paper_by_triple(self, paper_ids):
        pid, doi, sha = paper_ids
        pid = int(pid) if pid else None
        if pid and pid in self.pid_dict:
            return self.pid_dict[pid]
        if doi and doi.lower() in self.doi_dict:
            return self.doi_dict[doi]
        if sha and sha in self.sha_dict:
            return self.sha_dict[sha]
        return None

    def get_papers_in_venue(self, venue_str: str) -> List[Paper]:
        norm_venue, _ = normalize_venue(venue_str)
        if not norm_venue:
            return []
        return [p for p in self.papers if p.venue and p.venue == norm_venue]

    def get_papers_in_venue_by_year(self, venue_str: str) -> Tuple[Dict, List[Paper]]:
        matching_papers = self.get_papers_in_venue(venue_str)
        by_year = defaultdict(list)
        no_year = []
        for p in matching_papers:
            if not p.year:
                no_year.append(p)
            else:
                by_year[p.year].append(p)
        return by_year, no_year

    def get_papers_in_fos(self, fos: str) -> List[Paper]:
        return [p for p in self.papers if p.has_fos(fos)]
