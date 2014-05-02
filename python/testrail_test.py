import unittest
import mock
import testrail
import time


def _dummy_project(name, record_id):
    return {
        u'announcement': "hello",
        u'completed_on': int(time.time()),
        u'url': u'fake_url',
        u'is_completed': False,
        u'show_announcement': True,
        u'id': record_id,
        u'name': unicode(name, 'unicode-escape')
    }


def _dummy_suite(name, record_id):
    return {
        u'url': u'fake_url',
        u'description': "Blah",
        u'project_id': 123,
        u'id': record_id,
        u'name': name
    }


def _dummy_case(record_id):
    return {
        u'custom_steps': None,
        u'updated_by': 6,
        u'type_id': 6,
        u'estimate': None,
        u'refs': None,
        u'priority_id': 4,
        u'section_id': 2,
        u'created_by': 6,
        u'custom_preconds': None,
        u'created_on': 1399023029,
        u'custom_expected': None,
        u'suite_id': 3,
        u'updated_on': 1399023029,
        u'title': u'Potmeter position input',
        u'milestone_id': None,
        u'id': record_id,
        u'estimate_forecast': None
    }


def _dummy_run(record_id):
    return {
        u'include_all': False,
        u'is_completed': False,
        u'created_on': 1399024614,
        u'retest_count': 0,
        u'id': record_id,
        u'plan_id': None,
        u'created_by': 6,
        u'passed_count': 0,
        u'project_id': 2,
        u'config': None,
        u'failed_count': 0,
        u'description': None,
        u'suite_id': 3,
        u'milestone_id': None,
        u'name': u'Automated nighly run',
        u'assignedto_id': None,
        u'blocked_count': 0,
        u'completed_on': None,
        u'config_ids': [],
        u'url': u'fake_url',
        u'untested_count': 1,
        u'custom_status1_count': 0,
        u'custom_status7_count': 0
    }


def _dummy_test(record_id):
    return {
        u'assignedto_id': None,
        u'status_id': 3,
        u'priority_id': 4,
        u'title': u'Force A input',
        u'refs': None,
        u'run_id': 2,
        u'custom_steps': None,
        u'custom_preconds': None,
        u'case_id': 3,
        u'estimate_forecast': None,
        u'type_id': 6,
        u'estimate': None,
        u'milestone_id': None,
        u'id': record_id
    }


def _dummy_status(record_id):
    return {
        "color_bright": 12709313,
        "color_dark": 6667107,
        "color_medium": 9820525,
        "id": record_id,
        "is_final": True,
        "is_system": True,
        "is_untested": False,
        "label": "Passed",
        "name": "passed"
    }


class TestRailTestCase(unittest.TestCase):
    def test_get_projects_request(self):
        client = testrail.APIClient("server_url")
        client.send_get = mock.Mock(return_value=[])
        client.get_projects()

        client.send_get.assert_called_once_with("get_projects")

    def test_get_projects(self):
        response = [
            _dummy_project("project 1", 1),
            _dummy_project("project 2", 2)
        ]
        client = testrail.APIClient("")
        client.send_get = mock.Mock(return_value=response)

        projects = client.get_projects()
        self.assertEqual(2, len(projects))
        self.assertEqual(1, projects[0].id)
        self.assertEqual(2, projects[1].id)

    def test_get_statuses_request(self):
        client = testrail.APIClient("server_url")
        client.send_get = mock.Mock(return_value=[])
        client.get_statuses()

        client.send_get.assert_called_once_with("get_statuses")

    def test_get_statuses(self):
        response = [
            _dummy_status(1),
            _dummy_status(3)
        ]
        client = testrail.APIClient("")
        client.send_get = mock.Mock(return_value=response)

        statuses = client.get_statuses()
        self.assertEqual(2, len(statuses))
        self.assertEqual(1, statuses[0].id)
        self.assertEqual(3, statuses[1].id)


class ProjectTestCase(unittest.TestCase):
    def setUp(self):
        self.__client = mock.Mock()
        self.__dict_data = _dummy_project("test project", 3)

    def test_incomplete_json_raises_exception(self):
        self.assertRaises(testrail.APIError, testrail.Project, self.__client, {})

    def test_parse_data(self):
        project = testrail.Project(self.__client, self.__dict_data)
        self.assertEqual(3, project.id)
        self.assertEqual("test project", project.name)
        self.assertEqual("hello", project.announcement)
        self.assertEqual(self.__dict_data["completed_on"], project.completed_on)
        self.assertFalse(project.is_completed)
        self.assertTrue(project.show_announcement)

    def test_get_suites_request(self):
        self.__client.send_get = mock.Mock(return_value=[])
        project = testrail.Project(self.__client, self.__dict_data)

        project.get_suites()
        self.__client.send_get.assert_called_once_with("get_suites/3")

    def test_get_suites(self):
        response = [
            _dummy_suite("suite 1", 3),
            _dummy_suite("suite 2", 4)
        ]

        self.__client.send_get = mock.Mock(return_value=response)

        project = testrail.Project(self.__client, self.__dict_data)
        suites = project.get_suites()
        self.assertEqual(2, len(suites))
        self.assertEqual(3, suites[0].id)
        self.assertEqual(4, suites[1].id)

    def test_get_runs_request(self):
        response = [
            _dummy_run(3),
            _dummy_run(4)
        ]
        self.__client.send_get = mock.Mock(return_value=response)

        project = testrail.Project(self.__client, self.__dict_data)
        runs = project.get_runs()
        self.assertEqual(2, len(runs))
        self.assertEqual(3, runs[0].id)
        self.assertEqual(4, runs[1].id)


class SuiteTestCase(unittest.TestCase):
    def setUp(self):
        self.__client = mock.Mock()
        self.__dict_data = _dummy_suite("Sweet", 3)

    def test_incomplete_json_raises_exception(self):
        self.assertRaises(testrail.APIError, testrail.Suite, self.__client, {})

    def test_parse_data(self):
        suite = testrail.Suite(self.__client, self.__dict_data)
        self.assertEqual(self.__dict_data["id"], suite.id)
        self.assertEqual(self.__dict_data["name"], suite.name)
        self.assertEqual(self.__dict_data["description"], suite.description)
        self.assertEqual(self.__dict_data["project_id"], suite.project_id)

    def test_get_cases_request(self):
        self.__client.send_get = mock.Mock(return_value=[])
        suite = testrail.Suite(self.__client, self.__dict_data)

        suite.get_cases()
        self.__client.send_get.assert_called_once_with("get_cases/123&suite_id=3")

    def test_get_cases(self):
        response = [
            _dummy_case(5),
            _dummy_case(6)
        ]
        self.__client.send_get = mock.Mock(return_value=response)

        suite = testrail.Suite(self.__client, self.__dict_data)
        cases = suite.get_cases()
        self.assertEqual(2, len(cases))
        self.assertEqual(5, cases[0].id)
        self.assertEqual(6, cases[1].id)


class CaseTestCase(unittest.TestCase):
    def setUp(self):
        self.__client = mock.Mock()
        self.__dict_data = _dummy_case(3)

    def test_incomplete_json_raises_exception(self):
        self.assertRaises(testrail.APIError, testrail.Case, self.__client, {})

    def test_parse_data(self):
        case = testrail.Case(self.__client, self.__dict_data)
        self.assertEqual(self.__dict_data["id"], case.id)
        self.assertEqual(self.__dict_data["custom_steps"], case.custom_steps)
        self.assertEqual(self.__dict_data["updated_by"], case.updated_by)
        self.assertEqual(self.__dict_data["type_id"], case.type_id)
        self.assertEqual(self.__dict_data["estimate"], case.estimate)
        self.assertEqual(self.__dict_data["refs"], case.refs)
        self.assertEqual(self.__dict_data["priority_id"], case.priority_id)
        self.assertEqual(self.__dict_data["section_id"], case.section_id)
        self.assertEqual(self.__dict_data["created_by"], case.created_by)
        self.assertEqual(self.__dict_data["custom_preconds"], case.custom_preconds)
        self.assertEqual(self.__dict_data["created_on"], case.created_on)
        self.assertEqual(self.__dict_data["custom_expected"], case.custom_expected)
        self.assertEqual(self.__dict_data["suite_id"], case.suite_id)
        self.assertEqual(self.__dict_data["updated_on"], case.updated_on)
        self.assertEqual(self.__dict_data["title"], case.title)
        self.assertEqual(self.__dict_data["milestone_id"], case.milestone_id)
        self.assertEqual(self.__dict_data["estimate_forecast"], case.estimate_forecast)


class RunTestCase(unittest.TestCase):
    def setUp(self):
        self.__client = mock.Mock()
        self.__dict_data = _dummy_run(5)

    def test_incomplete_json_raises_exception(self):
        self.assertRaises(testrail.APIError, testrail.Run, self.__client, {})

    def test_parse_data(self):
        run = testrail.Run(self.__client, self.__dict_data)
        self.assertEqual(self.__dict_data["include_all"], run.include_all)
        self.assertEqual(self.__dict_data["is_completed"], run.is_completed)
        self.assertEqual(self.__dict_data["created_on"], run.created_on)
        self.assertEqual(self.__dict_data["retest_count"], run.retest_count)
        self.assertEqual(self.__dict_data["id"], run.id)
        self.assertEqual(self.__dict_data["plan_id"], run.plan_id)
        self.assertEqual(self.__dict_data["created_by"], run.created_by)
        self.assertEqual(self.__dict_data["passed_count"], run.passed_count)
        self.assertEqual(self.__dict_data["project_id"], run.project_id)
        self.assertEqual(self.__dict_data["config"], run.config)
        self.assertEqual(self.__dict_data["failed_count"], run.failed_count)
        self.assertEqual(self.__dict_data["description"], run.description)
        self.assertEqual(self.__dict_data["milestone_id"], run.milestone_id)
        self.assertEqual(self.__dict_data["name"], run.name)
        self.assertEqual(self.__dict_data["assignedto_id"], run.assignedto_id)
        self.assertEqual(self.__dict_data["blocked_count"], run.blocked_count)
        self.assertEqual(self.__dict_data["completed_on"], run.completed_on)
        self.assertEqual(self.__dict_data["config_ids"], run.config_ids)
        self.assertEqual(self.__dict_data["url"], run.url)
        self.assertEqual(self.__dict_data["untested_count"], run.untested_count)

    def test_parse_custom_data(self):
        run = testrail.Run(self.__client, self.__dict_data)
        assert "status1_count" in run.custom
        assert "status7_count" in run.custom

    def test_get_tests_request(self):
        self.__client.send_get = mock.Mock(return_value=[])

        run = testrail.Run(self.__client, self.__dict_data)
        run.get_tests()
        self.__client.send_get.assert_called_once_with("get_tests/5")

    def test_get_tests(self):
        response = [
            _dummy_test(7),
            _dummy_test(8)
        ]
        self.__client.send_get = mock.Mock(return_value=response)

        run = testrail.Run(self.__client, self.__dict_data)
        tests = run.get_tests()
        self.assertEqual(2, len(tests))
        self.assertEqual(7, tests[0].id)
        self.assertEqual(8, tests[1].id)


class TestTestCase(unittest.TestCase):
    def setUp(self):
        self.__client = mock.Mock()
        self.__dict_data = _dummy_test(5)

    def test_incomplete_json_raises_exception(self):
        self.assertRaises(testrail.APIError, testrail.Run, self.__client, {})

    def test_parse_data(self):
        test = testrail.Test(self.__client, self.__dict_data)
        self.assertEqual(self.__dict_data["assignedto_id"], test.assignedto_id)
        self.assertEqual(self.__dict_data["status_id"], test.status_id)
        self.assertEqual(self.__dict_data["priority_id"], test.priority_id)
        self.assertEqual(self.__dict_data["title"], test.title)
        self.assertEqual(self.__dict_data["refs"], test.refs)
        self.assertEqual(self.__dict_data["run_id"], test.run_id)
        self.assertEqual(self.__dict_data["case_id"], test.case_id)
        self.assertEqual(self.__dict_data["estimate_forecast"], test.estimate_forecast)
        self.assertEqual(self.__dict_data["type_id"], test.type_id)
        self.assertEqual(self.__dict_data["estimate"], test.estimate)
        self.assertEqual(self.__dict_data["milestone_id"], test.milestone_id)
        self.assertEqual(self.__dict_data["id"], test.id)

    def test_parse_custom_data(self):
        test = testrail.Test(self.__client, self.__dict_data)
        assert "steps" in test.custom
        assert "preconds" in test.custom

    def test_get_case(self):
        response = [
            _dummy_case(7)
        ]
        self.__client.send_get = mock.Mock(return_value=response)

        test = testrail.Test(self.__client, self.__dict_data)
        case = test.get_case()
        self.assertEqual(7, case.id)

    def test_get_case_raises_apierror_on_failure(self):
        self.__client.send_get = mock.Mock(return_value=[])
        test = testrail.Test(self.__client, self.__dict_data)
        self.assertRaises(testrail.APIError, test.get_case)


class StatusTestCase(unittest.TestCase):
    def setUp(self):
        self.__client = mock.Mock()
        self.__dict_data = _dummy_status(5)

    def test_incomplete_json_raises_exception(self):
        self.assertRaises(testrail.APIError, testrail.Run, self.__client, {})

    def test_parse_data(self):
        status = testrail.Status(self.__client, self.__dict_data)
        self.assertEqual(self.__dict_data["color_bright"], status.color_bright)
        self.assertEqual(self.__dict_data["color_dark"], status.color_dark)
        self.assertEqual(self.__dict_data["color_medium"], status.color_medium)
        self.assertEqual(self.__dict_data["id"], status.id)
        self.assertEqual(self.__dict_data["is_final"], status.is_final)
        self.assertEqual(self.__dict_data["is_system"], status.is_system)
        self.assertEqual(self.__dict_data["is_untested"], status.is_untested)
        self.assertEqual(self.__dict_data["label"], status.label)
        self.assertEqual(self.__dict_data["name"], status.name)

class StatusMapperTestCase(unittest.TestCase):
    def setUp(self):
        self.__client = mock.Mock()
        self.__statuses = [
            testrail.Status (self.__client, _dummy_status(5)),
            testrail.Status (self.__client, _dummy_status(6)),
        ]

    def test_mapping(self):
        mapper = testrail.StatusMapper(self.__statuses)
        self.assertEqual(self.__statuses[0], mapper[5])
        self.assertEqual(self.__statuses[1], mapper[6])

    def test_mapping_raises_apierror_on_failure(self):
        mapper = testrail.StatusMapper(self.__statuses)
        with self.assertRaises(testrail.APIError):
            mapper[3]

if __name__ == '__main__':
    unittest.main()
