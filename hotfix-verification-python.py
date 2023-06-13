import boto3
import csv
import sys
import os
import pandas as pd

def mainFunction():

    inputHotfix2012 = os.environ['Hotfix ID Win2012']
    inputHotfix2019 = os.environ['Hotfix ID Win2019']

    filterData(inputHotfix2012,inputHotfix2019)

def filterData(filterHotfix2012,filtHotfix2019):

    filter_df = pd.read_csv('servers-hotfix.csv')
    for index, row in filter_df.iterrows():
        rowServer = row['instanceid']
        rowRegion = row['reg']

        print(rowServer,rowRegion,filterHotfix2012,filtHotfix2019)
        runSSMCommand(rowServer,rowRegion,filterHotfix2012,filtHotfix2019)



def runSSMCommand(runServer,runRegion,runHotfix2012,runHotfix2019):
    from datetime import date
    runDocument="cp-verification-hotfix-document"
    
    runToday = date.today()
    runToday = runToday.strftime("%d%m%Y")
    runComment = (runServer + "-" +runToday)

    ssm_client = boto3.client('ssm',region_name=runRegion)
    response = ssm_client.send_command(
                    InstanceIds=[runServer],
                    Comment=runComment,
                    DocumentName=runDocument,
                    MaxConcurrency='100%',
                    Parameters={'Hotfixwin2012': 
                                [runHotfix2012],
                                'Hotfixwin2019': 
                                [runHotfix2019]
                                },
                    MaxErrors='100%',
                    TimeoutSeconds=900)

    command_id = response['Command']['CommandId']
    print("Command Id:" + command_id)

mainFunction()
