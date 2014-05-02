import testrail

if __name__ == "__main__":
    client = testrail.APIClient('http://myserver/testrail/')
    client.user = "chuck"
    client.password = "norris"

    status_mapper = testrail.StatusMapper(client.get_statuses())

    projects = client.get_projects()
    for p in projects:
        print(p.name)
        suites = p.get_suites()
        for s in suites:
            print("    [S] " + s.name)
            cases = s.get_cases()
            for c in cases:
                print("        [C] " + c.title)

        runs = p.get_runs()
        for r in runs:
            print("    [R] " + r.name)
            tests = r.get_tests()
            for t in tests:
                print("        [T] %s - > %s" % (t.title, status_mapper[t.status_id].name))
