# Bluetooth for Ball-E

This repository contains all the code and related logs/files pertaining to the Bluetooth functionality for Ball-E.

## Pre-requisites
---
* `Python 3.6.9`
* `PyBluez`
* `evdev`
* `pydbus`

## Branch Structure

### main
Contains 'production-level', 100% working code

### develop
Contains beta code. This will be the primary branch for system-wide testing

### feature branches
Freature branches are development branches which is always updated with the latest `develop` branch's code. A feature branch uses the following naming convention:

`feature/<ticket-#>`

## Project Structure

### src/
Contains code, usually `.py` files.

### logs/
_Note: This folder is in `.gitignore`. But when running the files directly, it will get created locally in your environment._

Logs from the code run in `src/`, updated on a date-basis. It will track all levels log statements (DEBUG, INFO, WARNING, ERROR, CRITICAL). Its naming convention:
`<mm_dd_yy>_debug.log`

**Please use `logging` instead of `print` statements to keep track of the code flow. It helps a lot in the long run!**

## File Structure

All `.py` files are fomatted using `autopep8`.