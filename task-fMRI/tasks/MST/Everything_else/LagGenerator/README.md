Sample code (currently all in Matlab, but should be ported to NumPy at some
point) showing how to create order files for the continuous version of the
task.

CreateOrder_AllShort.m - used by me (Craig) currently in an "easy" version of
the task.

CreateOrderLagBins_0_180.m - used in an earlier Matlab version of the task.
Would likely need to be modified to work directly here, but shows some
strategies for placing multiple sets of lags.

TestLagGenerator.m - just runs CreateOrder_AllShort a bunch of times to make
multiple sets of trial orders

AllShort_Set1 (and 2) - sample outputs that can be used
