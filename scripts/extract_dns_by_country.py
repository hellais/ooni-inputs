import os
import sys
import csv
import yaml
from glob import glob
import GeoIP

# Change this to point to the location of your geoip data files
geoip_data_dir = '/usr/share/GeoIP'

try:
    country_db = GeoIP.open(os.path.join(geoip_data_dir, 'GeoIP.dat'), GeoIP.GEOIP_STANDARD)
    asn_db = GeoIP.open(os.path.join(geoip_data_dir, 'GeoIPASNum.dat'), GeoIP.GEOIP_STANDARD)
except:
    print "Edit in %s the geoip_data_dir line to point to you geoip files" % sys.argv[0]

if len(sys.argv) != 3:
    print "%s [path to csv file containing the resolvers] [destination output directory]" % sys.argv[0]
    sys.exit(1)

csv_file = sys.argv[1]
output_dir = sys.argv[2]

def geodata(ipaddr):
    asn = 'AS0'
    org_name = 'unknown'
    cc = country_db.country_code_by_addr(ipaddr)
    org = asn_db.org_by_addr(ipaddr)
    if org:
        asn = org.split(' ')[0]
        org_name = ' '.join(org.split(' ')[1:])
    if not cc:
        cc = 'ZZ'
    return {'cc': cc, 'asn': asn, 'org_name': org_name}

def write_entry(cc, asn, row, org_name):
    target_dir = os.path.join(output_dir, cc, 'dns-servers')
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    try:
        with open(os.path.join(target_dir, '%s.yml' % asn)) as f:
            data = yaml.load(f)
    except:
        data = []
    data.append({
        'cc': cc, 
        'asn': asn, 
        'organization_name': org_name,
        'description': row[2],
        'address': row[0]
    })
    with open(os.path.join(target_dir, '%s.yml' % asn), 'w+') as f:
        yaml.dump(data, f)

reader = csv.reader(open(csv_file))
for row in reader:
    if row[2] == 'X-Internal-IP':
        continue
    elif row[2] == 'X-Unroutable':
        continue
    elif row[2] == 'X-Link_local':
        continue
    ipaddr = row[0]
    gd = geodata(ipaddr)
    write_entry(gd['cc'], gd['asn'], row, gd['org_name'])

