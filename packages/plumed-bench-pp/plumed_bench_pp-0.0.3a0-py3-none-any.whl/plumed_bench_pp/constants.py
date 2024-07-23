# SPDX-FileCopyrightText: 2024-present Daniele Rapetti <daniele.rapetti@sissa.it>
#
# SPDX-License-Identifier: MIT

TIMINGCOLS = ["Cycles", "Total", "Average", "Minimum", "Maximum"]
# These are the common row names in the benchmark output
BM_INIT = "A Initialization"
BM_FIRSTSTEP = "B0 First step"
BM_WARMUP = "B1 Warm-up"
BM_CALCULATION_PART1 = "B2 Calculation part 1"
BM_CALCULATION_PART2 = "B3 Calculation part 2"
TOTALTIME = "Plumed"
PREPARE = "1 Prepare dependencies"
SHARE = "2 Sharing data"
WAIT = "3 Waiting for data"
CALCULATE = "4 Calculating (forward loop)"
APPLY = "5 Applying (backward loop)"
UPDATE = "6 Update"
