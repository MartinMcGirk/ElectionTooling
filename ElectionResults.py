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
    _results = []

    def __init__(self):
        self.load_results()

    def load_results(self):
        with open('Data/2015Results.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                result = map_uk_result_to_election_result(ElectionResult(), row)
                self._results.append(result)

    def by_constituency(self, constituency):
        return [r for r in self._results if r.constituency_name == constituency]

    def by_country(self, country):
        return [r for r in self._results if r.country == country]

    def get_winner(self, results):
        return max(results, key=attrgetter('votes'))

    def get_winner_for(self, constituency):
        self.get_winner(self.by_constituency(constituency)).printResult()

    def get_results_for(self, constituency):
        for r in self.by_constituency(constituency):
            r.printResult()