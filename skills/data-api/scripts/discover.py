#!/usr/bin/env python3
import argparse
import json
import os
import sys
from pathlib import Path

# source key -> provider display-name fallback for the datasource card
SOURCES = {
    'x-twitter': 'X/Twitter',
    'linkedin': 'LinkedIn',
    'youtube': 'YouTube',
    'social-media': 'Social Media',
    'financial-market': 'Financial Market',
    'earnings-research': 'Quartr',
    'crunchbase': 'Crunchbase',
    'world-bank': 'World Bank',
    'google-trends': 'Google Trends',
    'app-store': 'App Store',
    'similarweb': 'Similarweb',
    'domain-check': 'Domainr',
    '3d-model': 'Tripo3D',
}
RUNTIME_DIR = Path(os.getenv('MANUS_RUNTIME_DIR', '/opt/.manus/.sandbox-runtime'))
sys.path.insert(0, str(RUNTIME_DIR))

from data_api import ApiClient  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description='Discover task-relevant Manus Data APIs')
    parser.add_argument('--source', required=True, choices=sorted(SOURCES))
    parser.add_argument('--query', required=True)
    parser.add_argument('--limit', type=int, default=3)
    args = parser.parse_args()

    result = ApiClient().discover_api(args.source, args.query, args.limit)
    if error := result.get('error'):
        print(f'Data API discovery failed: {error}', file=sys.stderr)
        return 1

    apis = result.get('apis', [])
    print(json.dumps({'apis': apis}, ensure_ascii=False, indent=2))
    resources = [
        {
            'id': api.get('apiName') or api.get('shortId'),
            'title': api.get('name') or api.get('apiName'),
            'provider': api.get('provider') or SOURCES[args.source],
        }
        for api in apis
    ]
    # No marker when discovery finds nothing: the datasource card should only appear for real matches.
    if resources:
        print('MANUS_RESOURCE_EVENT=' + json.dumps({'type': 'data_api', 'resources': resources}, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
