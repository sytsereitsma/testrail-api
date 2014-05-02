#
# TestRail API binding for Python (API v2, available since TestRail 3.0)
#
# Learn more:
#
# http://docs.gurock.com/testrail-api2/start
# http://docs.gurock.com/testrail-api2/accessing
#
# Copyright Gurock Software GmbH
#

import urllib2
import json
import base64

class APIError(Exception):
    pass

class APIClient:
    def __init__(self, base_url):
        self.user = ''
        self.password = ''
        if not base_url.endswith('/'):
            base_url += '/'
        self.__url = base_url + 'index.php?/api/v2/'

    #
    # Send Get
    #
    # Issues a GET request (read) against the API and returns the result
    # (as Python dict).
    #
    # Arguments:
    #
    # uri                 The API method to call including parameters
    #                     (e.g. get_case/1)
    #
    def send_get(self, uri):
        return self.__send_request('GET', uri, None)

    #
    # Send POST
    #
    # Issues a POST request (write) against the API and returns the result
    # (as Python dict).
    #
    # Arguments:
    #
    # uri                 The API method to call including parameters
    #                     (e.g. add_case/1)
    # data                The data to submit as part of the request (as
    #                     Python dict, strings must be UTF-8 encoded)
    #
    def send_post(self, uri, data):
        return self.__send_request('POST', uri, data)

    def __send_request(self, method, uri, data):
        url = self.__url + uri
        request = urllib2.Request(url)
        if method == 'POST':
            request.add_data(json.dumps(data))
        auth = base64.encodestring('%s:%s' % (self.user, self.password)).strip()
        request.add_header('Authorization', 'Basic %s' % auth)
        request.add_header('Content-Type', 'application/json')

        e = None
        try:
            response = urllib2.urlopen(request).read()
        except urllib2.HTTPError as e:
            response = e.read()

        if response:
            result = json.loads(response)
        else:
            result = {}

        if e is not None:
            if result and 'error' in result:
                error = '"' + result['error'] + '"'
            else:
                error = 'No additional error message received'
            raise APIError('TestRail API returned HTTP %s (%s)' % (e.code, error))

        return result

    def get_projects(self):
        response = self.send_get('get_projects')
        return map(lambda r: Project(self, r), response)

    def get_statuses(self):
        response = self.send_get('get_statuses')
        return map(lambda r: Status(self, r), response)


class _RecordBase(object):
    def __init__(self, client, data_dict):
        self._client = client
        try:
            self.__id = data_dict["id"]
        except KeyError as err:
            raise APIError("Failed to parse record data (%s)" % err)

    @property
    def id(self):
        return self.__id

    def _load_custom_data(self, data_dict):
        custom = {}
        for key in data_dict:
            if len(key) > 7 and key[:7] == "custom_":
                custom[key[7:]] = data_dict[key]

        return custom

class Project(_RecordBase):
    def __init__(self, client, data_dict):
        super(Project, self).__init__(client, data_dict)
        try:
            self.announcement = data_dict["announcement"]
            self.__completed_on = data_dict["completed_on"]
            self.is_completed = data_dict["is_completed"]
            self.show_announcement = data_dict["show_announcement"]
            self.name = data_dict["name"]
        except KeyError as err:
            raise APIError("Failed to parse project data (%s)" % err)

    @property
    def completed_on(self):
        return self.__completed_on

    def get_suites(self):
        response = self._client.send_get('get_suites/%d' % self.id)
        return map(lambda r: Suite(self._client, r), response)

    def get_runs(self):
        response = self._client.send_get('get_runs/%d' % self.id)
        return map(lambda r: Run(self._client, r), response)

class Suite(_RecordBase):
    def __init__(self, client, data_dict):
        super(Suite, self).__init__(client, data_dict)
        try:
            self.description = data_dict["description"]
            self.project_id = data_dict["project_id"]
            self.name = data_dict["name"]
        except KeyError as err:
            raise APIError("Failed to parse suite data (%s)" % err)

    def get_cases(self):
        response = self._client.send_get("get_cases/%d&suite_id=%d" % (self.project_id, self.id))
        return map(lambda r: Case(self._client, r), response)

class Case(_RecordBase):
    def __init__(self, client, data_dict):
        super(Case, self).__init__(client, data_dict)
        try:
            self.custom_steps = data_dict['custom_steps']
            self.updated_by = data_dict['updated_by']
            self.type_id = data_dict['type_id']
            self.estimate = data_dict['estimate']
            self.refs = data_dict['refs']
            self.priority_id = data_dict['priority_id']
            self.section_id = data_dict['section_id']
            self.created_by = data_dict['created_by']
            self.custom_preconds = data_dict['custom_preconds']
            self.created_on = data_dict['created_on']
            self.custom_expected = data_dict['custom_expected']
            self.suite_id = data_dict['suite_id']
            self.updated_on = data_dict['updated_on']
            self.title = data_dict['title']
            self.milestone_id = data_dict['milestone_id']
            self.estimate_forecast = data_dict['estimate_forecast']
        except KeyError as err:
            raise APIError("Failed to parse case data (%s)" % err)

class Run(_RecordBase):
    def __init__(self, client, data_dict):
        super(Run, self).__init__(client, data_dict)
        try:
            self.include_all = data_dict ["include_all"]
            self.is_completed = data_dict ["is_completed"]
            self.created_on = data_dict ["created_on"]
            self.retest_count = data_dict ["retest_count"]
            self.plan_id = data_dict ["plan_id"]
            self.created_by = data_dict ["created_by"]
            self.passed_count = data_dict ["passed_count"]
            self.project_id = data_dict ["project_id"]
            self.config = data_dict ["config"]
            self.failed_count = data_dict ["failed_count"]
            self.description = data_dict ["description"]
            self.suite_id = data_dict ["suite_id"]
            self.milestone_id = data_dict ["milestone_id"]
            self.name = data_dict ["name"]
            self.assignedto_id = data_dict ["assignedto_id"]
            self.blocked_count = data_dict ["blocked_count"]
            self.completed_on = data_dict ["completed_on"]
            self.config_ids = data_dict ["config_ids"]
            self.url = data_dict ["url"]
            self.untested_count = data_dict ["untested_count"]
        except KeyError as err:
            raise APIError("Failed to parse run data (%s)" % err)

        self.__custom = self._load_custom_data(data_dict)

    @property
    def custom(self):
        return self.__custom

    def get_tests(self):
        response = self._client.send_get("get_tests/%d" % (self.id))
        return map(lambda r: Test(self._client, r), response)

class Test(_RecordBase):
    def __init__(self, client, data_dict):
        super(Test, self).__init__(client, data_dict)
        try:
            self.assignedto_id = data_dict ["assignedto_id"]
            self.status_id = data_dict ["status_id"]
            self.priority_id = data_dict ["priority_id"]
            self.title = data_dict ["title"]
            self.refs = data_dict ["refs"]
            self.run_id = data_dict ["run_id"]
            self.case_id = data_dict ["case_id"]
            self.estimate_forecast = data_dict ["estimate_forecast"]
            self.type_id = data_dict ["type_id"]
            self.estimate = data_dict ["estimate"]
            self.milestone_id = data_dict ["milestone_id"]
        except KeyError as err:
            raise APIError("Failed to parse test data (%s)" % err)

        self.__custom = self._load_custom_data(data_dict)

    @property
    def custom(self):
        return self.__custom

    def get_case(self):
        response = self._client.send_get("get_case/%d" % (self.case_id))
        if(len(response) != 1):
            raise APIError("Invalid test case (test id %d, case id %d)" % (self.id, self.case_id))

        return Case(self._client, response[0])

class Status(_RecordBase):
    def __init__(self, client, data_dict):
        super(Status, self).__init__(client, data_dict)
        try:
            self.color_bright = data_dict["color_bright"]
            self.color_dark = data_dict["color_dark"]
            self.color_medium = data_dict["color_medium"]
            self.is_final = data_dict["is_final"]
            self.is_system = data_dict["is_system"]
            self.is_untested = data_dict["is_untested"]
            self.label = data_dict["label"]
            self.name = data_dict["name"]
        except KeyError as err:
            raise APIError("Failed to parse status data (%s)" % err)

class StatusMapper:
    def __init__(self, statuses):
        self.__statuses = statuses

    def __getitem__(self, key):
        for s in self.__statuses:
            if (s.id == key):
                return s

        raise APIError("Failed to map status ID %d" % key)
