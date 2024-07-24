from vectara_client.core import Factory
from vectara_client.models import CreateCorpusRequest, StructuredDocument, CreateDocumentRequest
from vectara_client.documents import DocumentManager
from vectara_client.corpus import CorpusManager, CorpusBuilder
from time import sleep
from pathlib import Path
import logging
import unittest

class DocumentManagerTest(unittest.TestCase):

    CORPUS_NAME = "Test-DocumentManager"
    CORPUS_KEY = "test-doc-manager"
    DOCUMENT_ID = "HR Complaint Process"
    TEST_DOCUMENT = "resources/hr_complaints/complaints.json"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.basicConfig(format='%(asctime)s:%(name)-35s %(levelname)s:%(message)s', level=logging.INFO,
                            datefmt='%H:%M:%S %z')
        self.logger = logging.getLogger(self.__class__.__name__)

    def test_check_document_exists(self):
        client = Factory().build()
        corpus_manager = client.corpus_manager

        self.logger.info("Checking if we need to setup our corpus")

        corpus = corpus_manager.find_corpus_by_name(self.CORPUS_NAME, fail_if_not_exist=False)
        if corpus:
            corpus_key = corpus.key
            self.logger.info(f"Existing corpus found with key [{corpus_key}]")
        else:
            self.logger.info(f"Creating new corpus with key [{self.CORPUS_KEY}]")

            corpus_manager.builder()

            request: CreateCorpusRequest = CreateCorpusRequest.from_dict({
                "name": self.CORPUS_NAME,
                "key": self.CORPUS_KEY
            })
            corpus = corpus_manager.create_corpus(request)
            corpus_key = corpus.key
            self.logger.info(f"New corpus created with id [{corpus.id}]")

        # Delete All in Corpus
        docs_response = client.documents_api.list_corpus_documents(corpus_key)
        if docs_response and docs_response.documents:
            for doc in docs_response.documents:
                self.logger.info(f"Deleting document [{doc.id}]")
                client.documents_api.delete_corpus_document(corpus_key, doc.id)

        # Sleep to ensure it's been deleted.
        sleep(5)

        # First run the negative.
        document_manager = client.document_manager
        self.assertFalse(document_manager.check_document_exists(corpus_key, self.DOCUMENT_ID))

        path = Path(self.TEST_DOCUMENT)
        result = document_manager.add_document(corpus_key, doc_path=path)

        self.logger.info(f"Waiting 5 seconds after upload")

        # Sleep to give time for eventual consistency to ingest document.
        sleep(5)

        self.assertTrue(document_manager.check_document_exists(corpus_key, self.DOCUMENT_ID))

        self.logger.info(f"Deleting test document [{self.DOCUMENT_ID}], waiting 5 seconds")
        client.documents_api.delete_corpus_document(corpus_key, self.DOCUMENT_ID)
        # Sleep to ensure it's been deleted.
        sleep(5)

        self.assertFalse(document_manager.check_document_exists(corpus_key, self.DOCUMENT_ID))












if __name__ == '__main__':
    unittest.main()
