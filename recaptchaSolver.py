# Standard imports
import re
import shutil
from time import sleep, time

# Third-party imports
import cv2
import numpy as np
import requests
from PIL import Image
from ultralytics import YOLO
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import seleniumwire.undetected_chromedriver as webdriver

# Initialize YOLO model
model = YOLO("./yolov8x.onnx", task="detect")

def find_between(s, first, last):
    """
    Find a substring between two substrings.
    :param s: string to search.
    :param first: first substring.
    :param last: last substring.
    """
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def random_delay(mu=0.3, sigma=0.1):
    """
    Random delay to simulate human behavior.
    :param mu: mean of normal distribution.
    :param sigma: standard deviation of normal distribution.
    """
    delay = np.random.normal(mu, sigma)
    delay = max(0.1, delay)
    sleep(delay)


def go_to_recaptcha_iframe1(driver):
    """
    Go to the first recaptcha iframe. (CheckBox)
    """
    driver.switch_to.default_content()
    recaptcha_iframe1 = WebDriverWait(driver=driver, timeout=20).until(
        EC.presence_of_element_located((By.XPATH, '//iframe[@title="reCAPTCHA"]')))
    driver.switch_to.frame(recaptcha_iframe1)


def go_to_recaptcha_iframe2(driver):
    """
    Go to the second recaptcha iframe. (Images)
    """
    driver.switch_to.default_content()
    recaptcha_iframe2 = WebDriverWait(driver=driver, timeout=20).until(
        EC.presence_of_element_located((By.XPATH, '//iframe[contains(@title, "challenge")]')))
    driver.switch_to.frame(recaptcha_iframe2)


def get_target_num(driver):
    """
    Get the target number from the recaptcha title.
    """
    target_mappings = {
        "bicycle": 1,
        "bus": 5,
        "boat": 8,
        "car": 2,
        "hydrant": 10,
        "motorcycle": 3,
        "traffic": 9
    }

    target = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, '//div[@id="rc-imageselect"]//strong')))
    
    for term, value in target_mappings.items():
        if re.search(term, target.text): return value

    return 1000


def dynamic_and_selection_solver(target_num, verbose, model):
    """
    Get the answers from the recaptcha images.
    :param target_num: target number.
    :param verbose: print verbose.
    """
    # Load image and predict
    image = Image.open("0.png")
    image = np.asarray(image)
    result = model.predict(image, task="detect", verbose=verbose)

    # Get the index of the target number
    target_index = []
    count = 0
    for num in result[0].boxes.cls:
        if num == target_num: target_index.append(count)
        count += 1

    # Get the answers from the index
    answers = []
    boxes = result[0].boxes.data
    count = 0
    for i in target_index:
        target_box = boxes[i]
        p1, p2 = (int(target_box[0]), int(target_box[1])
                  ), (int(target_box[2]), int(target_box[3]))
        x1, y1 = p1
        x2, y2 = p2

        xc = (x1+x2)/2
        yc = (y1+y2)/2

        row = yc // 100 
        col = xc // 100
        answer = int(row * 3 + col + 1)
        answers.append(answer)

        count += 1

    return list(set(answers))


def get_all_captcha_img_urls(driver):
    """
    Get all the image urls from the recaptcha.
    """
    images = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
        (By.XPATH, '//div[@id="rc-imageselect-target"]//img')))

    img_urls = []
    for img in images: img_urls.append(img.get_attribute("src"))

    return img_urls


def download_img(name, url):
    """
    Download the image.
    :param name: name of the image.
    :param url: url of the image.
    """

    response = requests.get(url, stream=True)
    with open(f'{name}.png', 'wb') as out_file: shutil.copyfileobj(response.raw, out_file)
    del response


def get_all_new_dynamic_captcha_img_urls(answers, before_img_urls, driver):
    """
    Get all the new image urls from the recaptcha.
    :param answers: answers from the recaptcha.
    :param before_img_urls: image urls before.
    """
    images = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
        (By.XPATH, '//div[@id="rc-imageselect-target"]//img')))
    img_urls = []

    # Get all the image urls
    for img in images:
        try: img_urls.append(img.get_attribute("src"))
        except:
            is_new = False
            return is_new, img_urls

    # Check if the image urls are the same as before
    index_common = []
    for answer in answers:
        if img_urls[answer-1] == before_img_urls[answer-1]: index_common.append(answer)

    # Return if the image urls are the same as before
    if len(index_common) >= 1:
        is_new = False
        return is_new, img_urls
    else:
        is_new = True
        return is_new, img_urls


def paste_new_img_on_main_img(main, new, loc):
    """
    Paste the new image on the main image.
    :param main: main image.
    :param new: new image.
    :param loc: location of the new image.
    """
    paste = np.copy(main)
    
    row = (loc - 1) // 3
    col = (loc - 1) % 3
    
    start_row, end_row = row * 100, (row + 1) * 100
    start_col, end_col = col * 100, (col + 1) * 100
    
    paste[start_row:end_row, start_col:end_col] = new
    
    paste = cv2.cvtColor(paste, cv2.COLOR_RGB2BGR)
    cv2.imwrite('0.png', paste)


def get_occupied_cells(vertices):
    """
    Get the occupied cells from the vertices.
    :param vertices: vertices of the image.
    """
    occupied_cells = set()
    rows, cols = zip(*[((v-1)//4, (v-1) % 4) for v in vertices])

    for i in range(min(rows), max(rows)+1):
        for j in range(min(cols), max(cols)+1):
            occupied_cells.add(4*i + j + 1)

    return sorted(list(occupied_cells))

def square_solver(target_num, verbose, model):
    """
    Get the answers from the recaptcha images.
    :param target_num: target number.
    :param verbose: print verbose.
    """
    # Load image and predict
    image = Image.open("0.png")
    image = np.asarray(image)
    result = model.predict(image, task="detect", verbose=verbose)
    boxes = result[0].boxes.data

    target_index = []
    count = 0
    for num in result[0].boxes.cls:
        if num == target_num:
            target_index.append(count)
        count += 1

    for i in target_index:
        target_box = boxes[i]
        p1, p2 = (int(target_box[0]), int(target_box[1])
                  ), (int(target_box[2]), int(target_box[3]))
        x1, y1 = p1
        x2, y2 = p2

    answers = []
    count = 0
    for i in target_index:
        target_box = boxes[i]
        p1, p2 = (int(target_box[0]), int(target_box[1])
                  ), (int(target_box[2]), int(target_box[3]))
        x1, y1 = p1
        x4, y4 = p2
        x2 = x4
        y2 = y1
        x3 = x1
        y3 = y4
        xys = [x1, y1, x2, y2, x3, y3, x4, y4]

        four_cells = []
        for i in range(4):
            x = xys[i*2]
            y = xys[(i*2)+1]

            if x < 112.5 and y < 112.5:
                four_cells.append(1)
            if 112.5 < x < 225 and y < 112.5:
                four_cells.append(2)
            if 225 < x < 337.5 and y < 112.5:
                four_cells.append(3)
            if 337.5 < x <= 450 and y < 112.5:
                four_cells.append(4)

            if x < 112.5 and 112.5 < y < 225:
                four_cells.append(5)
            if 112.5 < x < 225 and 112.5 < y < 225:
                four_cells.append(6)
            if 225 < x < 337.5 and 112.5 < y < 225:
                four_cells.append(7)
            if 337.5 < x <= 450 and 112.5 < y < 225:
                four_cells.append(8)

            if x < 112.5 and 225 < y < 337.5:
                four_cells.append(9)
            if 112.5 < x < 225 and 225 < y < 337.5:
                four_cells.append(10)
            if 225 < x < 337.5 and 225 < y < 337.5:
                four_cells.append(11)
            if 337.5 < x <= 450 and 225 < y < 337.5:
                four_cells.append(12)

            if x < 112.5 and 337.5 < y <= 450:
                four_cells.append(13)
            if 112.5 < x < 225 and 337.5 < y <= 450:
                four_cells.append(14)
            if 225 < x < 337.5 and 337.5 < y <= 450:
                four_cells.append(15)
            if 337.5 < x <= 450 and 337.5 < y <= 450:
                four_cells.append(16)
        answer = get_occupied_cells(four_cells)
        count += 1
        for ans in answer:
            answers.append(ans)
    answers = sorted(list(answers))
    return list(set(answers))


def solve_recaptcha(driver, verbose):
    """
    Solve the recaptcha.
    :param driver: selenium driver.
    :param verbose: print verbose.
    """

    go_to_recaptcha_iframe1(driver)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.XPATH, '//div[@class="recaptcha-checkbox-border"]'))).click()

    go_to_recaptcha_iframe2(driver)

    model = YOLO("./yolov8x.onnx", task="detect")

    while True:
        try:
            while True:
                reload = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, 'recaptcha-reload-button')))
                title_wrapper = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, 'rc-imageselect')))

                target_num = get_target_num(driver)

                if target_num == 1000:
                    random_delay()
                    if verbose: print("skipping")
                    reload.click()
                elif "squares" in title_wrapper.text:
                    if verbose: print("Square captcha found....")
                    img_urls = get_all_captcha_img_urls(driver)
                    download_img(0, img_urls[0])
                    answers = square_solver(target_num, verbose, model)
                    if len(answers) >= 1 and len(answers) < 16:
                        captcha = "squares"
                        break
                    else:
                        reload.click()
                elif "none" in title_wrapper.text:
                    if verbose: print("found a 3x3 dynamic captcha")
                    img_urls = get_all_captcha_img_urls(driver)
                    download_img(0, img_urls[0])
                    answers = dynamic_and_selection_solver(target_num, verbose, model)
                    if len(answers) > 2:
                        captcha = "dynamic"
                        break
                    else:
                        reload.click()
                else:
                    if verbose: print("found a 3x3 one time selection captcha")
                    img_urls = get_all_captcha_img_urls(driver)
                    download_img(0, img_urls[0])
                    answers = dynamic_and_selection_solver(target_num, verbose, model)
                    if len(answers) > 2:
                        captcha = "selection"
                        break
                    else:
                        reload.click()
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                    (By.XPATH, '(//div[@id="rc-imageselect-target"]//td)[1]')))

            if captcha == "dynamic":
                for answer in answers:
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                        (By.XPATH, f'(//div[@id="rc-imageselect-target"]//td)[{answer}]'))).click()
                    random_delay(mu=0.5, sigma=0.2)
                while True:
                    before_img_urls = img_urls
                    while True:
                        is_new, img_urls = get_all_new_dynamic_captcha_img_urls(
                            answers, before_img_urls, driver)
                        if is_new:
                            break

                    new_img_index_urls = []
                    for answer in answers:
                        new_img_index_urls.append(answer-1)
                    new_img_index_urls

                    for index in new_img_index_urls: download_img(index+1, img_urls[index])
                    while True:
                        try:
                            for answer in answers:
                                main_img = Image.open("0.png")
                                new_img = Image.open(f"{answer}.png")
                                location = answer
                                paste_new_img_on_main_img(
                                    main_img, new_img, location)
                            break
                        except:
                            while True:
                                is_new, img_urls = get_all_new_dynamic_captcha_img_urls(
                                    answers, before_img_urls, driver)
                                if is_new:
                                    break
                            new_img_index_urls = []
                            for answer in answers:
                                new_img_index_urls.append(answer-1)

                            for index in new_img_index_urls:
                                download_img(index+1, img_urls[index])

                    answers = dynamic_and_selection_solver(target_num, verbose, model)

                    if len(answers) >= 1:
                        for answer in answers:
                            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                                (By.XPATH, f'(//div[@id="rc-imageselect-target"]//td)[{answer}]'))).click()
                            random_delay(mu=0.5, sigma=0.1)
                    else:
                        break
            elif captcha == "selection" or captcha == "squares":
                for answer in answers:
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                        (By.XPATH, f'(//div[@id="rc-imageselect-target"]//td)[{answer}]'))).click()
                    random_delay()

            verify = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
                (By.ID, "recaptcha-verify-button")))
            random_delay(mu=2, sigma=0.2)
            verify.click()

            try:
                go_to_recaptcha_iframe1(driver)
                WebDriverWait(driver, 4).until(
                    EC.presence_of_element_located((By.XPATH, '//span[contains(@aria-checked, "true")]')))
                if verbose: print("solved")
                driver.switch_to.default_content()
                break
            except:
                go_to_recaptcha_iframe2(driver)
        except Exception as e:
            print(e)


def solver(url: str, cookies: dict=None, proxy: str=None, verbose=False, headless=True):
    """
    Solve the recaptcha.
    :param url: url of the recaptcha.
    :param cookies: cookies of the recaptcha.
    :param proxy: proxy for seleniumwire.
    :param verbose: print verbose.
    :param headless: run in headless mode.
    """

    # Set Up seleniumwire options with proxy if provided
    if proxy:
        seleniumwire_options = {
            'proxy': {
                'http': f'http://{proxy}',
                'https': f'https://{proxy}'
            },
            'no_proxy': 'localhost,127.0.0.1',
            'disable_encoding': True,
            'verify_ssl': False
        }
    else:
        seleniumwire_options = {
            'no_proxy': 'localhost,127.0.0.1',
            'disable_encoding': True,
            'verify_ssl': False
        }

    # Set Up Chrome Options with headless and no image loading if provided
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--ignore-certificate-errors-spki-list')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--lang=en-US')
    if headless:
        chrome_options.add_argument('--headless')
        chrome_prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", chrome_prefs)

    # Initialize driver with options and cookies if provided
    driver = webdriver.Chrome(options=chrome_options, seleniumwire_options=seleniumwire_options)
    driver.scopes = ['.*google.com/recaptcha.*']
    if cookies: driver.add_cookie(cookies)

    # Solve recaptcha
    driver.get(url)
    start = time()
    solve_recaptcha(driver, verbose)

    # Get recaptcha token and cookies
    for request in driver.requests:
        if 'recaptcha/api2/userverify' in request.url: token = find_between(request.response.body.decode('utf-8'), 'uvresp","', '"')
    cookies = driver.get_cookies()

    # Close driver and return results
    driver.quit()
    time_taken = (time() - start).__round__(2)
    
    return {"recaptcha_token" : token, "cookies" : cookies, "time_taken": time_taken}
