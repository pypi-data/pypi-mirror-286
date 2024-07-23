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

from pypdf import PdfReader
import mtbp3
import os
import pandas as pd
from mtbp3.util.cdt import ListTree

class pdfSummary:
    """
    A class to summarize information about a PDF file.

    Attributes:
        pdf_path (str): The path to the PDF file.
        demo (bool): A flag indicating whether the PDF file is a demo file.
        pp (PdfReader): A PdfReader object representing the PDF file.
        summary (dict): A dictionary containing summary information about the PDF file.
        summary_label (dict): A dictionary mapping summary keys to their corresponding labels.
        outline_list (list): A list containing the outline structure of the PDF file.

    Methods:
        get_summary_string(): Returns a string representation of the summary information.
        get_summary_df(): Returns a pandas DataFrame of the summary information.
        get_outline_list(max_itr): Returns the outline structure of the PDF file.
        show_outline_tree(max_itr, to_right): Returns a formatted string representation of the outline structure.
    """

    def __init__(self, path=None):
        """
        Initializes a pdfSummary object.

        Args:
            path (str, optional): The path to the PDF file. If not provided, a demo file will be used.
        """
        if not isinstance(path, str) or len(path) == 0:
            self.pdf_path = mtbp3.get_data('attention.pdf')
            self.demo = True
        else:
            self.pdf_path = path
            self.demo = False

        try:
            file = open(self.pdf_path, 'rb')
            self.pp = PdfReader(file)
        except FileNotFoundError:
            raise ValueError("File not found")

        tmp0 = self.pp.get_num_pages()
        tmp1 = [len(self.pp.pages[i].images) for i in range(tmp0)]
        self.summary = {
            'file_name': os.path.basename(self.pdf_path),
            'file_size': os.path.getsize(self.pdf_path),
            'file_creationdate': self.pp.metadata.creation_date,
            'file_moddate': self.pp.metadata.modification_date,
            'pdf_version': self.pp.pdf_header.split('-')[1],
            'n_page': tmp0,
            'n_image_in_page': tmp1,
            'n_image_in_file': sum(tmp1)
        }
        self.summary_label = {
            'file_name': "File name",
            'file_size': "File size (byte): ",
            'file_creationdate': "File creation date",
            'file_moddate': "File modification date",
            'pdf_version': "PDF version",
            'n_page': "Number of pages: ",
            'n_image_in_page': "Number of images in individual pages: ",
            'n_image_in_file': "Total number of images: ",
        }
        self.outline_list = []

    def get_summary_string(self):
        """
        Returns a string representation of the summary information.

        Returns:
            str: A string representation of the summary information.
        """
        return "\n".join([self.summary_label[key] + ": " + str(self.summary[key]) for key in self.summary.keys()])

    def get_summary_df(self):
        """
        Returns a pandas DataFrame of the summary information.

        Returns:
            pandas.DataFrame: A DataFrame of the summary information.
        """
        keys = sorted(list(self.summary.keys()))
        data = {
            'Summary Label': [self.summary_label[key] for key in keys],
            'Summary Value': [self.summary[key] for key in keys]
        }
        df = pd.DataFrame(data)
        return df

    def get_outline_list(self, max_itr=5):
        """
        Returns the outline structure of the PDF file.

        Args:
            max_itr (int, optional): The maximum number of iterations to traverse the outline structure. Defaults to 5.

        Returns:
            list: A list containing the outline structure and any unprocessed elements.

        Raises:
            ValueError: If max_itr is not an integer between 1 and 20.

        Note:
            The outline structure is obtained from the `outline` attribute of the `pp` object.
            The returned list contains the outline structure in a hierarchical format, along with any unprocessed elements.
        """
        if not isinstance(max_itr, int) or max_itr < 1 or max_itr > 20:
            raise ValueError("max_itr must be an integer between 1 and 20")
        if not self.pp:
            return
        if not self.pp.outline:
            return

        in_source = self.pp.outline
        in_source_label = [self.summary['file_name']] * len(in_source)
        out_list = [self.summary['file_name']]
        not_processed = []
        digits1 = len(str(max_itr))

        for i in range(1, max_itr+1):
            len_remain = len(in_source)
            if len_remain == 0:
                break
            digits2 = len(str(len_remain))
            remaining_in_source = []
            remaining_in_source_label = []

            for index, element in enumerate(in_source):
                if isinstance(element, dict):
                    tmp = "pseudo"+str(i).zfill(digits1) + "-" + str(index).zfill(digits2)
                    out_list = out_list + [in_source_label[index] + "." + tmp + " " + element['/Title']]
                elif isinstance(element, list):
                    tmp = "pseudo"+str(i).zfill(digits1) + "-" + str(index-1).zfill(digits2)
                    if i < max_itr:
                        remaining_in_source.extend(element)
                        remaining_in_source_label.extend([in_source_label[index]+"."+tmp] * len(element))
                    else:
                        tmp1 = sum(isinstance(elem, dict) for elem in element)
                        out_list = out_list + [in_source_label[index] + "." + tmp + ".sub " + str(tmp1) + " sub-sections"]
                else:
                    not_processed.append(element)

            in_source = remaining_in_source
            in_source_label = remaining_in_source_label

        return [out_list, not_processed]

    def show_outline_tree(self, max_itr=5, to_right=False):
        """
        Returns a formatted string representation of the outline structure.

        Args:
            max_itr (int, optional): The maximum number of iterations to traverse the outline structure. Defaults to 5.
            to_right (bool, optional): A flag indicating whether the tree should be displayed to the right. Defaults to False.

        Returns:
            str: A formatted string representation of the outline structure.
        """
        if not (isinstance(max_itr, int) and 1 < max_itr <= 20):
            max_itr = 1

        if len(self.outline_list) == 0:
            self.outline_list = self.get_outline_list(max_itr=max_itr)

        if not self.outline_list:
            return "no outline available"

        if len(self.outline_list) != 2:
            raise ValueError("self.outline_list should be a length 2 list")

        tree = ListTree(lst=self.outline_list[0], infmt='dotspace')
        return '\n'.join(tree.list_tree(to_right=to_right))

if __name__ == "__main__":
    pfr = pdfSummary("/Users/yh2020/dt2/proj/mtbp3/mtbp3/data/attention.pdf")
    print(pfr.get_outline_list(max_itr=1))

