#  Copyright (C) 2023-2024 Y Hsu <yh202109@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public license as published by
#  the Free software Foundation, either version 3 of the License, or
#  any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details
#
#  You should have received a copy of the GNU General Public license
#  along with this program. If not, see <https://www.gnu.org/license/>

import requests
import os
import pandas as pd
import json

class accessLib:
    """
    A class for accessing the CDISC library using an input file and API key.

    Attributes:
        input_file (str): The path to the input file containing the API key.

    Raises:
        FileNotFoundError: If the input file is not found.
        ValueError: If the API key is empty.
    """


    def __init__(self, input_file):
        self.input_file = input_file
        if not os.path.isfile(self.input_file):
            raise FileNotFoundError(f"Input file '{self.input_file}' not found.")
        with open(self.input_file, 'r') as file:
            self.api_key = file.read().strip()
        if not self.api_key:
            raise ValueError("API key is empty.")

        self.baseURL = "https://library.cdisc.org/api"
        self.ct_list = pd.DataFrame()
        self.ct_list_titles = []

    def get_ct_list(self, newest=True):
        """
        Retrieves a DataFrame containing information about CDISC library packages.

        This method sends a GET request to the CDISC library API to retrieve information about CDISC library packages.
        It returns a DataFrame containing package information, including the title, package series, effective date, path, and type of each package.

        Returns:
            dict: A dictionary containing the DataFrame with package information and a set of unique package titles.
                - 'ct': pandas.DataFrame: The DataFrame containing package information.
                - 'title': set: A set of unique package titles.
        """
        ep = "/mdr/products"
        pp = "/Terminology"
        req = requests.get(
            self.baseURL + ep + pp, 
            headers={'api-key': self.api_key, 'Accept': 'application/json'}
        )
        req.close()
        if req.status_code == 200:
            data = req.json()
            packages = data['_links']['packages']
            df = pd.DataFrame()
            for package in packages:
                title = package['title']
                t1, t2 = title.split(" Controlled Terminology Package ")
                t2, t3 = t2.split(" Effective ")
                df = df._append({'Title': t1, 'PkgSeries': t2, 'Effective': t3, 'Path': package['href'], 'Type': package['type']}, ignore_index=True)
            df['TitleL'] = df['Title'].str.lower()
            df['Newest'] = df['Effective'] == df.groupby('TitleL')['Effective'].transform('max')
        else:
            raise ValueError("Invalid status code: " + str(req.status_code) + " - " + req.reason)

        if newest:
            df = df[df['Newest']]
        self.ct_list = df
        self.ct_list_titles = set(df['Title'])
        return 

    def get_ct_package(self, title = "", pkg_series = "", out_folder = ""):
        """
        Downloads a CDISC library package based on the specified title and series.

        This method takes a title and series as input and downloads the corresponding CDISC library package.
        The package is downloaded from the URL specified in self.baseURL + self.ct_list['ct']['Path'].

        Args:
            title (str): The title of the package to download.
            series (str): The series of the package to download.

        Returns:
            bool: True if the package is successfully downloaded, False otherwise.
        """
        if self.ct_list.empty:
            self.get_ct_list()
        if title not in self.ct_list_titles:
            raise ValueError("Invalid title. Title not found in the CDISC library.")
        pkg_series = str(pkg_series)
        if not (isinstance(pkg_series, str) and len(pkg_series) <= 2):
            raise ValueError("Invalid series. Pkg_series must be a length 2 string or an integer.")

        df = self.ct_list[(self.ct_list['TitleL'] == title.lower())]

        if pkg_series == "":
            df = df[df['Newest']]
        else:
            if pkg_series not in df['PkgSeries'].values:
                raise ValueError("Invalid series. Series not found in the CDISC library.")
            df = df[(df['PkgSeries'] == pkg_series)]
        if len(df) != 1:
            raise ValueError("Invalid package. Multiple packages found with the same title and series.")

        package_url = self.baseURL + df['Path'].values[0]
        req = requests.get(package_url, headers={'api-key': self.api_key})
        req.close()
        if req.status_code == 200:
            c = req.json()
            package_info = {
                'description': c['description'],
                'effectiveDate': c['effectiveDate'],
                'label': c['label'],
                'name': c['name'],
                'source': c['source'],
                'registrationStatus': c['registrationStatus'],
                'version': c['version']
            }
        
            out = {'codelists': c['codelists'], 'package_info': package_info}
            if out_folder != "" and os.path.isdir(out_folder):
                package_name = package_url.split('/')[-1]
                out_path = os.path.join(out_folder, package_name)
                with open(out_path, 'w') as file:
                    json.dump(out, file)
        
            return out
        else:
            raise ValueError("Invalid status code: " + str(req.status_code) + " - " + req.reason)

if __name__ == "__main__":
    pass

    #cl = accessLib("/Users/yh2020/cdisc.txt")
    #cl.get_ct_list()
    #c = cl.get_ct_package('Protocol')