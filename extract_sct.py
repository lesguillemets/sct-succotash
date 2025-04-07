#!/usr/bin/python3

import pandas as pd
import numpy as np
import re

from typing import Optional
from unicodedata import normalize

# 小学生は part1-5 , part2-7,
# 中学生が part1-3:1and2, part2, 6
# 大人は25だけ

def main():
    df = pd.read_csv("../source.csv", header=1, dtype=str)
    df['parsed_age'] = df['年齢'].apply(Age.age_parser)
    df['parsed_age_year'] = df['parsed_age'].apply(lambda x: x.y)
    df['parsed_age_month'] = df['parsed_age'].apply(lambda x: x.m)
    print(df.columns)
    df['the_text'] = df.apply(
            row_to_text,
            axis=1
            )
    df = df.drop('parsed_age',axis=1)
    print(df)
    # df.to_csv("./result.csv")
    df.to_excel("./result.xlsx")

def row_to_text(row):
    if row['parsed_age'].is_definitely_elementary():
        return f"5: {row['5']} \npart2-7: {row['7.1']}"
    elif row['parsed_age'].is_definitely_juniorhigh():
        return f"3(1): {row['3(1)']}\n, 3(2): {row['3(2)']}\npart2-6-1: {row['6(1)']}\npart2-6-2: {row['6(2)']}"
    elif row['parsed_age'].is_definitely_adult():
        return row['25']
    elif row['parsed_age'].y  == 12:
        # 小学生かもしれないし中学生かもしれない
        return "\n".join([
            "EITHER",
            f"    5: {row['5']} \n    part2-7: {row['7.1']}",
            "OR",
            f"    3(1): {row['3(1)']}\n,     3(2): {row['3(2)']}\n    part2-6-1: {row['6(1)']}\n    part2-6-2: {row['6(2)']}"
            ])
    elif row['parsed_age'].y  == 15:
        # 中学生かもしれないしそれ以上かもしれない
        return "\n".join([
            "EITHER",
            f"    3(1): {row['3(1)']}\n,     3(2): {row['3(2)']}\n    part2-6-1: {row['6(1)']}\n    part2-6-2: {row['6(2)']}",
            "OR",
            f"{row['25']}"
            ])

class Age:
    def __init__(self, y:Optional[int], m:Optional[int]):
        self.y = y
        self.m = m

    def __repl__(self):
        return f"{self.y}-{self.m}"

    def is_definitely_elementary(self) -> bool:
        # 12歳未満は小学生ですよね
        return self.y is not None and self.y < 12
    def is_definitely_juniorhigh(self) -> bool:
        # 12歳は小学生かもしれないし，15歳は高校生かもしれない
        return self.y is not None and (12 < self.y and self.y < 15 )
    def is_definitely_adult(self) -> bool:
        return self.y is not None and self.y > 15

    @staticmethod
    def age_parser(s:str) -> 'Age':
        if s is np.nan:
            return Age(None, None)
        s = normalize("NFKC", s)
        if s == "?" or s == "":
            return Age(None, None)
        m =  age_regex_ja.match(s) or age_regex_period.match(s) or age_only_regex_ja.match(s)
        if m is not None:
            y = int(m.group(1))
            try:
                m = int(m.group(2))
            except:
                m = None
            return Age(y, m)
        return Age(None, None)

age_only_regex_ja: re.Pattern[str] = re.compile(r"(\d{1,2})歳")
age_regex_ja: re.Pattern[str] = re.compile(r"(\d{1,2})歳(\d{1,2})か月")
age_regex_period: re.Pattern[str] = re.compile(r"(\d{1,2}).(\d{1,2})")


if __name__ == "__main__":
    main()
