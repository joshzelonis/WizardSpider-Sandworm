#!/bin/bash
#

vendors='ahnlab bitdefender checkpoint cisco crowdstrike cybereason cycraft cylance cynet deepinstinct elastic eset f-secure fidelis fireeye fortinet malwarebytes mcafee microsoft paloaltonetworks qualys rapid7 reaqta sentinelone somma sophos symantec trendmicro uptycs vmware'

echo "this isn't working right now, please download manually while I get this working again."
#cd data/
#for val in $vendors; do
#	curl -k "https://attackevals.mitre-engenuity.org/api/export/?participant=$val&adversary=wizard-spider-sandworm" -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:98.0) Gecko/20100101 Firefox/98.0' -H 'Accept: application/json, text/plain, */*' -H 'Accept-Language: en-US,en;q=0.5' -H 'Accept-Encoding: gzip, deflate, br' -H 'Referer: https://attackevals.mitre-engenuity.org/enterprise/participants/ahnlab?view=overview&adversary=wizard-spider-sandworm' -H 'DNT: 1' -H 'Connection: keep-alive' -H 'Sec-Fetch-Dest: empty' -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin' -H 'Sec-GPC: 1' --output "$val.json"
#done
