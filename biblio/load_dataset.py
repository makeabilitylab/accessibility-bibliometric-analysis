import os
import json
import gzip
from collections import defaultdict
from typing import Tuple, Dict

from biblio.utils.list_utils import flatten
from biblio.papers import Paper, PaperLookup


DATASET_PATH = 'data/analysis/a11y_bibliometrics_dataset.jsonl.gz'


def load_dataset(data_path=DATASET_PATH) -> Tuple[Dict, Dict, PaperLookup]:
    """
    Load a11y bibliometric dataset
    :param data_path:
    :return:
    """
    print('loading data...')
    with gzip.open(data_path, 'rb') as f:
        dataset = json.load(f)

    print('generating paper list...')
    core = defaultdict(list)
    for venue, plist in dataset['core'].items():
        for pdict in plist:
            try:
                paper = Paper(**pdict)
                core[venue].append(paper)
            except TypeError:
                print('Error: ', pdict)
                continue
    extended = defaultdict(list)
    for venue, plist in dataset['extended'].items():
        for pdict in plist:
            try:
                paper = Paper(**pdict)
                extended[venue].append(paper)
            except TypeError:
                print('Error: ', pdict)
                continue

    print('generate special a11y subsets...')
    a11y_assets = []
    a11y_chi = []
    for paper in core['a11y']:
        if paper.venue == 'conf/assets':
            a11y_assets.append(paper)
        elif paper.venue == 'conf/chi':
            a11y_chi.append(paper)
        else:
            print('Unknown venue! ', paper.venue)
    core['a11y_assets'] = a11y_assets
    core['a11y_chi'] = a11y_chi

    all_paper_list = flatten(core.values()) + flatten(extended.values())
    all_paper_list = list(set(all_paper_list))

    print('forming lookup tables...')
    lookup = PaperLookup(
        paper_list=all_paper_list
    )
    return core, extended, lookup


if __name__ == '__main__':
    core_ds, extended_ds, lookup_dict = load_dataset()
    assets_papers = lookup_dict.get_papers_in_venue('conf/assets')
    print(f'{len(assets_papers)} ASSETS papers')
    assets_papers_by_year, no_year_info = lookup_dict.get_papers_in_venue_by_year('conf/assets')
    for year, papers_that_year in assets_papers_by_year.items():
        print(f'{year}\t{len(papers_that_year)}')
    print('No year info: ', len(no_year_info))
