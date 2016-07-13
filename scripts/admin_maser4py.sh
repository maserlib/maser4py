#!/bin/bash

# Set READ/WRITE privileges to users for maser4py Git repos.
# X.Bonnin (LESIA, Obs.Paris, CNRS), 13-JUL-2016

ssh git@git.obspm.fr perms projets/Plasma/maser4py + WRITERS xbonnin
ssh git@git.obspm.fr perms projets/Plasma/maser4py + WRITERS qnnguyen
ssh git@git.obspm.fr perms projets/Plasma/maser4py + WRITERS cecconi
ssh git@git.obspm.fr perms projets/Plasma/maser4py + READERS anonymous
