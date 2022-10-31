import requests
import json
from tabulate import tabulate
from prettytable import PrettyTable
import pandas as pd
import csv
import datetime
import os


#url = 'https://s.rfihub.com/ws/17169175/meta/CitiHomeNGA'
#data = 'RequestObject={\"GUID\":\"85d1e010-ec98-49fe-8482-c0e9c8a903ba\",\"IPAddress\":\"99.141.144.93\",\"XP_UID\":\"SY-00DW9AAouUHvI=510\",\"Data\":{\"r\":\"1\",\"ssv_s2s\":\"Y\",\"ssv_pop\":\"25\",\"ssv_ecm\":\"Y\",\"ssvm_member\": \"PAAE\",\"ssv_resp\":\"I000\",\"ssvm_pid\":\"056_X;410_X;051_X;093_X\"},\"CreateXPUID\":\"false\",\"ForceUIDMatch\":\"false\",\"ContentTypeJSON\":\"true\",\"Referer\":\"https://www.citi.com\",\"UserAgent\":\"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0\"},\n    \"CreateXPUID\": \"false\",\n    \"ForceUIDMatch\": \"false\",\n    \"ContentTypeJSON\": \"true\",\n    \"Referer\": \"https://www.citi.com\",\n    \"UserAgent\": \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0\"\n}'


class CitiTester(object):
    def callEndpoint(url, data):
        #url = 'http://s.rfihub.com/ws/17169175/meta/citi-com-homepage-ang'
        #data = 'RequestObject={\n    \"GUID\": \"GUIDTest\",\n    \"IPAddress\": \"68.56.115.110\",\n    \"XP_UID\": \"abc123456\",\n    \"Data\": {\n        \"ssv_pop\": \"5\",\n        \"ssv_darrentest\": \"1\",\n        \"ssv_device\": \"S\",\n        \"ssv_ecm\": \"N\",\n        \"ssv_resp\": \"I000\",\n        \"ssv_cbcatcham\": \"B178_01\",\n        \"ssv_lob\": \"cb\",\n        \"ssv_ex\": \"Uncookied\",\n        \"ssvm_cpi\": \"N\",\n        \"ssv_pricreg\": \"OUT\",\n        \"ssvm_pid\": \"D384;AAF_X;S201;M185;C701;408_X;S723;089_X;MPC_X;257_X\"\n    },\n    \"CreateXPUID\": \"false\",\n    \"ForceUIDMatch\": \"false\",\n    \"ContentTypeJSON\": \"true\",\n    \"Referer\": \"https://www.citi.com\",\n    \"UserAgent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36\"\n}'
        response = {'somekey': 'somevalue'}


        x = requests.post(url, data)
        return x.text

    def ReadInput():
        currentDirectory = os.getcwd()
        currentDirectory = currentDirectory + '\\' + 'input' + '\\' + 'TestCalls.txt'

        InputFile = open(currentDirectory, 'r')
        Lines = InputFile.readlines()
        InputFile.close()

        return Lines


    def ParseJSON(postResult):

        result = json.loads(postResult)
        return result

    def FindPage():

        tempURL = url.split('/')

        length = len(tempURL)
        metaTagCode = tempURL[length-1]

        return metaTagCode


    def GetContentIDs(output, PageName):

        ContentIDArray = []
        ScenarioIDArray = []

        counter = 0

        if PageName == 'citi-com-homepage-ang':
            for placement in output['ContentData']['rf_placements']:
                tempContent = output['ContentData']['rf_placements'][placement]['contentID']
                ContentIDArray.append(tempContent)
                tempContent = output['ContentData']['rf_placements'][placement]['scenarioID']
                ScenarioIDArray.append(tempContent)
                counter += 1
        elif PageName == 'CitiVACNGA' or 'CitiHomeNGA':
            for placement in output['ContentData']:
                tempContent = output['ContentData'][placement]['contentID']
                ContentIDArray.append(tempContent)
                tempContent = output['ContentData'][placement]['scenarioID']
                ScenarioIDArray.append(tempContent)
                counter += 1

        return ContentIDArray, ScenarioIDArray

    def GetScenarioIDs(output, PageName):

        ScenarioList = []

        if PageName == 'citi-com-homepage-ang':
            for placement in output['ContentData']['rf_placements']:
                tempContent = output['ContentData']['rf_placements'][placement]['scenarioID']
                ScenarioList.append(tempContent)
        elif PageName == 'CitiVACNGA' or 'CitiHomeNGA':
            for placement in output['ContentData']:
                tempContent = output['ContentData'][placement]['scenarioID']
                ScenarioList.append(tempContent)

        return list(dict.fromkeys(ScenarioList))

TestCalls = CitiTester.ReadInput()

for Call in TestCalls:
    tempCall = Call.split('\t')
    url = tempCall[0]
    data = tempCall[1]


    testIterations = 25
    x = 0
    resultsList = []
    ContentTable = PrettyTable(["Content_ID", "Placement", "Scenario_ID"])
    ContentDataFrame = pd.DataFrame()
    RowDataFrame = pd.DataFrame()
    ContentRows = []
    ScenarioOutputList = []
    TempScenarioOutputList = []

    PageName = CitiTester.FindPage()

    while x <= testIterations:
        result = CitiTester.callEndpoint(url, data)
        text = result
        output = CitiTester.ParseJSON(result)
        TempScenarioOutputList = CitiTester.GetScenarioIDs(output, PageName)
        ScenarioOutputList.extend(TempScenarioOutputList)
        ContentIDList = CitiTester.GetContentIDs(output, PageName)


        temp = []

        count = 0
        y = 1
        cursor = 0
        for item in ContentIDList[0]:
            ContentTable.add_row(([item, y, ContentIDList[1][cursor]]))
            # RowDataFrame = pd.DataFrame({item, y})
            # ContentDataFrame.append(RowDataFrame)
            tempscenarioID = ContentIDList[1][cursor]
            temp.append(item)
            temp.append(y)
            temp.append(tempscenarioID)
            temp.append(count)
            ContentRows.append(temp)
            temp = []
            y += 1
            cursor += 1

        #ContentRows = [['A', '1'], ['B', '2']]
        ContentDataFrame = pd.DataFrame(ContentRows, columns = ['ContentID','Placement','Scenario_ID','Content_Counts'])

        x += 1
    CountsList = []
    pd.ContentDataFrameCounts = []

    #ContentDataFrameCounts = ContentDataFrame
    ContentDataFrame = pd.DataFrame(ContentRows, columns = ['ContentID', 'Placement','Scenario_ID','Content_Counts'])

    #ContentDataFrame.groupby(['ContentID','Placement','Scenario_ID'])['Content_Counts'].count()
    #ContentDataFrame['Content_Counts'] = ''
    #ContentDataFrame = ContentDataFrame.groupby(['ContentID', 'Placement'])['Content_Counts'].transform('count')
    ContentDataFrame.groupby(['ContentID', 'Placement', 'Scenario_ID'])['Content_Counts'].count()
    ContentDataFrameCounts = ContentDataFrame
    ListTest = ContentDataFrameCounts['Content_Counts'].tolist()

    CountsList = ContentDataFrame.groupby(['ContentID','Placement','Scenario_ID'])['Content_Counts'].transform('count')

    index = 0

    for value in CountsList:
        ContentDataFrameCounts.at[index, 'Content_Counts'] = value
        index += 1

    ContentDataFrameCounts = ContentDataFrameCounts.drop_duplicates(subset=None, keep="first", ignore_index=True)
    print(ContentDataFrameCounts)

    #removing print statements
    #print(ContentDataFrameCounts.loc[ContentDataFrameCounts['Content_Counts'] > 1])
    print(list(dict.fromkeys(ScenarioOutputList)))

    currentTime = datetime.datetime.now()
    currentTime = currentTime.strftime("%y%m%d%H%M%S")
    currentTime = str(currentTime)
    ScenarioID = ContentDataFrameCounts.loc[0][2]
    filename = 'C:\\temp\\Citi_Multi_Call_Tester_Output_' + ScenarioID + '_' + currentTime + '.csv'

    OutputData = url + '\r' + data + '\r'
    OutputData += ContentDataFrameCounts.to_csv(index=False, lineterminator='\r')

    file = open(filename, "w")
    file.write(OutputData)
    #writer.writerow()


    test2 = text
