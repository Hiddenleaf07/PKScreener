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
import warnings
from unittest.mock import ANY, MagicMock, patch, PropertyMock

import numpy as np
import platform

warnings.simplefilter("ignore", DeprecationWarning)
warnings.simplefilter("ignore", FutureWarning)
import pandas as pd
import pytest
from PKDevTools.classes.log import default_logger as dl
from PKDevTools.classes.ColorText import colorText
import pkscreener.classes.ConfigManager as ConfigManager
import pkscreener.classes.Utility as Utility
from pkscreener.classes.ScreeningStatistics import ScreeningStatistics
from PKDevTools.classes.PKDateUtilities import PKDateUtilities
@pytest.fixture
def configManager():
    return ConfigManager.tools()


@pytest.fixture
def default_logger():
    return dl()


@pytest.fixture
def tools_instance(configManager, default_logger):
    return ScreeningStatistics(configManager, default_logger)


def test_positive_case_find52WeekHighBreakout(tools_instance):
    df = pd.DataFrame({
        "High": [50, 60, 70, 80, 90, 100]  # Assuming recent high is 100
    })
    assert tools_instance.find52WeekHighBreakout(df) == False

def test_negative_case_find52WeekHighBreakout(tools_instance):
    df = pd.DataFrame({
        "High": [50, 60, 70, 80, 90, 80]  # Assuming recent high is 80
    })
    assert tools_instance.find52WeekHighBreakout(df) == False

def test_empty_dataframe_find52WeekHighBreakout(tools_instance):
    df = pd.DataFrame()
    assert tools_instance.find52WeekHighBreakout(df) == False

def test_dataframe_with_nan_find52WeekHighBreakout(tools_instance):
    df = pd.DataFrame({
        "High": [50, 60, np.nan, 80, 90, 100]  # Assuming recent high is 100
    })
    assert tools_instance.find52WeekHighBreakout(df) == False

def test_dataframe_with_inf_find52WeekHighBreakout(tools_instance):
    df = pd.DataFrame({
        "High": [50, 60, np.inf, 80, 90, 100]  # Assuming recent high is 100
    })
    assert tools_instance.find52WeekHighBreakout(df) == False

def test_find52WeekHighBreakout_positive(tools_instance):
    data = pd.DataFrame({"High": [110, 60, 70, 80, 90, 100]})
    assert tools_instance.find52WeekHighBreakout(data) == True


def test_find52WeekHighBreakout_negative(tools_instance):
    data = pd.DataFrame({"High": [50, 60, 80, 60, 60, 40, 100, 110, 120, 50, 170]})
    assert tools_instance.find52WeekHighBreakout(data) == False


def test_find52WeekHighBreakout_edge(tools_instance):
    data = pd.DataFrame(
        {
            "High": [
                50,
                60,
                70,
                80,
                90,
                100,
                110,
                120,
                130,
                140,
                150,
                160,
                170,
                180,
                190,
                200,
            ]
        }
    )
    assert tools_instance.find52WeekHighBreakout(data) == False


def test_find52WeekHighBreakout_nan_values(tools_instance):
    data = pd.DataFrame({"High": [50, 60, np.nan, 80, 90, 100]})
    assert tools_instance.find52WeekHighBreakout(data) == False


def test_find52WeekHighBreakout_inf_values(tools_instance):
    data = pd.DataFrame({"High": [50, 60, np.inf, 80, 90, 100]})
    assert tools_instance.find52WeekHighBreakout(data) == False


def test_find52WeekHighBreakout_negative_inf_values(tools_instance):
    data = pd.DataFrame({"High": [50, 60, -np.inf, 80, 90, 100]})
    assert tools_instance.find52WeekHighBreakout(data) == False


def test_find52WeekHighBreakout_last1WeekHigh_greater(tools_instance):
    data = pd.DataFrame({"High": [50, 60, 70, 80, 90, 100]})
    assert tools_instance.find52WeekHighBreakout(data) == False


def test_find52WeekHighBreakout_previousWeekHigh_greater(tools_instance):
    data = pd.DataFrame({"High": [50, 60, 70, 80, 90, 100]})
    assert tools_instance.find52WeekHighBreakout(data) == False


def test_find52WeekHighBreakout_full52WeekHigh_greater(tools_instance):
    data = pd.DataFrame({"High": [50, 60, 70, 80, 90, 100]})
    assert tools_instance.find52WeekHighBreakout(data) == False


# Positive test case for find52WeekLowBreakout function
def test_find52WeekLowBreakout_positive(tools_instance):
    data = pd.DataFrame({"Low": [10, 20, 30, 40, 50]})
    result = tools_instance.find52WeekLowBreakout(data)
    assert result == True


# Negative test case for find52WeekLowBreakout function
def test_find52WeekLowBreakout_negative(tools_instance):
    data = pd.DataFrame({"Low": [50, 40, 30, 20, 10]})
    result = tools_instance.find52WeekLowBreakout(data)
    assert result == False


# Edge test case for find52WeekLowBreakout function
def test_find52WeekLowBreakout_edge(tools_instance):
    data = pd.DataFrame(
        {
            "Low": [
                10,
                20,
                30,
                40,
                50,
                60,
                70,
                80,
                90,
                100,
                110,
                120,
                130,
                140,
                150,
                160,
                170,
                180,
                190,
                200,
            ]
        }
    )
    result = tools_instance.find52WeekLowBreakout(data)
    assert result == True

def test_find52WeekHighLow_positive_case(tools_instance):
    df = pd.DataFrame({
        "High": [100, 60, 70, 80, 90, 100],  # Assuming recent high is 100
        "Low": [5, 30, 20, 10, 5, 5]  # Assuming recent low is 40
    })
    saveDict = {}
    screenDict = {}
    tools_instance.find52WeekHighLow(df, saveDict, screenDict)
    assert saveDict["52Wk-H"] == "100.00"
    assert saveDict["52Wk-L"] == "5.00"
    assert screenDict["52Wk-H"] == f"{colorText.GREEN}100.00{colorText.END}"
    assert screenDict["52Wk-L"] == f"{colorText.FAIL}5.00{colorText.END}"

    df = pd.DataFrame({
        "High": [90, 60, 70, 80, 90, 100],  # Assuming recent high is 90
        "Low": [110, 130, 120, 110, 115, 100]  # Assuming recent low is 110
    })
    saveDict = {}
    screenDict = {}
    tools_instance.find52WeekHighLow(df, saveDict, screenDict)
    assert saveDict["52Wk-H"] == "100.00"
    assert saveDict["52Wk-L"] == "100.00"
    assert screenDict["52Wk-H"] == f"{colorText.WARN}100.00{colorText.END}"
    assert screenDict["52Wk-L"] == f"{colorText.WARN}100.00{colorText.END}"

    df = pd.DataFrame({
        "High": [50, 60, 70, 80, 90, 100],  # Assuming recent high is 50
        "Low": [40, 30, 20, 10, 5, 0]  # Assuming recent low is 40
    })
    saveDict = {}
    screenDict = {}
    tools_instance.find52WeekHighLow(df, saveDict, screenDict)
    assert saveDict["52Wk-H"] == "100.00"
    assert saveDict["52Wk-L"] == "0.00"
    assert screenDict["52Wk-H"] == f"{colorText.FAIL}100.00{colorText.END}"
    assert screenDict["52Wk-L"] == f"{colorText.GREEN}0.00{colorText.END}"

def test_find52WeekHighLow_negative_case(tools_instance):
    df = pd.DataFrame({
        "High": [50, 60, 70, 80, 90, 80],  # Assuming recent high is 80
        "Low": [40, 30, 20, 10, 5, 10]  # Assuming recent low is 10
    })
    saveDict = {}
    screenDict = {}

    tools_instance.find52WeekHighLow(df, saveDict, screenDict)

    assert saveDict["52Wk-H"] == "90.00"
    assert saveDict["52Wk-L"] == "5.00"
    assert screenDict["52Wk-H"] == f"{colorText.FAIL}90.00{colorText.END}"
    assert screenDict["52Wk-L"] == f"{colorText.GREEN}5.00{colorText.END}"
    assert tools_instance.find52WeekHighLow(None,saveDict, screenDict) is False
    assert tools_instance.find52WeekHighLow(pd.DataFrame(),saveDict, screenDict) is False

def test_find52WeekLowBreakout_positive_case(tools_instance):
    df = pd.DataFrame({
        "Low": [50, 60, 70, 80, 90, 0]  # Assuming recent low is 0
    })
    assert tools_instance.find52WeekLowBreakout(df) == False

def test_find52WeekLowBreakout_negative_case(tools_instance):
    df = pd.DataFrame({
        "Low": [50, 60, 70, 80, 90, 10]  # Assuming recent low is 10
    })
    assert tools_instance.find52WeekLowBreakout(df) == False

# Positive test case for find10DaysLowBreakout function
def test_find10DaysLowBreakout_positive(tools_instance):
    data = pd.DataFrame({"Low": [10, 20, 30, 40, 50]})
    result = tools_instance.find10DaysLowBreakout(data)
    assert result == True


# Negative test case for find10DaysLowBreakout function
def test_find10DaysLowBreakout_negative(tools_instance):
    data = pd.DataFrame({"Low": [50, 40, 30, 20, 10]})
    result = tools_instance.find10DaysLowBreakout(data)
    assert result == False


# Edge test case for find10DaysLowBreakout function
def test_find10DaysLowBreakout_edge(tools_instance):
    data = pd.DataFrame(
        {
            "Low": [
                10,
                20,
                30,
                40,
                50,
                60,
                70,
                80,
                90,
                100,
                110,
                120,
                130,
                140,
                150,
                160,
                170,
                180,
                190,
                200,
            ]
        }
    )
    result = tools_instance.find10DaysLowBreakout(data)
    assert result == True


# Positive test case for findAroonBullishCrossover function
def test_findAroonBullishCrossover_positive(tools_instance):
    data = pd.DataFrame({"High": [50, 60, 70, 80, 90], "Low": [10, 20, 30, 40, 50]})
    result = tools_instance.findAroonBullishCrossover(data)
    assert result == False


# Negative test case for findAroonBullishCrossover function
def test_findAroonBullishCrossover_negative(tools_instance):
    data = pd.DataFrame({"High": [90, 80, 70, 60, 50], "Low": [50, 40, 30, 20, 10]})
    result = tools_instance.findAroonBullishCrossover(data)
    assert result == False


# Edge test case for findAroonBullishCrossover function
def test_findAroonBullishCrossover_edge(tools_instance):
    data = pd.DataFrame(
        {
            "High": [
                10,
                20,
                30,
                40,
                50,
                60,
                70,
                80,
                90,
                100,
                110,
                120,
                130,
                140,
                150,
                160,
                170,
                180,
                190,
                200,
            ],
            "Low": [
                50,
                40,
                30,
                20,
                10,
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
            ],
        }
    )
    result = tools_instance.findAroonBullishCrossover(data)
    assert result == False

def test_positive_case_findBreakingoutNow(tools_instance):
    df = pd.DataFrame({
        "Open": [50, 60, 70, 80, 90, 100],
        "Close": [55, 65, 75, 85, 95, 105]
    })
    assert tools_instance.findBreakingoutNow(df,df,{},{}) == False

    df = pd.DataFrame({
        "Open": [100,100,100,100,100,100,100,100,100,100,100,100],
        "Close": [130,110,110,110,110,110,110,110,110,110,110,110,]
    })
    assert tools_instance.findBreakingoutNow(df,df,{},{}) == True

def test_negative_case_findBreakingoutNow(tools_instance):
    df = pd.DataFrame({
        "Open": [50, 60, 70, 80, 90, 80],
        "Close": [55, 65, 75, 85, 95, 85]
    })
    assert tools_instance.findBreakingoutNow(df,df,{},{}) == False

def test_empty_dataframe_findBreakingoutNow(tools_instance):
    df = pd.DataFrame()
    assert tools_instance.findBreakingoutNow(df,df,{},{}) == False

def test_dataframe_with_nan_findBreakingoutNow(tools_instance):
    df = pd.DataFrame({
        "Open": [50, 60, np.nan, 80, 90, 100],
        "Close": [55, 65, np.nan, 85, 95, 105]
    })
    assert tools_instance.findBreakingoutNow(df,df,{},{}) == False

def test_dataframe_with_inf_findBreakingoutNow(tools_instance):
    df = pd.DataFrame({
        "Open": [50, 60, np.inf, 80, 90, 100],
        "Close": [55, 65, np.inf, 85, 95, 105]
    })
    assert tools_instance.findBreakingoutNow(df,df,{},{}) == False


# Positive test case for findBreakoutValue function
def test_findBreakoutValue_positive(tools_instance):
    data = pd.DataFrame({"High": [50, 60, 70, 80, 90], "Close": [40, 50, 60, 70, 80]})
    screenDict = {}
    saveDict = {"Stock": "SBIN"}
    daysToLookback = 5
    result = tools_instance.findBreakoutValue(
        data, screenDict, saveDict, daysToLookback
    )
    assert result == True


# Negative test case for findBreakoutValue function
def test_findBreakoutValue_negative(tools_instance):
    data = pd.DataFrame(
        {
            "High": [90, 80, 70, 60, 50],
            "Close": [80, 70, 60, 50, 40],
            "Open": [80, 70, 60, 50, 40],
        }
    )
    screenDict = {}
    saveDict = {"Stock": "SBIN"}
    daysToLookback = 5
    result = tools_instance.findBreakoutValue(
        data, screenDict, saveDict, daysToLookback
    )
    assert result == False


# Edge test case for findBreakoutValue function
def test_findBreakoutValue_edge(tools_instance):
    data = pd.DataFrame(
        {
            "High": [
                10,
                20,
                30,
                40,
                50,
                60,
                70,
                80,
                90,
                100,
                110,
                120,
                130,
                140,
                150,
                160,
                170,
                180,
                190,
                200,
            ],
            "Open": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
            "Close": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
        }
    )
    screenDict = {}
    saveDict = {"Stock": "SBIN"}
    daysToLookback = 5
    result = tools_instance.findBreakoutValue(
        data, screenDict, saveDict, daysToLookback
    )
    assert result == False

def test_positive_case_findNR4Day(tools_instance):
    df = pd.DataFrame({
        "Volume": [60000, 70000, 80000, 90000, 100000],
        "Close": [10, 9, 8, 7, 6],
        "High": [11, 10, 9, 8, 7],
        "Low": [9, 8, 7, 6, 5],
        "SMA10": [8, 7, 6, 5, 4],
        "SMA50": [7, 6, 5, 4, 3],
        "SMA200": [6, 5, 4, 3, 2]
    })
    assert tools_instance.findNR4Day(df) == False

def test_negative_case_findNR4Day(tools_instance):
    df = pd.DataFrame({
        "Volume": [40000, 50000, 60000, 70000, 80000],
        "Close": [10, 9, 8, 7, 6],
        "High": [11, 10, 9, 8, 7],
        "Low": [9, 8, 7, 6, 5],
        "SMA10": [8, 7, 6, 5, 4],
        "SMA50": [7, 6, 5, 4, 3],
        "SMA200": [6, 5, 4, 3, 2]
    })
    assert tools_instance.findNR4Day(df) == False

def test_empty_dataframe_findNR4Day(tools_instance):
    df = pd.DataFrame()
    assert tools_instance.findNR4Day(df) == False

def test_dataframe_with_nan_findNR4Day(tools_instance):
    df = pd.DataFrame({
        "Volume": [60000, 70000, np.nan, 90000, 100000],
        "Close": [10, 9, np.nan, 7, 6],
        "High": [11, 10, np.nan, 8, 7],
        "Low": [9, 8, np.nan, 6, 5],
        "SMA10": [8, 7, np.nan, 5, 4],
        "SMA50": [7, 6, np.nan, 4, 3],
        "SMA200": [6, 5, np.nan, 3, 2]
    })
    assert tools_instance.findNR4Day(df) == False

def test_dataframe_with_inf_findNR4Day(tools_instance):
    df = pd.DataFrame({
        "Volume": [60000, 70000, np.inf, 90000, 100000],
        "Close": [10, 9, np.inf, 7, 6],
        "High": [11, 10, np.inf, 8, 7],
        "Low": [9, 8, np.inf, 6, 5],
        "SMA10": [8, 7, np.inf, 5, 4],
        "SMA50": [7, 6, np.inf, 4, 3],
        "SMA200": [6, 5, np.inf, 3, 2]
    })
    assert tools_instance.findNR4Day(df) == False


# Positive test case for findBullishIntradayRSIMACD function
def test_findBullishIntradayRSIMACD_positive():
    # Mocking the data
    data = pd.DataFrame(
        {
            "High": [
                10,
                20,
                30,
                40,
                50,
                60,
                70,
                80,
                90,
                100,
                110,
                120,
                130,
                140,
                150,
                160,
                170,
                180,
                190,
                200,
            ],
            "Open": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
            "Close": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
        }
    )
    # Create an instance of the tools class
    tool = ScreeningStatistics(None, None)
    # Call the function and assert the result
    assert tool.findBullishIntradayRSIMACD(data) == False
    assert tool.findBullishIntradayRSIMACD(None) == False
    assert tool.findBullishIntradayRSIMACD(pd.DataFrame()) == False


# # Positive test case for findNR4Day function
def test_findNR4Day_positive():
    # Mocking the data
    data = pd.DataFrame(
        {
            "High": [
                10,
                20,
                30,
                40,
                50,
                60,
                70,
                80,
                90,
                100,
                110,
                120,
                130,
                140,
                150,
                160,
                170,
                180,
                190,
                200,
            ],
            "Open": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
            "Close": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
            "Low": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
            "Volume": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
        }
    )
    # Create an instance of the tools class
    tool = ScreeningStatistics(None, None)
    # Call the function and assert the result
    assert tool.findNR4Day(data) == False


# Positive test case for findReversalMA function
def test_findReversalMA_positive(tools_instance):
    # Mocking the data
    data = pd.DataFrame(
        {
            "High": [
                10,
                20,
                30,
                40,
                50,
                60,
                70,
                80,
                90,
                100,
                110,
                120,
                130,
                140,
                150,
                160,
                170,
                180,
                190,
                200,
            ],
            "Open": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
            "Close": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
            "Low": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
            "Volume": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
        }
    )
    # Call the function and assert the result
    assert tools_instance.findReversalMA(data, {}, {}, 3) == False


# Positive test case for findTrend function
def test_findTrend_positive(tools_instance):
    # Mocking the data
    data = pd.DataFrame(
        {
            "High": [
                10,
                20,
                30,
                40,
                50,
                60,
                70,
                80,
                90,
                100,
                110,
                120,
                130,
                140,
                150,
                160,
                170,
                180,
                190,
                200,
            ],
            "Open": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
            "Close": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
            "Low": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
            "Volume": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
        }
    )
    # Call the function and assert the result
    assert tools_instance.findTrend(data, {}, {}, 10) == "Unknown"

def test_findTrend_valid_input(tools_instance):
    # Create a sample DataFrame for testing
    df = pd.DataFrame({'Close': [10, 15, 20, 25, 30, 35, 40, 45, 50]})

    # Define the expected trend for the given DataFrame
    expected_trend = 'Unknown'

    # Call the findTrend function with the sample DataFrame and expected trend
    result = tools_instance.findTrend(df, {}, {}, daysToLookback=9, stockName='')

    # Assert that the returned trend matches the expected trend
    assert result == expected_trend

def test_findTrend_empty_input(tools_instance):
    # Create an empty DataFrame for testing
    df = pd.DataFrame()

    # Call the findTrend function with the empty DataFrame
    result = tools_instance.findTrend(df, {}, {})

    # Assert that the returned trend is 'Unknown'
    assert result == 'Unknown'

def test_findTrend_insufficient_data(tools_instance):
    # Create a DataFrame with less than the required number of days
    df = pd.DataFrame({'Close': [10, 15, 20]})

    # Call the findTrend function with the insufficient DataFrame
    result = tools_instance.findTrend(df, {}, {})

    # Assert that the returned trend is 'Unknown'
    assert result == 'Unknown'

def test_findTrend_exception(tools_instance):
    # Create a DataFrame with invalid data that will raise an exception
    df = pd.DataFrame({'Close': ['a', 'b', 'c']})
    # Call the findTrend function with the invalid DataFrame
    tools_instance.findTrend(df, {}, {}) == 'Unknown'

def test_findTrend_tops_data(tools_instance):
    # Create a DataFrame with less than the required number of days
    df = pd.DataFrame({'Close': [10, 15, 20]})
    with patch("numpy.rad2deg",return_value=0):
        assert tools_instance.findTrend(df, {}, {}) == 'Unknown'
    with patch("numpy.rad2deg",return_value=30):
        assert tools_instance.findTrend(df, {}, {}) == 'Sideways'
    with patch("numpy.rad2deg",return_value=-30):
        assert tools_instance.findTrend(df, {}, {}) == 'Sideways'
    with patch("numpy.rad2deg",return_value=10):
        assert tools_instance.findTrend(df, {}, {}) == 'Sideways'
    with patch("numpy.rad2deg",return_value=-20):
        assert tools_instance.findTrend(df, {}, {}) == 'Sideways'
    with patch("numpy.rad2deg",return_value=60):
        assert tools_instance.findTrend(df, {}, {}) == 'Weak Up'
    with patch("numpy.rad2deg",return_value=61):
        assert tools_instance.findTrend(df, {}, {}) == 'Strong Up'
    with patch("numpy.rad2deg",return_value=-40):
        assert tools_instance.findTrend(df, {}, {}) == 'Weak Down'
    with patch("numpy.rad2deg",return_value=-60):
        assert tools_instance.findTrend(df, {}, {}) == 'Weak Down'
    with patch("numpy.rad2deg",return_value=-61):
        assert tools_instance.findTrend(df, {}, {}) == 'Strong Down'
    with patch("pkscreener.classes.Pktalib.pktalib.argrelextrema",side_effect=[np.linalg.LinAlgError]):
        tools_instance.findTrend(df, {}, {}) == 'Unknown'
    with patch("pkscreener.classes.Pktalib.pktalib.argrelextrema",side_effect=[([0,1,2],)]):
        tools_instance.findTrend(df, {}, {}) == 'Unknown'

# Positive test case for findTrendlines function
def test_findTrendlines_positive(tools_instance):
    # Mocking the data
    data = pd.DataFrame(
        {
            "High": [
                10,
                20,
                30,
                40,
                50,
                60,
                70,
                80,
                90,
                100,
                110,
                120,
                130,
                140,
                150,
                160,
                170,
                180,
                190,
                200,
            ],
            "Open": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
            "Close": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
            "Low": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
            "Volume": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
        }
    )

    # Call the function and assert the result
    assert tools_instance.findTrendlines(data, {}, {}) == True


# Positive test case for getCandleType function
def test_getCandleType_positive(tools_instance):
    # Mocking the dailyData
    dailyData = pd.DataFrame(
        {
            "High": [
                10,
                20,
                30,
                40,
                50,
                60,
                70,
                80,
                90,
                100,
                110,
                120,
                130,
                140,
                150,
                160,
                170,
                180,
                190,
                200,
            ],
            "Open": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
            "Close": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
            "Low": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
            "Volume": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
        }
    )
    # Call the function and assert the result
    assert tools_instance.getCandleType(dailyData) == True


@pytest.mark.skipif(
    "Windows" in platform.system(),
    reason="Exception:UnicodeEncodeError: 'charmap' codec can't encode characters in position 18-37: character maps to <undefined>",
)
# PositiveNiftyPrediction function
def test_getNiftyPrediction_positive(tools_instance):
    # Mocking the data
    data = pd.DataFrame(
        {
            "High": [
                10,
                20,
                30,
                40,
                50,
                60,
                70,
                80,
                90,
                100,
                110,
                120,
                130,
                140,
                150,
                160,
                170,
                180,
                190,
                200,
            ],
            "Open": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
            "Close": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
            "Low": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
            "Volume": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
        }
    )
    # Mocking the scaler
    scaler = MagicMock()
    pkl = {"columns": scaler}
    # Mocking the model
    model = MagicMock()
    model.predict.return_value = [0.6]
    # Mocking the Utility class
    Utility.tools.getNiftyModel.return_value = (model, pkl)
    # Call the function and assert the result
    assert tools_instance.getNiftyPrediction(data) is not None
    #         == (
    #     ANY,
    #     "Market may Open BULLISH next day! Stay Bullish!",
    #     "Probability/Strength of Prediction = 0.0%",
    # ) or tools_instance.getNiftyPrediction(data) == (
    #     ANY,
    #     "Market may Open BEARISH next day! Hold your Short position!",
    #     "Probability/Strength of Prediction = 100.0%",
    # ))


# # Positive test case for monitorFiveEma function
# def test_monitorFiveEma_positive():
#     # Mocking the fetcher
#     fetcher = MagicMock()
#     fetcher.fetchFiveEmaData.return_value = (MagicMock(), MagicMock(), MagicMock(), MagicMock())

#     # Mocking the result_df
#     result_df = MagicMock()

#     # Mocking the last_signal
#     last_signal = MagicMock()

#     # Create an instance of the tools class
#     tool = tools(None, None)

#     # Call the function and assert the result
#     assert tool.monitorFiveEma(fetcher, result_df, last_signal) == result_df

# # Negative test case for monitorFiveEma function
# def test_monitorFiveEma_negative():
#     # Mocking the fetcher
#     fetcher = MagicMock()
#     fetcher.fetchFiveEmaData.return_value = (MagicMock(), MagicMock(), MagicMock(), MagicMock())
#     # Mocking the result_df
#     result_df = MagicMock()
#     # Mocking the last_signal
#     last_signal = MagicMock()
#     # Create an instance of the tools class
#     tool = tools(None, None)
#     # Call the function and assert the result
#     assert tool.monitorFiveEma(fetcher, result_df, last_signal) != result_df


# Positive test case for preprocessData function
def test_preprocessData_positive(tools_instance):
    # Mocking the data
    data = pd.DataFrame(
        {
            "High": [
                10,
                20,
                30,
                40,
                50,
                60,
                70,
                80,
                90,
                100,
                110,
                120,
                130,
                140,
                150,
                160,
                170,
                180,
                190,
                200,
            ],
            "Open": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
            "Close": [
                200.1,
                190.1,
                180.1,
                170.1,
                160.1,
                150.1,
                140.1,
                130.1,
                120.1,
                110.1,
                100.1,
                90.1,
                80.1,
                70.1,
                60.1,
                50.1,
                40.1,
                30.1,
                20.1,
                10.1,
            ],
            "Low": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
            "Volume": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
            "Other": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
        }
    )

    # Call the function and assert the result
    assert tools_instance.preprocessData(data, 10) is not None


def test_preprocessData_valid_input(tools_instance):
    # Create a sample DataFrame for testing
    df = pd.DataFrame({'Close': [10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45, 50],
                       'Volume': [100, 200, 300, 400, 500, 600, 700, 800, 900],
                       'High': [12.0, 18, 22, 28, 32, 38, 42, 48, 52],
                       'Low': [8.0, 12, 16, 20, 24, 28, 32, 36, 40],
                       'Open': [8.0, 12, 16, 20, 24, 28, 32, 36, 40]})
    df = pd.concat([df]*23, ignore_index=True)
    # Call the preprocessData function with the sample DataFrame
    fullData, trimmedData = tools_instance.preprocessData(df, daysToLookback=9)
    # Assert that the returned dataframes have the expected shape and columns
    assert fullData.shape == (207, 14)
    assert trimmedData.shape == (9, 14)
    assert list(fullData.columns) == ['Close', 'Volume', 'High', 'Low', 'Open', 'SMA', 'LMA', 'SSMA', 'SSMA20', 'VolMA', 'RSI', 'CCI', 'FASTK', 'FASTD']

    tools_instance.configManager.useEMA = True
    # Call the preprocessData function with the sample DataFrame
    fullData, trimmedData = tools_instance.preprocessData(df, daysToLookback=9)
    # Assert that the returned dataframes have the expected shape and columns
    assert fullData.shape == (207, 14)
    assert trimmedData.shape == (9, 14)
    assert list(fullData.columns) == ['Close', 'Volume', 'High', 'Low', 'Open', 'SMA', 'LMA', 'SSMA', 'SSMA20', 'VolMA', 'RSI', 'CCI', 'FASTK', 'FASTD']

def test_preprocessData_empty_input(tools_instance):
    # Create an empty DataFrame for testing
    df = pd.DataFrame()

    # Call the preprocessData function with the empty DataFrame
    df1,df2 = tools_instance.preprocessData(df)
    assert df1.empty
    assert df2.empty

def test_preprocessData_insufficient_data(tools_instance):
    # Create a DataFrame with less than the required number of days
    df = pd.DataFrame({'Close': [10, 15, 20]})

    # Call the preprocessData function with the insufficient DataFrame
    df1,df2 = tools_instance.preprocessData(df)
    assert not df1.empty
    assert not df2.empty

# Positive test case for validate15MinutePriceVolumeBreakout function
def test_validate15MinutePriceVolumeBreakout_positive(tools_instance):
    # Mocking the data
    data = pd.DataFrame(
        {
            "High": [
                10,
                20,
                30,
                40,
                50,
                60,
                70,
                80,
                90,
                100,
                110,
                120,
                130,
                140,
                150,
                160,
                170,
                180,
                190,
                200,
            ],
            "Open": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
            "Close": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
            "Low": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
            "Volume": [
                200,
                190,
                180,
                170,
                160,
                150,
                140,
                130,
                120,
                110,
                100,
                90,
                80,
                70,
                60,
                50,
                40,
                30,
                20,
                10,
            ],
        }
    )
    # Call the function and assert the result
    assert tools_instance.validate15MinutePriceVolumeBreakout(data) == True


def test_positive_case_findPotentialBreakout(tools_instance):
    df = pd.DataFrame({
        "Volume": [100000, 90000, 80000, 70000, 60000],
        "Close": [10, 9, 8, 7, 6],
        "High": [11, 10, 9, 8, 7]
    })
    screenDict = {}
    saveDict = {"Breakout": ""}
    daysToLookback = 30
    assert tools_instance.findPotentialBreakout(df, screenDict, saveDict, daysToLookback) == False
    assert saveDict["Breakout"] == ""

    daysToLookback = 30
    df = pd.DataFrame({
        "Volume": [100000, 90000, 80000, 70000, 60000],
        "Close": [120, 9, 8, 7, 6],
        "High": [110, 10, 9, 8, 7]
    })
    df_lastrow = pd.DataFrame({
        "Volume": [80000],
        "Close": [120],
        "High": [111]
    })
    df = pd.concat([df]*46, ignore_index=True)
    screenDict = {"Breakout":""}
    saveDict = {"Breakout": ""}
    assert tools_instance.findPotentialBreakout(df, screenDict, saveDict, daysToLookback) == False
    assert saveDict["Breakout"] == ""

    df = pd.concat([df, df_lastrow], axis=0)
    screenDict = {"Breakout":""}
    saveDict = {"Breakout": "125.0"}
    assert tools_instance.findPotentialBreakout(df, screenDict, saveDict, daysToLookback) == True
    assert saveDict["Breakout"] == "125.0(Potential)"
    assert screenDict["Breakout"] == colorText.GREEN + " (Potential)" + colorText.END

def test_negative_case_findPotentialBreakout(tools_instance):
    df = pd.DataFrame({
        "Volume": [100000, 90000, 80000, 70000, 60000],
        "Close": [6, 7, 8, 9, 10],
        "High": [7, 8, 9, 10, 11]
    })
    screenDict = {}
    saveDict = {"Breakout": ""}
    daysToLookback = 30
    assert tools_instance.findPotentialBreakout(df, screenDict, saveDict, daysToLookback) == False
    assert saveDict["Breakout"] == ""

def test_empty_dataframe_findPotentialBreakout(tools_instance):
    df = pd.DataFrame()
    screenDict = {}
    saveDict = {"Breakout": ""}
    daysToLookback = 30
    assert tools_instance.findPotentialBreakout(df, screenDict, saveDict, daysToLookback) == False
    assert saveDict["Breakout"] == ""

def test_dataframe_with_nan_findPotentialBreakout(tools_instance):
    df = pd.DataFrame({
        "Volume": [100000, 90000, np.nan, 70000, 60000],
        "Close": [10, 9, np.nan, 7, 6],
        "High": [11, 10, np.nan, 8, 7]
    })
    screenDict = {}
    saveDict = {"Breakout": ""}
    daysToLookback = 30
    assert tools_instance.findPotentialBreakout(df, screenDict, saveDict, daysToLookback) == False
    assert saveDict["Breakout"] == ""

def test_dataframe_with_inf_findPotentialBreakout(tools_instance):
    df = pd.DataFrame({
        "Volume": [100000, 90000, np.inf, 70000, 60000],
        "Close": [10, 9, np.inf, 7, 6],
        "High": [11, 10, np.inf, 8, 7]
    })
    screenDict = {}
    saveDict = {"Breakout": ""}
    daysToLookback = 30
    assert tools_instance.findPotentialBreakout(df, screenDict, saveDict, daysToLookback) == False
    assert saveDict["Breakout"] == ""

def test_positive_case_validateBullishForTomorrow(tools_instance):
    df = pd.DataFrame({
        "Close": [10, 11, 12, 13, 14],
    })
    assert tools_instance.validateBullishForTomorrow(df) == False

def test_negative_case_validateBullishForTomorrow(tools_instance):
    df = pd.DataFrame({
        "Close": [14, 13, 12, 11, 10],
    })
    assert tools_instance.validateBullishForTomorrow(df) == False

def test_empty_dataframe_validateBullishForTomorrow(tools_instance):
    df = pd.DataFrame()
    assert tools_instance.validateBullishForTomorrow(df) == False

def test_dataframe_with_nan_validateBullishForTomorrow(tools_instance):
    df = pd.DataFrame({
        "Close": [10, 11, np.nan, 13, 14],
    })
    assert tools_instance.validateBullishForTomorrow(df) == False

def test_dataframe_with_inf_validateBullishForTomorrow(tools_instance):
    df = pd.DataFrame({
        "Close": [10, 11, np.inf, 13, 14],
    })
    assert tools_instance.validateBullishForTomorrow(df) == False

def test_validateHigherHighsHigherLowsHigherClose_invalid_input(tools_instance):
    # Create a sample DataFrame for testing
    df = pd.DataFrame({'High': [10, 15, 20, 25,10, 15, 20, 25],
                       'Low': [5, 10, 15, 20,5, 10, 15, 20],
                       'Close': [12, 18, 22, 28,12, 18, 22, 28]})

    # Call the validateHigherHighsHigherLowsHigherClose function with the sample DataFrame
    assert tools_instance.validateHigherHighsHigherLowsHigherClose(df) == False

def test_validateHigherHighsHigherLowsHigherClose_valid_input(tools_instance):
    # Create a sample DataFrame with invalid data
    df = pd.DataFrame({'High': [25, 20, 15, 10,5, 15, 20, 25],
                       'Low': [25, 20, 15, 10,5, 10, 15, 20],
                       'Close': [25, 20, 15, 10,5, 18, 22, 28]})
    df = pd.concat([df]*20, ignore_index=True)
    # Call the validateHigherHighsHigherLowsHigherClose function with the invalid DataFrame
    assert tools_instance.validateHigherHighsHigherLowsHigherClose(df) == True


def test_validateHigherHighsHigherLowsHigherClose_empty_input(tools_instance):
    # Create an empty DataFrame for testing
    df = pd.DataFrame(data=[1,2,3,4],columns=["A"])

    # Call the validateHigherHighsHigherLowsHigherClose function with the empty DataFrame
    with pytest.raises(KeyError):
        tools_instance.validateHigherHighsHigherLowsHigherClose(df)

def test_validateHigherHighsHigherLowsHigherClose_insufficient_data(tools_instance):
    # Create a DataFrame with less than the required number of days
    df = pd.DataFrame({'High': [10, 15],
                       'Low': [5, 10],
                       'Close': [12, 18]})

    # Call the validateHigherHighsHigherLowsHigherClose function with the insufficient DataFrame
    assert tools_instance.validateHigherHighsHigherLowsHigherClose(df) == False

def test_validateHigherHighsHigherLowsHigherClose_exception(tools_instance):
    # Create a DataFrame with invalid data that will raise an exception
    df = pd.DataFrame({'High': ['a', 'b', 'c','c'],
                       'Low': ['d', 'e', 'f','f'],
                       'Close': ['g', 'h', 'i','i']})

    # Call the validateHigherHighsHigherLowsHigherClose function with the invalid DataFrame
    with pytest.raises(Exception):
        tools_instance.validateHigherHighsHigherLowsHigherClose(df)


def test_validateInsideBar_valid_input(tools_instance):
    # Create a sample DataFrame for testing
    df = pd.DataFrame({'High': [10, 15, 20, 25, 50, 35, 40, 45, 50],
                       'Low': [45, 40, 35, 30, 25, 30, 35, 40, 45],
                       'Open': [12, 18, 22, 28, 32, 44, 42, 43, 44],
                       'Close': [32, 38, 32, 28, 32, 38, 42, 48, 52]})
    saveDict = {"Trend":"Weak Up","MA-Signal":"50MA-Support"}
    # Define the expected pattern
    expected_pattern = 'Inside Bar (5)'

    # Call the validateInsideBar function with the sample DataFrame and expected pattern
    result = tools_instance.validateInsideBar(df, {}, saveDict, chartPattern=1, daysToLookback=5)

    # Assert that the returned pattern matches the expected pattern
    assert result == 5
    assert saveDict["Pattern"] == expected_pattern
    result = tools_instance.validateInsideBar(df, {}, saveDict, chartPattern=2, daysToLookback=5)
    assert result == 0
    saveDict = {"Trend":"Weak Up","MA-Signal":"50MA-Resist"}
    result = tools_instance.validateInsideBar(df, {}, saveDict, chartPattern=1, daysToLookback=5)
    assert result == 0
    saveDict = {"Trend":"Weak Down","MA-Signal":"50MA-Resist"}
    result = tools_instance.validateInsideBar(df, {}, saveDict, chartPattern=2, daysToLookback=5)

    # Assert that the returned pattern matches the expected pattern
    assert result == 5
    assert saveDict["Pattern"] == expected_pattern
    
    saveDict = {"Trend":"Weak Down","MA-Signal":"50MA-Support"}
    result = tools_instance.validateInsideBar(df, {}, saveDict, chartPattern=2, daysToLookback=5)
    assert result == 0
    assert tools_instance.validateInsideBar(df, {}, saveDict, chartPattern=2, daysToLookback=-1) == 0

def test_validateInsideBar_invalid_input(tools_instance):
    # Create a sample DataFrame with invalid data
    df = pd.DataFrame({'High': [10, 15, 20, 25, 30, 35, 40, 45, 50],
                       'Low': [45, 40, 35, 30, 25, 30, 35, 40, 45],
                       'Open': [12, 18, 22, 28, 32, 38, 42, 48, 52],
                       'Close': [32, 38, 32, 28, 32, 38, 42, 48, 52]})
    saveDict = {"Trend":"Weak Up","MA-Signal":"50MA-Support"}
    # Call the validateInsideBar function with the invalid DataFrame
    result = tools_instance.validateInsideBar(df, {}, saveDict, chartPattern=1, daysToLookback=5)

    # Assert that the returned pattern is not the expected pattern
    assert result != 5

def test_validateInsideBar_empty_input(tools_instance):
    # Create an empty DataFrame for testing
    df = pd.DataFrame(data=[1,2,3,4],columns=["A"])

    # Call the validateInsideBar function with the empty DataFrame
    with pytest.raises(KeyError):
        tools_instance.validateInsideBar(df, {}, {}, chartPattern=1, daysToLookback=5)

def test_validateInsideBar_insufficient_data(tools_instance):
    # Create a DataFrame with less than the required number of days
    df = pd.DataFrame({'High': [10, 15, 20],
                       'Low': [5, 10, 15],
                       'Open': [12, 18, 22],
                       'Close': [12, 18, 22]})

    # Call the validateInsideBar function with the insufficient DataFrame
    with pytest.raises(KeyError):
        tools_instance.validateInsideBar(df, {}, {}, chartPattern=1, daysToLookback=5)

def test_validateInsideBar_exception(tools_instance):
    # Create a DataFrame with invalid data that will raise an exception
    df = pd.DataFrame({'High': ['a', 'b', 'c'],
                       'Low': ['d', 'e', 'f'],
                       'Open': ['g', 'h', 'i'],
                       'Close': ['j', 'k', 'l']})

    # Call the validateInsideBar function with the invalid DataFrame
    with pytest.raises(Exception):
        tools_instance.validateInsideBar(df, {}, {}, chartPattern=1, daysToLookback=5)

def test_validateIpoBase_valid_input(tools_instance):
    # Create a sample DataFrame for testing
    df = pd.DataFrame({'Open': [10, 15, 20, 12],
                       'Close': [12, 18, 22, 28],
                       'High': [12, 15, 12, 15]})
    saveDict = {}
    # Call the validateIpoBase function with the sample DataFrame
    result = tools_instance.validateIpoBase('stock', df, {}, saveDict, percentage=0.3)
    # Assert that the function returns True
    assert result == True
    assert saveDict["Pattern"] == 'IPO Base (0.0 %)'
    df = pd.DataFrame({'Open': [10, 15, 20, 12],
                       'Close': [12.1, 18, 22, 28],
                       'High': [12, 15, 12, 15]})
    result = tools_instance.validateIpoBase('stock', df, {}, saveDict, percentage=0.3)
    # Assert that the function returns True
    assert result == True
    assert saveDict["Pattern"] == 'IPO Base (0.0 %), IPO Base (0.8 %)'

def test_validateIpoBase_invalid_input(tools_instance):
    # Create a sample DataFrame with invalid data
    df = pd.DataFrame({'Open': [10, 15, 20, 25],
                       'Close': [30, 35, 40, 45],
                       'High': [30, 35, 40, 45]})

    # Call the validateIpoBase function with the invalid DataFrame
    result = tools_instance.validateIpoBase('stock', df, {}, {}, percentage=0.3)

    # Assert that the function returns False
    assert result == False
    df = pd.DataFrame({'Open': [13, 15, 20, 13],
                       'Close': [8.1, 18, 22, 28],
                       'High': [12, 15, 12, 15]})
    assert tools_instance.validateIpoBase('stock', df, {}, {}, percentage=0.3) == False

def test_validateIpoBase_empty_input(tools_instance):
    # Create an empty DataFrame for testing
    df = pd.DataFrame(data=[1,2,3,4],columns=["A"])

    # Call the validateIpoBase function with the empty DataFrame
    with pytest.raises(KeyError):
        tools_instance.validateIpoBase('stock', df, {}, {}, percentage=0.3)

def test_validateIpoBase_exception(tools_instance):
    # Create a DataFrame with invalid data that will raise an exception
    df = pd.DataFrame({'Open': ['a', 'b', 'c'],
                       'Close': ['d', 'e', 'f'],
                       'High': ['g', 'h', 'i']})

    # Call the validateIpoBase function with the invalid DataFrame
    with pytest.raises(Exception):
        tools_instance.validateIpoBase('stock', df, {}, {}, percentage=0.3)

def test_validateLorentzian_buy_signal(tools_instance):
    # Create a sample DataFrame with a buy signal
    df = pd.DataFrame({'Open': [10, 15, 20, 25],
                       'Close': [12, 18, 22, 28],
                       'High': [12, 18, 22, 28],
                       'Low': [8, 12, 16, 20],
                       'Volume': [100, 200, 300, 400]})

    # Call the validateLorentzian function with the sample DataFrame and lookFor=1 (Buy)
    screenDict = {}
    saveDict = {}
    mock_lc = MagicMock()
    with patch("advanced_ta.LorentzianClassification") as mock_lc:
        mock_lc.return_value = mock_lc
        mock_lc.df = pd.DataFrame([{"isNewSellSignal":False,"isNewBuySignal":True}])
        result = tools_instance.validateLorentzian(df, screenDict, saveDict, lookFor=1)
        # Assert that the function returns True and sets the appropriate screenDict and saveDict values
        assert result == True
        assert screenDict["Pattern"] == (colorText.GREEN + "Lorentzian-Buy" + colorText.END)
        assert saveDict["Pattern"] == "Lorentzian-Buy"
        assert tools_instance.validateLorentzian(df, screenDict, saveDict, lookFor=2) == False

def test_validateLorentzian_sell_signal(tools_instance):
    # Create a sample DataFrame with a sell signal
    df = pd.DataFrame({'Open': [10, 15, 20, 25],
                       'Close': [12, 18, 22, 28],
                       'High': [12, 18, 22, 28],
                       'Low': [8, 12, 16, 20],
                       'Volume': [100, 200, 300, 400]})

    # Call the validateLorentzian function with the sample DataFrame and lookFor=2 (Sell)
    screenDict = {}
    saveDict = {}
    mock_lc = MagicMock()
    with patch("advanced_ta.LorentzianClassification") as mock_lc:
        mock_lc.return_value = mock_lc
        mock_lc.df = pd.DataFrame([{"isNewSellSignal":True,"isNewBuySignal":False}])
        result = tools_instance.validateLorentzian(df, screenDict, saveDict, lookFor=2)
        # Assert that the function returns True and sets the appropriate screenDict and saveDict values
        assert result == True
        assert screenDict["Pattern"] == (colorText.FAIL + "Lorentzian-Sell" + colorText.END)
        assert saveDict["Pattern"] == "Lorentzian-Sell"
        assert tools_instance.validateLorentzian(df, screenDict, saveDict, lookFor=1) == False
        mock_lc.df = pd.DataFrame([{"isNewSellSignal":False,"isNewBuySignal":False}])
        assert tools_instance.validateLorentzian(df, screenDict, saveDict, lookFor=1) == False

def test_validateLorentzian_no_signal(tools_instance):
    # Create a sample DataFrame without any signals
    df = pd.DataFrame({'Open': [10, 15, 20, 25],
                       'Close': [12, 18, 22, 28],
                       'High': [12, 18, 22, 28],
                       'Low': [8, 12, 16, 20],
                       'Volume': [100, 200, 300, 400]})

    # Call the validateLorentzian function with the sample DataFrame and lookFor=3 (Any)
    screenDict = {}
    saveDict = {}
    result = tools_instance.validateLorentzian(df, screenDict, saveDict, lookFor=3)

    # Assert that the function returns False and does not modify screenDict and saveDict
    assert result == False
    assert screenDict == {}
    assert saveDict == {}

def test_validateLorentzian_exception(tools_instance):
    # Create a sample DataFrame that raises an exception
    df = pd.DataFrame({'Open': ['a', 'b', 'c', 'd'],
                       'Close': ['e', 'f', 'g', 'h'],
                       'High': ['i', 'j', 'k', 'l'],
                       'Low': ['m', 'n', 'o', 'p'],
                       'Volume': ['q', 'r', 's', 't']})

    # Call the validateLorentzian function with the invalid DataFrame
    screenDict = {}
    saveDict = {}
    result = tools_instance.validateLorentzian(df, screenDict, saveDict, lookFor=3)

    # Assert that the function returns False and does not modify screenDict and saveDict
    assert result == False
    assert screenDict == {}
    assert saveDict == {}

def test_validateLowerHighsLowerLows_valid_input(tools_instance):
    # Create a sample DataFrame with lower highs, lower lows, and higher RSI
    df = pd.DataFrame({'High': [7, 8, 9, 10],
                       'Low': [2, 3, 4, 5],
                       'RSI': [50, 55, 60, 65]})

    # Call the validateLowerHighsLowerLows function with the sample DataFrame
    result = tools_instance.validateLowerHighsLowerLows(df)

    # Assert that the function returns True
    assert result == True

def test_validateLowerHighsLowerLows_invalid_input(tools_instance):
    # Create a sample DataFrame without lower highs or lower lows
    df = pd.DataFrame({'High': [10, 12, 8, 7],
                       'Low': [5, 6, 3, 2],
                       'RSI': [60, 55, 50, 45]})

    # Call the validateLowerHighsLowerLows function with the sample DataFrame
    result = tools_instance.validateLowerHighsLowerLows(df)

    # Assert that the function returns False
    assert result == False

def test_validateLowerHighsLowerLows_no_higher_RSI(tools_instance):
    # Create a sample DataFrame without higher RSI
    df = pd.DataFrame({'High': [10, 9, 8, 7],
                       'Low': [5, 4, 3, 2],
                       'RSI': [40, 35, 30, 25]})

    # Call the validateLowerHighsLowerLows function with the sample DataFrame
    result = tools_instance.validateLowerHighsLowerLows(df)

    # Assert that the function returns False
    assert result == False

def test_validateLowerHighsLowerLows_empty_input(tools_instance):
    # Create an empty DataFrame for testing
    df = pd.DataFrame(data=[1,2,3,4],columns=["A"])

    # Call the validateLowerHighsLowerLows function with the empty DataFrame
    with pytest.raises(KeyError):
        tools_instance.validateLowerHighsLowerLows(df)

def test_validateLowerHighsLowerLows_insufficient_data(tools_instance):
    # Create a DataFrame with less than the required number of days
    df = pd.DataFrame({'High': [10, 9],
                       'Low': [5, 4],
                       'RSI': [60, 55]})

    # Call the validateLowerHighsLowerLows function with the insufficient DataFrame
    assert tools_instance.validateLowerHighsLowerLows(df) == False

def test_validateLowerHighsLowerLows_exception(tools_instance):
    # Create a DataFrame with invalid data that will raise an exception
    df = pd.DataFrame({'High': ['a', 'b', 'c', 'd'],
                       'Low': ['e', 'f', 'g', 'h'],
                       'RSI': ['i', 'j', 'k', 'l']})

    # Call the validateLowerHighsLowerLows function with the invalid DataFrame
    with pytest.raises(Exception):
        tools_instance.validateLowerHighsLowerLows(df)

def test_validateLowestVolume_valid_input(tools_instance):
    # Create a sample DataFrame with lowest volume
    df = pd.DataFrame({'Volume': [70, 80, 90, 100, 110, 120, 130]})

    # Call the validateLowestVolume function with the sample DataFrame and daysForLowestVolume=7
    result = tools_instance.validateLowestVolume(df, daysForLowestVolume=7)

    # Assert that the function returns True
    assert result == True

def test_validateLowestVolume_invalid_input(tools_instance):
    # Create a sample DataFrame without lowest volume
    df = pd.DataFrame({'Volume': [100, 200, 150, 120, 80, 90, 110]})

    # Call the validateLowestVolume function with the sample DataFrame and daysForLowestVolume=7
    result = tools_instance.validateLowestVolume(df, daysForLowestVolume=7)

    # Assert that the function returns False
    assert result == False

def test_validateLowestVolume_empty_input(tools_instance):
    # Create an empty DataFrame for testing
    df = pd.DataFrame()

    # Call the validateLowestVolume function with the empty DataFrame
    assert tools_instance.validateLowestVolume(df, daysForLowestVolume=7) == False

def test_validateLowestVolume_insufficient_data(tools_instance):
    # Create a DataFrame with less than the required number of days
    df = pd.DataFrame({'Volume': [100, 200]})

    # Call the validateLowestVolume function with the insufficient DataFrame
    assert tools_instance.validateLowestVolume(df, daysForLowestVolume=7) == False

def test_validateLowestVolume_nan_value(tools_instance):
    # Create a sample DataFrame with NaN value in Volume
    df = pd.DataFrame({'Volume': [100, 200, np.nan, 120, 80, 90, 70]})

    # Call the validateLowestVolume function with the sample DataFrame and daysForLowestVolume=7
    result = tools_instance.validateLowestVolume(df, daysForLowestVolume=7)

    # Assert that the function returns False
    assert result == False

def test_validateLowestVolume_none_value(tools_instance):
    # Create a sample DataFrame with NaN value in Volume
    df = pd.DataFrame({'Volume': [100, 200, np.nan, 120, 80, 90, 70]})

    # Call the validateLowestVolume function with the sample DataFrame and daysForLowestVolume=7
    result = tools_instance.validateLowestVolume(df, daysForLowestVolume=None)

    # Assert that the function returns False
    assert result == False

def test_validateLowestVolume_exception(tools_instance):
    # Create a DataFrame with invalid data that will raise an exception
    df = pd.DataFrame({'Volume': ['a', 'b', 'c', 'd', 'e', 'f', 'g']})

    # Call the validateLowestVolume function with the invalid DataFrame
    with pytest.raises(Exception):
        tools_instance.validateLowestVolume(df, daysForLowestVolume=7)

def test_validateLTP_valid_input(tools_instance):
    # Create a sample DataFrame with a valid LTP
    df = pd.DataFrame({'Close': [10, 15, 20, 25]})

    # Call the validateLTP function with the sample DataFrame and minLTP=10, maxLTP=25
    screenDict = {}
    saveDict = {}
    result, verifyStageTwo = tools_instance.validateLTP(df, screenDict, saveDict, minLTP=10, maxLTP=25)

    # Assert that the function returns True for ltpValid and True for verifyStageTwo
    assert result == True
    assert verifyStageTwo == True
    assert saveDict["LTP"] == 10
    assert screenDict["LTP"] == (colorText.GREEN + "10.00" + colorText.END)

def test_validateLTP_invalid_input(tools_instance):
    # Create a sample DataFrame with an invalid LTP
    df = pd.DataFrame({'Close': [10, 15, 20, 25]})

    # Call the validateLTP function with the sample DataFrame and minLTP=30, maxLTP=40
    screenDict = {}
    saveDict = {}
    result, verifyStageTwo = tools_instance.validateLTP(df, screenDict, saveDict, minLTP=30, maxLTP=40)

    # Assert that the function returns False for ltpValid and True for verifyStageTwo
    assert result == False
    assert verifyStageTwo == True
    assert saveDict["LTP"] == 10
    assert screenDict["LTP"] == (colorText.FAIL + "10.00" + colorText.END)

def test_validateLTP_verifyStageTwo(tools_instance):
    # Create a sample DataFrame with more than 250 rows and an invalid LTP for verifyStageTwo
    df = pd.DataFrame({'Close': [10, 15, 20, 25] * 100})

    # Call the validateLTP function with the sample DataFrame and minLTP=10, maxLTP=25
    screenDict = {}
    saveDict = {"Stock":"SomeStock"}
    result, verifyStageTwo = tools_instance.validateLTP(df, screenDict, saveDict, minLTP=10, maxLTP=25)

    # Assert that the function returns True for ltpValid and False for verifyStageTwo
    assert result == True
    assert verifyStageTwo == False
    assert saveDict["LTP"] == 10
    assert screenDict["LTP"] == (colorText.GREEN + "10.00" + colorText.END)
    assert screenDict["Stock"] == (colorText.FAIL + saveDict["Stock"] + colorText.END)

def test_validateLTP_empty_input(tools_instance):
    # Create an empty DataFrame for testing
    df = pd.DataFrame()

    # Call the validateLTP function with the empty DataFrame
    with pytest.raises(KeyError):
        tools_instance.validateLTP(df, {}, {}, minLTP=10, maxLTP=25)

def test_validateLTP_exception(tools_instance):
    # Create a DataFrame with invalid data that will raise an exception
    df = pd.DataFrame({'Close': ['a', 'b', 'c', 'd']})

    # Call the validateLTP function with the invalid DataFrame
    with pytest.raises(Exception):
        tools_instance.validateLTP(df, {}, {}, minLTP=10, maxLTP=25)

def test_findUptrend_valid_input_downtrend(tools_instance):
    # Create a sample DataFrame with an uptrend
    df = pd.DataFrame({'Close': [10, 15, 20, 25, 30, 35, 40, 45, 50]*50})
    screenDict = {"Trend":""}
    saveDict = {"Trend":""}
    result = tools_instance.findUptrend(df, screenDict, saveDict, testing=False,stock="SBIN")
    assert result == (False,ANY,0)
    assert f"T:{colorText.DOWNARROW}" in saveDict["Trend"]
    assert f"T:{colorText.DOWNARROW}" in screenDict["Trend"]

def test_findUptrend_uptrend(tools_instance):
    # Create a sample DataFrame with a downtrend
    df = pd.DataFrame({'Close': [50, 45, 40, 35, 30, 25, 20, 15, 10]*50})

    # Call the findUptrend function with the sample DataFrame
    screenDict = {"Trend":""}
    saveDict = {"Trend":""}
    result = tools_instance.findUptrend(df, screenDict, saveDict, testing=False,stock="SBIN")

    # Assert that the function returns False and sets the appropriate screenDict and saveDict values
    assert result == (True,ANY,0)
    assert f"T:{colorText.UPARROW}" in saveDict["Trend"]
    assert f"T:{colorText.UPARROW}" in screenDict["Trend"]

def test_findUptrend_empty_input(tools_instance):
    # Create an empty DataFrame for testing
    df = pd.DataFrame()
    # Call the findUptrend function with the empty DataFrame
    result = tools_instance.findUptrend(df, {"Trend":""}, {"Trend":""}, testing=False,stock="SBIN")
    # Assert that the function returns False
    assert result == (False,ANY,0)

def test_findUptrend_insufficient_data(tools_instance):
    # Create a DataFrame with less than 300 rows
    df = pd.DataFrame({'Close': [10, 15, 20, 25]})

    # Call the findUptrend function with the insufficient DataFrame
    result = tools_instance.findUptrend(df, {"Trend":""}, {"Trend":""}, testing=False,stock="SBIN")

    # Assert that the function returns False
    assert result == (False,ANY,0)

def test_findUptrend_testing_mode(tools_instance):
    # Create a sample DataFrame
    df = pd.DataFrame({'Close': [10, 15, 20, 25, 30, 35, 40, 45, 50]})

    # Call the findUptrend function with testing=True
    result = tools_instance.findUptrend(df, {"Trend":""}, {"Trend":""}, testing=True,stock="SBIN")

    # Assert that the function returns False
    assert result == (False,ANY,0)

def test_findUptrend_exception(tools_instance):
    # Create a DataFrame with invalid data that will raise an exception
    df = pd.DataFrame({'Close': ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']})

    # Call the findUptrend function with the invalid DataFrame
    assert tools_instance.findUptrend(df, {"Trend":""}, {"Trend":""}, testing=False,stock="SBIN") == (False,ANY,0)

# # Positive test case for validateBullishForTomorrow function
# def test_validateBullishForTomorrow_positive(tools_instance):
#     # Mocking the data
#     data = pd.DataFrame({'High': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200],
#                          'Open': [200, 190, 180, 170, 160, 150, 140, 130, 120, 110, 100, 90, 80, 70, 60, 50, 40, 30, 20, 10],
#                          'Close': [200, 190, 180, 170, 160, 150, 140, 130, 120, 110, 100, 90, 80, 70, 60, 50, 40, 30, 20, 10],
#                          'Low': [200, 190, 180, 170, 160, 150, 140, 130, 120, 110, 100, 90, 80, 70, 60, 50, 40, 30, 20, 10],
#                          'Volume': [200, 190, 180, 170, 160, 150, 140, 130, 120, 110, 100, 90, 80, 70, 60, 50, 40, 30, 20, 10],})

#     # Call the function and assert the result
#     assert tools_instance.validateBullishForTomorrow(data) == True

def test_validateCCI():
    tool = ScreeningStatistics(None, None)
    # Test case 1: CCI within specified range and trend is Up
    df = pd.DataFrame({'CCI': [50]})
    screenDict = {}
    saveDict = {}
    minCCI = 40
    maxCCI = 60
    assert tool.validateCCI(df, screenDict, saveDict, minCCI, maxCCI) == False
    assert screenDict['CCI'] == colorText.FAIL + '50' + colorText.END

    # Test case 2: CCI below minCCI and trend is Up
    df = pd.DataFrame({'CCI': [30]})
    screenDict = {}
    saveDict = {"Trend":"Weak Up"}
    minCCI = 20
    maxCCI = 60
    assert tool.validateCCI(df, screenDict, saveDict, minCCI, maxCCI) == True
    assert screenDict['CCI'] == colorText.GREEN + '30' + colorText.END

    # Test case 3: CCI above maxCCI and trend is Up
    df = pd.DataFrame({'CCI': [70]})
    screenDict = {}
    saveDict = {"Trend":"Weak Up"}
    minCCI = 20
    maxCCI = 60
    assert tool.validateCCI(df, screenDict, saveDict, minCCI, maxCCI) == False
    assert screenDict['CCI'] == colorText.FAIL + '70' + colorText.END

    # Test case 4: CCI within specified range and trend is not Up
    df = pd.DataFrame({'CCI': [50]})
    screenDict = {}
    saveDict = {}
    minCCI = 40
    maxCCI = 60
    saveDict['Trend'] = 'Down'
    assert tool.validateCCI(df, screenDict, saveDict, minCCI, maxCCI) == True
    assert screenDict['CCI'] == colorText.FAIL + '50' + colorText.END

    df = pd.DataFrame({'CCI': [70]})
    screenDict = {}
    saveDict = {"Trend":"Weak Down"}
    minCCI = 40
    maxCCI = 60
    assert tool.validateCCI(df, screenDict, saveDict, minCCI, maxCCI) == False
    assert screenDict['CCI'] == colorText.FAIL + '70' + colorText.END

def test_validateConfluence():
    tool = ScreeningStatistics(None, None)
    # Test case 1: SMA and LMA are within specified percentage and SMA is greater than LMA
    df = pd.DataFrame({'SMA': [50], 'LMA': [45], 'Close': [100]})
    screenDict = {}
    saveDict = {}
    percentage = 0.1
    assert tool.validateConfluence(None, df, screenDict, saveDict, percentage) == False

    # Test case 2: SMA and LMA are within specified percentage and SMA is less than LMA
    df = pd.DataFrame({'SMA': [50], 'LMA': [45], 'Close': [100]})
    screenDict = {}
    saveDict = {}
    percentage = 0.1
    assert tool.validateConfluence(None, df, screenDict, saveDict, percentage) == False
    # assert screenDict['MA-Signal'] == colorText.GREEN + 'Confluence (5.0%)' + colorText.END

    # Test case 3: SMA and LMA are not within specified percentage
    df = pd.DataFrame({'SMA': [50], 'LMA': [60], 'Close': [100]})
    screenDict = {}
    saveDict = {}
    percentage = 0.1
    assert tool.validateConfluence(None, df, screenDict, saveDict, percentage) == False

    # Test case 4: SMA and LMA are equal
    df = pd.DataFrame({'SMA': [50], 'LMA': [50], 'Close': [100]})
    screenDict = {}
    saveDict = {}
    percentage = 0.1
    assert tool.validateConfluence(None, df, screenDict, saveDict, percentage) == False
    # assert screenDict['MA-Signal'] == colorText.GREEN + 'Confluence (0.0%)' + colorText.END

    df = pd.DataFrame({'SMA': [45], 'LMA': [49], 'Close': [100]})
    screenDict = {}
    saveDict = {}
    percentage = 0.1
    assert tool.validateConfluence(None, df, screenDict, saveDict, percentage) == False
    # assert screenDict['MA-Signal'] == colorText.FAIL + 'Confluence (4.0%)' + colorText.END

def test_validateConsolidation():
    tool = ScreeningStatistics(None, None)
    # Test case 1: High and low close prices within specified percentage
    df = pd.DataFrame({'Close': [100, 95]})
    screenDict = {}
    saveDict = {}
    percentage = 10
    assert tool.validateConsolidation(df, screenDict, saveDict, percentage) == 5.0
    assert screenDict['Consol.'] == colorText.GREEN + 'Range:5.0%' + colorText.END

    # Test case 2: High and low close prices not within specified percentage
    df = pd.DataFrame({'Close': [100, 80]})
    screenDict = {}
    saveDict = {}
    percentage = 10
    assert tool.validateConsolidation(df, screenDict, saveDict, percentage) == 20.0
    assert screenDict['Consol.'] == colorText.FAIL + 'Range:20.0%' + colorText.END

    # Test case 3: High and low close prices are equal
    df = pd.DataFrame({'Close': [100, 100]})
    screenDict = {}
    saveDict = {}
    percentage = 10
    assert tool.validateConsolidation(df, screenDict, saveDict, percentage) == 0.0
    assert screenDict['Consol.'] == colorText.FAIL + 'Range:0.0%' + colorText.END

# # Positive test case for validateInsideBar function
# def test_validateInsideBar_positive():
#     # Mocking the data
#     data = MagicMock()
#     data.tail().iloc[0].return_value = 100
#     data.tail().iloc[1].return_value = 90
#     data.tail().iloc[2].return_value = 80
#     data.tail().iloc[3].return_value = 70
#     data.tail().iloc[4].return_value = 60
#     data.tail().iloc[5].return_value = 50
#     data.tail().iloc[6].return_value = 40
#     data.tail().iloc[7].return_value = 30
#     data.tail().iloc[8].return_value = 20
#     data.tail().iloc[9].return_value = 10

#     # Create an instance of the tools class
#     tool = tools(None, None)

#     # Call the function and assert the result
#     assert tool.validateInsideBar(data, {}, {}, 1, 10) == 1

# # Negative test case for validateInsideBar function
# def test_validateInsideBar_negative():
#     # Mocking the data
#     data = MagicMock()
#     data.tail().iloc[0].return_value = 100
#     data.tail().iloc[1].return_value = 90
#     data.tail().iloc[2].return_value = 80
#     data.tail().iloc[3].return_value = 70
#     data.tail().iloc[4].return_value = 60
#     data.tail().iloc[5].return_value = 50
#     data.tail().iloc[6].return_value = 40
#     data.tail().iloc[7].return_value = 30
#     data.tail().iloc[8].return_value = 20
#     data.tail().iloc[9].return_value = 5

#     # Create an instance of the tools class
#     tool = tools(None, None)

#     # Call the function and assert the result
#     assert tool.validateInsideBar(data, {}, {}, 1, 10) == 0

# # Positive test case for validateIpoBase function
# def test_validateIpoBase_positive():
#     # Mocking the data
#     data = MagicMock()
#     data[::-1].head.return_value =()
#     data[::-1].min()["Close"].return_value = 100
#     data[::-1].max()["Close"].return_value = 200
#     data.head().iloc[0].return_value = 150

#     # Create an instance of the tools class
#     tool = tools(None, None)

#     # Call the function and assert the result
#     assert tool.validateIpoBase(None, data, {}, {}, 0.3) == True

# # Negative test case for validateIpoBase function
# def test_validateIpoBase_negative():
#     # Mocking the data
#     data = MagicMock()
#     data[::-1].head.return_value = MagicMock()
#     data[::-1].min()["Close"].return_value = 100
#     data[::-1].max()["Close"].return_value = 200
#     data.head().iloc[0].return_value = 250

#     # Create an instance of the tools class
#     tool = tools(None, None)

#     # Call the function and assert the result
#     assert tool.validateIpoBase(None, data, {}, {}, 0.3) == False

# # Positive test case for validateLowestVolume function
# def test_validateLowestVolume_positive():
#     # Mocking the data
#     data = MagicMock()
#     data.describe()["Volume"]["min"].return_value = 100
#     data.head().iloc[0].return_value = 100

#     # Create an instance of the tools class
#     tool = tools(None, None)

#     # Call the function and assert the result
#     assert tool.validateLowestVolume(data, 10) == True

# # Negative test case for validateLowestVolume function
# def test_validateLowestVolume_negative():
#     # Mocking the data
#     data = MagicMock()
#     data.describe()["Volume"]["min"].return_value = 100
#     data.head().iloc[0].return_value = 200

#     # Create an instance of the tools class
#     tool = tools(None, None)

#     # Call the function and assert the result
#     assert tool.validateLowestVolume(data, 10) == False


# Positive test case for validateLTP function
def test_validateLTP_positive(tools_instance):
    data = pd.DataFrame({"Close": [100, 110, 120]})
    screenDict = {}
    saveDict = {}
    result, verifyStageTwo = tools_instance.validateLTP(
        data, screenDict, saveDict, minLTP=100, maxLTP=120
    )
    assert result == True
    assert verifyStageTwo == True
    assert screenDict["LTP"] == "\x1b[32m100.00\x1b[0m"
    assert saveDict["LTP"] == 100


# Negative test case for validateLTP function
def test_validateLTP_negative(tools_instance):
    data = pd.DataFrame({"Close": [90, 95, 100]})
    screenDict = {}
    saveDict = {}
    result, verifyStageTwo = tools_instance.validateLTP(
        data, screenDict, saveDict, minLTP=100, maxLTP=120
    )
    assert result == False
    assert verifyStageTwo == True
    assert screenDict["LTP"] == "\x1b[31m90.00\x1b[0m"
    assert saveDict["LTP"] == 90


# Positive test case for validateMACDHistogramBelow0 function
def test_validateMACDHistogramBelow0_positive(tools_instance):
    data = pd.DataFrame({"Close": [100, 110, 120]})
    result = tools_instance.validateMACDHistogramBelow0(data)
    assert result == False


# # Negative test case for validateMACDHistogramBelow0 function
# def test_validateMACDHistogramBelow0_negative(tools_instance):
#     data = pd.DataFrame({'Close': [100, 90, 80]})
#     result = tools.validateMACDHistogramBelow0(data)
#     assert result == True

# # Positive test case for validateMomentum function
# def test_validateMomentum_positive(tools_instance):
#     data = pd.DataFrame({'Close': [100, 110, 120], 'Open': [90, 100, 110]})
#     screenDict = {}
#     saveDict = {}
#     result = tools_instance.validateMomentum(data, screenDict, saveDict)
#     assert result == True
#     assert screenDict['Pattern'] == '\x1b[1m\x1b[92mMomentum Gainer\x1b[0m'
#     assert saveDict['Pattern'] == 'Momentum Gainer'


# Negative test case for validateMomentum function
def test_validateMomentum_negative(tools_instance):
    data = pd.DataFrame({"Close": [100, 90, 80], "Open": [110, 100, 90]})
    screenDict = {}
    saveDict = {}
    result = tools_instance.validateMomentum(data, screenDict, saveDict)
    assert result == False


# # Positive test case for validateMovingAverages function
# def test_validateMovingAverages_positive(tools_instance):
#     data = pd.DataFrame({'Close': [100, 110, 120], 'SMA': [90, 100, 110], 'LMA': [80, 90, 100]})
#     screenDict = {}
#     saveDict = {}
#     result = tools_instance.validateMovingAverages(data, screenDict, saveDict)
#     assert result == 1
#     assert screenDict['MA-Signal'] == '\x1b[1m\x1b[92mBullish\x1b[0m'

# # Negative test case for validateMovingAverages function
# def test_validateMovingAverages_negative(tools_instance):
#     data = pd.DataFrame({'Close': [100, 90, 80], 'SMA': [110, 100, 90], 'LMA': [120, 110, 100]})
#     screenDict = {}
#     saveDict = {}
#     result = tools_instance.validateMovingAverages(data, screenDict, saveDict)
#     assert result == -1
#     assert screenDict['MA-Signal'] == '\x1b[1m\x1b[91mBearish\x1b[0m'
#     assert saveDict['MA-Signal'] == 'Bearish'

# # Positive test case for validateNarrowRange function
# def test_validateNarrowRange_positive(tools_instance):
#     data = pd.DataFrame({'Close': [100, 110, 120, 130]})
#     screenDict = {}
#     saveDict = {}
#     result = tools_instance.validateNarrowRange(data, screenDict, saveDict, nr=3)
#     assert result == True
#     assert screenDict['Pattern'] == '\x1b[1m\x1b[92mBuy-NR3\x1b[0m'
#     assert saveDict['Pattern'] == 'Buy-NR3'

# # Negative test case for validateNarrowRange function
# def test_validateNarrowRange_negative(tools_instance):
#     data = pd.DataFrame({'Close': [100, 110, 120, 130]})
#     screenDict = {}
#     saveDict = {}
#     result = tools_instance.validateNarrowRange(data, screenDict, saveDict, nr=2)
#     assert result == False


# Positiveed function
def test_validateNewlyListed_positive(tools_instance):
    data = pd.DataFrame({"Close": [100, 110, 120]})
    result = tools_instance.validateNewlyListed(data, daysToLookback="2d")
    assert result == False


# Negative test case for validateNewlyListed function
def test_validateNewlyListed_negative(tools_instance):
    data = pd.DataFrame({"Close": [100]})
    result = tools_instance.validateNewlyListed(data, daysToLookback="2d")
    assert result == True


@pytest.fixture
def mock_data():
    return pd.DataFrame(
        {
            "Close": [100, 105, 110, 115],
            "RSI": [60, 65, 70, 75],
            "FASTK": [30, 40, 50, 60],
            "Open": [95, 100, 105, 110],
            "High": [105, 110, 115, 120],
            "Low": [95, 100, 105, 110],
            "Volume": [1000, 2000, 3000, 4000],
            "VolMA": [1500, 2000, 2500, 3000],
        }
    )


@pytest.fixture
def mock_screen_dict():
    return {}


@pytest.fixture
def mock_save_dict():
    return {}

def test_validatePriceRisingByAtLeast2Percent_positive(mock_data, mock_screen_dict, mock_save_dict, tools_instance):
    mock_data["Close"] = [115, 110, 105, 100]
    assert tools_instance.validatePriceRisingByAtLeast2Percent(mock_data, mock_screen_dict, mock_save_dict) == True
    assert mock_screen_dict["%Chng"] == '\x1b[32m4.5% (4.8%, 5.0%)\x1b[0m'
    assert mock_save_dict["%Chng"] == '4.5% (4.8%, 5.0%)'



def test_validatePriceRisingByAtLeast2Percent_negative(
    mock_data, mock_screen_dict, mock_save_dict, tools_instance
):
    mock_data["Close"] = [100, 105, 110, 112]
    assert (
        tools_instance.validatePriceRisingByAtLeast2Percent(
            mock_data, mock_screen_dict, mock_save_dict
        )
        == False
    )
    assert mock_screen_dict.get("LTP") is None
    assert mock_save_dict.get("LTP") is None


def test_validateRSI_positive(mock_data, mock_screen_dict, mock_save_dict, tools_instance):
    assert tools_instance.validateRSI(mock_data, mock_screen_dict, mock_save_dict, 60, 80) == True
    assert mock_screen_dict["RSI"] == '\x1b[32m60\x1b[0m' 
    assert mock_save_dict["RSI"] == 60

def test_validateRSI_negative(mock_data, mock_screen_dict, mock_save_dict, tools_instance):
    assert tools_instance.validateRSI(mock_data, mock_screen_dict, mock_save_dict, 80, 90) == False
    assert mock_screen_dict["RSI"] == '\x1b[31m60\x1b[0m' 
    assert mock_save_dict["RSI"] == 60

# def test_validateShortTermBullish_positive(mock_data, mock_screen_dict, mock_save_dict, tools_instance):
#     assert tools_instance.validateShortTermBullish(mock_data, mock_screen_dict, mock_save_dict) == True
#     assert mock_screen_dict["MA-Signal"] == "\033[32mBullish\033[0m"
#     assert mock_save_dict["MA-Signal"] == "Bullish"


def test_validateShortTermBullish_negative(
    mock_data, mock_screen_dict, mock_save_dict, tools_instance
):
    mock_data["FASTK"] = [70, 60, 50, 40]
    assert (
        tools_instance.validateShortTermBullish(
            mock_data, mock_screen_dict, mock_save_dict
        )
        == False
    )
    assert mock_screen_dict.get("MA-Signal") is None
    assert mock_save_dict.get("MA-Signal") is None

def test_validateMomentum(tools_instance):
    # Mock the required functions and classes
    patch('pandas.DataFrame.copy')
    patch('pandas.DataFrame.head')
    patch('pandas.DataFrame.iterrows')
    patch('pandas.DataFrame.sort_values')
    patch('pandas.DataFrame.equals')
    patch('pandas.DataFrame.iloc')
    patch('pandas.concat')
    patch('pandas.DataFrame.rename')
    patch('pandas.DataFrame.debug')

    # Create a test case
    df = pd.DataFrame({'Open': [1.1, 2, 3], 'High': [4.1, 5, 6], 'Low': [7.1, 8, 9], 'Close': [10.1, 11, 12], 'Volume': [13, 14, 15]})
    df = pd.concat([df]*150, ignore_index=True)
    screenDict = {}
    saveDict = {}

    # Call the function under test
    result = tools_instance.validateMomentum(df, screenDict, saveDict)

    # Assert the expected behavior
    assert result == False
    # assert screenDict['Pattern'] == '\033[32mMomentum Gainer\033[0m'
    # assert saveDict['Pattern'] == 'Momentum Gainer'

def test_validateLTPForPortfolioCalc(tools_instance):
    # Mock the required functions and classes
    patch('pandas.DataFrame.copy')
    patch('pandas.DataFrame.head')
    patch('pandas.DataFrame.reset_index')
    patch('pandas.DataFrame.iloc')
    patch('pandas.concat')
    patch('pandas.DataFrame.rename')
    patch('pandas.DataFrame.debug')

    # Create a test case
    df = pd.DataFrame({'Open': [1, 2, 3], 'High': [4, 5, 6], 'Low': [7, 8, 9], 'Close': [10, 11, 12], 'Volume': [13, 14, 15]})
    df = pd.concat([df]*150, ignore_index=True)
    screenDict = {}
    saveDict = {}

    # Call the function under test
    result = tools_instance.validateLTPForPortfolioCalc(df, screenDict, saveDict)

    # Assert the expected behavior
    assert result == None
    assert screenDict['LTP1'] == '\033[32m11.00\033[0m'
    assert saveDict['LTP1'] == 11.0

def test_validateNarrowRange(tools_instance):
    # Mock the required functions and classes
    patch('pandas.DataFrame.copy')
    patch('PKDevTools.PKDateUtilities.PKDateUtilities.isTradingTime')
    patch('pandas.DataFrame.head')
    patch('pandas.DataFrame.describe')
    patch('pandas.DataFrame.iloc')
    patch('pandas.concat')
    patch('pandas.DataFrame.rename')
    patch('pandas.DataFrame.debug')

    # Create a test case
    isTrading = PKDateUtilities.isTradingTime()
    closeValue = 10.1 if isTrading else 11
    df = pd.DataFrame({'Open': [1.1, 2, 3], 'High': [4.1, 5, 6], 'Low': [7.1, 8, 9], 'Close': [10.1, closeValue , 12], 'Volume': [13, 14, 15]})
    df = pd.concat([df]*150, ignore_index=True)
    screenDict = {}
    saveDict = {}

    # Call the function under test
    result = tools_instance.validateNarrowRange(df, screenDict, saveDict)

    # Assert the expected behavior
    assert result == True
    assert screenDict['Pattern'] == '\033[32mNR4\033[0m' if not isTrading else "\033[32mBuy-NR4\033[0m"
    assert saveDict['Pattern'] == 'NR4' if not isTrading else "Buy-NR4"

# def test_validateVCP_positive(mock_data, mock_screen_dict, mock_save_dict, tools_instance):
#     # mock_data["High"] = [205, 210, 215, 220]
#     assert tools_instance.validateVCP(mock_data, mock_screen_dict, mock_save_dict, "Stock A", 3, 3) == False
#     assert mock_screen_dict["Pattern"] == "\033[32mVCP (BO: 115.0)\033[0m"
#     assert mock_save_dict["Pattern"] == "VCP (BO: 115.0)"


def test_validateVCP_negative(
    mock_data, mock_screen_dict, mock_save_dict, tools_instance
):
    mock_data["High"] = [105, 110, 115, 120]
    assert (
        tools_instance.validateVCP(
            mock_data, mock_screen_dict, mock_save_dict, "Stock A", 3, 3
        )
        == False
    )
    assert mock_screen_dict.get("Pattern") is None
    assert mock_save_dict.get("Pattern") is None


def test_validateVolume_positive(mock_data, mock_screen_dict, mock_save_dict, tools_instance):
    assert tools_instance.validateVolume(mock_data, mock_screen_dict, mock_save_dict, 2.5) == (False,True)
    assert mock_screen_dict["Volume"] == 0.67
    assert mock_save_dict["Volume"] == 0.67
    mock_data.loc[0, "VolMA"] = 1000
    mock_data.loc[0, "Volume"] = 2500
    assert tools_instance.validateVolume(mock_data, mock_screen_dict, mock_save_dict, 2.5,1000) == (True, True)
    assert mock_screen_dict["Volume"] == 2.5
    assert mock_save_dict["Volume"] == 2.5

def test_validateVolume_negative(mock_data, mock_screen_dict, mock_save_dict, tools_instance):
    mock_data["Volume"] = [1000, 2000, 3000, 3500]
    assert tools_instance.validateVolume(mock_data, mock_screen_dict, mock_save_dict, 2.5) == (False, True)
    assert mock_screen_dict["Volume"] == 0.67
    assert mock_save_dict["Volume"] == 0.67
    mock_data.loc[0, "VolMA"] = 0
    assert tools_instance.validateVolume(mock_data, mock_screen_dict, mock_save_dict, 2.5,10000) == (False, False)

def test_SpreadAnalysis_positive(mock_data, mock_screen_dict, mock_save_dict, tools_instance):
    mock_data["Open"] = [140, 135, 150, 155]
    assert tools_instance.validateVolumeSpreadAnalysis(mock_data, mock_screen_dict, mock_save_dict) == True
    assert mock_screen_dict["Pattern"] == "\033[32mSupply Drought\033[0m"
    assert mock_save_dict["Pattern"] == "Supply Drought"

def test_validateVolumeSpreadAnalysis_negative(mock_data, mock_screen_dict, mock_save_dict, tools_instance):
    mock_data["Open"] = [100, 105, 110,120]
    assert tools_instance.validateVolumeSpreadAnalysis(mock_data, mock_screen_dict, mock_save_dict) == False
    assert mock_screen_dict.get("Pattern") == None
    assert mock_save_dict.get("Pattern") == None

def test_validateVolumeSpreadAnalysis_datalength_lessthan2(mock_data, mock_screen_dict, mock_save_dict, tools_instance):
    assert tools_instance.validateVolumeSpreadAnalysis(mock_data.head(1), mock_screen_dict, mock_save_dict) == False
    assert mock_screen_dict.get("Pattern") == None
    assert mock_save_dict.get("Pattern") == None

def test_validateVolumeSpreadAnalysis_open_less_than_close(mock_data, mock_screen_dict, mock_save_dict, tools_instance):
    mock_data.loc[1, "Open"] = 100
    mock_data.loc[1, "Close"] = 110
    assert tools_instance.validateVolumeSpreadAnalysis(mock_data, mock_screen_dict, mock_save_dict) == False
    assert mock_screen_dict.get("Pattern") == None
    assert mock_save_dict.get("Pattern") == None

def test_validateVolumeSpreadAnalysis_spread0_lessthan_spread1(mock_data, mock_screen_dict, mock_save_dict, tools_instance):
    mock_data.loc[1, "Open"] = 120
    mock_data.loc[1, "Close"] = 100
    mock_data.loc[0, "Open"] = 110
    mock_data.loc[0, "Close"] = 100
    mock_data.loc[0, "Volume"] = mock_data.iloc[0]["VolMA"] + 1000
    mock_data.loc[1, "Volume"] = mock_data["Volume"].iloc[0] -1000
    assert tools_instance.validateVolumeSpreadAnalysis(mock_data, mock_screen_dict, mock_save_dict) == True
    assert mock_screen_dict.get("Pattern") == colorText.GREEN + "Demand Rise" + colorText.END 
    assert mock_save_dict.get("Pattern") == 'Demand Rise'

# def test_validateShortTermBullish(tools_instance):
#     # Mock the required functions and classes
#     patch('pandas.DataFrame.copy')
#     patch('numpy.round')
#     patch('pandas.DataFrame.fillna')
#     patch('pandas.DataFrame.replace')
#     patch('pandas.DataFrame.head')
#     patch('pandas.concat')
#     patch('pandas.DataFrame.rename')
#     patch('pandas.DataFrame.debug')

#     # Create a test case
#     df = pd.DataFrame({'Open': [1.0, 2.0, 3.0], 'High': [4.1, 5.1, 6.1], 'Low': [7.1, 8.1, 9.1], 'Close': [10.1, 11.1, 120.1], 'Volume': [13.1, 14.1, 15.1]})
#     df = pd.concat([df]*150, ignore_index=True)
#     ichi = pd.DataFrame({"ISA_9":[100,100,100],"ISB_26":[90,90,90],"IKS_26":[110,110,110],"ITS_9":[111,111,111]})
#     ichi = pd.concat([ichi]*150, ignore_index=True)
#     screenDict = {}
#     saveDict = {}
#     df,_ = tools_instance.preprocessData(df,30)
#     df["FASTK"].iloc[2] = 21
#     df["SSMA"].iloc[0] = 48
#     df["FASTD"].iloc[100] = 100
#     df["FASTK"].iloc[100] = 110
#     df["FASTD"].iloc[101] = 110
#     df["FASTK"].iloc[101] = 100
#     # Call the function under test
#     with patch('pkscreener.classes.Pktalib.pktalib.ichimoku',return_value=ichi):
#         result = tools_instance.validateShortTermBullish(df, screenDict, saveDict)

#         # Assert the expected behavior
#         assert result == False
#         assert screenDict['MA-Signal'] == '\033[32mBullish\033[0m'
#         assert saveDict['MA-Signal'] == 'Bullish'
#     ichi = pd.DataFrame({"ISB_26":[100,100,100],"ISA_9":[90,90,90],"IKS_26":[110,110,110],"ITS_9":[111,111,111]})
#     ichi = pd.concat([ichi]*150, ignore_index=True)
#     with patch('pkscreener.classes.Pktalib.pktalib.ichimoku',return_value=ichi):
#         result = tools_instance.validateShortTermBullish(df, screenDict, saveDict)

#         # Assert the expected behavior
#         assert result == True
#         assert screenDict['MA-Signal'] == '\033[32mBullish\033[0m, \033[32mBullish\033[0m'
#         assert saveDict['MA-Signal'] == 'Bullish, Bullish'

import unittest
from pkscreener.classes.ScreeningStatistics import ScreeningStatistics

class TestCupAndHandleDetection(unittest.TestCase):

    def setUp(self):
        """Create sample stock data for testing."""
        dates = pd.date_range(start="2023-01-01", periods=80, freq='D')
        
        # Generate a synthetic cup and handle pattern
        close_prices = np.concatenate([
            np.linspace(100, 85, 20),  # Left cup side (down)
            np.linspace(85, 90, 20),  # Cup bottom (stabilizing)
            np.linspace(90, 100, 20),  # Right cup side (up)
            np.linspace(100, 98, 5),  # Handle downtrend
            np.linspace(98, 102, 10),  # Handle recovery
            np.linspace(102, 110, 5)   # Breakout
        ])
        
        volume = np.concatenate([
            np.linspace(2000, 1500, 20),  # Decreasing volume in cup
            np.linspace(1500, 1400, 20),  # Stabilized low volume
            np.linspace(1400, 1800, 20),  # Increasing volume in recovery
            np.linspace(1800, 1750, 5),   # Stable volume in handle
            np.linspace(1750, 2200, 10),  # Volume picking up
            np.linspace(2200, 3000, 5)    # Breakout volume spike
        ])

        self.df = pd.DataFrame({'Date': dates, 'Close': close_prices, 'Volume': volume})
        self.df['Volatility'] = self.df['Close'].rolling(window=20).std()
        self.df.set_index('Date', inplace=True)
        self.screener = ScreeningStatistics(ConfigManager.tools(),None)

    def test_valid_cup_and_handle(self):
        """Test if a valid Cup and Handle pattern is detected."""
        points = self.screener.find_cup_and_handle(self.df)
        self.assertIsNotNone(points, "Cup and Handle pattern should be detected.")

    def test_dynamic_order_calculation(self):
        """Test if the order parameter adjusts based on volatility."""
        high_vol_df = self.df.copy()
        high_vol_df['Close'] += np.random.normal(0, 15, len(high_vol_df))  # Add artificial volatility
        high_order = self.screener.get_dynamic_order(high_vol_df)
        
        low_vol_df = self.df.copy()
        low_vol_df['Close'] += np.random.normal(0, 1, len(low_vol_df))  # Reduce volatility
        low_order = self.screener.get_dynamic_order(low_vol_df)

        self.assertGreaterEqual(high_order, low_order, "Higher volatility should increase order parameter.")
    
    def test_reject_v_shaped_cup(self):
        """Ensure sharp V-bottoms are not detected as valid cups."""
        v_shaped_df = self.df.copy()
        v_shaped_df.iloc[10:30, v_shaped_df.columns.get_loc("Close")] = 85  # Sharp bottom
        _,points = self.screener.find_cup_and_handle(v_shaped_df)
        self.assertIsNone(points, "V-bottom shape should be rejected.")

    def test_handle_depth_constraint(self):
        """Ensure the handle does not drop too much (more than 50% of cup depth)."""
        deep_handle_df = self.df.copy()
        deep_handle_df.iloc[60:65, deep_handle_df.columns.get_loc("Close")] -= 5  # Excessive handle drop
        _,points = self.screener.find_cup_and_handle(deep_handle_df)
        self.assertIsNone(points, "Pattern should be rejected due to a deep handle.")

    def test_no_breakout_rejection(self):
        """Ensure patterns without a breakout are rejected."""
        no_breakout_df = self.df.copy()
        no_breakout_df.iloc[-5:, no_breakout_df.columns.get_loc("Close")] = 100  # No breakout
        _,points = self.screener.find_cup_and_handle(no_breakout_df)
        self.assertIsNone(points, "Pattern should be rejected without a breakout.")

    def test_no_cup_no_detection(self):
        """Ensure detection doesn't falsely identify a pattern when there's no cup formation."""
        random_df = pd.DataFrame({
            'Date': pd.date_range(start="2023-01-01", periods=100, freq='D'),
            'Close': np.random.uniform(90, 110, 100),
            'Volume': np.random.uniform(1500, 2500, 100)
        })
        random_df['Volatility'] = random_df['Close'].rolling(window=20).std()
        random_df.set_index('Date', inplace=True)
        _,points = self.screener.find_cup_and_handle(random_df)
        self.assertIsNone(points, "No cup pattern exists, should return None.")
