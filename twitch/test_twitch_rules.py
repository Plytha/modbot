import pytest
from rule import Rule

def build_from_dict(rule_dict):
    if "ordered" in rule_dict.keys():
        ordered = rule_dict["ordered"]
    else:
        ordered = False
    rule_object = Rule(rule_dict["name"], 
                       rule_dict["matches"] == "all", 
                       ordered,
                       rule_dict["filters"]["words"],
                       rule_dict["filters"]["regex"])
    return rule_object

def test_one_word_rule_fires_on_word_found():
    rule_dict = {
        "name": "one word test",
        "matches": "all",
        "filters": 
        {
            "words": ["test"],
            "regex": []
        }
    }

    rule = build_from_dict(rule_dict)
    message_string = "there is the word test in me"
    assert rule.check(message_string)

def test_one_word_rule_does_not_fire_on_word_missing():
    rule_dict = {
        "name": "one word test",
        "matches": "all",
        "filters": 
        {
            "words": ["test"],
            "regex": []
        }
    }

    rule = build_from_dict(rule_dict)
    message_string = "the word is absent in me"
    assert not rule.check(message_string)

def test_multiple_word_any_rule_fires_on_words_found():
    rule_dict = {
        "name": "multiple words any",
        "matches": "any",
        "filters": 
        {
            "words": ["red", "blue"],
            "regex": []
        }
    }

    rule = build_from_dict(rule_dict)
    message_string = "bla bla bla red bla bla"
    assert rule.check(message_string)

def test_multiple_word_any_rule_does_not_fire_on_words_missing():
    rule_dict = {
        "name": "multiple words any",
        "matches": "any",
        "filters": 
        {
            "words": ["red", "blue"],
            "regex": []
        }
    }

    rule = build_from_dict(rule_dict)
    message_string = "bla bla bla bla bla"
    assert not rule.check(message_string)

def test_multiple_word_all_ordered_rule_fires_on_words_found():
    rule_dict = {
        "name": "multiple words all ordered",
        "matches": "all",
        "ordered": True,
        "filters": 
        {
            "words": ["three", "four"],
            "regex": []
        }
    }

    rule = build_from_dict(rule_dict)
    message_string = "one two three four five six seven"
    assert rule.check(message_string)

def test_multiple_word_all_ordered_rule_does_not_fire_on_words_missing():
    rule_dict = {
        "name": "multiple words all ordered",
        "matches": "all",
        "ordered": True,
        "filters": 
        {
            "words": ["three", "four"],
            "regex": []
        }
    }

    rule = build_from_dict(rule_dict)
    message_string = "one two three ten five six"
    assert not rule.check(message_string)

def test_multiple_word_all_ordered_rule_does_not_fire_on_words_unordered():
    rule_dict = {
        "name": "multiple words all ordered",
        "matches": "all",
        "ordered": True,
        "filters": 
        {
            "words": ["three", "four"],
            "regex": []
        }
    }

    rule = build_from_dict(rule_dict)
    message_string = "five four three two one"
    assert not rule.check(message_string)

def test_multiple_word_all_unordered_rule_fires_on_words_found():
    rule_dict = {
        "name": "multiple words all unordered",
        "matches": "all",
        "ordered": False,
        "filters": 
        {
            "words": ["one", "two"],
            "regex": []
        }
    }

    rule = build_from_dict(rule_dict)
    message_string = "one two three four five six seven"
    assert rule.check(message_string)

def test_multiple_word_all_unordered_rule_does_not_fire_on_words_missing():
    rule_dict = {
        "name": "multiple words all unordered",
        "matches": "all",
        "ordered": False,
        "filters": 
        {
            "words": ["one", "two"],
            "regex": []
        }
    }

    rule = build_from_dict(rule_dict)
    message_string = "one three ten five six"
    assert not rule.check(message_string)

def test_ensure_having_a_word_as_a_substring_of_another_does_not_fire():
    rule_dict = {
        "name": "one word test",
        "matches": "all",
        "filters": 
        {
            "words": ["test"],
            "regex": []
        }
    }

    rule = build_from_dict(rule_dict)
    message_string = "Man I love writing unit tests"
    assert not rule.check(message_string)