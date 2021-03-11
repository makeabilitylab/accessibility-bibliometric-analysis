import os, sys
import json
import gzip


MAG_FILE = 'data/analysis/a11y_biblioemtrics_mag_fos.jsonl.gz'


# create MAG FoS similarity lookup
class MagLookup:
    def __init__(self, mag_file=MAG_FILE):
        l0_lookup = dict()
        l1_lookup = dict()
        name_lookup = dict()
        with gzip.open(mag_file, 'rb') as f:
            for line in f:
                entry = json.loads(line)
                if entry['level'] <= 2:
                    l0_lookup[entry['mag_id']] = entry['l0_parent']
                    l1_lookup[entry['mag_id']] = entry['l1_parent']
                if entry['level'] <= 2:
                    name_lookup[entry['mag_id']] = entry['normalizedname']
        self.l0_dict = l0_lookup
        self.l1_dict = l1_lookup
        self.name_dict = name_lookup

    def get_name(self, m: int) -> str:
        """
        Get FoS name from id
        :param m:
        :return:
        """
        return self.name_dict.get(m, None)

    def get_l0(self, m: int) -> int:
        """
        Get l0 FoS of this fos
        :param m:
        :return:
        """
        return self.l0_dict.get(m, None)

    def get_l1(self, m: int) -> int:
        """
        Get l1 FoS of this fos
        :param m:
        :return:
        """
        return self.l1_dict.get(m, None)

    def sim(self, m1: int, m2: int) -> float:
        """
        Given two MAG FoS ids, compute similarity
        :param m1:
        :param m2:
        :return:
        """
        # same, similarity = 1
        if m1 == m2:
            return 1.

        # check l1 fos
        m1_l1 = self.l1_dict.get(m1, [])
        m2_l1 = self.l1_dict.get(m2, [])
        if m1_l1 and m2_l1 and set(m1_l1) & set(m2_l1):
            return 0.5

        # check l0 fos
        m1_l0 = self.l0_dict.get(m1, [])
        m2_l0 = self.l0_dict.get(m2, [])
        if m1_l0 and m2_l0 and set(m1_l0) & set(m2_l0):
            return 0.25

        # no parents in common, return 1/(2^3)
        return 0.125