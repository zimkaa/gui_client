import re

from . import pattern


finder_all_items = re.compile(pattern.ALL_ITEMS_FULL_INFO)

finder_item_name = re.compile(pattern.ITEM_NAME)

finder_property_and_request = re.compile(pattern.PROPERTY_AND_REQUIREMENTS)

finder_every_text_in_tag_brackets = re.compile(pattern.EVERY_TEXT_IN_TAG_BRACKETS)

finder_every_action = re.compile(pattern.EVERY_ACTION)
