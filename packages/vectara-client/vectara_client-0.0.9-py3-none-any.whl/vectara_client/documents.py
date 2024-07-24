from vectara_client.api import QueriesApi, UploadApi, IndexApi, DocumentsApi
from vectara_client.models import (QueryCorpusRequest, SearchCorpusParameters, IndividualSearchResult,
                                   StructuredDocument, CoreDocument, CreateDocumentRequest)
from types import MappingProxyType
from typing import Union, Any
from pathlib import Path

import logging
import json


class DocumentManager:

    DEFAULT_METADATA: dict[str: Any] = MappingProxyType({})

    def __init__(self, queries_api: QueriesApi, upload_api: UploadApi, index_api: IndexApi,
                 documents_api: DocumentsApi):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.queries_api = queries_api
        self.upload_api = upload_api
        self.index_api = index_api
        self.documents_api = documents_api

    def get_document(self, corpus_key: str, document_id: str) -> IndividualSearchResult:
        self.logger.info(f"Retrieving document [{document_id}] from corpus [{corpus_key}]")
        search = SearchCorpusParameters(
            metadata_filter=f"(doc.id = '{document_id}')"
        )

        request = QueryCorpusRequest(
            query='',
            search=search,
            generation=None
        )

        response = self.queries_api.query_corpus(corpus_key=corpus_key, query_corpus_request=request)
        if response.search_results and len(response.search_results) > 0:
            self.logger.info(f"Returning document [{document_id}] from corpus [{corpus_key}]")
            return response.search_results[0]
        else:
            self.logger.info(f"Did not find document [{document_id}] in corpus [{corpus_key}]")

    def check_document_exists(self, corpus_key: str, document_id: str):
        self.logger.info(f"Checking if document [{document_id}] exists in corpus [{corpus_key}]")
        if self.get_document(corpus_key, document_id):
            self.logger.info(f"Document [{document_id}] exists in corpus [{corpus_key}]")
            return True
        else:
            self.logger.info(f"Document [{document_id}] does not exist in corpus [{corpus_key}]")
            return False

    def add_document(self, corpus_key: str, doc_path: Path = None, doc_json: str = None,
                     content: Union[StructuredDocument, CoreDocument, dict[str, Any]] = None,
                     encoding: str = "utf-8", metadata: dict[str, Any] = None,
                     check_exists:bool = True, overwrite: bool = True) -> bool:
        # First validate inputs.
        if doc_path:
            file_name = str(doc_path.resolve())

            if not doc_path.name.lower().endswith("json"):
                # Process as upload.
                doc_id = file_name

                if self.check_document_exists(corpus_key, doc_id):
                    self.logger.info("The document with id [" + doc_id + "] already exists")
                    if overwrite:
                        self.logger.info("Overwriting document, deleting old version")
                        self.documents_api.delete_corpus_document(corpus_key, doc_id)
                    else:
                        self.logger.info("Skipping this document as overwrite set to false")
                        return False


                self.logger.info(f"We will ingest [{file_name}] as a binary type")

                if metadata:
                    self.upload_api.upload_file(corpus_key, file_name, metadata=metadata)
                else:
                    self.upload_api.upload_file(corpus_key, file_name, metadata)
                return True
            else:
                self.logger.info(f"Loading document to index from path [{file_name}]")
                with open(doc_path, "r", encoding=encoding) as r:
                    doc_json = r.read()

        if doc_json:
            content = json.loads(doc_json)

        parsed_content: Union[StructuredDocument, CoreDocument]

        if content:
            if isinstance(content, dict):
                self.logger.debug("Parsing content from dict")
                doc_type = content["type"]

                if not doc_type:
                    raise Exception("For API v2, you must provide a type attribute (core or structured).")
                if doc_type == "structured":
                    self.logger.debug("Found doc type of `structured`")
                    parsed_content = StructuredDocument.from_json(doc_json)
                elif doc_type == "core":
                    self.logger.debug("Found doc type of `core`")
                    parsed_content = CoreDocument.from_json(doc_json)
                else:
                    raise Exception(f"Unknown doc type [{doc_type}] for API v2 Index, you must provide a type attribute (`core` or `structured`).")
            else:
                parsed_content = content
        else:
            raise Exception("You must specify either `doc_path`, `doc_json` or `content` parameters.")

        self.logger.info(f"Creating new document with id [{parsed_content.id}]")
        self.index_api.create_corpus_document(corpus_key, CreateDocumentRequest(parsed_content))