#!/bin/bash

python -c "from ruts.datasets import SovChLit; scl = SovChLit(); scl.download()"
python -c "from ruts.datasets import StalinWorks; sw = StalinWorks(); sw.download()"