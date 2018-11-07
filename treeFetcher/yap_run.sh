#!/bin/sh
pwd
./treeFetcher/parsing_handler/yapproj/src/yap/yap hebma -raw ./treeFetcher/parsing_handler/yapproj/src/yap/data/input.raw -out ./treeFetcher/parsing_handler/yapproj/src/yap/data/lattices.conll
./treeFetcher/parsing_handler/yapproj/src/yap/yap md -in ./treeFetcher/parsing_handler/yapproj/src/yap/data/lattices.conll -om ./treeFetcher/parsing_handler/yapproj/src/yap/data/output.conll
./treeFetcher/parsing_handler/yapproj/src/yap/yap dep -inl ./treeFetcher/parsing_handler/yapproj/src/yap/data/output.conll -oc ./treeFetcher/parsing_handler/yapproj/src/yap/data/dep_output.conll

