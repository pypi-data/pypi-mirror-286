import json
# import attributes, config, report, xray
from .attributes import *
from .config import Config
from .report import Report
from .xray import Xray

class ListenerV2:
    """Optional base class for listeners using the listener API version 2."""
    ROBOT_LISTENER_API_VERSION = 2
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self
        self.report = []
        self.suite_index = 0
        self.test_index = 0
        self.keyword_index = 0
        self.is_template = False
        # self.recorder = pyscreenrec.ScreenRecorder()

    def start_suite(self, name: str, attributes: StartSuiteAttributes):
        """Called when a suite starts."""
        if Config.debug():
            print("start_suite")
            print(json.dumps(attributes, indent=4))

        self._start_suite(attributes)

    def end_suite(self, name: str, attributes: EndSuiteAttributes):
        """Called when a suite end."""
        if Config.debug():
            print("\nend_suite")
            print(json.dumps(attributes, indent=4))

        self._end_suite(attributes)

        self.suite_index += 1
        self.test_index = 0
        self.keyword_index = 0

    def start_test(self, name: str, attributes: StartTestAttributes):
        """Called when a test or task starts."""
        if Config.debug():
            print("start_test")
            print(json.dumps(attributes, indent=4))

        self._start_test(attributes)
        self._set_xray_test(attributes)
        
        # self.recorder.start_recording("{}.mp4".format(attributes.get('id')), 10)

    def end_test(self, name: str, attributes: EndTestAttributes):
        """Called when a test or task ends."""
        if Config.debug():
            print("end_test")
            print(json.dumps(attributes, indent=4))

        self._end_test(attributes)

        # self.recorder.stop_recording()

        # recording = "{}.mp4".format(attributes.get('id'))
        # with open(recording, 'rb') as video_file:
        #     test['video'] = base64.b64encode(video_file.read()).decode('utf-8')

        # if os.path.isfile(recording):
        #     os.remove(recording)
        
        self.test_index += 1
        self.keyword_index = 0

    def start_keyword(self, name: str, attributes: StartKeywordAttributes):
        """Called when a keyword or a control structure like IF starts.

        The type of the started item is in ``attributes['type']``. Control
        structures can contain extra attributes that are only relevant to them.
        """
        if Config.debug():
            print("start_keyword")
            print(json.dumps(attributes, indent=4))

        self._start_keyword(attributes)

    def end_keyword(self, name: str, attributes: EndKeywordAttributes):
        """Called when a keyword or a control structure like IF ends.

        The type of the started item is in ``attributes['type']``. Control
        structures can contain extra attributes that are only relevant to them.
        """
        if Config.debug():
            print("end_keyword")
            print(json.dumps(attributes, indent=4))
            
        self._end_keyword(attributes)

        self.keyword_index = self.keyword_index + 1

    def log_message(self, message: MessageAttributes):
        """Called when a normal log message are emitted.

        The messages are typically logged by keywords, but also the framework
        itself logs some messages. These messages end up to output.xml and
        log.html.
        """
        if Config.debug():
            print("log_message")
            print(json.dumps(message, indent=4))

        self._log_message(message)

        # AJUSTAR
        # if message['message'].__contains__('<img'):
        #     soup = BeautifulSoup(message['message'], 'html.parser')
        #     image_src = soup.img.get('src')

        #     if not image_src.__contains__('data:image/png;base64,'):
        #         with open(join(BuiltIn().get_variable_value('${OUTPUT_DIR}'), image_src), 'rb') as img_file:
        #             b64_string = base64.b64encode(img_file.read())
        #             keyword = self.report[self.suite_index]['tests'][self.test_index]['keywords'][self.keyword_index]
        #             keyword['evidence'] = '{}'.format(b64_string.decode('utf-8'))
        #     else:
        #         keyword = self.report[self.suite_index]['tests'][self.test_index]['keywords'][self.keyword_index]
        #         keyword['evidence'] = image_src.replace('data:image/png;base64,', '')

    def message(self, message: MessageAttributes):
        """Called when framework's internal messages are emitted.

        Only logged by the framework itself. These messages end up to the syslog
        if it is enabled.
        """
        if Config.debug():
            print("message")
            print(json.dumps(message, indent=4))

    def library_import(self, name: str, attributes: LibraryAttributes):
        """Called after a library has been imported."""
        if Config.debug():
            print("library_import")
            print(json.dumps(attributes, indent=4))

    def resource_import(self, name: str, attributes: ResourceAttributes):
        """Called after a resource file has been imported."""
        if Config.debug():
            print("resource_import")
            print(json.dumps(attributes, indent=4))

    def variables_import(self, name: str, attributes: VariablesAttributes):
        """Called after a variable file has been imported."""
        if Config.debug():
            print("variables_import")
            print(json.dumps(attributes, indent=4))

    def output_file(self, path: str):
        """Called after the output file has been created.

        At this point the file is guaranteed to be closed.
        """

    def log_file(self, path: str):
        """Called after the log file has been created."""

    def report_file(self, path: str):
        """Called after the report file has been created."""

    def xunit_file(self, path: str):
        """Called after the xunit compatible output file has been created."""

    def debug_file(self, path: str):
        """Called after the debug file has been created."""

    def close(self):
        """Called when the whole execution ends.

        With library listeners called when the library goes out of scope.
        """
        Report.cucumber(self.report)
        Xray.importExecutionCucumber()
        # self._send_evidence(self.report, testExecutionId)

    def _send_evidence(self, report, testExecutionId):
        for suite in report:
            for test in suite['tests']:
                id = Xray.getTestRun(test['issueId'], testExecutionId)
                Xray.addEvidenceToTestRun(id, 'Evidence_{}.mp4'.format(test['xraytest']), "video/mp4", test['video'])
                print('- {}, evidence submitted successfully!'.format(test['originalname']))

    def _start_suite(self, attributes: StartSuiteAttributes):
        self.report.append({
            "id": attributes.get('id'),
            "doc": attributes.get('doc') + ' Test Suite.',
            "metadata": attributes.get('metadata'),
            "starttime": attributes.get('starttime'),
            "longname": attributes.get('longname'),
            "tests": [],
            "suites": attributes.get('suites'),
            "totaltests": attributes.get('totaltests'),
            "source": attributes.get('source'),
        })

    def _end_suite(self, attributes: EndSuiteAttributes):
        suite = self.report[self.suite_index]
        suite['endtime'] = attributes.get('endtime')
        suite['elapsedtime'] = attributes.get('elapsedtime')
        suite['status'] = attributes.get('status')
        suite['message'] = attributes.get('message')
        suite['statistics'] = attributes.get('statistics')

    def _start_test(self, attributes: StartTestAttributes):
        self.report[self.suite_index]['tests'].append({
            "id": attributes.get('id'),
            "doc": attributes.get('doc'),
            "tags": attributes.get('tags'),
            "lineno": attributes.get('lineno'),
            "starttime": attributes.get('starttime'),
            "longname": attributes.get('longname'),
            "source": attributes.get('source'),
            "template": attributes.get('template'),
            "originalname": attributes.get('originalname'),
            "endtime": '',
            "elapsedtime": 0,
            "status": 'NOT SET',
            "message": '',
            "xraytest": '',
            "issueId": '',
            "video": '',
            "keywords": [],
        })

    def _set_xray_test(self, attributes: StartTestAttributes):
        for tag in attributes.get('tags'):
            if Config.project_key() in tag:
                test = self.report[self.suite_index]['tests'][self.test_index]
                test['xraytest'] = Xray.getTest(tag)
    
    def _end_test(self, attributes: EndTestAttributes):
        test = self.report[self.suite_index]['tests'][self.test_index]
        test['endtime'] = attributes.get('endtime')
        test['elapsedtime'] = attributes.get('elapsedtime')
        test['status'] = attributes.get('status')
        test['message'] = attributes.get('message')

    def _start_keyword(self, attributes: StartKeywordAttributes):
        keyword = self.report[self.suite_index]['tests'][self.test_index]
        keyword['keywords'].append({
            "doc": attributes.get('doc'),
            "lineno": attributes.get('lineno'),
            "type": attributes.get('type'),
            "status": attributes.get('status'),
            "starttime": attributes.get('starttime'),
            "source": attributes.get('source'),
            "kwname": attributes.get('kwname'),
            "libname": attributes.get('libname'),
            "args": attributes.get('args'),
            "assign": attributes.get('assign'),
            "tags": attributes.get('tags'),
            "messages": [],
            "endtime": '',
            "elapsedtime": 0,
        })

    def _end_keyword(self, attributes: EndKeywordAttributes):
        keyword = self.report[self.suite_index]['tests'][self.test_index]['keywords'][self.keyword_index]
        keyword['status'] = attributes.get('status')
        keyword['endtime'] = attributes.get('endtime')
        keyword['elapsedtime'] = attributes.get('elapsedtime')

    def _log_message(self, message: MessageAttributes):
        msg = self.report[self.suite_index]['tests'][self.test_index]['keywords'][self.keyword_index]
        msg['messages'].append({
            "timestamp": message.get('timestamp'),
            "message": message.get('message'),
            "level": message.get('level'),
            "html": message.get('html'),
        })

# if __name__ == '__main__':
#     if __package__ is None:
#         import sys
#         from os import path
#         sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
#         import ListenerV2
#     else:
#         from .ListenerV2 import ListenerV2