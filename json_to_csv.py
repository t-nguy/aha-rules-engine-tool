path = 'output.json'
output_path = 'output.csv'

import csv
import json

def output_json_to_csv():
    with open(path, 'r') as f:
        out = open(output_path, 'w')
        writer = csv.writer(out, delimiter='|') 
        writer.writerow(['Blood Test Name', 'First Rule Hit', 'Max Score', 'Max Score Organ', 'Organs', 'All Rules Hit', 'Summary Opener', 'Summary Explanation', 'Summary Last', 'Recommendations', 'Future Recommendations', 'Prescription Info', 'Prescription Link', 'Biomarker Data'])
 
        data = json.load(f)
        for file in data:
            payload = json.loads(data[file]['response']['Payload'])
            firstRuleHit = payload['firstRuleHit']
            writer.writerow([file,
                             firstRuleHit['Order']['N'] + ': ' + firstRuleHit['Biomarker']['S'], 
                             payload['maxScore'], 
                             payload['maxOrgan'],
                             json.dumps(payload['organs']),
                             json.dumps(payload['rulesHit']),
                             firstRuleHit['Summary Opener Paragraph']['S'] if 'Summary Opener Paragraph' in firstRuleHit else '',
                             firstRuleHit['Summary Explanation Paragraph']['S'] if 'Summary Explanation Paragraph' in firstRuleHit else '',
                             firstRuleHit['Summary Last Paragraph']['S'] if 'Summary Last Paragraph' in firstRuleHit else '',
                             firstRuleHit['Recommendations']['S'] if 'Recommendations' in firstRuleHit else '',
                             firstRuleHit['Future Recommendations']['S'] if 'Future Recommendations' in firstRuleHit else '',
                             firstRuleHit['Prescription Info']['S'] if 'Prescription Info' in firstRuleHit else '',
                             firstRuleHit['Prescription Link']['S'] if 'Prescription Link' in firstRuleHit else '',
                             json.dumps(data[file]['biomarkers'])
                            ])
        out.close()
    f.close()

output_json_to_csv()


    