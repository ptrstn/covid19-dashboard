import datetime
import platform

import pandas as pd

STRFTIME_DATA_FRAME_FORMAT = (
    "%#m/%#d/%y" if platform.system() == "Windows" else "%-m/%-d/%y"
)


def daily_report(date_string=None):
    report_directory = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"

    if date_string is None:
        yesterday = datetime.date.today() - datetime.timedelta(days=2)
        file_date = yesterday.strftime("%m-%d-%Y")
    else:
        file_date = date_string

    df = pd.read_csv(report_directory + file_date + ".csv", dtype={"FIPS": str})
    return df


def daily_confirmed():
    URL = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/jhu/new_cases.csv"
    df = pd.read_csv(URL)
    return df


def daily_deaths():
    URL = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/jhu/new_deaths.csv"
    df = pd.read_csv(URL)
    return df


def confirmed_report():
    URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    df = pd.read_csv(URL)
    return df


def deaths_report():

    URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
    df = pd.read_csv(URL)
    return df


def recovered_report():
    URL = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
    df = pd.read_csv(URL)
    return df


def realtime_growth(date_string=None, weekly=False, monthly=False):
    confirmed_df = confirmed_report()[confirmed_report().columns[4:]].sum()
    deaths_df = deaths_report()[deaths_report().columns[4:]].sum()
    recovered_df = recovered_report()[recovered_report().columns[4:]].sum()

    growth_df = pd.DataFrame([])
    growth_df["Confirmed"], growth_df["Deaths"], growth_df["Recovered"] = (
        confirmed_df,
        deaths_df,
        recovered_df,
    )
    growth_df.index = growth_df.index.rename("Date")

    yesterday = pd.Timestamp("now").date() - pd.Timedelta(days=1)

    if date_string is not None:
        return growth_df.loc[growth_df.index == date_string]

    if weekly is True:
        weekly_df = pd.DataFrame([])
        intervals = (
            pd.date_range(end=yesterday, periods=8, freq="7D")
            .strftime(STRFTIME_DATA_FRAME_FORMAT)
            .tolist()
        )
        for day in intervals:
            weekly_df = weekly_df.append(growth_df.loc[growth_df.index == day])
        return weekly_df

    elif monthly is True:
        monthly_df = pd.DataFrame([])
        intervals = (
            pd.date_range(end=yesterday, periods=3, freq="1M")
            .strftime(STRFTIME_DATA_FRAME_FORMAT)
            .tolist()
        )
        for day in intervals:
            monthly_df = monthly_df.append(growth_df.loc[growth_df.index == day])
        return monthly_df

    return growth_df


def percentage_difference():
    current = realtime_growth(weekly=True).iloc[-1]
    last_week = realtime_growth(weekly=True).iloc[-2]
    trends = round(number=((current - last_week) / last_week) * 100, ndigits=1)

    rate_change = round(
        ((current.Deaths / current.Confirmed) * 100)
        - ((last_week.Deaths / last_week.Confirmed) * 100),
        ndigits=2,
    )
    trends = trends.append(pd.Series(data=rate_change, index=["Death_rate"]))

    return trends


def global_cases():
    df = daily_report()[
        ["Country_Region", "Confirmed", "Recovered", "Deaths", "Active"]
    ]
    df.rename(columns={"Country_Region": "Country"}, inplace=True)
    df = df.groupby("Country", as_index=False).sum()
    df.sort_values(by=["Confirmed"], ascending=False, inplace=True)

    for index, row in df.iterrows():
        country_cases = int(row["Confirmed"])
        country_deaths = int(row["Deaths"])
        if country_cases == 0:
            death_rate_formatted = format(0, ".2f")
            df.loc[index, "Death Rate"] = death_rate_formatted
        else:
            death_rate = float(country_deaths / country_cases) * 100
            death_rate_formatted = format(death_rate, ".2f")
            df.loc[index, "Death Rate"] = death_rate_formatted
    return df


def us_counties():
    counties_url = "https://raw.githubusercontent.com/balsama/us_counties_data/master/data/counties.csv"
    populations = pd.read_csv(counties_url)[["FIPS Code", "Population"]]
    populations.rename(columns={"FIPS Code": "fips"}, inplace=True)
    us_counties_url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-counties.csv"
    df = pd.read_csv(
        us_counties_url,
        dtype={"fips": str},
    ).iloc[:, :6]
    df = pd.merge(df, populations, on="fips")
    df["cases/capita"] = (df.cases / df.Population) * 100000

    return df
