# GRO weapon form

Form for adding weapons to Ghost Recon Online [database](https://github.com/zeroKilo/GROBackendWV/blob/master/GROBackendWV/bin/x86/Release/database.sqlite) (SQLite).

![demo](https://github.com/michal-kapala/gro-weapon-form/assets/48450427/2cbe9ed4-207c-4cd7-a96a-b78c385aa0b2)

## Config

Create `.env` file with GRO database path in the root directory:
```
# Unescaped Windows path to the database (example)
SQLITE_PATH=C:\GROBackendWV\GROBackendWV\bin\x86\Release\database.sqlite
```

## Run

Install dependencies and run the server (port 5000):
```
pip install -r requirements.txt
python server.py
```

Requires Python 3.10 or newer.

## Usage

Component inputs expect hexadecimal values (`0x` is optional). Components that should be created but don't have their asset keys (fire modes, ForeGripAndBarrel) should get `0` as input.
