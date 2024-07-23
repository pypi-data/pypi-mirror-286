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

class CorrCalculator:
    """
    A class for calculating correlation and plotting scatter plots.

    Parameters:
    - y: A pandas DataFrame or a list
        - If y is a pandas DataFrame, it must be a 2-dimensional DataFrame with at least 2 columns and 2 rows.
        - If y is a list, it must be a list with at least 2 elements, where each element is a list of strings or numbers.
    - remove_na: bool, optional (default=True)
        - If True, remove rows with missing values (NA) from the input data.
        - If False, raise a ValueError if the input data contains missing values (NA).

    Methods:
    - calculate_kendall_tau():
        - Calculates the Kendall's tau correlation coefficient between the first two columns of the input data.
        - Returns the Kendall's tau coefficient as a float.

    - plot_y_list(loc=[0,1], axis_label=['x','y']):
        - Plots a scatter plot of the input data.
        - loc: list, optional (default=[0,1])
            - The indices of the columns to be plotted on the x and y axes.
        - axis_label: list, optional (default=['x','y'])
            - The labels for the x and y axes of the scatter plot.
    """

    def __init__(self, y, remove_na=True):

        assert isinstance(y, (pd.DataFrame, list)), "y must be either a pandas DataFrame or a list"
        if isinstance(y, pd.DataFrame):
            assert y.ndim == 2, "y must be a 2-dimensional DataFrame"
            assert y.shape[0] >= 2 and y.shape[1] >= 2, "y must be a pd.DataFrame with at least 2 columns and 2 rows"
            if remove_na == True:
                self.y_df = y.dropna()
            else:
                if y.isna().any().any():
                    raise ValueError("Input data contains missing values (NA)")
            self.y_shape0, self.y_shape1 = self.y_df.shape
            self.y_list = self.y_df.values.tolist()
        else:
            assert isinstance(y, list) and len(y) >= 2, "y must be a list with at least 2 elements"
            assert all(isinstance(x, list) for x in y), "all elements of y must be lists"
            assert all(isinstance(x, (str, int)) for sublist in y for x in sublist if x is not None), "all elements of y must be strings or numbers"
            assert all(len(x) == len(y[0]) for x in y), "all sublists in y must have the same length"
            self.y_shape0 = len(y[0])
            self.y_shape1 = len(y)
            self.y_list = y
            self.y_df = pd.DataFrame(self.y_list).T.dropna()

        return
            
    @staticmethod
    def __g(x):
        result = [np.sign(sublist[0] - sublist[1]) for sublist in x]
        return result

    def calculate_kendall_tau(self):
        """
        Calculates the Kendall's tau correlation coefficient between the first two columns of the input data.

        Returns:
        - tau: float
            - The Kendall's tau correlation coefficient.
        """
        tau1 = np.sign(np.repeat(self.y_list[0], self.y_shape0)-np.tile(self.y_list[0], self.y_shape0))
        tau2 = np.sign(np.repeat(self.y_list[1], self.y_shape0)-np.tile(self.y_list[1], self.y_shape0))
        tau = np.sum(np.multiply(tau1,tau2))/np.sqrt(np.multiply(np.sum(np.abs(tau1)),np.sum(np.abs(tau2))))
        return tau


    def plot_y_list(self, loc=[0,1], axis_label=['x','y']):
        """
        Plots a scatter plot of the input data.

        Parameters:
        - loc: list, optional (default=[0,1])
            - The indices of the columns to be plotted on the x and y axes.
        - axis_label: list, optional (default=['x','y'])
            - The labels for the x and y axes of the scatter plot.
        """
        plt.scatter(self.y_list[loc[0]], self.y_list[loc[1]])
        plt.xlabel(axis_label[0])
        plt.ylabel(axis_label[1])
        plt.title('Scatter Plot')
        plt.show()

if __name__ == "__main__":

    pass
