import pandas as pd
import math, os
import numpy as np
from io import StringIO
from pprint import pprint


class ParticleData():
    def __init__(self, directory, suffix,oversize_bin_cutoff=16.6):
        self.directory = directory
        self.suffix = suffix
        self.oversize_bin_cutoff = oversize_bin_cutoff
        self.file_path = self._find_file()
        self._header = self._get_header()
        self._data = self._get_data()
        self._bin_cutoffs = self._get_bin_cutoffs()
        self._num_bins = len(self._bin_cutoffs)-1
        self._mean_diameters = self._get_mean_diameters()
        self._time_points = self._data['Elapsed Time [s]']
        self._bin_volumes = (4/3) * math.pi * ((self._mean_diameters / 2) ** 3) # volume per particle for each bin in femto liters
        self._counts = self._get_counts() # 2D array of counts over time
        self._volumes = self._counts * self._bin_volumes # 2D array of volumes over time
        self._sum_counts = np.sum(self._counts, axis = 0)
        self._mean_counts = np.mean(self._counts, axis=0)
        self._sum_volumes = np.sum(self._volumes, axis = 0)
        self._mean_volumes = np.mean(self._volumes, axis=0)
        self._total_count = self._get_total_count()
        self._total_volume = self._get_total_volume()
        self._dlogD = self._calculate_dlogD()


    def _find_file(self):
        """
        Searches for the CSV file in the specified directory that ends with the given suffix or matches the full file name.
        Strips off '.csv' from the end of the suffix if it is present.

        Returns:
            str: The path to the found file.

        Raises:
            FileNotFoundError: If no file matching the suffix is found.
        """
        suffix = str(self.suffix)
        if suffix.endswith('.csv'):
            suffix = suffix[:-4]

        for file in os.listdir(self.directory):
            if file.endswith(suffix + '.csv') or file == self.suffix:
                return os.path.join(self.directory, file)
        raise FileNotFoundError(f"No file ending with {suffix}.csv found in directory {self.directory}")



    def _get_header(self) -> dict:
        """
        Parses the header section of a CSV file into a dictionary.

        Args:
            file_path (str): The path to the CSV file.

        Returns:
            dict: A dictionary containing the header key-value pairs.
        """
        header_dict = {}
        with open(self.file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith(','):
                    break
                if ',' in line:
                    key, value = line.split(',', 1)  # Split only at the first comma
                    header_dict[key.strip()] = value.strip()
        return header_dict


    def _get_data(self) -> pd.DataFrame:
        """
        Parses the data section of a CSV file into a pandas DataFrame, starting after the line that begins with a comma.
        The first line after the comma is used as the header.

        Args:
            file_path (str): The path to the CSV file.

        Returns:
            pd.DataFrame: A DataFrame containing the parsed data.
        """
        data_started = False
        data_lines = []

        with open(self.file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if data_started:
                    data_lines.append(line)
                elif line.startswith(','):
                    data_started = True

        # Combine the collected data lines into a single string for pd.read_csv
        data_str = '\n'.join(data_lines)
        # Use pd.read_csv with StringIO to read the CSV data from the string, treating the first line as the header
        data_df = pd.read_csv(StringIO(data_str))

        return data_df
    
    def _get_bin_cutoffs(self):
        """
        Extracts the bin cutoffs from the header and appends the oversize bin cutoff.

        Returns:
            np.ndarray: An array of bin cutoffs as floats.

        Raises:
            ValueError: If no bin cutoffs are found in the header.
        """
        cutoffs = []
        for key, value in self.header.items():
            if key.startswith('Bin'):
                cutoffs.append(value)
        
        if not cutoffs:
            raise ValueError("No bin cutoffs found in the header.")
        
        cutoffs.append(self.oversize_bin_cutoff)
        return np.array([float(item) for item in cutoffs])

    def _get_mean_diameters(self):
        """
        Calculates the mean diameters for each bin based on the bin cutoffs.
        The unit of the mean diameters is in microns.

        Returns:
            np.ndarray: An array of mean diameters as floats.

        Raises:
            ValueError: If the bin cutoffs array has less than 2 elements.
        """
        if len(self._bin_cutoffs) < 2:
            raise ValueError("Bin cutoffs array must have at least 2 elements to calculate mean diameters.")
        
        mean_diameters = []
        for i in range(1, len(self._bin_cutoffs)):
            mean_diameters.append((self._bin_cutoffs[i] + self._bin_cutoffs[i - 1]) / 2)

        return np.array(mean_diameters)


    def _get_counts(self):
        """
        Extracts the counts for each bin from the data.
        
        Returns:
            np.ndarray: A 2D array of counts over time.

        Raises:
            ValueError: If the number of bins is not consistent with the data columns.
        """
        counts = []
        for index, row in self._data.iterrows():
            if self._num_bins + 1 > len(row):
                raise ValueError("Number of bins exceeds the available data columns.")
            counts.append(row[1:self._num_bins+1].values)  # Ensure to extract values as a list
        
        return np.array(counts)


    def _get_total_volume(self):
        """
        Calculates the total volume over all time points and bins.
        The unit of the volume is in femto liters.

        Returns:
            float: The total volume in femto liters.

        Raises:
            ValueError: If the volumes array is empty.
        """
        if len(self._volumes) == 0:
            raise ValueError("Volumes array is empty.")
        
        total_volume = np.sum(self._volumes)
        return total_volume



    def _get_total_count(self):
        """
        Calculates the total particle count over all time points and bins.

        Returns:
            float: The total particle count.

        Raises:
            ValueError: If the counts array is empty.
        """
        if len(self._counts) == 0:
            raise ValueError("Counts array is empty.")
        
        total_count = np.sum(self._counts)
        return total_count

    def get_count_over_time(self, bin_num=None):
        """
        Calculates the particle count over time for a specific bin or for all bins combined.

        Args:
            bin_num (int, optional): The bin number to calculate the count for. If None, the counts for all bins are summed.

        Returns:
            np.ndarray: An array of particle counts over time.

        Raises:
            ValueError: If bin_num is out of range.
        """
        if bin_num is not None and (bin_num < 0 or bin_num >= self._num_bins):
            raise ValueError(f"bin_num must be between 0 and {self._num_bins - 1}")

        result = []
        if bin_num is None:
            for i in range(len(self._counts)):
                current = np.sum(self._counts[i])
                result.append(current)
        else:
            for i in range(len(self._counts)):
                result.append(self._counts[i][bin_num])

        return np.array(result)



    def get_volume_over_time(self, bin_num=None):
        """
        Calculates the volume over time for a specific bin or for all bins combined.
        The unit of the volume is in femto liters.

        Args:
            bin_num (int, optional): The bin number to calculate the volume for. If None, the volumes for all bins are summed.

        Returns:
            np.ndarray: An array of volumes over time.

        Raises:
            ValueError: If bin_num is out of range.
        """
        if bin_num is not None and (bin_num < 0 or bin_num >= self._num_bins):
            raise ValueError(f"bin_num must be between 0 and {self._num_bins - 1}")

        result = []
        if bin_num is None:
            for i in range(len(self._volumes)):
                current = np.sum(self._volumes[i])
                result.append(current)
        else:
            for i in range(len(self._volumes)):
                result.append(self._volumes[i][bin_num])

        return np.array(result)

    def _calculate_dlogD(self):
        """
        Calculates the logarithmic difference (dlogD) between consecutive bin cutoffs.
        The unit of the bin cutoffs is assumed to be in microns.

        Returns:
            np.ndarray: An array of dlogD values.

        Raises:
            ValueError: If the bin cutoffs array has less than 2 elements.
        """
        if len(self._bin_cutoffs) < 2:
            raise ValueError("Bin cutoffs array must have at least 2 elements to calculate dlogD.")

        dlogD = []
        for i in range(1, len(self._bin_cutoffs)):
            dlogD.append(np.log10(self._bin_cutoffs[i]) - np.log10(self._bin_cutoffs[i - 1]))
        
        return np.array(dlogD)

    def calculate_bar_plot_widths(self, log_base=10, bar_width=0.25):
        """
        Calculate the widths of bars for a bar plot on a logarithmic scale.

        Args:
            log_base (float, optional): The base of the logarithm to use for the x-axis. Defaults to 10.
            bar_width (float, optional): The fixed width of each bar in logarithmic scale. Defaults to 0.25.

        Returns:
            list: A list of bar widths in linear scale that ensures equal visual width on the logarithmic scale.
        """
        widths = [bar_width * (log_base ** (np.log(val) / np.log(log_base) + bar_width / 2) - log_base ** (np.log(val) / np.log(log_base) - bar_width / 2)) for val in self._mean_diameters]
        return np.array(widths)


    @property
    def header(self):
        return self._header
    
    @property
    def data(self):
        return self._data

    @property
    def bin_cutoffs(self):
        return self._bin_cutoffs
    
    @property
    def mean_diameters(self):
        return self._mean_diameters

    @property
    def dlogD(self):
        return self._dlogD

    @property
    def bin_volumes(self):
        return self._bin_volumes
    @property
    def time_points(self):
        return np.array(self._time_points)
    
    @property
    def counts(self):
        return self._counts
    
    @property
    def volumes(self):
        return self._volumes

    @property
    def mean_counts(self):
        return self._mean_counts

    @property
    def sum_counts(self):
        return self._sum_counts

    @property
    def mean_volumes(self):
        return self._mean_volumes

    @property
    def sum_volumes(self):
        return self._sum_volumes
    
    @property
    def total_volume(self):
        return self._total_volume

    @property
    def total_count(self):
        return self._total_count
