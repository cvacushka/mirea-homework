import pytest
from main import ConfigParser

def test_remove_multiline_comments():
    parser = ConfigParser()
    text_with_comments = "Hello {{! multline\n comment !}}\nWorld"
    assert parser.remove_multiline_comments(text_with_comments) == "Hello \nWorld"

def test_parse_value_direct_assignment():
    parser = ConfigParser()
    assert parser.parse_value("42") == 42

def test_parse_value_constant():
    parser = ConfigParser()
    parser.constants = {"foo": 100}
    assert parser.parse_value("foo") == 100

def test_parse_value_expression():
    parser = ConfigParser()
    parser.constants = {"a": 3, "b": 4}
    assert parser.parse_value(".[a b +].") == 7

def test_parse_expressions_single():
    parser = ConfigParser()
    parser.parse_expressions("number is 10;")
    assert parser.constants["number"] == 10

def test_parse_expressions_multiple():
    parser = ConfigParser()
    parser.parse_expressions("x is 3; y is 4; sum is .[x y +].;")
    assert parser.constants["x"] == 3
    assert parser.constants["y"] == 4
    assert parser.constants["sum"] == 7

def test_evaluate_expression_addition():
    parser = ConfigParser()
    result = parser.evaluate_expression(".[2 3 +].")
    assert result == 5

def test_evaluate_expression_nested():
    parser = ConfigParser()
    parser.constants = {"a": 5}
    result = parser.evaluate_expression(".[max(a,2) 3 + 2 *].")
    assert result == 16

def test_parse_to_correct_json():
    parser = ConfigParser()
    input_text = """
    username is @john_doe;
    age is 30;
    height_in_cm is .[180].;
    user_info is dict(name=username, age=30);
    """
    expected_json = """{
    "username": "john_doe",
    "age": 30,
    "height_in_cm": 180,
    "user_info": {
        "name": "john_doe",
        "age": 30
    }
}"""
    result_json = parser.parse(input_text)
    assert result_json == expected_json


if __name__ == "__main__":
    pytest.main()