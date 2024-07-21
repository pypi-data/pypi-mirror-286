import logging

from ..conf import METADATA_ATTRS, PAGINATION_ATTRS

logger = logging.getLogger(__name__)


class SugarSpiderParserError(Exception):
    pass


def google_search_parser(page: dict):
    metadata = {k: page.get(k) for k in METADATA_ATTRS}

    records = list()
    for results_type, contents in page.items():
        try:
            if results_type in [*METADATA_ATTRS, *PAGINATION_ATTRS]:
                continue
            if not isinstance(contents, list):
                records.append({"key": results_type, "value": {**metadata, results_type: contents}})
                continue
            for item in contents:
                records.append({"key": results_type, "value": {**metadata, results_type: item}})
        except Exception as ex:
            logger.warning()
            SugarSpiderParserError(ex)

    return records
