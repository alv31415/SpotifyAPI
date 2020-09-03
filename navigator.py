import time  # used to stop program

from selenium import webdriver  # used for automating & working through a browser


# special thanks to:
# https://towardsdatascience.com/controlling-the-web-with-python-6fceb22c5f08

def spotify_login(driver, password, username, walkthrough_mode=True):
    """
    Automatically logs in to spotify account
    :param driver: the instance of the automated browser on which we work
    :param user_id: the username of the Spotify Account to which we log in.
    :param password: the password of the Spotify Account to which we log in.
    :param walkthrough_mode: a boolean value used to determine whether the user sees the token obtaining process
    """

    # get css names of "stuff" to fill in
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
    :param driver: the instance of the automated browser on which we work
    :param max_scroll: the y coordinate of the destination of the scroll
    :param walkthrough_mode: a boolean value used to determine whether the user sees the token obtaining process
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


def extract_token(user_id, password, walkthrough_mode=True):
    """
    Gets a usable token for playlist functionality
    :param user_id: the username of the Spotify Account to which we log in.
    :param password: the password of the Spotify Account to which we log in.
    :param walkthrough_mode: a boolean value used to determine whether the user sees the token obtaining process
    """

    automatic_token_url = "https://developer.spotify.com/console/post-playlists/"

    if walkthrough_mode:
        # use google chrome
        driver = webdriver.Chrome()
    else:
        # don't show the process if we want it fast
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument("disable-gpu")
        driver = webdriver.Chrome(options=options)

    # open the website
    driver.get(automatic_token_url)

    # scroll to see playlist creation details
    driver_scroll(driver=driver, max_scroll=450, walkthrough_mode=walkthrough_mode)

    # get names (ids) of username and get token button
    user_id_id = "path-param-user_id"
    auth_button_selector = ".btn-green"

    # fill in username
    user_id_box = driver.find_element_by_id(user_id_id)
    user_id_box.send_keys(user_id)

    if walkthrough_mode:
        time.sleep(2)

    if walkthrough_mode:
        time.sleep(2)

    # click button to request token
    auth_button_box = driver.find_element_by_css_selector(auth_button_selector)
    auth_button_box.click()

    if walkthrough_mode:
        time.sleep(2)
    else:
        time.sleep(0.2)

    # get names (ids) of checkboxes
    checkbox_pmpublic_id = "scope-playlist-modify-public"
    checkbox_pmpublic_selector = "#scope-playlist-modify-public+ .control-indicator"

    # select checkboxes if they are not already
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

    # get names (ids) of request token button
    token_request_selector = "#oauthRequestToken"
    token_request_box = driver.find_element_by_css_selector(token_request_selector)

    # scroll to request token button
    driver.execute_script("arguments[0].scrollIntoView(true)", token_request_box)

    # click request token button
    token_request_box.click()

    if walkthrough_mode:
        time.sleep(2)

   # log in to authorise token
    spotify_login(driver, password, user_id, walkthrough_mode)

    if walkthrough_mode:
        time.sleep(3)

    # scroll to get token
    driver_scroll(driver, 450, walkthrough_mode=walkthrough_mode)

    if walkthrough_mode:
        time.sleep(1)
    else:
        time.sleep(0.2)

    # retrieve token
    ouath_token_id = "oauth-input"
    access_token = driver.find_element_by_id(ouath_token_id).get_attribute("value")

    return access_token
