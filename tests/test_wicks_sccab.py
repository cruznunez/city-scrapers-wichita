from datetime import datetime
from os.path import dirname, join

import pytest
from city_scrapers_core.constants import BOARD
from city_scrapers_core.utils import file_response
from freezegun import freeze_time

from city_scrapers.spiders.wicks_sccab import WicksSccabSpider

test_response = file_response(
    join(dirname(__file__), "files", "wicks_sccab.html"),
    url="https://www.sedgwickcounty.org/corrections/corrections-advisory-boards/",
)
spider = WicksSccabSpider()

freezer = freeze_time("2024-04-01")
freezer.start()

parsed_items = [item for item in spider.parse(test_response)]

freezer.stop()


def test_title():
    assert (
        parsed_items[0]["title"]
        == "Community Corrections Advisory Board Monthly Meeting"
    )  # noqa


def test_description():
    assert parsed_items[0]["description"] == ""


def test_start():
    assert parsed_items[0]["start"] == datetime(2024, 1, 11, 8, 0)


def test_end():
    assert parsed_items[0]["end"] == datetime(2024, 1, 11, 9, 0)


def test_time_notes():
    assert parsed_items[0]["time_notes"] == ""


def test_id():
    assert (
        parsed_items[0]["id"]
        == "wicks_sccab/202401110800/x/community_corrections_advisory_board_monthly_meeting"  # noqa
    )


def test_status():
    assert parsed_items[0]["status"] == "passed"


def test_location():
    assert parsed_items[0]["location"] == {
        "name": "Adult Field Services",
        "address": "905 N. Main, Wichita, Kansas",
    }


def test_source():
    assert (
        parsed_items[0]["source"]
        == "https://www.sedgwickcounty.org/corrections/corrections-advisory-boards/"
    )  # noqa


def test_links():
    assert parsed_items[0]["links"] == [
        {
            "title": "Agenda",
            "href": "https://www.sedgwickcounty.org/media/65739/01-11-24-agenda.docx",
        },
        {
            "title": "Minutes",
            "href": "https://www.sedgwickcounty.org/media/65966/1-11-24-minutes.docx",
        },
    ]


def test_classification():
    assert parsed_items[0]["classification"] == BOARD


@pytest.mark.parametrize("item", parsed_items)
def test_all_day(item):
    assert item["all_day"] is False
