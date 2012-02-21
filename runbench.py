import sys
import csv
import subprocess
import time
import re

GETS = 10000
concurrencies = [(4 ** x) for x in (1,2,3,4)]
REPS = [1]

is_pypy = hasattr(sys, 'pypy_version_info')
gevent = [] if is_pypy else ['gevent']

def servers():
    yield 'cyclone', 'cyclone', subprocess.Popen('python servers/cyc.py'.split())
    yield 'tornado', 'tornado', subprocess.Popen('python servers/torn.py'.split())

    for host in gevent + ['twisted', 'tornado', 'paste', 'rocket']: #excluded wsgiref twisted
        yield 'bottle', host, subprocess.Popen(('python servers/bot.py %s' % host).split())

    for host in gevent + ['tornado']: #excluded wsgiref twisted
        yield 'flask', host, subprocess.Popen(('python servers/fla.py %s' % host).split())



def metrics(result):
    mets = {}

    mets['reqs_per_sec'] = float(re.search('Requests per second:\s+(\S+)', result).group(1))

    reqs = re.search('Total:\s+(\d+)\s+(\d+)\s+(\S+)\s+(\d+)\s+(\d+)', result)
    mets['rs.min'] = reqs.group(1)
    mets['rs.mean'] = reqs.group(2)
    mets['rs.std'] = reqs.group(3)
    mets['rs.median'] = reqs.group(4)
    mets['rs.max'] = reqs.group(5)
    print mets
    return mets


headers = 'pypy name host conc rep reqs_per_sec rs.min rs.mean rs.std rs.median rs.max'.split()

out = csv.writer(file('results.txt', 'w'), delimiter='\t')
out.writerow(headers)

def write_result(setup, result):
    out.writerow(setup + [result[x] for x in headers[len(setup):]])

for conc in concurrencies:

    for name, host, server in servers():
        print 'testing %(name)s, %(host)s at concurrency %(conc)s' % locals()
        time.sleep(1)
        try:
            for rep in REPS:


                command = 'ab -n %(GETS)s -c %(conc)s http://127.0.0.1:8000/' % locals()
                ab = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
                ab.wait()
                result = ab.stdout.read()
                if ab.returncode == 0:
                    write_result([is_pypy, name, host, conc, rep], metrics(result))
                else:
                    write_result([is_pypy, name, host, conc, rep], dict([(x,'') for x in headers]))
        finally:
            server.terminate()
            server.wait()

