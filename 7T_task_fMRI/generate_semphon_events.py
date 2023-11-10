import os
import pandas as pd
import numpy as np

path = os.path.normpath(os.getcwd()).split(os.sep)
if path[2] == 'neichert':
    outdir = '/Users/neichert/Library/CloudStorage/OneDrive-Nexus365/Fellowship/MTL'
elif path[2] == 'mica3':
    outdir = '/data/mica1/03_projects/neichert/7T'
else:
    outdir = os.getcwd()

conditions_both = np.array(
        [['A1', 'B1', 'C1', 'D'],
         ['C1', 'A1', 'B1', 'D'],
         ['B1', 'C1', 'A1', 'D'],
         ['B2', 'C2', 'A2', 'D'],
         ['A2', 'B2', 'C2', 'D'],
         ['C2', 'A2', 'B2', 'D']])

all_blocks = list(conditions_both.flatten())
blocks_semphon1 = all_blocks[0:12]
blocks_semphon2 = all_blocks[12::]

duration = 30
for i_run, blocks in enumerate([blocks_semphon1, blocks_semphon2]):
    events_df = pd.DataFrame(columns=('onset', 'duration', 'condition'))
    onset = 0
    for i_block, block in enumerate(blocks):
        if 'A' in block:
            condition = "phonological"
        elif 'B' in block:
            condition = "semantic"
        elif 'C' in block:
            condition = "visual"
        elif 'D' in block:
            condition = "rest"
        onset = onset + 3
        events_df = events_df.append({'onset': onset, 'duration': duration, 'condition': condition}, ignore_index=True)

        onset = onset + duration
    events_df = events_df.reset_index(drop=True)
    # save output
    out_file = os.path.join(outdir, f'task-semphon{i_run+1}_events.tsv')
    events_df.to_csv(out_file, sep='\t', index=False)
    print('saved: ')
    print(out_file)
