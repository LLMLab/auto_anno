# import os
# import sys
# sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from .utils.anno.cls.text_classification import text_classification as cls
from .utils.anno.ner.entity_extract import extract_named_entities
def ner(*args, **kwargs):
  try:
    return extract_named_entities(*args, **kwargs)
  except Exception as e:
    return []
from .utils.anno.gen.text_generate import text_generate as gen
from .local_config import config
