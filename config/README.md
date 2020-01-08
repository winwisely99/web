## How **`hugoconfig.yml`** works?

- The gsheet is located in [bootstrap](https://github.com/getcouragenow/bootstrap) repository under `tool/googleshhet` folder.

## How to add a new sheet to **`hugoconfig.yml`**?

1. First you need to create a [googlesheet](https://docs.google.com/spreadsheets) then `share it` and `publish it`.
2. Once the googlesheet is ready add a new object to `hugoconfig.xml` and populate these fields:

Key|Value
---|---
ID| `1po7GuEo4H04HEPTuG6DFreenBDvJ2QKLUQiIRPKzEBI`
URL|`https://docs.google.com/spreadsheets/d/...`
CSV|`https://docs.google.com/spreadsheets/d/e/.../pub?output=csv`
MERGE|you can choose how to merge googlesheet cells: `cell`, `column` or `row`
OUT_DIR| Out folder path exemple `outputs/content/` and use: `outputs/content/XXX/` to generate multi language folders example: `outputs/content/en/`, `outputs/content/fr/` ...
FILE_NAME| if empty gsheet use default one on googlesheet. use `languages.XXX` if file is multi languages.
EXTENSION| `.toml` if file_name is empty gsheet use default one on sheet. 
