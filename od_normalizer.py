#!/usr/bin/env python3

import argparse
import pandas as pd
from openpyxl import load_workbook
import os
from gooey import GooeyParser, Gooey 

# NB: run with --ignore-gooey to force the CLI.
@Gooey
def main():
    parser = GooeyParser()
    # TODO: how to make the labels of the arguments in Gooey nicer?
    # (Specifically, how to divorce them from their attribute names?)
    parser.add_argument(
        "in_file", type=str, widget="FileChooser",
        help="The input Excel file from Sunrise. The ODs should be stored in Sheet1 within the workbook.")
    parser.add_argument("target_od", type=float)
    parser.add_argument(
        "final_volume", type=int, default=200,
        help="The final volume in the Target plate in µL.")
    parser.add_argument(
        "min_pipette", type=int, default=1,
        help="The minimum pipetting volume in µL.")
    parser.add_argument(
        "max_pipette", type=int, default=197,
        help="The maximum pipetting volume µL.")
    parser.add_argument(
        "out_folder", type=str, widget="DirChooser", default=os.getcwd(),
        help="The output folder where 'ddw.csv' and 'source.csv' will be saved.")
    
    args = parser.parse_args()
    
    in_file = args.in_file
    wb = load_workbook(filename=in_file)
    sheet = wb["Sheet1"]
    
    for row_ix, row in enumerate(sheet.iter_rows()):
        if "Rawdata" in str(row[0].value):
            break
        
    df = pd.read_excel(
        in_file,
        skiprows=row_ix+1,
        nrows=8,
        usecols="B:M"
    )
    
    target_od = args.target_od
    target_vol = args.final_volume
    min_pipette = args.min_pipette
    max_pipette = args.max_pipette
    
    # TODO: handle the following cases:
    # 1: wells below target_id
    # 2: need to take less than 1 uL of source
    # 3: need to take more than 197 uL of source
    
    source_df = (target_od * target_vol / df).round().astype(int)
    ddw_df = (target_vol - source_df).round().astype(int)
    
    out_folder = args.out_folder
    ddw_fname = "ddw.csv"
    source_fname = "source.csv"
    
    # Output format by columns:
    # 1 - source name
    # 2 - source position
    # 3 - target name
    # 4 - target position
    # 5 - volume
    with open(os.path.join(out_folder, ddw_fname), "w") as ddw_file:
        for col_ix, column in enumerate(ddw_df):
            series = ddw_df.loc[:, column]
            for vol_ix, vol in enumerate(series):
                ddw_file.write(f"DDW,{vol_ix+1},Target,{vol_ix+1+col_ix*8},{vol}\n")
                
    with open(os.path.join(out_folder, source_fname), "w") as source_file:
        for col_ix, column in enumerate(source_df):
            series = source_df.loc[:, column]
            for vol_ix, vol in enumerate(series):
                pos = vol_ix+1+col_ix*8
                source_file.write(f"Source,{pos},Target,{pos},{vol}\n")
                
    print("Done!") # TODO: how to change the output of Gooey?
    

if __name__ == "__main__":
    main()