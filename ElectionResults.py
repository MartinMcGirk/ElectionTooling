import csv
from operator import attrgetter


class ElectionResult:
    """Generic Election Result class to hold information about an election result"""
    def printResult(self):
        print(self.forename, self.surname, "(" + self.party + ")", ":", self.votes)


def map_uk_result_to_election_result(result_object, props):
    """Mapping function so that I can decouple the ElectionResult class from the column names on the csv"""
    result_object.forename = props['Forename']
    result_object.surname = props['Surname']
    result_object.constituency_name = props['Constituency Name']
    result_object.votes = int(props['Votes'])
    result_object.percentage_share = props['Share (%)']
    result_object.change = props['Change']
    result_object.county = props['County']
    result_object.region = props['Region']
    result_object.country = props['Country']
    result_object.party = props['Party abbreviation']
    return result_object


class ResultsViewer:
    """Class to query the election results that we've accumulated."""
    def __init__(self):
        self.load_results()

    def load_results(self):
        self._results = []
        with open('Data/2015Results.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                result = map_uk_result_to_election_result(ElectionResult(), row)
                self._results.append(result)

    def query(self, seq, f):
        """Filters a sequence seq based on the result of function f"""
        return [r for r in seq if f(r)]

    def by_constituency(self, seq, constituency):
        return self.query(seq, lambda x: x.constituency_name == constituency)

    def by_country(self, seq, country):
        return self.query(seq, lambda x: x.country == country)

    def get_max(self, seq, attr):
        return max(seq, key=attrgetter(attr))

    def get_winner_for(self, constituency):
        self.get_max(self.by_constituency(constituency), "votes").printResult()

    def get_results_for(self, constituency):
        for r in self.query(self._results, lambda x: x.constituency_name == constituency):
            r.printResult()