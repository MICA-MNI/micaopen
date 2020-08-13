# MST
Mnemonic Similarity Task

The goal of this repository is to provide the stimuli and source code used
to run the Mnemonic Similarity Task (MST).  I (Craig Stark) have coded the
MST up for a number of different platforms over the years, but the goal here
is to provide people with the current, cross-platform code used in the 
stand-alone C++ variant and the PsychoPy variant.  These should be well-
suited to behavioral testing and readily modified for things like fMRI
or EEG testing.  Bug fixes, enhancements, etc. are welcome!

The MST (formerly the BPSO or SPST – yes, it’s had a few names!) is a 
behavioral task designed to tax pattern separation. Pattern separation can 
really only be assessed by looking at representations of information and we 
clearly can’t do that behaviorally. But, the goal is to have a task that would 
place strong demands on a system that performed pattern separation and, in so 
doing, get some measure of this.

The task consists of assessing recognition memory performance for objects 
using not only the traditional targets and unrelated foils, but also using 
similar lures (that intentionally vary along several different dimensions). 
This certainly isn’t a unique concept. Here, however, we have developed the 
task since its creation (Kirwan & Stark, 2007, Learning & Memory) to create 
a set of well-matched stimuli that have been tested extensively both in our 
lab and in others. Note, the behavioral task is an explicit one that asks 
participants to respond “Old”, “Similar”, or “New” on each trial (we have done 
“Old” vs. “New” and even “R”, “K”, “N”). Typically, this has been done in a 
study-test variant, but we have (often while in the scanner) done a continuous 
version as well (Yassa et al., 2010, NeuroImage).  A good place to turn for 
some of the behavioral comparisons is the S. Stark et al. (2015, Behavioral
Neuroscience) paper.
