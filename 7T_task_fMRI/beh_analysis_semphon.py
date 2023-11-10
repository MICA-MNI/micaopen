import numpy as np
import pandas as pd
import seaborn as sns
import os
from matplotlib import pyplot as plt
import sys

currentDir = os.getcwd()
path = os.path.normpath(currentDir)
path = path.split(os.sep)
if path[2] == 'neichert':
    rootLog = '/Users/neichert/code/micaopen/7T_task_fMRI/logs'
    audiobookdir = currentDir + '/audiobook'
elif path[2] == 'percy':
    rootLog = '/data/mica3/7T_task_fMRI/logs'
    audiobookdir = '/data/mica3/7T_task_fMRI/audiobooks'
    VLCBIN = '/usr/bin/vlc'
elif path[2] == 'mica3':
    rootLog = '/data/mica3/BIDS_PNI/sorted'
    audiobookdir = '/data/mica3/7T_task_fMRI/audiobooks'
else:
    audiobookdir = currentDir + '/audiobook'


# condition names:
conditions = {'A': 'phonological',
              'B': 'semantic',
              'C': 'visual',
              'D': 'Rest'}

colors = {'phonological': "#F28E2B", 'semantic': "#4E79A7", 'visual': "#79706E"}

# subjects to analyse
# indicate which sssion and runs to use for the two task blocks):
# normally: ('04',['01', '01'])
subs_run_dict = {'PNC013': ('04', ['01', '01'])}

log_all = pd.DataFrame()
for (sub, (ses, runs_list)) in subs_run_dict.items():
    for rep, run in enumerate(runs_list):
        # load logfile
        log_fpath = f'{rootLog}/sub-{sub}_ses-{ses}/beh/sub-{sub}_ses-{ses}_sp{rep+1}_run-{run}.tsv'
        if os.path.exists(log_fpath):
            log = pd.read_table(log_fpath, sep='\t', dtype={'RT': np.float64}, na_values=['-', 'nan'])
            # minor procssing
            log['Condition'] = log['Condition'].replace(conditions)
            log = log[log['Condition']!='Rest']
            log['is_correct'] = log['Given_answer'] == log['Expected_answer']
            log['sub'] = sub
            log['run'] = run
            log_all = pd.concat([log_all, log], ignore_index=True)
        else:
            print(f'{log_fpath} not found. Skip.')
### Summary statistics
# per condition
RT = log_all.groupby('Condition')['RT'].mean().reset_index()
p_correct = log_all.groupby( 'Condition')['is_correct'].value_counts(normalize=True)\
    .unstack(fill_value=0).stack() \
    .reset_index().query('is_correct==True').drop(['is_correct'], axis=1)\
    .rename(columns={0: 'p_correct'})
summary_per_condition = RT.merge(p_correct)
print(summary_per_condition)

# per subject
RT = log_all.groupby('sub')['RT'].mean().reset_index()
p_correct = log_all.groupby('sub')['is_correct'].value_counts(normalize=True)\
    .unstack(fill_value=0).stack() \
    .reset_index().query('is_correct==True').drop(['is_correct'], axis=1)\
    .rename(columns={0: 'p_correct'})

summary_per_subject = RT.merge(p_correct)
print(summary_per_subject)

<<<<<<< HEAD
### Plotting
# plot RT

fig, axes = plt.subplots(1, 2)
sns.barplot(data=log_all, x='Condition', y='RT', ax=axes[0], palette=colors)
axes[0].set_title('Reaction time (ms)')

# plot percentage correct
log_all.groupby('Condition')['is_correct'].value_counts(normalize=True)\
    .unstack(fill_value=0).stack() \
    .reset_index().query('is_correct==True').drop(['is_correct'], axis=1)\
    .rename(columns={0: 'p_correct'})\
    .pipe((sns.barplot, "data"), ax=axes[1], x='Condition', y='p_correct', palette=colors)
axes[1].set_ylim(0, 1)
axes[1].set_title('% correct responses')
plt.show()
