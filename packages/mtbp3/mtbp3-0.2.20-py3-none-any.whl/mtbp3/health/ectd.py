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

import pandas as pd
import os
from mtbp3.util.cdt import ListTree
import mtbp3
    
class ctoc_by_fda:
    def __init__(self, ectd_version="3.2.2", ctoc_version="2.3.3"):
        assert isinstance(ectd_version, str) and all(char.isdigit() or char == '.' for char in ectd_version), "Version must be a string with integers and dots"
        assert isinstance(ctoc_version, str) and all(char.isdigit() or char == '.' for char in ctoc_version), "Version must be a string with integers and dots"
        self.ectd_version = ectd_version
        self.ctoc_version = ctoc_version
        self.folder_name = mtbp3.get_data(f'supp_ectd/fda_ectd{ectd_version}_ctocv{ctoc_version}.txt')
        self.ctoc = self.__load_list()

    def __load_list(self):
        #file_path = f'./mtbp3/data/supp_ectd/fda_ectd{self.ectd_version}_ctocv{ctoc_version}.txt'
        file_path = self.folder_name
        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                lines = file.readlines()
            lines = [line.strip() for line in lines if line.strip()]
            return lines
        else:
            print(f"eCTD Version {self.ectd_version} with CTOC Version {self.ctoc_version} not found.")
            return []

    def show_ctoc_tree(self, module=None, to_right=False):
        if not (isinstance(module, int) and 1 <= module <= 5):
            module = 1

        filtered_ctoc = [item for item in self.ctoc if item.startswith(str(module))]
        tree = ListTree(lst=filtered_ctoc, infmt='dotspace')
        return tree.list_tree(to_right=to_right)
    
    @staticmethod
    def color_output(out="", words=[], color='red'):
        assert isinstance(out, str) or not out, "out must be a string"
        if isinstance(words, str) and words:
            words = [words]
        elif isinstance(words, list) and words:
            assert all(isinstance(word, str) and word for word in words), "Elements in the list must be strings"
        color_dic = {'red': 31, 'green': 32, 'yellow': 33, 'blue': 34, 'magenta': 35, 'cyan': 36}
        if color not in color_dic.keys():
            return out
        else:
            color_str = f"\x1b[{color_dic[color]}m"

            row = out
            for word in words:
                try:
                    start = row.lower().index(word.lower())
                    end = start + len(word)
                except ValueError:
                    continue
                start = row.lower().index(word.lower())
                end = start + len(word)
                row = row[:start] + color_str + row[start:end] + "\x1b[0m" + row[end:]
        
            return row

    def find_section_given_words(self, words, outfmt='simple', include='up', to_right=False, colored=None):
        if isinstance(words, str) and words:
            words = [words]
        elif isinstance(words, list) and len(words)>0:
            assert all(isinstance(word, str) for word in words), "Elements in the list must be strings"
        else:
            raise ValueError("words must be a string or a list")
        
        if include not in ['up', 'both']:
            raise ValueError("Invalid value for include. Supported values are 'up' and 'both'.")

        out = [row for row in self.ctoc if any(word.lower() in row.lower() for word in words)]

        if outfmt == 'simple':
            return out
        elif outfmt == 'tree':
            out1 = []
            for out0 in out:
                out0_str = out0.split(' ', 1)[0]
                out0_str0 = out0_str.split(".")
                for str0 in range(len(out0_str0)):
                    out0_str1 = ".".join(out0_str0[:str0])
                    out2 = [item for item in self.ctoc if item.startswith(out0_str1 + " ")]
                    out1 = out1+out2
            out = list(set(out+out1))

            if colored:
                out_colored=[]
                for row in out: 
                    split_row = row.split(' ', 1)
                    if len(split_row) > 1:
                        first_part = split_row[0]
                        second_part = split_row[1]
                        colored_second_part = self.color_output(second_part, words=words, color=colored)
                        out_colored.append(f"{first_part} {colored_second_part}")
                    else:
                        out_colored.append(row)
                out_tree = ListTree(lst=out_colored, infmt='dotspace')
            else:
                out_tree = ListTree(lst=out, infmt='dotspace')
            return out_tree.list_tree(to_right=to_right)
        else:
            raise ValueError("Invalid value for outfmt. Supported values are 'simple' and 'tree'.")

if __name__ == "__main__":
    pass
    words = ['rems', 'dsur']
    ctoc = ctoc_by_fda()
    sections = ctoc.find_section_given_words(words, outfmt='tree')
    print(sections)
