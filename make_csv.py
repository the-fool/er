import json
import csv

with open('democrat.json', 'r') as dem_file:
    dem_data = json.load(dem_file).get('results')

with open('republican.json', 'r') as rep_file:
    rep_data = json.load(rep_file).get('results')

with open('election.csv', 'wb') as out:
    csvwriter = csv.writer(out)
    csvwriter.writerow(['GEOID', 'CLINTON', 'SANDERS', 'OTHER_DEM', 'TRUMP', 'CRUZ', 'OTHER_REP'])
    for key in dem_data.keys():
        if len(key) == 5:  # limit keys to fips / geoid numbers
            row = [key, 'clinton', 'sanders', 'other_dem', 'trump', 'cruz', 'other_rep']
            # do dems
            for result in dem_data.get(key).get('results'):
                candidate_id = result['candidate_id']
                if 'clinton' in candidate_id:
                    row[1] = result['votes']
                elif 'sanders' in candidate_id:
                    row[2] = result['votes']
                else:
                    row[3] = result['votes']
            # join republicans
            republican_row = rep_data.get(key, None)
            if republican_row:
                for result in republican_row.get('results'):
                    candidate_id = result['candidate_id']
                    if 'trump' in candidate_id:
                        row[4] = result['votes']
                    elif 'cruz' in candidate_id:
                        row[5] = result['votes']
                    else:
                        row[6] = result['votes']
                # only write row if it is joinable between the parties
                csvwriter.writerow(row)
