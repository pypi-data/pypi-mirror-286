# SPDX-FileCopyrightText: 2023 - 2024 Gabriele Pongelli
#
# SPDX-License-Identifier: MIT

"""Main module."""
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List

from requests_cache import CacheMixin
from requests_html import HTMLResponse, HTMLSession

from python_active_versions.utility import configure_logger


class CachedHTMLSession(CacheMixin, HTMLSession):  # pylint: disable=W0223
    """Session with features from both CachedSession and HTMLSession."""


def _fetch_tags(package: str, version: str) -> List:
    """Fetch available docker tags.

    Arguments:
        package: package name to be fetched, default to python
        version: python's version to fetch docker images

    Returns:
        list of docker imaged of package at that version
    """
    _names = []

    _next_page = True
    _page = 1
    session = CachedHTMLSession(backend='sqlite', cache_control=True, expire_after=604800)  # one week
    while _next_page:
        logging.info("Fetching docker tags for %s %s , page %s", package, version, _page)
        result = session.get(
            f"https://registry.hub.docker.com/v2/repositories/library/{package}/tags?name={version}&page={_page}",
            timeout=120,
        )
        _json = result.json()
        if not _json['next']:
            _next_page = False
        _page += 1
        _names.extend([r["name"] for r in _json['results']])

    return _names


def get_active_python_versions(
    docker_images: bool = False, log_level: str = 'INFO', no_main: bool = True
) -> List[dict]:  # pylint: disable=too-many-locals
    """Get active python versions.

    Arguments:
        docker_images: flag to return also available docker images
        log_level: string indicating log level on stdout
        no_main: Filter out "main" branch that has no explicit version numbering.

    Returns:
        dict containing all information of active python versions.
    """
    configure_logger(log_level)
    versions = []
    version_table_selector = "#status-of-python-versions table"

    session = CachedHTMLSession(backend='sqlite', cache_control=True, expire_after=604800)  # one week
    _versions: HTMLResponse = session.get("https://devguide.python.org/versions/")
    version_table = _versions.html.find(version_table_selector, first=True)

    # match development information with the latest downloadable release
    _py_specific_release = ".download-list-widget li"
    _downloads: HTMLResponse = session.get("https://www.python.org/downloads/")
    spec_table = _downloads.html.find(_py_specific_release)
    _downloadable_versions = [li.find('span a', first=True).text.split(' ')[1] for li in spec_table]

    def worker(ver, no_main_branch):
        branch, _, _, first_release, end_of_life, _ = [v.text for v in ver.find("td")]

        if no_main_branch is True and branch == 'main':
            return

        logging.info("Found Python branch: %s", branch)
        _matching_version = list(
            filter(lambda d: d.startswith(branch), _downloadable_versions)  # pylint: disable=cell-var-from-loop
        )
        _latest_sw = branch
        if _matching_version:
            _latest_sw = _matching_version[0]

        _d = {"version": branch, "latest_sw": _latest_sw, "start": first_release, "end": end_of_life}
        if docker_images:
            _d['docker_images'] = _fetch_tags('python', _latest_sw)

        versions.append(_d)

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(worker, tr, no_main) for tr in version_table.find("tbody tr")]
        as_completed(futures, 10)

    return versions
