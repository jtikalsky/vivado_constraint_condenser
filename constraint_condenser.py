#!/usr/bin/python3

import re
import sys
from typing import Dict, List, Optional, Set

CONF: List[str] = sys.stdin.read().split('\n')

r_SINGLE_PROP = re.compile(r'^set_property\s+(?P<property>[A-Z_]+)\s+(?P<value>.*)\s+(?P<pin>\[get_ports.*\])\s*$')
r_MULTI_PROP = re.compile(r'^set_property\s+-dict\s+\{(?P<dict_data>[^\}]+)\}\s+(?P<pin>\[get_ports.*\])\s*$')
r_PROP_PAIR = re.compile(r'(?P<key>\S+)\s+(?P<value>\S+)\s*')
r_PIN_NORM = re.compile(r'\[get_ports\s+{?(?P<pinid>[^}]+)}?\]')


def norm_pin(pin: str) -> str:
	m = r_PIN_NORM.match(pin)
	assert m is not None, f"Unable to parse pin {pin!r}"
	return m.group('pinid')


def parse_line(line: str, data: Dict[str, Dict[str, str]] = {}) -> Optional[str]:
	if (m := r_SINGLE_PROP.match(line)) is not None:
		npin = norm_pin(m.group('pin'))
		data.setdefault(npin, {'__name__': m.group('pin')})[m.group('property')] = m.group('value')
		return npin
	elif (m := r_MULTI_PROP.match(line)) is not None:
		npin = norm_pin(m.group('pin'))
		for m2 in r_PROP_PAIR.finditer(m.group('dict_data')):
			data.setdefault(npin, {'__name__': m.group('pin')})[m2.group('key')] = m2.group('value')
		return npin
	else:
		return None


PIN_PARAMS: Dict[str, Dict[str, str]] = {}
for line in CONF:
	parse_line(line, PIN_PARAMS)

newconf: List[str] = []
seen: Set[str] = set()
for line in CONF:
	pin = parse_line(line)
	if pin is None:
		newconf.append(line)
	elif pin in seen:
		continue
	else:
		data = PIN_PARAMS[pin]
		newconf.append(
		    'set_property -dict {{{data}}} {pin}'.format(
		        pin=data['__name__'], data=' '.join(f'{k} {v}' for k, v in data.items() if not k == '__name__')
		    )
		)
		seen.add(pin)
print('\n'.join(newconf))
