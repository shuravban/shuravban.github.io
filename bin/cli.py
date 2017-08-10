#!/usr/bin/python3

# sorry
from boot import api

import argparse
import json
import sys

def _to_dict(param_list):
    """Convert a list of key=value to dict[key]=value"""
    if param_list:
        return {
            name: value for (name, value) in
                [param.split('=') for param in param_list]}
    else:
        return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Request any Twitter Streaming or REST API endpoint')
    parser.add_argument(
        '-endpoint',
        metavar='ENDPOINT',
        type=str,
        help='Twitter endpoint',
        required=True)
    parser.add_argument(
        '-parameters',
        metavar='NAME_VALUE',
        type=str,
        help='parameter NAME=VALUE',
        nargs='+')
    args = parser.parse_args()

    try:
        params = _to_dict(args.parameters)

        response = api.request(args.endpoint, params)

        print(response.text)
    except KeyboardInterrupt:
        print('Terminated by user')

    except Exception as e:
        print('STOPPED: %s' % e)
