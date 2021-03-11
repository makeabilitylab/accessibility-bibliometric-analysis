import os, sys
from typing import Dict, Set, Optional, List

from biblio.load_fos import MagLookup
from biblio.papers import Paper, PaperLookup


# prop : dict(key=mag_id, value=count_of_papers_with_mag_id)
# this_fos: set of mag_id corresponding to this paper
# mag_lookup: MagLookup class
def compute_lcdi(prop: Dict, this_fos: List, mag_lookup: MagLookup) -> float:
    """
    Compute Leinster–Cobbold diversity index for paper
    :param prop:
    :param this_fos:
    :param mag_lookup:
    :return:
    """
    # proportion for normalizing each summation in denominator
    j_norm_prop = 1. / len(this_fos)

    # total number of papers
    total_p = sum(prop.values())

    # compute denominator (sum(s_ij p_i p_j))
    denom = 0
    for j in this_fos:
        sum_val = 0
        for i, p_i in prop.items():
            sum_val += mag_lookup.sim(i, j) * (p_i / total_p) * (prop.get(j, 0) / total_p)
        denom += j_norm_prop * sum_val

    return 1. / denom


def compute_lcdi_for_paper_refs_l1(
        paper: Paper,
        lookup: PaperLookup,
        fos_of_interest:
        Set, mag_lookup: MagLookup
) -> Optional[float]:
    """
    Get LCDI for a paper
    :return:
    """
    # get this paper's fos
    if paper.l1_fos:
        this_fos_dict = list(set([fos[0] for fos in paper.l1_fos]))
    else:
        return None
    if not this_fos_dict:
        return None

    # initialize fos prop
    p_dict = {fos: 0 for fos in fos_of_interest}
    for mag_id in this_fos_dict:
        p_dict[mag_id] += 1. / len(this_fos_dict)

    ref_papers = [lookup.get_paper_by_triple(ref) for ref in paper.refs]
    for ref in ref_papers:
        if ref.l1_fos:
            ref_l1_fos = [fos[0] for fos in ref.l1_fos]
        else:
            continue
        for mag_id in ref_l1_fos:
            p_dict[mag_id] += 1. / len(ref_l1_fos)

    lcdi = compute_lcdi(p_dict, this_fos_dict, mag_lookup)
    return lcdi


def compute_lcdi_for_paper_cits_l1(
        paper: Paper,
        lookup: PaperLookup,
        fos_of_interest:
        Set, mag_lookup: MagLookup
) -> Optional[float]:
    """
    Get LCDI for papers citing this paper
    :return:
    """
    # get this paper's fos
    if paper.l1_fos:
        this_fos_dict = list(set([fos[0] for fos in paper.l1_fos]))
    else:
        return None
    if not this_fos_dict:
        return None

    # initialize fos prop
    p_dict = {fos: 0 for fos in fos_of_interest}
    for mag_id in this_fos_dict:
        p_dict[mag_id] += 1. / len(this_fos_dict)

    cit_papers = [lookup.get_paper_by_triple(ref) for ref in paper.cits]
    for cit in cit_papers:
        if not cit:
            continue
        if cit.l1_fos:
            cit_l1_fos = [fos[0] for fos in cit.l1_fos]
        else:
            continue
        for mag_id in cit_l1_fos:
            p_dict[mag_id] += 1. / len(cit_l1_fos)

    lcdi = compute_lcdi(p_dict, this_fos_dict, mag_lookup)
    return lcdi