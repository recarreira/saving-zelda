import httpretty
import pytest
import os
import logging
from bs4 import BeautifulSoup
from savingzelda import SavingZelda


here = os.path.dirname(os.path.abspath(__file__))
TESTS_DATA = os.path.join(here, 'data')


def create_logger():
    handler = logging.FileHandler(os.path.join(here, 'logs', 'test.log'))
    formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s %(message)s')
    handler.setFormatter(formatter)
    logger = logging.getLogger("test Shooter")
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    return logger


logger = create_logger()

zelda_args = {
    'url': 'http://github.com',
    'logger': logger,
}


def html_data(file_name):
    file = open(os.path.join(TESTS_DATA, file_name), 'r')
    return file.read()


@httpretty.activate
def test_get_page_should_return_body_content_for_a_200_status_code_page():
    httpretty.register_uri(httpretty.GET, "http://github.com/",
                           body="here is the mocked body",
                           status=200)
    saving_zelda = SavingZelda(**zelda_args)
    saving_zelda.get_page("http://github.com/")
    assert "here is the mocked body" == saving_zelda.body


def test_get_page_should_return_error_message_for_a_404_status_code_page():
    saving_zelda = SavingZelda(**zelda_args)

    with pytest.raises(Exception) as context:
        saving_zelda.get_page("http://httpbin.org/status/404")

    assert "Oops! The page returned a status code 404" == context.value.message


def test_get_page_should_return_error_message_for_a_403_status_code_page():
    saving_zelda = SavingZelda(**zelda_args)

    with pytest.raises(Exception) as context:
        saving_zelda.get_page("http://httpbin.org/status/403")

    assert "Oops! The page returned a status code 403" == context.value.message


@httpretty.activate
def test_get_page_should_return_proper_html_content():
    httpretty.register_uri(httpretty.GET, "http://saving-zelda.com",
                           body=html_data("simple.html"),
                           status=200)
    saving_zelda = SavingZelda(**zelda_args)
    saving_zelda.get_page("http://saving-zelda.com/")
    soup = BeautifulSoup(saving_zelda.body)
    assert "Saving Zelda" == soup.title.string


def test_get_links_should_return_a_valid_list_of_links():
    body = html_data("simple.html")
    saving_zelda = SavingZelda(**zelda_args)
    saving_zelda.get_links(body)
    assert ["http://httpbin.org/status/200", "http://httpbin.org/status/404"] == saving_zelda.list_of_links


def test_get_links_should_return_a_valid_list_of_links_with_https():
    body = html_data("https.html")
    saving_zelda = SavingZelda(**zelda_args)
    saving_zelda.get_links(body)
    assert ["https://httpbin.org/status/200", "https://httpbin.org/status/404"] == saving_zelda.list_of_links


def test_get_links_should_return_empty_list_if_no_links_are_found():
    body = html_data("without-links.html")
    saving_zelda = SavingZelda(**zelda_args)
    saving_zelda.get_links(body)
    assert [] == saving_zelda.list_of_links


def test_get_links_should_ignore_when_found_a_mailto_link():
    body = html_data("mailto.html")
    saving_zelda = SavingZelda(**zelda_args)
    saving_zelda.get_links(body)
    assert ["http://httpbin.org/status/200"] == saving_zelda.list_of_links


def test_get_links_should_ignore_when_found_non_link_hrefs():
    body = html_data("whatever.html")
    saving_zelda = SavingZelda(**zelda_args)
    saving_zelda.get_links(body)
    assert ["http://httpbin.org/status/200"] == saving_zelda.list_of_links


def test_check_link_should_append_link_and_status_for_a_valid_link():
    saving_zelda = SavingZelda(**zelda_args)
    saving_zelda.check_link("http://httpbin.org/status/200")
    assert {"http://httpbin.org/status/200": 200,} == saving_zelda.links_and_status


def test_check_link_should_work_with_https():
    saving_zelda = SavingZelda(**zelda_args)
    saving_zelda.check_link("https://httpbin.org/status/200")
    assert {"https://httpbin.org/status/200": 200,} == saving_zelda.links_and_status


def test_check_link_should_cry_when_given_an_invalid_url():
    saving_zelda = SavingZelda(**zelda_args)
    saving_zelda.check_link("http://this.url.does.not.have.a.valid.status.code.renatacarreira.com")
    assert {"http://this.url.does.not.have.a.valid.status.code.renatacarreira.com": "Nodename nor servname provided, or not known",} == saving_zelda.links_and_status


def test_check_links_should_return_a_dictionary_with_links_and_status():
    saving_zelda = SavingZelda(**zelda_args)
    links = ["http://httpbin.org/status/200", "http://httpbin.org/status/404"]
    saving_zelda.check_links(links)
    expected_results = {"http://httpbin.org/status/200": 200,
                        "http://httpbin.org/status/404": 404}
    assert expected_results == saving_zelda.links_and_status


def test_check_links_should_return_an_empty_dictionary_given_an_empy_list():
    saving_zelda = SavingZelda(**zelda_args)
    saving_zelda.check_links([])
    assert {} == saving_zelda.links_and_status


def test_dict_with_all_status_code_200_should_save_the_day():
    links_and_status =  {"http://httpbin.org/status/200": 200, "http://httpbin.org/status/200": 200}
    saving_zelda = SavingZelda(**zelda_args)
    assert saving_zelda.can_we_save_the_day(links_and_status) is True


def test_dict_with_one_non_200_status_code_should_let_hyrule_down():
    links_and_status = {"http://httpbin.org/status/404": 404, "http://httpbin.org/status/200": 200}
    saving_zelda = SavingZelda(**zelda_args)
    assert saving_zelda.can_we_save_the_day(links_and_status) is False
