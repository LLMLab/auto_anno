# import os
# import sys
# sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from .utils.anno.cls.text_classification import text_classification as cls
from .utils.anno.ner.entity_extract import extract_named_entities as ner
from .local_config import config
