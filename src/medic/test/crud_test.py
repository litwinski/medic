import unittest

from collections import defaultdict
from datetime import date
from io import StringIO
from tempfile import TemporaryFile

from medic.orm import Citation, Section, Author, Descriptor, Qualifier, Database, Identifier, \
        Chemical, Keyword, PublicationType, Abstract
from medic.crud import _dump

DATA = [
    Abstract(1, 'NLM', None),
    Section(1, 'NLM', 1, 'Abstract', 'The Abstract 1'),
    Section(1, 'NLM', 2, 'Abstract', 'The Abstract 2'),
    Descriptor(1, 1, 'd_name', True),
    Descriptor(1, 2, 'd_name'),
    Qualifier(1, 1, 1, 'q_name', True),
    Author(1, 1, 'first'),
    Author(1, 2, 'last'),
    Identifier(1, 'ns', 'id'),
    Database(1, 'name', 'accession'),
    PublicationType(1, 'some'),
    PublicationType(1, 'another'),
    Chemical(1, 1, 'name', 'uid'),
    Keyword(1, 'NOTNLM', 1, 'name', True),
    Citation(1, 'MEDLINE', 'title', 'journal', 'pub_date', date.today()),
]


class ParserMock:
    def __init__(self, instances):
        self.instances = instances

    def parse(self, _):
        for i in self.instances:
            yield i


class TestDump(unittest.TestCase):

    def setUp(self):
        self.out = {
            Citation.__tablename__: StringIO(),
            Abstract.__tablename__: StringIO(),
            Section.__tablename__: StringIO(),
            Descriptor.__tablename__: StringIO(),
            Qualifier.__tablename__: StringIO(),
            Author.__tablename__: StringIO(),
            Identifier.__tablename__: StringIO(),
            Database.__tablename__: StringIO(),
            PublicationType.__tablename__: StringIO(),
            Chemical.__tablename__: StringIO(),
            Keyword.__tablename__: StringIO(),
            'delete': StringIO(),
        }

    def testDumpCount(self):
        parser = ParserMock(DATA + DATA)
        self.assertEqual(2, _dump(TemporaryFile(), self.out, parser, False))

    def testDumping(self):
        parser = ParserMock(DATA)
        results = defaultdict(str)
        results['delete'] = "1\n".format(
            Citation.__tablename__
        )

        for i in DATA:
            results[i.__tablename__] += str(i)

        self.assertEqual(1, _dump(TemporaryFile(), self.out, parser, True))

        for tbl, buff in self.out.items():
            self.assertEqual(results[tbl], buff.getvalue())


if __name__ == '__main__':
    unittest.main()
