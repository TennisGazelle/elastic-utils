# elastic-utils
utilities for faster elastic dev

## `es-index-deletion.py`
Need to delete a lot of indices en masse, and the console only lets you do one at a time?
Want to also have the flexibility of regexing the ones to save?

1. Set a credential file that fills these variables in

```bash
AWS_ACCESS_KEY_ID=anything
AWS_SECRET_ACCESS_KEY=anythingelse
host=<host>
port=<port>
ignore=<regex> # e.g. index-1-*,index-2-*,...
```

2.
```bash
pip3 install elasticsearch requests_aws4auth # Prerequisites
python3 ./es-index-deletion.py
```
