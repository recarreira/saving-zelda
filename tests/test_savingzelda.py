import httpretty
import pytest
import os
from bs4 import BeautifulSoup
from savingzelda import SavingZelda


here = os.path.dirname(os.path.abspath(__file__))
TESTS_DATA = os.path.join(here, 'data')

zelda_args = {
   'url': 'http://github.com',
}

def html_data(file_name):
    file = open(os.path.join(TESTS_DATA, file_name),'r')
    return file.read()


@httpretty.activate
def test_get_page_should_return_body_content_for_a_200_status_code_page():
    httpretty.register_uri(httpretty.GET, "http://github.com",
                           body="here is the mocked body",
                           status=200)
    saving_zelda = SavingZelda(**zelda_args)
    saving_zelda.get_page("http://github.com")
    assert "here is the mocked body" == saving_zelda.body


@httpretty.activate
def test_get_page_should_return_error_message_for_a_non_200_status_code_page():
    httpretty.register_uri(httpretty.GET, "http://github.com/",
                           body="here is the mocked body",
                           status=404)
    saving_zelda = SavingZelda(**zelda_args)

    with pytest.raises(Exception) as context:
        saving_zelda.get_page("http://github.com/")

    assert "Oops! The page returned a status code 404" == context.value.message


@httpretty.activate
def test_get_page_should_return_proper_html_content():
    httpretty.register_uri(httpretty.GET, "http://github.com",
                           body= html_data("simple.html"),
                           status=200)
    saving_zelda = SavingZelda(**zelda_args)
    saving_zelda.get_page("http://github.com/")
    soup = BeautifulSoup(saving_zelda.body)
    assert "Renata Carreira" == soup.title.string


def test_get_links_should_return_a_valid_list_of_links():
    body = html_data("simple.html")
    saving_zelda = SavingZelda(**zelda_args)
    saving_zelda.get_links(body)
    assert ["http://renatacarreira.com", "https://github.com/recarreira"] == saving_zelda.list_of_links


def test_get_links_should_return_empty_list_if_no_links_are_found():
    body = html_data("without-links.html")
    saving_zelda = SavingZelda(**zelda_args)
    saving_zelda.get_links(body)
    assert [] == saving_zelda.list_of_links

def test_get_links_should_ignore_when_found_a_mailto_link():
    body = html_data("mailto.html")
    saving_zelda = SavingZelda(**zelda_args)
    saving_zelda.get_links(body)
    assert ["http://renatacarreira.com", "https://github.com/recarreira"] == saving_zelda.list_of_links


def test_get_links_should_ignore_when_found_non_link_hrefs():
    body = html_data("whatever.html")
    saving_zelda = SavingZelda(**zelda_args)
    saving_zelda.get_links(body)
    assert ["http://renatacarreira.com"] == saving_zelda.list_of_links

@httpretty.activate
def test_check_links_should_return_a_dictionary_with_links_and_status():
    httpretty.register_uri(httpretty.GET, "http://renatacarreira.com",
                           body= html_data("simple.html"),
                           status=200)
    httpretty.register_uri(httpretty.GET, "https://github.com/recarreira",
                           body= html_data("simple.html"),
                           status=404)
    saving_zelda = SavingZelda(**zelda_args)
    links = ["http://renatacarreira.com", "https://github.com/recarreira"]
    saving_zelda.check_links(links)
    assert {"http://renatacarreira.com": 200, "https://github.com/recarreira": 404} == saving_zelda.links_and_status


def test_check_links_should_return_an_empty_dictionary_given_an_empy_list():
    saving_zelda = SavingZelda(**zelda_args)
    saving_zelda.check_links([])
    assert {} == saving_zelda.links_and_status


def test_dict_with_all_status_code_200_should_save_the_day():
    links_and_status =  {"http://renatacarreira.com": 200, "https://github.com/recarreira": 200}
    saving_zelda = SavingZelda(**zelda_args)
    assert True == saving_zelda.can_we_save_the_day(links_and_status)


def test_dict_with_one_non_200_status_code_should_let_hyrule_down():
    links_and_status = {"http://renatacarreira.com": 404, "https://github.com/recarreira": 200}
    saving_zelda = SavingZelda(**zelda_args)
    assert False == saving_zelda.can_we_save_the_day(links_and_status)
