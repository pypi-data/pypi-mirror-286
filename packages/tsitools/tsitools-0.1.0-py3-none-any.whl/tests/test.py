import unittest, os
import os
import numpy as np
import pandas as pd
from tsitools import ParticleData

class TestParticleData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Path to the directory containing the real data
        cls.directory = os.path.join(os.path.dirname(__file__), '../data')
        cls.suffix = '123'
        cls.particle_data = ParticleData(directory=cls.directory, suffix=cls.suffix)

    def test_find_file(self):
        # Test the _find_file method
        self.assertIsNotNone(self.particle_data.file_path)

    def test_get_header(self):
        # Test the _get_header method
        header = self.particle_data._get_header()
        self.assertIsInstance(header, dict)

    def test_get_data(self):
        # Test the _get_data method
        data = self.particle_data._get_data()
        self.assertIsInstance(data, pd.DataFrame)

    def test_get_bin_cutoffs(self):
        # Test the _get_bin_cutoffs method
        bin_cutoffs = self.particle_data._get_bin_cutoffs()
        self.assertIsInstance(bin_cutoffs, np.ndarray)

    def test_get_mean_diameters(self):
        # Test the _get_mean_diameters method
        mean_diameters = self.particle_data._get_mean_diameters()
        self.assertIsInstance(mean_diameters, np.ndarray)

    def test_get_counts(self):
        # Test the _get_counts method
        counts = self.particle_data._get_counts()
        self.assertIsInstance(counts, np.ndarray)

    def test_get_total_volume(self):
        # Test the _get_total_volume method
        total_volume = self.particle_data._get_total_volume()
        self.assertIsInstance(total_volume, float)

    def test_get_total_count(self):
        # Test the _get_total_count method
        total_count = self.particle_data._get_total_count()
        self.assertIsInstance(total_count, float)

    def test_get_count_over_time(self):
        # Test the get_count_over_time method
        count_over_time = self.particle_data.get_count_over_time()
        self.assertIsInstance(count_over_time, np.ndarray)

    def test_get_volume_over_time(self):
        # Test the get_volume_over_time method
        volume_over_time = self.particle_data.get_volume_over_time()
        self.assertIsInstance(volume_over_time, np.ndarray)

if __name__ == '__main__':
    unittest.main()
