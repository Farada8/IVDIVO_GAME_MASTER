#!/usr/bin/env python3
import json,sys
REQ=['model','source_set','answer','evidence','defect_class','confidence']

def validate_record(record):
    return [k for k in REQ if k not in record or record[k] in (None,'',[])]

if __name__=='__main__':
    rows=json.load(open(sys.argv[1],encoding='utf-8'))
    failed=0
    for row in rows:
        missing=validate_record(row)
        print(row.get('id'),'PASS' if not missing else 'FAIL',missing)
        failed += int(bool(missing))
    raise SystemExit(1 if failed else 0)
