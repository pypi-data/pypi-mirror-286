import json, requests, os
# import config
from .config import Config
from ntpath import join
from datetime import datetime

class Xray:
    def authentication() -> str:
        if os.getenv('JWT_TOKEN'):
            print("Autenticação via JWT TOKEN = ", os.getenv('JWT_TOKEN'))
            return 'Bearer ' + os.getenv('JWT_TOKEN')
        
        print("Token JWT não configurado, gerando outro...")
        XRAY_API = Config.xray_api()
        XRAY_CLIENT_ID = Config.xray_client_id()
        XRAY_CLIENT_SECRET = Config.xray_client_secret()

        json_data = json.dumps({'client_id': XRAY_CLIENT_ID, 'client_secret': XRAY_CLIENT_SECRET})
        resp = requests.post(f'{XRAY_API}/authenticate', data=json_data, headers={'Content-Type':'application/json'})
            
        if resp.status_code == 200:
            return 'Bearer ' + resp.json()
        else:
            print(resp.json())
            print("Authentication error: {}".format(resp.status_code))

    def createTestExecution():
        print("\n------------------------------------------------------------------------------")
        print("A função createTestExecution está sendo executada!")

        PROJECT_KEY = Config.project_key()
        XRAY_API = Config.xray_api()
        test_execution_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        json_data = f'''
            mutation {{
                createTestExecution(
                    testIssueIds: [],
                    testEnvironments: [],
                    jira: {{
                        fields: {{
                            summary: "QA Automation Execution | { test_execution_date }",
                            project: {{ key: "{ PROJECT_KEY }" }}
                        }}
                    }}
                ) {{
                    testExecution {{
                        issueId
                        jira(fields: ["key"])
                    }}
                    warnings
                    createdTestEnvironments
                }}
            }}
        '''

        resp = requests.post(
            f'{XRAY_API}/graphql',
            json={ 'query': json_data },
            headers={
                'Content-Type': 'application/json',
                'Authorization': Xray.authentication()
            },
        )

        result = json.dumps({
            'issueId': resp.json().get('data').get('createTestExecution').get('testExecution').get('issueId'),
            'key': resp.json().get('data').get('createTestExecution').get('testExecution').get('jira').get('key')
        })

        if resp.status_code == 200:
            if Config.debug():
                print(json.dumps(resp.json(), indent=4))
            print("------------------------------------------------------------------------------")
            return json.loads(result)
        else:
            print('Error create test execution: ' + resp.status_code)

    def getTest(testKey: str):
        print("\n------------------------------------------------------------------------------")
        print("A função getTest está sendo executada!")
        if Config.debug():
            print("A função recebeu testKey {}".format(testKey))

        XRAY_API = Config.xray_api()

        json_data = f'''
            {{
                getTests(
                    jql: "key = '{ testKey }'",
                    limit: 1
                ) {{
                    results {{
                        issueId
                    }}
                }}
            }}
        '''

        resp = requests.post(
            f'{XRAY_API}/graphql',
            json={
                'query': json_data
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': Xray.authentication()
            },
        )

        if resp.status_code == 200:
            if Config.debug():
                print(json.dumps(resp.json(), indent=4))
            print("------------------------------------------------------------------------------")
            return resp.json().get('data').get('getTests').get('results')[0].get('issueId')
        else:
            print('Error getting test ID: ' + resp.status_code)

    def getTestRun(testIssueId: str, testExecutionIssueId: str):
        print("\n------------------------------------------------------------------------------")
        print("A função getTestRun está sendo executada!")
        if Config.debug():
            print("A função recebeu testIssueId {} e testExecutionIssueId {}".format(testIssueId, testExecutionIssueId))

        XRAY_API = Config.xray_api()

        json_data = f'''
            {{
                getTestRun(
                    testIssueId: "{ testIssueId }",
                    testExecIssueId: "{ testExecutionIssueId }"
                ) {{
                    id
                }}
            }}
        '''

        resp = requests.post(
            f'{XRAY_API}/graphql',
            json={
                'query': json_data
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': Xray.authentication()
            },
        )

        if resp.status_code == 200:
            if Config.debug():
                print(json.dumps(resp.json(), indent=4))
            print("------------------------------------------------------------------------------")
            return resp.json().get('data').get('getTestRun').get('id')
        else:
            print('Error getting run ID: ' + resp.status_code)

    def createTestExecution():
        print("\n------------------------------------------------------------------------------")
        print("A função createTestExecution está sendo executada!")

        PROJECT_KEY = Config.project_key()
        XRAY_API = Config.xray_api()
        test_execution_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

        json_data = f'''
            mutation {{
                createTestExecution(
                    testIssueIds: [],
                    testEnvironments: [],
                    jira: {{
                        fields: {{
                            summary: "QA Automation Execution | { test_execution_date }",
                            project: {{ key: "{ PROJECT_KEY }" }}
                        }}
                    }}
                ) {{
                    testExecution {{
                        issueId
                        jira(fields: ["key"])
                    }}
                    warnings
                    createdTestEnvironments
                }}
            }}
        '''

        resp = requests.post(
            f'{XRAY_API}/graphql',
            json={
                'query': json_data
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': Xray.authentication()
            },
        )

        result = json.dumps({
            'issueId': resp.json().get('data').get('createTestExecution').get('testExecution').get('issueId'),
            'key': resp.json().get('data').get('createTestExecution').get('testExecution').get('jira').get('key')
        })

        if resp.status_code == 200:
            if Config.debug():
                print(json.dumps(resp.json(), indent=4))
            print("------------------------------------------------------------------------------")
            return json.loads(result)
        else:
            print('Error create test execution ' + resp.status_code)

    def addEvidenceToTestRun(id: int, filename: str, mimeType: str, data: str):
        print("\n------------------------------------------------------------------------------")
        print("A função addEvidenceToTestRun está sendo executada!")
        if Config.debug():
            print("A função recebeu id {}, filename {} e mimeType {}".format(id, filename, mimeType))

        XRAY_API = Config.xray_api()

        json_data = f'''
            mutation {{
                addEvidenceToTestRun(
                    id: "{ id }",
                    evidence: [
                        {{
                            filename: "{ filename }"
                            mimeType: "{ mimeType }"
                            data: "{ data }"
                        }}
                    ]
                ) {{
                    addedEvidence
                    warnings
                }}
            }}
        '''

        resp = requests.post(
            f'{XRAY_API}/graphql',
            json={
                'query': json_data
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': Xray.authentication()
            },
        )

        if resp.status_code != 200:
            print("Infelizmente ocorreu um erro no envio de evidência")
            print("Código de erro {}".format(resp.status_code))
            print("------------------------------------------------------------------------------")
        else:
            if Config.debug():
                print(json.dumps(resp.json(), indent=4))
            print("------------------------------------------------------------------------------")

    def getTestPlan(key: str):
        print("\n------------------------------------------------------------------------------")
        print("A função getTestPlan está sendo executada!")
        if Config.debug():
            print("A função recebeu key {}".format(key))

        XRAY_API = Config.xray_api()

        json_data = f'''
            {{
                getTestPlans(jql: "key = '{ key }'", limit: 1) {{
                    results {{
                        issueId
                    }}
                }}
            }}
        '''

        resp = requests.post(
            f'{XRAY_API}/graphql',
            json={
                'query': json_data
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': Xray.authentication()
            },
        )

        if resp.status_code != 200:
            print("Infelizmente ocorreu um erro ao obter o issueId do TestPlan")
            print("Código de erro {}".format(resp.status_code))
            print("------------------------------------------------------------------------------")
        else:
            if Config.debug():
                print(json.dumps(resp.json(), indent=4))
            print("------------------------------------------------------------------------------")
            return resp.json().get('data').get('getTestPlans').get('results')[0].get('issueId')
        
    def addTestExecutionsToTestPlan(issueId: str, testExecIssueId: str):
        print("\n------------------------------------------------------------------------------")
        print("A função addTestExecutionsToTestPlan está sendo executada!")
        if Config.debug():
            print("A função recebeu issueId {} e testExecIssueId {}".format(issueId, testExecIssueId))

        XRAY_API = Config.xray_api()

        json_data = f'''
            mutation {{
                addTestExecutionsToTestPlan(
                    issueId: "{ issueId }",
                    testExecIssueIds: ["{ testExecIssueId }"]
                ) {{
                    addedTestExecutions
                    warning
                }}
            }}
        '''

        resp = requests.post(
            f'{XRAY_API}/graphql',
            json={
                'query': json_data
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': Xray.authentication()
            },
        )

        if resp.status_code != 200:
            print("Infelizmente ocorreu um erro ao adicionar os resultados ao Plano de Teste")
            print("Código de erro {}".format(resp.status_code))
            print("------------------------------------------------------------------------------")
        else:
            if Config.debug():
                print(json.dumps(resp.json(), indent=4))
            print("------------------------------------------------------------------------------")
            return resp.json().get('data').get('getTestPlans').get('results')[0].get('issueId')

    def importExecutionCucumber(key: str = None):
        print("A importação dos resultados do testes estão a ser enviados.")
        print("Aguarde um momento...")
        print("------------------------------------------------------------------------------")
        print("A função importExecutionCucumber está sendo executada!")
        if Config.debug():
            print("A função recebeu key {}".format(key))

        PROJECT_KEY = Config.project_key()
        XRAY_API = Config.xray_api()

        resp = requests.post(f'{XRAY_API}/import/execution/cucumber', 
            data = open(Config.cucumber_path() + '/cucumber.json', 'rb'),
            params = { 
                'projectKey': PROJECT_KEY
            },
            headers = {
                'Content-Type': 'application/json',
                'Authorization': Xray.authentication()
            }
        )

        if key != None:
            issueId = Xray.getTestPlan(key)
            Xray.addTestExecutionsToTestPlan(str(issueId), str(resp.json().get('id')))
        
        if resp.status_code == 200:
            print("O arquivo '{}' foi gerado!".format(join(Config.cucumber_path(), 'cucumber.json')))
            if Config.debug():
                print(json.dumps(resp.json(), indent=4))
            splitInfo = resp.json().get('self').split('/')
            print("Resultados encontram-se em {}//{}/browse/{}".format(splitInfo[0], splitInfo[2], resp.json().get('key')))
            print("------------------------------------------------------------------------------")
            return resp.json().get('id')
        else:
            print("Infelizmente ocorreu um erro no envio dos resultados")
            print("Código de erro {}".format(resp.status_code))
            print(json.dumps(resp.json(), indent=4))
            print("------------------------------------------------------------------------------")