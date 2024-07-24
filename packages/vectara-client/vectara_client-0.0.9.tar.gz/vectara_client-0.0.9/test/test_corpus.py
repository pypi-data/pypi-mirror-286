from vectara_client.core import Factory
from vectara_client.models import CreateCorpusRequest, StructuredDocument, CreateDocumentRequest
from vectara_client.documents import DocumentManager
from vectara_client.corpus import CorpusManager, CorpusBuilder
from time import sleep
from pathlib import Path
import logging
import unittest

class CorpusBuilderTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.basicConfig(format='%(asctime)s:%(name)-35s %(levelname)s:%(message)s', level=logging.INFO,
                            datefmt='%H:%M:%S %z')
        self.logger = logging.getLogger(self.__class__.__name__)

    def test_corpus_key(self):
        builder = CorpusBuilder("My Corpus  Yay")
        self.assertEqual(builder.build().key, "my-corpus-yay")


    def test_invalid_key(self):
        with self.assertRaises(ValueError) as context:
            CorpusBuilder("My Corpus Yay", "Non valid KEY^&")

        self.assertTrue(r"must validate the regular expression /[a-zA-Z0-9_\=\-]+$/" in context.exception.args[0])

        with self.assertRaises(ValueError) as context:
            builder = CorpusBuilder("My Corpus Yay")
            builder.key("Non valid KEY^&")

        self.assertTrue(r"must validate the regular expression /[a-zA-Z0-9_\=\-]+$/" in context.exception.args[0])

    def test_add_attribute(self):
        corpus = (CorpusBuilder("filter-attrs")
                  .add_attribute("first", "MyFirstAttr")
                  .add_attribute("second", type="boolean", indexed=False)
                  .add_attribute("third", document=False)
                  .build()
                  )
        # Test the first filter attribute
        first = corpus.filter_attributes[0]
        self.assertEqual(first.name, "first")
        self.assertEqual(first.description, "MyFirstAttr")
        self.assertTrue(first.indexed)
        self.assertEqual(first.type, "text")
        self.assertEqual(first.level, "document")

        # Test the second filter attribute
        second = corpus.filter_attributes[1]
        self.assertEqual(second.name, "second")
        self.assertIsNone(second.description)
        self.assertEqual(second.type, "boolean")
        self.assertFalse(second.indexed)

        # Test the third filter attribute
        third = corpus.filter_attributes[2]
        self.assertEqual(third.name, "third")
        self.assertEqual(third.level, "part")

    def test_add_attribute_invalid_type(self):
        with self.assertRaises(ValueError) as context:
            CorpusBuilder("filter-attrs").add_attribute("first", type="unknown")


        self.assertTrue("must be one of enum values ('integer', 'real_number', 'text', 'boolean', 'list[integer]', 'list[real_number]', 'list[text]')" in context.exception.args[0])

    def test_add_dimension(self):
        corpus = (CorpusBuilder("dimensions")
                  .add_dimension("my-dimension",
                                 0.1, 0.2)
                  .build())

        dimension = corpus.custom_dimensions[0]
        self.assertEqual(dimension.name, "my-dimension")
        self.assertEqual(dimension.indexing_default, 0.1)
        self.assertEqual(dimension.querying_default, 0.2)








class CorpusManagerTest(unittest.TestCase):

    CORPUS_NAME = "Test-DocumentManager"
    CORPUS_KEY = "test-doc-manager"
    DOCUMENT_ID = "HR Complaint Process"
    TEST_DOCUMENT = "resources/hr_complaints/complaints.json"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.basicConfig(format='%(asctime)s:%(name)-35s %(levelname)s:%(message)s', level=logging.INFO,
                            datefmt='%H:%M:%S %z')
        self.logger = logging.getLogger(self.__class__.__name__)

