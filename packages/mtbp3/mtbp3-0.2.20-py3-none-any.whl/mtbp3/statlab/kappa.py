#  Copyright (C) 2023-2024 Y Hsu <yh202109@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public license as published by
#  the Free software Foundation, either version 3 of the License, or
#  any later version.
#j
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details
#
#  You should have received a copy of the GNU General Public license
#  along with this program. If not, see <https://www.gnu.org/license/>

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.utils import resample
import os
import seaborn as sns
import random


class KappaCalculator:
    """
    A class for calculating Cohen's kappa and Fleiss' kappa.

    Parameters:
    - y: The input data. It can be either a pandas DataFrame or a list.
    - infmt: The format of the input data. Allowed values are 'sample_list', 'sample_df', 'count_sq_df', and 'count_df'.
    - stringna: The string representation of missing values.

    Methods:
    - bootstrap_cohen_ci(n_iterations, confidence_level, outfmt, out_digits): Calculates the bootstrap confidence interval for Cohen's kappa.

    """

    def __init__(self, y, infmt='sample_list', stringna="stringna"):
        """
        Initializes the KappaCalculator object.

        Parameters:
        - y: The input data. It can be either a pandas DataFrame or a list.
        - infmt: The format of the input data. Allowed values are 'sample_list', 'sample_df', 'count_sq_df', and 'count_df'.
        - stringna: The string representation of missing values.

        Raises:
        - ValueError: If the value of infmt is invalid.
        - AssertionError: If the input data does not meet the required conditions.

        """

        assert isinstance(y, (pd.DataFrame, list)), "y must be either a pandas DataFrame or a list"
        if isinstance(y, pd.DataFrame):
            assert y.ndim == 2, "y must be a 2-dimensional DataFrame"
            assert y.shape[0] >= 2 and y.shape[1] >= 2, "y must be a pd.DataFrame with at least 2 columns and 2 rows"
        else:
            assert isinstance(y, list) and len(y) >= 2, "y must be a list with at least 2 elements"
            assert all(isinstance(x, list) for x in y), "all elements of y must be lists"
            assert all(isinstance(x, (str, int)) for sublist in y for x in sublist if x is not None), "all elements of y must be strings or numbers"
            assert all(len(x) == len(y[0]) for x in y), "all sublists in y must have the same length"

        if infmt not in ['sample_list', 'sample_df', 'count_sq_df', 'count_df']:
            raise ValueError("Invalid value for infmt. Allowed values are 'sample_list', 'sample_df', 'count_sq_df' and 'count_df'.")

        if infmt == 'sample_list' or infmt == 'sample_df':
            if infmt == 'sample_list':
                self.y_list = self.__convert_2dlist_to_string(y, stringna=stringna)
                self.y_df = pd.DataFrame(self.y_list).T
            else:
                self.y_df = y.replace({np.nan: stringna, None: stringna})
                self.y_df = self.y_df.applymap(lambda x: str(x) if isinstance(x, (int, float)) else x)
                self.y_list = self.y_df.values.tolist()

            self.y_count = self.y_df.apply(pd.Series.value_counts, axis=1).fillna(0)
            if stringna in self.y_count.columns:
                column_values = self.y_count[stringna].unique()
                assert len(column_values) == 1, f"Total number in value '{stringna}' must be the same for all sample"
                self.y_count.drop(columns=stringna, inplace=True)
            tmp_row_sum = self.y_count.sum(axis=1) 
            assert tmp_row_sum.eq(tmp_row_sum[0]).all(), "Total number of raters per sample must be equal"
            self.category = self.y_count.columns
            self.n_category = len(self.category)
            self.n_rater = tmp_row_sum[0]

            if self.n_rater == 2:
                self.y_count_sq = pd.crosstab(self.y_list[0], self.y_list[1], margins = False, dropna=False)
                i = self.y_count_sq.index.union(self.y_count_sq.columns, sort=True)
                self.y_count_sq.reindex(index=i, columns=i, fill_value=0)
            else:
                self.y_count_sq = None

        elif infmt == 'count_sq_df':
            assert y.shape[0] == y.shape[1], "y must be a square DataFrame"
            self.y_count_sq = y
            self.category = y.columns
            self.n_category = len(self.category)
            self.n_rater = 2
            tmp_count = self.y_count_sq.unstack().reset_index(name='count')
            self.y_df = tmp_count.loc[np.repeat(tmp_count.index.values, tmp_count['count'])]
            self.y_df.drop(columns='count', inplace=True)
            self.y_list = self.y_df.values.tolist()
            self.y_count = self.y_df.apply(pd.Series.value_counts, axis=1).fillna(0)

        elif infmt == 'count_df':
            self.y_count = y
            if stringna in self.y_count.columns:
                column_values = self.y_count[stringna].unique()
                assert len(column_values) == 1, f"All values in column '{stringna}' must be the same"
                self.y_count.drop(columns=stringna, inplace=True)
            tmp_row_sum = self.y_count.sum(axis=1) 
            assert tmp_row_sum.eq(tmp_row_sum[0]).all(), "Row sums of y must be equal"
            self.category = self.y_count.columns
            self.n_category = len(self.category)
            self.n_rater = tmp_row_sum[0]
            self.y_count_sq= None
            self.y_list = None
            self.y_df = None

        else:
            self.y_list = None
            self.y_df = None
            self.y_count= None
            self.y_count_sq= None
            self.category = None
            self.n_rater = None
            self.n_category = None
            return


        if self.n_rater == 2:
            if self.y_list is not None:
                self.cohen_kappa = self.__calculate_cohen_kappa(self.y_list[0],self.y_list[1])
            else:
                self.cohen_kappa = None
        else:
            self.cohen_kappa = None
        
        if self.n_rater >= 2:
            if self.y_count is not None:
                self.fleiss_kappa = self.__calculate_fleiss_kappa(self.y_count)
            else:
                self.fleiss_kappa = None
        else:
            self.fleiss_kappa = None

        return
            
    @staticmethod
    def __convert_2dlist_to_string(y=[], stringna=""):
        """
        Converts a 2-dimensional list to a string representation.

        Parameters:
        - y: The input list.
        - stringna: The string representation of missing values.

        Returns:
        - The converted list.

        """
        for i in range(len(y)):
            if any(isinstance(x, (int)) for x in y[i]):
                y[i] = [str(x) if x is not None else stringna for x in y[i]]
        return y

    @staticmethod
    def __calculate_cohen_kappa(y1, y2):
        """
        Calculates Cohen's kappa.

        Parameters:
        - y1: The first rater's ratings.
        - y2: The second rater's ratings.

        Returns:
        - The calculated Cohen's kappa value.

        """
        total_pairs = len(y1)
        observed_agreement = sum(1 for i in range(total_pairs) if y1[i] == y2[i]) / total_pairs
        unique_labels = set(y1 + y2)
        expected_agreement = sum((y1.count(label) / total_pairs) * (y2.count(label) / total_pairs) for label in unique_labels)
        return (observed_agreement - expected_agreement) / (1 - expected_agreement)

    @staticmethod
    def __calculate_fleiss_kappa(y):
        """
        Calculates Fleiss' kappa.

        Parameters:
        - y: The count matrix.

        Returns:
        - The calculated Fleiss' kappa value.

        """
        nR = y.values.sum()
        p = y.values.sum(axis = 0)/nR
        Pbar_E = (p ** 2).sum()
        R = y.values.sum(axis = 1)[0]
        Pbar_O = (((y ** 2).sum(axis=1) - R) / (R * (R - 1))).mean()

        return (Pbar_O - Pbar_E) / (1 - Pbar_E)

    def bootstrap_cohen_ci(self, n_iterations=1000, confidence_level=0.95, outfmt='string', out_digits=6):
        """
        Calculates the bootstrap confidence interval for Cohen's kappa.

        Parameters:
        - n_iterations: The number of bootstrap iterations.
        - confidence_level: The desired confidence level.
        - outfmt: The output format. Allowed values are 'string' and 'list'.
        - out_digits: The number of digits to round the output values.

        Returns:
        - If outfmt is 'string', returns a string representation of the result.
        - If outfmt is 'list', returns a list containing the result values.

        """
        assert isinstance(n_iterations, int) and n_iterations > 1, "n_iterations must be an integer greater than 1"
        assert isinstance(confidence_level, (float)) and 0 < confidence_level < 1, "confidence_level must be a number between 0 and 1"

        if self.n_rater != 2:
            return []

        y1 = self.y_list[0]
        y2 = self.y_list[1]
        kappa_values = []
        idx = range(len(y1))
        for _ in range(n_iterations):
            idxr = resample(idx)
            y1r = [y1[i] for i in idxr]
            y2r = [y2[i] for i in idxr]

            kappa = self.__calculate_cohen_kappa(y1r, y2r)
            kappa_values.append(kappa)

        lower_percentile = (1 - confidence_level) / 2
        upper_percentile = 1 - lower_percentile
        lower_bound = np.percentile(kappa_values, lower_percentile * 100)
        upper_bound = np.percentile(kappa_values, upper_percentile * 100)
        if outfmt=='string':
            return "Cohen's kappa: {:.{}f}".format(self.cohen_kappa, out_digits) + "\nConfidence Interval ({}%): [{:.{}f}, {:.{}f}]".format(confidence_level * 100, lower_bound, out_digits, upper_bound, out_digits)
        else:
            return [self.cohen_kappa, n_iterations, confidence_level, lower_bound, upper_bound]

    def create_bubble_plot(self, out_path="", axis_label=[], max_size_ratio=0, hist=False, reverse_y=False):
        """
        Creates a bubble plot based on the y_count_sq matrix.

        Parameters:
        - out_path (str): The output path to save the plot. If not provided, the plot will be displayed.
        - title (str): The title of the plot. If not provided, the default title is 'Bubble Plot'.
        - axis_label (list): A list of two strings representing the labels for the x-axis and y-axis. 
                             If not provided, the default labels are ['Rater 1', 'Rater 2'].
        - max_size_ratio (int): The maximum size ratio for the bubbles. The size of the bubbles is determined by the values in the y_count_sq matrix. 
                                The maximum size of the bubbles will be max_size_ratio times the maximum value in the matrix. 
                                If not provided, the default value is 100.

        Returns:
        - None

        Raises:
        - None

        """
        if self.n_rater == 2 and self.y_count_sq is not None and self.y_count_sq.shape[0] == self.y_count_sq.shape[1] and self.y_count_sq.shape[0] > 0:
            categories = self.y_count_sq.columns
            n_categories = len(categories)

            r1 = [] 
            r2 = []
            sizes = []
            for i1, c1 in enumerate(categories):
                for i2, c2 in enumerate(categories):
                    r1.append(c1)
                    r2.append(c2)
                    sizes.append(self.y_count_sq.iloc[i1, i2])
            df0 = pd.DataFrame({'r1': r1, 'r2': r2, 'sizes': sizes})
            df0['r1'] = pd.Categorical(df0['r1'])
            df0['r2'] = pd.Categorical(df0['r2'])
            df0['agree'] = np.where(df0['r1'] == df0['r2'], 'agree', 'disagree')
            max_size_ratio = max_size_ratio if max_size_ratio >= 1 else max(1,int((6000/max(sizes)) / n_categories))
            if hist:
                sns.jointplot(
                    data=df0, x="r1", y="r2", kind="scatter", 
                    height=5, ratio=3, marginal_ticks=True, 
                    marginal_kws={"hue": df0['agree'], "multiple": "stack", "weights": sizes, "shrink":.5, "legend": False}, 
                    joint_kws={"hue": df0['agree'], "size": sizes, "legend": False, "sizes":(min(sizes)*max_size_ratio, max(sizes)*max_size_ratio)}
                    ) 
                if not reverse_y:
                    tmp1 = plt.ylim()
                    plt.ylim(tmp1[1], tmp1[0])
            else:
                sns.scatterplot(data=df0, x="r1", y="r2", size="sizes", hue="agree", sizes=(min(sizes)*max_size_ratio, max(sizes)*max_size_ratio), legend=False)
                tmp1 = plt.xlim()
                tmp1d = ((tmp1[1] - tmp1[0])/n_categories)
                plt.xlim(tmp1[0] - tmp1d, tmp1[1] + tmp1d)
                plt.ylim(tmp1[0] - tmp1d, tmp1[1] + tmp1d)
                if reverse_y:
                    tmp1 = plt.ylim()
                    plt.ylim(tmp1[1], tmp1[0])

            for i in range(len(df0)):
                plt.text(df0['r1'][i], df0['r2'][i], df0['sizes'][i], ha='center', va='center')

            if not axis_label:
                axis_label = ['Rater 1', 'Rater 2']
            plt.xlabel(axis_label[0])
            plt.ylabel(axis_label[1])

            plt.tight_layout()
            if out_path:
                try:
                    if os.path.isdir(out_path):
                        plt.savefig(os.path.join(out_path, "bubble_plot.svg"))
                    else:
                        plt.savefig(out_path)
                except Exception as e:
                    print("Error saving the figure:", str(e))
            else:
                plt.show()
        else:
            print("Cannot create bubble plot. y_count_sq is not a square non-empty matrix.")

if __name__ == "__main__":

    pass
