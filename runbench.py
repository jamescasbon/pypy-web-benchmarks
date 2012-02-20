import sys
import csv
import subprocess
import time
import re

GETS = 1000
concurrencies = [10]#,100,1000]


def servers():
    yield 'cyclone', subprocess.Popen('python servers/cyc.py'.split())
    yield 'tornado', subprocess.Popen('python servers/torn.py'.split())
    yield 'flask:tornado', subprocess.Popen('python servers/fla.py'.split())

    for host in ['tornado', 'paste', 'rocket']: #excluded wsgiref twisted
        yield 'bottle:%s' % host, subprocess.Popen(('python servers/bot.py %s' % host).split())


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


headers = 'name conc reqs_per_sec rs.min rs.mean rs.std rs.median rs.max'.split()

out = csv.writer(file('results.txt', 'w'), delimiter='\t')
out.writerow(headers)

def write_result(setup, result):
    out.writerow(setup + [result[x] for x in headers[len(setup):]])

for conc in concurrencies:

    for name, server in servers():
        print 'testing %(name)s at concurrency %(conc)s' % locals()
        time.sleep(1)
        try:
            command = 'ab -n %(GETS)s -c %(conc)s http://localhost:8000/' % locals()
            ab = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
            ab.wait()
            result = ab.stdout.read()
            if ab.returncode == 0:
                write_result([name, conc], metrics(result))
            else:
                write_result([name, conc], dict([(x,'') for x in headers]))
        finally:
            server.terminate()


