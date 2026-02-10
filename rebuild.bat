@echo off
REM Navigate to docs folder
cd docs

REM Clean previous builds
call make clean html

REM Build HTML docs
call make html

REM Return to project root
cd ..
