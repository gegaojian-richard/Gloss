#!/usr/bin/env python3
# coding=utf-8

import sys
import time
from progressbar import ProgressBar,Bar,Percentage


pbar = ProgressBar(widgets=[Percentage(), Bar()], maxval=1000).start()
for i in range(1000):
    time.sleep(0.01)
    pbar.update(i + 1)
pbar.finish()