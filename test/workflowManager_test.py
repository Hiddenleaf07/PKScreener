"""
    The MIT License (MIT)

    Copyright (c) 2023 pkjmesra

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

"""
from unittest.mock import patch

import pytest
from PKDevTools.classes.Environment import PKEnvironment

import pkscreener.classes.ConfigManager as ConfigManager
from pkscreener.classes.Fetcher import screenerStockDataFetcher
from pkscreener.classes.WorkflowManager import run_workflow

configManager = ConfigManager.tools()


@pytest.fixture
def mock_fetcher():
    with patch.object(screenerStockDataFetcher, "postURL") as mock_postURL:
        yield mock_postURL


def test_run_workflow_positive(mock_fetcher):
    mock_fetcher.return_value.status_code = 204
    _, _, _, ghp_token = PKEnvironment().secrets
    result = run_workflow("command", "user", "options")
    assert result == mock_fetcher.return_value
    mock_fetcher.assert_called_once_with(
        "https://api.github.com/repos/pkjmesra/PKScreener/actions/workflows/w13-workflow-backtest_generic.yml/dispatches",
        data='{"ref":"main","inputs":{"user":"user","params":"options:D:D:D:D:D","name":"command"}}',
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + ghp_token,
            "Content-Type": "application/json",
        },
    )


def test_run_workflow_negative(mock_fetcher):
    mock_fetcher.return_value.status_code = 400
    _, _, _, ghp_token = PKEnvironment().secrets
    result = run_workflow("command", "user", "options")
    assert result == mock_fetcher.return_value
    mock_fetcher.assert_called_once_with(
        "https://api.github.com/repos/pkjmesra/PKScreener/actions/workflows/w13-workflow-backtest_generic.yml/dispatches",
        data='{"ref":"main","inputs":{"user":"user","params":"options:D:D:D:D:D","name":"command"}}',
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + ghp_token,
            "Content-Type": "application/json",
        },
    )


def test_run_workflow_edge(mock_fetcher):
    mock_fetcher.return_value.status_code = 200
    _, _, _, ghp_token = PKEnvironment().secrets
    result = run_workflow("command", "user", "options")
    assert result == mock_fetcher.return_value
    mock_fetcher.assert_called_once_with(
        "https://api.github.com/repos/pkjmesra/PKScreener/actions/workflows/w13-workflow-backtest_generic.yml/dispatches",
        data='{"ref":"main","inputs":{"user":"user","params":"options:D:D:D:D:D","name":"command"}}',
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": "Bearer " + ghp_token,
            "Content-Type": "application/json",
        },
    )


def test_run_workflow_error(mock_fetcher):
    _, _, _, ghp_token = PKEnvironment().secrets
    mock_fetcher.side_effect = Exception("Error")
    with pytest.raises(Exception):
        result = run_workflow("command", "user", "options")
        assert result == mock_fetcher.side_effect
        mock_fetcher.assert_called_once_with(
            "https://api.github.com/repos/pkjmesra/PKScreener/actions/workflows/w13-workflow-backtest_generic.yml/dispatches",
            data='{"ref":"main","inputs":{"user":"user","params":"options","name":"command"}}',
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": "Bearer " + ghp_token,
                "Content-Type": "application/json",
            },
        )
