#!/usr/bin/python3
import sys
import json

cluster_name = sys.argv[1]
update_operation = sys.argv[2]
input_list = json.loads(sys.argv[3])

result_dict = {}
for each_cluster in input_list:
    if each_cluster.get('cluster') == cluster_name:
        for eachReport in each_cluster.get('hostComplianceReports'):
            tmp_dict = {eachReport.get('serviceTag'): []}
            for eachCompliance in eachReport.get('componentCompliances'):
                if eachCompliance.get('updateAction').lower() == update_operation.lower():
                    tmp_dict[eachReport.get('serviceTag')].append(eachCompliance.get('sourceName'))
            result_dict.update(tmp_dict)
        all_value = [set(value) for key, value in result_dict.items()]
        common_value = list(all_value[0].intersection(*all_value[1:]))
        result_dict.update({'common': common_value})

print(json.dumps(result_dict))