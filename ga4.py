# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "fastapi",
#   "requests",
#   "pandas",
#   "bs4",
#   "beautifulsoup4",
#   "httpx",
#   "geopy"
# ]
# ///


import json
import httpx
import pandas as pd
from bs4 import BeautifulSoup

tools_ga4 = [
    # GA4, Question 1
    {
        "type": "function",
        "function": {
            "name": "espn_cricinfo_scraping",
            "description": """ESPN Cricinfo has ODI batting stats for each batsman. 
            The result is paginated across multiple pages. Count the number of ducks in page number 5.

            Understanding the Data Source: ESPN Cricinfo's ODI batting statistics are spread across multiple pages, 
            each containing a table of player data. Go to page number 5.
            Setting Up Google Sheets: Utilize Google Sheets' IMPORTHTML function to import table data from the 
            URL for page number 5.
            Data Extraction and Analysis: Pull the relevant table from the assigned page into Google Sheets. 
            Locate the column that represents the number of ducks for each player. (It is titled "0".) 
            Sum the values in the "0" column to determine the total number of ducks on that page.

            What is the total number of ducks across players on page number 5 of ESPN Cricinfo's ODI batting stats?
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "page_number": {
                        "type": "number",
                        "description": "Page number of ESPN Cricinfo's ODI Batting Stats",
                    }
                },
                "required": [
                    "page_number",
                ],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    # GA4, Question 2
    {
        "type": "function",
        "function": {
            "name": "imdb_scraping",
            "description": """
            Develop a Python program that interacts with IMDb's dataset to extract detailed
              information about titles within a specified rating range. The extracted data should include the movie's 
              unique ID, title, release year, and rating. This information will be used to inform content acquisition decisions, 
              ensuring that StreamFlix consistently offers high-quality and well-received films to its audience.

        Imagine you are a data analyst at StreamFlix, responsible for expanding the platform's movie library. 
        Your task is to identify titles that have received favorable ratings on IMDb, 
        ensuring that the selected titles meet the company's quality standards and resonate with subscribers.

        To achieve this, you need to:

        Extract Data: Retrieve movie information from IMDb for all films that have a rating between 5 and 7.
        Format Data: Structure the extracted information into a JSON format containing the following fields:
        id: The unique identifier for the movie on IMDb.
        title: The official title of the movie.
        year: The year the movie was released.
        rating: The IMDb user rating for the movie.
        Your Task
        Source: Utilize IMDb's advanced web search at https://www.imdb.com/search/title/ to access movie data.
        Filter: Filter all titles with a rating between 5 and 7.
        Format: For up to the first 25 titles, extract the necessary details: ID, title, year, and rating. 
        The ID of the movie is the part of the URL after tt in the href attribute. For example, tt10078772. 
        """,
            "parameters": {
                "type": "object",
                "properties": {
                    "rating_from": {
                        "type": "number",
                        "description": "Minimum rating from the range of rating to filter the movies or titles on, can have decimals",
                    },
                    "rating_to": {
                        "type": "number",
                        "description": "Maximum rating from the range of rating to filter the movies or titles on, can have decimals",
                    },
                    "num_titles": {
                        "type": "integer",
                        "description": "Number of titles to extract the necessary details",
                    },
                },
                "required": ["rating_from", "rating_to", "num_titles"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    # GA4, Question 3 - Summary from wikipedia
    {
        "type": "function",
        "function": {
            "name": "return_wiki_entrypoint",
            "description": """
            To address these challenges, GlobalEdu Platforms has decided to develop a web application
              that exposes a RESTful API. This API will allow their educational tools to fetch and 
              display structured outlines of Wikipedia pages for any given country. The application needs to:

            Accept a country name as a query parameter.
            Fetch the corresponding Wikipedia page for that country.
            Extract all headings (H1 to H6) from the page.
            Generate a Markdown-formatted outline that reflects the hierarchical structure of the content.
            Enable Cross-Origin Resource Sharing (CORS) to allow GET requests from any origin, facilitating seamless integration with various educational platforms.
            Your Task
            Write a web application that exposes an API with a single query parameter: ?country=. 
            It should fetch the Wikipedia page of the country, extracts all headings (H1 to H6), 
            and create a Markdown outline for the country. 
        """,
            "parameters": {
                "type": "object",
                "properties": {
                    "query_parameter": {
                        "type": "string",
                        "description": "Query parameter name that will be passed, for example country",
                    }
                },
                "required": [
                    "query_parameter",
                ],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    # GA 4, Question 4: BBC Weather
    {
        "type": "function",
        "function": {
            "name": "get_bbc_weather",
            "description": """
            You are tasked with developing a system that automates the following:

            API Integration and Data Retrieval: Use the BBC Weather API to fetch the 
            weather forecast for Kuala Lumpur. Send a GET request to the locator service 
            to obtain the city's locationId. Include necessary query parameters such as API key, 
            locale, filters, and search term (city).
            Weather Data Extraction: Retrieve the weather forecast data using the obtained 
            locationId. Send a GET request to the weather broker API endpoint with the 
            locationId.
            Data Transformation: Extract the localDate and enhancedWeatherDescription 
            from each day's forecast. Iterate through the forecasts array in the API response and map each localDate to its corresponding enhancedWeatherDescription. Create a JSON object where each key is the localDate and the value is the enhancedWeatherDescription.        """,
            "parameters": {
                "type": "object",
                "properties": {
                    "CITY": {
                        "type": "string",
                        "description": "The city for which the weather has to be fetched",
                    }
                },
                "required": [
                    "CITY",
                ],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
    # GA 4, Question 5: Nominatim
    {
        "type": "function",
        "function": {
            "name": "nominatim",
            "description": """
        Find the minimum or maximum latitude or longitude of the given city using Nominatim API. 
        If osm_id is given, use that to identify the matching city from the list of multiple cities
        returned by Nominatim
        """,
            "parameters": {
                "type": "object",
                "properties": {
                    "city_description": {
                        "type": "string",
                        "description": "The city for which details need to be fetched, preferably in the form 'City, Country'",
                    },
                    "lat_or_lon": {
                        "type": "string",
                        "description": "Whether the question asks to find out about latitude or longitude. If not given, consider the value as 'latitude'",
                    },
                    "min_or_max": {
                        "type": "string",
                        "description": "Whether the question asks to find out minimum or maximum of the attribute. If not given, consider the value as 'minimum'",
                    },
                    "osm_id": {
                        "type": "string",
                        "description": "osm_id if provided, to be used for filtering down the city. If not given, consider blank",
                    },
                },
                "required": ["city_description", "lat_or_lon", "min_or_max", "osm_id"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    },
]


# GA5, Question 6 - Hackernews


async def hacker_news(topic="AI", min_points=36):
    import re

    URL = f"https://hnrss.org/newest"

    final_url = URL + f"?q={topic}" + f"&count=100&points={min_points}"
    print(final_url)

    async with httpx.AsyncClient() as client:
        response = await client.get(final_url)
        response.raise_for_status()
        # html_content = response.text

    # response = requests.get(final_url)

    print(response.text)

    soup = BeautifulSoup(response.text, "xml")

    items = soup.find_all("item")
    for item in items:
        m = re.search(r"Points:\s[0-9]+", item.text)
        if m:
            points_str = m.group(0)
            points = int(points_str.split(" ")[1])
            link = ""
            if points >= min_points:
                print(f"Points: {points:4} :: {item.title.text}")
                print(f"{item.link.text}")
                link = item.link.text
                break
    return link


async def ga5_q6_test():
    val = await hacker_news(topic="AI", min_points=36)
    print(val)


# GA4 Question 5
async def nominatim(
    city_description, lat_or_lon="latitude", min_or_max="minimum", osm_id=""
):
    import geopy as gp
    from geopy.geocoders import Nominatim

    locator = Nominatim(user_agent="myGeocoder")
    location = locator.geocode(city_description)
    corner1 = location.raw["boundingbox"][0:2]
    corner2 = location.raw["boundingbox"][2:4]
    if "lat" in lat_or_lon.lower():
        array_index = 0
    else:
        array_index = 1

    if "min" in min_or_max.lower():
        if corner1[array_index] < corner2[array_index]:
            ret_val = corner1[array_index]
        else:
            ret_val = corner2[array_index]

    else:
        if corner1[array_index] > corner2[array_index]:
            ret_val = corner1[array_index]
        else:
            ret_val = corner2[array_index]

    print(f"{city_description=}, {ret_val=}")
    return ret_val


async def ga5_q5_test():
    val = await nominatim(
        "Dhaka, Bangladesh", lat_or_lon="latitude", min_or_max="minimum"
    )
    print(val)


# GA4 Question 4
from ga4_q04 import get_bbc_weather  # since entire function is defined in ga4_q04,

# we don't need to do anything here


# GA 4, Question 3: Wikipedia API
# The below function just returns the end point for GA 4, Q3
# The entry point will then call the actual function "generate_markdown_outline" once
# the query is passed by the evaluator
async def return_wiki_entrypoint(query_parameter="country"):
    return "http://127.0.0.1:8000/wiki"


async def generate_markdown_outline(country):
    # Fetch Wikipedia page for the country
    print(f"Request received for: {country}")
    wikipedia_url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"

    import requests
    from fastapi.responses import JSONResponse

    try:
        response = requests.get(wikipedia_url)
        response.raise_for_status()  # Will raise an exception for bad responses
    except requests.exceptions.RequestException as e:
        return JSONResponse(
            status_code=400,
            content={"message": f"Error fetching Wikipedia page: {str(e)}"},
        )

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract headings (H1 to H6)
    headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])

    # Create the Markdown outline
    # markdown_outline = "## Contents\n\n"
    markdown_outline = ""

    print(headings)

    last_level = 1  # To keep track of heading levels (H1-H6)
    for heading in headings:
        level = int(heading.name[1])  # H1 -> 1, H2 -> 2, ..., H6 -> 6
        text = heading.get_text(strip=True)

        # Ensure markdown format by adding appropriate number of '#'
        # markdown_heading = f"{'#' * level} {text}"

        # Adjust heading levels based on the last heading level
        if level == 1:
            markdown_outline += f"\n# {text}\n"
        elif level == 2:
            markdown_outline += f"\n## {text}\n"
        elif level == 3:
            markdown_outline += f"\n### {text}\n"
        elif level == 4:
            markdown_outline += f"\n#### {text}\n"
        elif level == 5:
            markdown_outline += f"\n##### {text}\n"
        elif level == 6:
            markdown_outline += f"\n###### {text}\n"

    # return JSONResponse(content={"markdown_outline": markdown_outline})
    return markdown_outline


# GA 4 Question 2: IMDB Scraping
async def scrape_imdb_data(rating_from: int, rating_to: int, num_titles: int):
    source_url = (
        f"https://www.imdb.com/search/title/?user_rating={rating_from},{rating_to}"
    )
    print(f"{source_url=}")

    # Send a GET request to the URL

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }
    # Fetch the page content
    async with httpx.AsyncClient() as client:
        response = await client.get(source_url, headers=headers)
        response.raise_for_status()
        html_content = response.text

    # Check if the request was successful
    if response.status_code != 200:
        print("Failed to retrieve the page")
        return []

    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all the blocks containing the relevant data
    all_blocks = soup.find_all("li", class_="ipc-metadata-list-summary-item")
    json_array = []

    # Loop through each block and extract the relevant information
    for block in all_blocks:
        # # Extract the title from the first <h3> tag
        # title_tag = block.find("h3", class_="ipc-title__text")
        # title = title_tag.get_text(strip=True) if title_tag else ""

        try:
            title = block.find_all("h3", class_="ipc-title__text")[0].get_text().strip()
        except AttributeError:
            title = ""

        # Extract the IMDb ID from the first <a> tag's href
        try:
            imdb_id = (
                block.find("a", class_="ipc-title-link-wrapper")
                .get("href")
                .strip()
                .split("/")[2]
            )

        except AttributeError:
            imdb_id = ""

        # Extract the year from the span tags
        try:
            year = block.find("span", class_="dli-title-metadata-item").get_text()
        except AttributeError:
            year = ""

        # Extract the rating from the span tag
        try:
            rating = block.find("span", class_="ipc-rating-star--rating").get_text()
        except AttributeError:
            rating = ""

        # Create a dictionary for the current element
        element = {
            "id": imdb_id,
            "title": title,
            "year": year,
            "rating": rating,
        }

        # Append the element to the JSON array
        json_array.append(element)

    # Return the first 25 elements
    return json.dumps(json_array[:num_titles], indent=2)


async def q2_test():

    scraped_data = await scrape_imdb_data(rating_from=5, rating_to=7, num_titles=25)

    print(f"Script answer={(scraped_data)}")
    # print(f"Expected answer={expected_answers['GA5.2']}")
    # if ducks == expected_answers["GA5.1"]:
    #     print("GA5.2 Passed")
    # else:
    #     print("GA5.2 Failed")


# GA 4, Question 1: ESPN Cricinfo Scraping
async def espn_cricinfo_scraping(page_number):
    url = f"https://stats.espncricinfo.com/ci/engine/stats/index.html?class=2;page={page_number};template=results;type=batting"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }
    # Fetch the page content
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        html_content = response.text

    soup = BeautifulSoup(html_content, "html.parser")

    # Find the main stats table
    tables = soup.find_all("table", class_="engineTable")
    stats_table = None

    for table in tables:
        if table.find("th", string="Player"):
            stats_table = table
            break

    headers = [th.get_text(strip=True) for th in stats_table.find_all("th")]
    print(headers)

    data_list = []

    for row in stats_table.find_all("tr"):
        data = [td.get_text(strip=True) for td in row.find_all("td")]
        if len(data) > 0:
            data_list.append(data)

    df = pd.DataFrame(data_list, columns=headers)

    df["ducks"] = pd.to_numeric(df["0"], errors="coerce")
    df["ducks"] = df["ducks"].fillna(0).astype(int)
    num_ducks = df["ducks"].sum()
    print(f"Number of ducks on page {page_number} = {num_ducks}")
    return str(num_ducks)


async def q1_test():
    ducks = asyncio.run(espn_cricinfo_scraping(3))
    print(f"Script answer={ducks}")
    print(f"Expected answer={expected_answers['GA5.1']}")
    if ducks == expected_answers["GA5.1"]:
        print("GA5.1 Passed")
    else:
        print("GA5.1 Failed")


expected_answers = {"GA5.1": "511"}


if __name__ == "__main__":
    import asyncio

    asyncio.run(ga5_q6_test())

    # GA5 Q2
