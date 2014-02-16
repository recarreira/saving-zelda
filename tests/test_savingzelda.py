import httpretty
import pytest
from savingzelda import get_page


@httpretty.activate
def test_get_page_should_return_proper_html_for_a_200_status_code_page():
    httpretty.register_uri(httpretty.GET, "http://github.com/",
                           body="here is the mocked body",
                           status=200)
    assert "here is the mocked body" == get_page("http://github.com/")


@httpretty.activate
def test_get_page_should_return_error_message_for_a_non_200_status_code_page():
    httpretty.register_uri(httpretty.GET, "http://github.com/",
                           body="here is the mocked body",
                           status=404)
    with pytest.raises(Exception) as context:
        get_page("http://github.com/")

    assert "Oops! The page returned a status code 404" == context.value.message
