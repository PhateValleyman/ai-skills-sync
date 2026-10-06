#!/usr/bin/env python3
import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

RUNTIME_DIR = Path(os.getenv('MANUS_RUNTIME_DIR', '/opt/.manus/.sandbox-runtime'))
sys.path.insert(0, str(RUNTIME_DIR))

from data_api import ApiClient  # noqa: E402


def json_object(value: str | None) -> dict[str, Any] | None:
    if value is None:
        return None
    parsed = json.loads(value)
    if not isinstance(parsed, dict):
        raise argparse.ArgumentTypeError('JSON argument must be an object')
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser(description='Call a discovered Manus Data API')
    parser.add_argument('--api', required=True, help='Exact apiName returned by discover.py')
    parser.add_argument('--query-json')
    parser.add_argument('--body-json')
    parser.add_argument('--path-params-json')
    parser.add_argument('--multipart-form-data-json')
    args = parser.parse_args()

    try:
        result = ApiClient().call_api(
            args.api,
            query=json_object(args.query_json),
            body=json_object(args.body_json),
            path_params=json_object(args.path_params_json),
            multipart_form_data=json_object(args.multipart_form_data_json),
        )
    except (json.JSONDecodeError, argparse.ArgumentTypeError) as error:
        parser.error(str(error))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if 'error' in result else 0


if __name__ == '__main__':
    raise SystemExit(main())
