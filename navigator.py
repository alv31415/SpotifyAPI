from selenium import webdriver

# special thanks to:
# https://towardsdatascience.com/controlling-the-web-with-python-6fceb22c5f08

import time

test_url = "https://accounts.spotify.com/authorize?client_id=59b88838dd0e46b7b4d4e9a52e00c755&response_type=code&redirect_uri=https%3A%2F%2Fexample.com%2Fcallback&state=mynameejeff&scope=playlist-modify-public+user-read-email+user-read-private+playlist-read-collaborative&show_dialog=true"

def spotify_login(driver, password, username, walkthrough_mode = True):
    """
    Automatically logs in to spotify account
    """
    # get names of "stuff" to fill in
    username_id = "login-username"
    password_id = "login-password"
    checkbox_id = "login-remember"
    checkbox_selector = ".control-indicator"
    login_button_id = "login-button"

    # fill in username
    username_box = driver.find_element_by_id(username_id)
    username_box.send_keys(username)
    if walkthrough_mode:
        time.sleep(0.5)

    # fill in password
    password_box = driver.find_element_by_id(password_id)
    password_box.send_keys(password)
    if walkthrough_mode:
        time.sleep(0.5)
    checkbox = driver.find_element_by_id(checkbox_id)

    # don't remember user
    if checkbox.is_selected():
        checkbox_box = driver.find_element_by_css_selector(checkbox_selector)
        checkbox_box.click()
    if walkthrough_mode:
        time.sleep(2)

    # log in into account
    login_button_box = driver.find_element_by_id(login_button_id)
    login_button_box.click()

def driver_scroll(driver, max_scroll, walkthrough_mode=True):
    """
    Scrolls a desired amount
    """
    if walkthrough_mode:
        time.sleep(3)
        # scroll smoothly to bottom of the page (sees all that the user is allowing)
        scheight = 1
        while scheight < max_scroll:
            driver.execute_script(f"window.scrollTo(0, {scheight})")
            scheight += 1

        time.sleep(3)
    else:
        time.sleep(0.2)
        # scroll to access details & confirm authorisation
        driver.execute_script(f"window.scrollTo(0, {max_scroll})")
        time.sleep(0.2)

def extract_token(user_id, password, request_body = "", walkthrough_mode = True):
    """
    Gets a usable token for playlist functionality
    """
    # request body not necessary
    automatic_token_url = "https://developer.spotify.com/console/post-playlists/"

    # implement checking of request_body

    if walkthrough_mode:
        # use google chrome
        driver = webdriver.Chrome()
    else:
        # don't show the process if we want it fast
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument("disable-gpu")
        driver = webdriver.Chrome(options=options)

    # Open the website
    driver.get(automatic_token_url)

    driver_scroll(driver = driver, max_scroll = 450, walkthrough_mode = walkthrough_mode)

    user_id_id = "path-param-user_id"
    request_body_input_id = "body-input"
    auth_button_selector = ".btn-green"

    user_id_box = driver.find_element_by_id(user_id_id)
    user_id_box.send_keys(user_id)

    if walkthrough_mode:
        time.sleep(2)

    request_body_input_box = driver.find_element_by_id(request_body_input_id)
    request_body_input_box.clear()
    request_body_input_box.send_keys(request_body)

    if walkthrough_mode:
        time.sleep(2)

    auth_button_box = driver.find_element_by_css_selector(auth_button_selector)
    auth_button_box.click()

    if walkthrough_mode:
        time.sleep(2)
    else:
        time.sleep(0.2)

    checkbox_pmpublic_id = "scope-playlist-modify-public"
    checkbox_pmpublic_selector = "#scope-playlist-modify-public+ .control-indicator"

    checkbox_pmpublic_box = driver.find_element_by_id(checkbox_pmpublic_id)

    if not checkbox_pmpublic_box.is_selected():
        checkbox_pmpublic = driver.find_element_by_css_selector(checkbox_pmpublic_selector)
        checkbox_pmpublic.click()

    if walkthrough_mode:
        time.sleep(2)
    else:
        time.sleep(0.2)

    checkbox_pmprivate_id = "scope-playlist-modify-private"
    checkbox_pmprivate_selector = "#scope-playlist-modify-private+ .control-indicator"

    checkbox_pmprivate_box = driver.find_element_by_id(checkbox_pmprivate_id)

    if not checkbox_pmprivate_box.is_selected():
        checkbox_pmprivate = driver.find_element_by_css_selector(checkbox_pmprivate_selector)
        checkbox_pmprivate.click()

    if walkthrough_mode:
        time.sleep(1)

    token_request_selector = "#oauthRequestToken"
    token_request_box = driver.find_element_by_css_selector(token_request_selector)

    driver.execute_script("arguments[0].scrollIntoView(true)", token_request_box)

    token_request_box.click()

    if walkthrough_mode:
        time.sleep(2)

    spotify_login(driver, password, user_id, walkthrough_mode)

    if walkthrough_mode:
        time.sleep(3)

    driver_scroll(driver, 450, walkthrough_mode = walkthrough_mode)

    if walkthrough_mode:
        time.sleep(1)
    else:
        time.sleep(0.2)

    ouath_token_id = "oauth-input"
    access_token = driver.find_element_by_id(ouath_token_id).get_attribute("value")

    return access_token


