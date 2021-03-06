
from enum import Enum
import pandas as pd
import argparse
import json
import glob
import os


class EvalMitreResults():
    def __init__(self, filename, strict_mitre=False):
        self._strict_mitre = strict_mitre
        self._vendor = filename.split(os.sep, 2)[-1]
        self._vendor = self._vendor.split('.', 1)[0]
        print('Processing %s' % self._vendor)
        with open(filename, 'r', encoding='utf-8') as infile:
            data=infile.read()

        self._obj = json.loads(data)
        self._adv = None
        self._df = pd.DataFrame(columns=('Substep', 'Criteria', 'Tactic', 'TechniqueId', 'TechniqueName', 'SubtechniqueId', 'SubtechniqueName', 'Detection', 'Modifiers', 'Indicator', 'IndicatorName'))


    def getDetection(self, detections):
        allowModifiers = self._strict_mitre
        ret = {'Detection_Type':'None', 'Modifiers':'', 'Indicator':'', 'Indicator_Name':''} 
        dt = Enum('DetectionTypes', 'None Telemetry General Tactic Technique N/A')
        sev = Enum('Severity', 'Informational Low Medium High Critical')
        for detection in detections:
            # check if we're allowing modifiers
            if not allowModifiers and len(detection['Modifiers']):
                continue
            # checks for a better detection 
            if dt[ret['Detection_Type']].value < dt[detection['Detection_Type']].value:
                ret = detection
            # TODO - is this the same type but higher severity?
#            elif dt[ret['Detection_Type']].value == dt[detection['Detection_Type']].value and len(ret['Indicator']) and sev[ret['Indicator']].value < sev[detection['Indicator']].value:
#                ret = detection
        return (ret['Detection_Type'], ret['Modifiers'], ret['Indicator'], ret['Indicator_Name'])


    # append detection info for the substep to dataframe
    def appendSubstep(self, substep):
        obj = { 'Substep':None, 'Criteria':None, 'Tactic':None, 'TechniqueId':None, 'TechniqueName':None, 'SubtechniqueId':None, 'SubtechniqueName':None, 'Detection':None, 'Modifiers':None, 'Indicator':None, 'IndicatorName':None}
        obj['Substep'] = substep['Substep']
        obj['Criteria'] = substep['Criteria']
        obj['Tactic'] = substep['Tactic']['Tactic_Name']
        obj['TechniqueId'] = substep['Technique']['Technique_Id']
        obj['TechniqueName'] = substep['Technique']['Technique_Name']
        obj['SubtechniqueId'] = substep['Subtechnique']['Subtechnique_Id']
        obj['SubtechniqueName'] = '' if substep['Subtechnique']['Subtechnique_Name'] is None else substep['Subtechnique']['Subtechnique_Name'].split(':')[1][1:]

        (obj['Detection'], obj['Modifiers'], obj['Indicator'], obj['IndicatorName']) = self.getDetection(substep['Detections'])

        self._df.loc[len(self._df.index)] = obj


    # iterator function to process each substep
    def iterSteps(self):
        for scenario in self._adv['Detections_By_Step']:
            for step in self._adv['Detections_By_Step'][scenario]['Steps']:
                for substep in step['Substeps']:
                    self.appendSubstep(substep)


    # select adversary to analyze (stubbed out for future)
    def selectAdversary(self, adversary='wizard-spider-sandworm'):
        for adversary in self._obj[0]['Adversaries']:
            if adversary['Adversary_Name'] == 'wizard-spider-sandworm':
                self._adv = adversary
                break
        self.iterSteps()

    # iterate protection steps and calculate percentage blocked
    def scoreProtections(self):
        try:
            blocks = 0
            tests = len(self._adv['Protections']['Protection_Tests'])
        except KeyError:
            return 'n/a'

        for test in self._adv['Protections']['Protection_Tests']:
            for step in test['Substeps']:
                if step['Protection_Type'] == 'Blocked':
                    blocks += 1
                    break
        return blocks/tests
    


    # generate vendor performance metrics
    def scoreVendor(self):
        counts = self._df.Detection.value_counts()
        try:
            techniques = counts['Technique']
        except KeyError:
            techniques = 0
        try:
            misses = counts['None']
        except KeyError:
            misses = 0
        try:
            tactic = counts['Tactic']
        except KeyError:
            tactic = 0
        try:
            general = counts['General']
        except KeyError:
            general = 0
        try:
            na = counts['N/A']
        except KeyError:
            na = 0
        substeps = len(obj._df.index) - na
        visibility = substeps - misses
        analytics = (techniques + tactic + general)/substeps
        protections = self.scoreProtections()
        linux = 'yes' if 'Linux Capability' in self._adv['Participant_Capabilities'] else 'no'
        return (visibility/substeps, techniques/substeps, analytics, protections, linux)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Query utility for analyzing the MITRE ATT&CK Evaluations'
    )
    parser.add_argument(
        '--strict-mitre',
        help='Override analysis and stick to raw data',
        default=True,
        action='store_true'
    )

    args = parser.parse_args()

    return args


if __name__ == '__main__':

    args = parse_args()
    fname = 'wizard-spider-sandworm-mitre.xlsx'

    dfs = {}
    for infile in sorted(glob.glob(os.path.join('data', '*json'))):
        obj = EvalMitreResults(infile, args.strict_mitre)
        obj.selectAdversary('wizard-spider-sandworm')
        dfs.update({obj._vendor: obj})

    writer = pd.ExcelWriter(fname, engine='xlsxwriter')
    results = pd.DataFrame(columns=['vendor',       \
                                    'visibility',   \
                                    'techniques',   \
                                    'analytics',    \
                                    'protection',   \
                                    'linux'])

    # Write out results tab
    for vendor in dfs.keys():
        (visibility, techniques, analytics, protection, linux) = dfs[vendor].scoreVendor()
        results.loc[len(results.index)] = {'vendor':vendor, 'visibility':visibility, 'techniques':techniques, 'analytics':analytics, 'protection':protection, 'linux':linux}
    results.to_excel(writer, sheet_name='Results', index=False)

    # Write out individual vendor tabs
    for vendor in dfs.keys():
        dfs[vendor]._df.to_excel(writer, sheet_name=vendor, index=False, columns=['Substep', 'Criteria', 'Tactic', 'TechniqueId', 'TechniqueName', 'SubtechniqueId', 'SubtechniqueName', 'Detection', 'Modifiers', 'Indicator', 'IndicatorName'])
    writer.save()

    print('%s has been written.' % fname)

