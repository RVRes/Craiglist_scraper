#!/bin/bash
# Переходим в категорию GIT
PATH=$PATH:'/bin':'/bin/git':'/home/roman/scripts/craiglis_scrap'
cd '/home/roman/scripts/craiglis_scrap'


# Загружаем данные из ветки main
git checkout main
git pull