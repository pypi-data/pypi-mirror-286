from tourist.core import file_to_string, func_to_string, TouristScraper

TOURIST_BASE = "http://localhost:8000"
TOURIST_X_SECRET = "supersecret"

tourist_scraper = TouristScraper(TOURIST_BASE, TOURIST_X_SECRET)


if __name__ == "__main__":
    # custom selenium script
    actions_script = file_to_string(
        "/home/joe/workspace/projects/apps/tourist/examples/custom_selenium/selenium_script.txt"
    )

    # output from the script
    # data = tourist_scraper.do_actions(actions_script)
    # print(data)

    # custom selenium function
    def my_selenium_function():
        global driver
        global actions_output
        driver.get("https://www.example.com")
        driver.implicitly_wait(2)
        actions_output["current_url"] = driver.current_url

    actions_script = func_to_string(my_selenium_function)
    print(actions_script)
