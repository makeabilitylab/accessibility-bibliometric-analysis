import os, sys
import json
import tqdm
from collections import defaultdict

from biblio.utils.list_utils import flatten
from biblio.load_dataset import load_dataset
from biblio.load_fos import MagLookup
from biblio.utils.lcdi_utils import compute_lcdi_for_paper_refs_l1, compute_lcdi_for_paper_cits_l1
from biblio.constants import VENUES_TO_PLOT


if __name__ == '__main__':
    # load dataset
    core, extended, lookup = load_dataset('data/analysis/a11y_bibliometrics_dataset.jsonl.gz')

    # mag lookup
    print('loading mag...')
    mag_lookup = MagLookup('data/analysis/a11y_bibliometrics_mag_fos.jsonl.gz')

    # COMPARATIVE analysis (compute individually then average)
    print('Computing individual LCDI (refs)...')
    all_fos = []
    for voi in VENUES_TO_PLOT:
        papers = lookup.get_papers_in_venue(voi)
        voi_refs = flatten([p.refs for p in papers])
        voi_cits = flatten([p.cits for p in papers])
        voi_ref_papers = [lookup.get_paper_by_triple(tuple(ref)) for ref in voi_refs]
        voi_cit_papers = [lookup.get_paper_by_triple(tuple(cit)) for cit in voi_cits]
        all_fos += flatten(
            [p.fos for p in papers if p and p.fos] + \
            [p.fos for p in voi_ref_papers if p and p.fos] + \
            [p.fos for p in voi_cit_papers if p and p.fos]
        )
    all_l1_fos = set([entry[0] for entry in all_fos if entry[-1] == 1])

    lcdi_results = defaultdict(dict)

    for p in tqdm.tqdm(core['a11y']):
        lcdi = compute_lcdi_for_paper_refs_l1(p, lookup, all_l1_fos, mag_lookup)
        if lcdi:
            lcdi_results['a11y'][p.pid] = lcdi

    for p in tqdm.tqdm(core['a11y_assets']):
        lcdi = compute_lcdi_for_paper_refs_l1(p, lookup, all_l1_fos, mag_lookup)
        if lcdi:
            lcdi_results['a11y_assets'][p.pid] = lcdi

    for p in tqdm.tqdm(core['a11y_chi']):
        lcdi = compute_lcdi_for_paper_refs_l1(p, lookup, all_l1_fos, mag_lookup)
        if lcdi:
            lcdi_results['a11y_chi'][p.pid] = lcdi

    for voi in VENUES_TO_PLOT:
        print(voi)
        papers = lookup.get_papers_in_venue(voi)
        for p in tqdm.tqdm(papers):
            lcdi = compute_lcdi_for_paper_refs_l1(p, lookup, all_l1_fos, mag_lookup)
            if lcdi:
                lcdi_results[voi][p.pid] = lcdi

    with open('data/analysis/lcdi_refs_by_papers_l1.json', 'w') as outf:
        json.dump(lcdi_results, outf)

    # CITATIONS!!! COMPARATIVE analysis (compute individually then average)
    print('Computing individual LCDI (cits)...')
    all_fos = []
    for voi in VENUES_TO_PLOT:
        papers = lookup.get_papers_in_venue(voi)
        voi_refs = flatten([p.refs for p in papers])
        voi_cits = flatten([p.cits for p in papers])
        voi_ref_papers = [lookup.get_paper_by_triple(tuple(ref)) for ref in voi_refs]
        voi_cit_papers = [lookup.get_paper_by_triple(tuple(cit)) for cit in voi_cits]
        all_fos += flatten(
            [p.fos for p in papers if p and p.fos] + \
            [p.fos for p in voi_ref_papers if p and p.fos] + \
            [p.fos for p in voi_cit_papers if p and p.fos]
        )
    all_l1_fos = set([entry[0] for entry in all_fos if entry[-1] == 1])

    lcdi_results = defaultdict(dict)

    for p in tqdm.tqdm(core['a11y']):
        lcdi = compute_lcdi_for_paper_cits_l1(p, lookup, all_l1_fos, mag_lookup)
        if lcdi:
            lcdi_results['a11y'][p.pid] = lcdi

    for p in tqdm.tqdm(core['a11y_assets']):
        lcdi = compute_lcdi_for_paper_cits_l1(p, lookup, all_l1_fos, mag_lookup)
        if lcdi:
            lcdi_results['a11y_assets'][p.pid] = lcdi

    for p in tqdm.tqdm(core['a11y_chi']):
        lcdi = compute_lcdi_for_paper_cits_l1(p, lookup, all_l1_fos, mag_lookup)
        if lcdi:
            lcdi_results['a11y_chi'][p.pid] = lcdi

    for voi in VENUES_TO_PLOT:
        print(voi)
        papers = lookup.get_papers_in_venue(voi)
        for p in tqdm.tqdm(papers):
            if not p:
                continue
            lcdi = compute_lcdi_for_paper_cits_l1(p, lookup, all_l1_fos, mag_lookup)
            if lcdi:
                lcdi_results[voi][p.pid] = lcdi

    with open('data/analysis/lcdi_cits_by_papers_l1.json', 'w') as outf:
        json.dump(lcdi_results, outf)

    print('done.')


