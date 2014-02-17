import httpretty
import pytest
import os
from bs4 import BeautifulSoup
from savingzelda import get_page, get_links, check_links


here = os.path.dirname(os.path.abspath(__file__))
TESTS_DATA = os.path.join(here, 'data')


def html_data(file_name):
    file = open(os.path.join(TESTS_DATA, file_name),'r')
    return file.read()

@httpretty.activate
def test_get_page_should_return_body_content_for_a_200_status_code_page():
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


@httpretty.activate
def test_get_page_should_return_proper_html_content():
    httpretty.register_uri(httpretty.GET, "http://github.com/",
                           body= html_data("simple.html"),
                           status=200)
    soup = BeautifulSoup(get_page("http://github.com/"))
    assert "Renata Carreira" == soup.title.string


def test_get_links_should_return_a_valid_list_of_links():
    body = html_data("simple.html")
    assert ["http://renatacarreira.com", "https://github.com/recarreira"] == get_links(body)


def test_get_links_should_return_empty_list_if_no_links_are_found():
    body = html_data("without-links.html")
    assert [] == get_links(body)


@httpretty.activate
def test_check_links_should_return_a_dictionary_with_links_and_status():
    httpretty.register_uri(httpretty.GET, "http://renatacarreira.com",
                           body= html_data("simple.html"),
                           status=200)
    httpretty.register_uri(httpretty.GET, "https://github.com/recarreira",
                           body= html_data("simple.html"),
                           status=404)
    links = ["http://renatacarreira.com", "https://github.com/recarreira"]
    assert {"http://renatacarreira.com": 200, "https://github.com/recarreira": 404} == check_links(links)


def test_check_links_should_return_an_empty_dictionary_given_an_empy_list():
    assert {} == check_links([])
