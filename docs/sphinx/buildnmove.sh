#!/bin/bash
make html
cp .build/html/* ../ -r
echo "Build files have been copied to docs for Jekyll"
