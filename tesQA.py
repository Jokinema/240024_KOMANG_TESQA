import time

from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

debug_delay = 15
def run_test1(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")  # Bypass OS security model, REQUIRED for Docker and some Linux environments
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--disable-gpu")  # Applicable for headless setups, but may be deprecated soon
    options.add_argument('--disable-software-rasterizer')
    options.add_argument("--verbose")
    options.add_argument("--log-path=chrome.log")
    driver = webdriver.Chrome(options=options)
    score = 0
    max = 45
    message = []
    try:
        driver.get(url)
        button = WebDriverWait(driver, 20 + debug_delay).until(
            EC.presence_of_element_located((By.XPATH, "//button"))
        )
        try:
            # Check for the presence of the button

            score += 5  # Button exists, +5 points

            # Check if the button's text is "HelloWord"
            if button.text == "HelloWord":
                score += 10  # Correct text, +10 points
            else:
                message.append("Button text is incorrect")
                score += 0  # Incorrect text, +0 points

        except TimeoutException:
            message.append("Button not found")
            score += 0  # No button found, +0 points

        try:
            # Trigger the button click and check for alert
            button.click()
            alert = WebDriverWait(driver, 2 + debug_delay).until(EC.alert_is_present())
            alert_text = alert.text
            alert.accept()
            score += 5  # Alert exists, +5 points

            # Check the text of the alert
            if alert_text == "Hello!":
                score += 10  # Correct alert text, +10 points
            else:
                message.append("""Alert text is incorrect""")
                score += 5  # Incorrect alert text, +5 points

            alert = WebDriverWait(driver, 2 + debug_delay).until(EC.alert_is_present())
            alert_text = alert.text
            alert.accept()
            score += 5  # Alert exists, +5 points

            # Check the text of the alert
            if alert_text == "Goodbye":
                score += 10  # Correct alert text, +10 points
            else:
                message.append("""Alert text is incorrect""")
                score += 5  # Incorrect alert text, +5 points

        except TimeoutException:
            score += 0  # No alert found after click, +0 points

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        message.append(f"An error occurred: {str(e)}")
    finally:
        driver.quit()
        return score, max, message



def run_test2(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")  # Bypass OS security model, REQUIRED for Docker and some Linux environments
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--disable-gpu")  # Applicable for headless setups, but may be deprecated soon
    options.add_argument('--disable-software-rasterizer')  # Not Using Any Extentionsion
    options.add_argument("--verbose")
    options.add_argument("--log-path=chrome.log")

    score = 0
    max = 50
    message = []
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)

        # Check for presence and interact with username input
        try:
            username_input = WebDriverWait(driver, 10 + debug_delay).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Username']")) # Regeular Expression REGEX
            )
            username_input.send_keys("admin")
            score += 10  # Presence and interaction successful, +10 points
        except TimeoutException:
            message.append("Username input not found.")
            score += 0  # Username input missing, +0 points

        # Check for presence and interact with password input
        try:
            password_input = WebDriverWait(driver, 5 + debug_delay).until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Password']"))
            )
            password_input.send_keys("password")
            score += 10  # Presence and interaction successful, +10 points
        except TimeoutException:
            message.append("Password input not found.")
            score += 0  # Password input missing, +0 points

        # Check for presence and interaction with the login button
        try:
            login_button = WebDriverWait(driver, 5 + debug_delay).until(
                EC.element_to_be_clickable((By.XPATH, "//button"))
            )
            login_button.click()
            score += 10  # Button click successful, +10 points
        except TimeoutException:
            message.append("Login button not clickable or not found.")
            score += 0  # Button missing or not clickable, +0 points

        # Check for success message
        try:
            success_message = WebDriverWait(driver, 5 + debug_delay).until(
                EC.visibility_of_element_located((By.XPATH, "//h1"))
            )
            print(success_message)
            print("Login success: 'Halo, admin!' found.")
            score += 20  # Correct success message found, +20 points
        except TimeoutException:
            # Check  for failure alert
            try:
                alert = WebDriverWait(driver, 5 + debug_delay).until(EC.alert_is_present())
                alert_text = alert.text
                alert.accept()
                if alert_text == "Login gagal.":
                    print("Login failed alert confirmed.")
                    score += 10  # Correct failure alert found, +10 points
                else:
                    message.append("Unexpected alert text.")
                    score += 5  # Alert found, but text incorrect, +5 points
            except TimeoutException:
                message.append("No alert or message after login attempt.")
                score += 0  # No alert or message after login, +0 points

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        message.append(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

    print(f"Final Score: {score}")
    return score, max, message

def run_test3(url) :
    # Configuration for headless mode
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")  # Bypass OS security model, REQUIRED for Docker and some Linux environments
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--disable-gpu")  # Applicable for headless setups, but may be deprecated soon
    options.add_argument('--disable-software-rasterizer')
    options.add_argument("--verbose")
    options.add_argument("--log-path=chrome.log")
    driver = webdriver.Chrome(options=options)

    # Maximum points and initial score
    max_score = 60
    score = 0
    message = []
    try:
        driver.get(url)

        # Wait for the input box to be visible and interactable
        input_box = WebDriverWait(driver, 10 + debug_delay).until(
            EC.visibility_of_element_located((By.TAG_NAME, "input"))
        )

        # Set an initial value
        input_box.clear()
        input_box.send_keys("22")
        set_button = driver.find_element(By.XPATH, "//button[text()='Set']")
        set_button.click()

        # Check if the number is correctly set
        count_display = driver.find_element(By.TAG_NAME, "h1")
        if count_display.text == "22":
            print("Set to 22: Success")
            score += 15
        else:
            message.append("Set to 22: Fail")

        # Increment the number
        increment_button = driver.find_element(By.XPATH, "//button[text()='Increment']")
        increment_button.click()
        if count_display.text == "23":
            print("Increment to 23: Success")
            score += 15
        else:
            message.append("Increment to 23: Fail")

        # Decrement the number
        decrement_button = driver.find_element(By.XPATH, "//button[text()='Decrement']")
        decrement_button.click()
        decrement_button.click()  # Decrement twice
        if count_display.text == "21":
            print("Decrement to 21: Success")
            score += 15
        else:
            message.append("Decrement to 21: Fail")

        # Reset the number
        reset_button = driver.find_element(By.XPATH, "//button[text()='Reset']")
        reset_button.click()
        if count_display.text == "0":
            print("Reset to 0: Success")
            score += 15
        else:
            message.append("Reset to 0: Fail")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        message.append(f"Error: {str(e)}")
    finally:
        driver.quit()

    print(f"Final Score: {score} out of {max_score}")
    return score, max_score, message
def run_test4(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")  # Bypass OS security model, REQUIRED for Docker and some Linux environments
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--disable-gpu")  # Applicable for headless setups, but may be deprecated soon
    options.add_argument('--disable-software-rasterizer')
    options.add_argument("--verbose")
    options.add_argument("--log-path=chrome.log")
    driver = webdriver.Chrome(options=options)
    score = 0
    max_score = 25
    message= []

    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.TAG_NAME, "h1"))
        )

        # Enter username and password for a successful login
        username_input = driver.find_element(By.XPATH, "//input[@placeholder='Username']")
        password_input = driver.find_element(By.XPATH, "//input[@placeholder='Password']")

        username_input.send_keys("React")
        password_input.send_keys("password")

        # Click the login button
        login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
        login_button.click()

        # Check for Sweet Alert for successful login
        try:
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "swal2-title"))
            )
            success_title = driver.find_element(By.CLASS_NAME, "swal2-title").text
            if success_title == "Login Successful!":
                print("Successful login alert verified.")
                score += 25
        except TimeoutException:
            message.append("Sweet alert for successful login not found.")

        # Clear inputs for a failed login attempt
        username_input.clear()
        password_input.clear()

        username_input.send_keys("wronguser")
        password_input.send_keys("wrongpass")
        login_button.click()

        # Check for Sweet Alert for failed login
        try:
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "swal2-title"))
            )
            fail_title = driver.find_element(By.CLASS_NAME, "swal2-title").text
            if fail_title == "Login Failed!":
                print("Failed login alert verified.")
                score += 20
        except TimeoutException:
            message.append("Sweet alert for failed login not found.")

        # Toggle show password
        show_password_checkbox = driver.find_element(By.XPATH, "//input[@type='checkbox']")
        show_password_checkbox.click()

        # Check if the password input type has changed
        password_type = password_input.get_attribute("type")
        if password_type == "text":
            print("Password visibility toggle verified.")
            score += 5

    except Exception as e:
        message.append(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

    final_score = min(score, max_score)
    print(f"Final Score: {final_score} out of {max_score}")
    return final_score, max_score, message

def run_test5(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")  # Bypass OS security model, REQUIRED for Docker and some Linux environments
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--disable-gpu")  # Applicable for headless setups, but may be deprecated soon
    options.add_argument('--disable-software-rasterizer')
    options.add_argument("--verbose")
    options.add_argument("--log-path=chrome.log")
    driver = webdriver.Chrome(options=options)
    score = 0
    max_score = 50
    messages = []
    try:
        driver.get(url)

        # Assuming the user is already logged in and at the page with the logout button
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".logout-button"))
        )

        # Click the logout button
        logout_button = driver.find_element(By.CSS_SELECTOR, ".logout-button")
        logout_button.click()

        # Wait for the logout confirmation Sweet Alert and interact with it
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "swal2-confirm"))
        )
        confirm_button = driver.find_element(By.CLASS_NAME, "swal2-confirm")
        confirm_button.click()

        # Wait for the success alert and validate
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "swal2-title"))
        )
        success_message = driver.find_element(By.CLASS_NAME, "swal2-title").text
        if "Logged Out" in success_message:

            messages.append("Logout success alert verified.")
            score += 25
        else:
            messages.append("Logout success alert text incorrect.")

        # Check if the user is redirected to the login page
        WebDriverWait(driver, 5).until(
            EC.url_contains("/")
        )
        if "/" in driver.current_url:
            messages.append("Redirect to login page verified.")
            score += 25
        else:
            messages.append("Redirect to login page failed.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        messages.append(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

    final_score = min(score, max_score)
    print(f"Final Score: {final_score} out of {max_score}")
    return final_score, max_score, messages


def run_test_php1(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")  # Bypass OS security model, REQUIRED for Docker and some Linux environments
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--disable-gpu")  # Applicable for headless setups, but may be deprecated soon
    options.add_argument('--disable-software-rasterizer')
    options.add_argument("--verbose")
    options.add_argument("--log-path=chrome.log")
    driver = webdriver.Chrome(options=options)

    score = 0
    max_score = 20  # Assuming two checks: connection and table creation
    message = []
    try:
        driver.get(url)

        # Wait for the page to load and check the text content
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        body_text = driver.find_element(By.TAG_NAME, "body").text

        # Check for database connection message
        if "Koneksi dengan MYSQL berhasil" in body_text:
            print("Database connection successful.")
            message.append("Database connection successful.")
            score += 10
        else:
            message.append("Database connection failed.")
            print("Database connection failed.")
            score += 5

        # Check for table creation message
        if "Tabel siswa berhasil dibuat" in body_text or "exist" in body_text:
            message.append("Table creation successful.")
            print("Table creation successful.")
            score += 10
        else:
            print("Table creation failed.")
            message.append("Table creation failed.")
            score += 5

    except Exception as e:
        print(f"An error occurred during the test: {str(e)}")
        message.append(f"An error occurred during the test: {str(e)}")

    finally:
        driver.quit()

    print(f"Final Score: {score} out of {max_score}")
    return score, max_score, message

def run_test_php2(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")  # Bypass OS security model, REQUIRED for Docker and some Linux environments
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--disable-gpu")  # Applicable for headless setups, but may be deprecated soon
    options.add_argument('--disable-software-rasterizer')
    options.add_argument("--verbose")
    options.add_argument("--log-path=chrome.log")
    driver = webdriver.Chrome(options=options)

    score = 0
    max_score = 10  # Assuming two checks: connection and table creation

    messages = []
    try:
        driver.get(url)

        # Check if the failure message is displayed
        try:
            # Wait for any possible error message (specifically looking for connection failure)
            error_message = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//body[contains(text(), 'Koneksi dengan MYSQL gagal')]"))
            )
            print("Database connection failed. Error: " + error_message.text)
            score += 5  # Partial score since the connection failed
        except TimeoutException:
            # No error message, assuming connection was successful
            messages.append("No error message found. Assuming database connection was successful.")
            score += 10  # Full score for successful connection

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        messages.append(f"An error occurred: {str(e)}")

    finally:
        driver.quit()

    print(f"Final Score: {score} out of {max_score}")
    return score,  max_score, messages
def run_test_php3(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")  # Bypass OS security model, REQUIRED for Docker and some Linux environments
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--disable-gpu")  # Applicable for headless setups, but may be deprecated soon
    options.add_argument('--disable-software-rasterizer')
    options.add_argument("--verbose")
    options.add_argument("--log-path=chrome.log")
    driver = webdriver.Chrome(options=options)
    total_score = 20  # Maximum possible score
    score = 0
    messages = []
    try:
        driver.get(url)

        # Wait for the page to load and read the body text
        body_text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        ).text

        # Check for database connection success or failure
        if "Koneksi dengan MYSQL berhasil" in body_text:
            print("Database connection successful.")
            score += 10
        elif "Koneksi dengan MYSQL gagal" in body_text:
            messages.append("Database connection failed.")
            score += 5

        # Check for successful data insertion
        if "Data berhasil" in body_text:
            print("Data insertion successful.")
            score += 10
        elif "Data gagal ditambahkan" in body_text:
            messages.append("Data insertion failed.")
            score += 5

    except TimeoutException:
        print("The page did not load in time or the expected text was not found.")
        messages.append("The page did not load in time or the expected text was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        messages.append(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

    print(f"Final Score: {score} out of {total_score}")
    return score, total_score, messages
def run_test_php4(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")  # Bypass OS security model, REQUIRED for Docker and some Linux environments
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--disable-gpu")  # Applicable for headless setups, but may be deprecated soon
    options.add_argument('--disable-software-rasterizer')
    options.add_argument("--verbose")
    options.add_argument("--log-path=chrome.log")
    driver = webdriver.Chrome(options=options)
    total_score = 20  # Maximum possible score
    score = 0
    messages = []
    try:
        driver.get(url)

        # Wait for the page to load and read the body text
        body_text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        ).text

        # Check for database connection success or failure
        if "Koneksi dengan MYSQL berhasil" in body_text:
            print("Database connection successful.")
            score += 10  # Full points for successful connection
        elif "Koneksi dengan MYSQL gagal" in body_text:
            print("Database connection failed.")
            messages.append("Database connection failed.")
            score += 5  # Half points for connection failure

        # Check for successful database creation
        if "Database berhasil" in body_text or "database exists"  in body_text :
            print("Database creation successful.")
            score += 10  # Full points for successful creation
        elif "Database gagal dibuat" in body_text:
            print("Database creation failed.")
            messages.append("Database creation failed.")
            score += 5  # Half points for creation failure

    except TimeoutException:
        print("The page did not load in time or the expected text was not found.")
        messages.append("The page did not load in time or the expected text was not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        messages.append(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

    print(f"Final Score: {score} out of {total_score}")
    return score,total_score, messages

def run_test_php5(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")  # Bypass OS security model, REQUIRED for Docker and some Linux environments
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--disable-gpu")  # Applicable for headless setups, but may be deprecated soon
    options.add_argument('--disable-software-rasterizer')
    options.add_argument("--verbose")
    options.add_argument("--log-path=chrome.log")
    driver = webdriver.Chrome(options=options)
    total_score = 20  # Maximum possible score
    score = 0
    messages = []
    try:
        driver.get(url)

        # Fill out the form with test data
        driver.find_element(By.NAME, "nama_depan").send_keys("Ahmad")
        driver.find_element(By.NAME, "nama_belakang").send_keys("Fikri")
        driver.find_element(By.NAME, "email").send_keys("ahmadfikri@gmail.com")
        driver.find_element(By.ID, "laki-laki").click()  # Selecting 'Laki-Laki' radio button

        # Submit the form
        driver.find_element(By.NAME, "submit").click()

        # Wait for possible redirection or check for a specific element indicating success
        redirected_url = "selectTable_Siswa.php"
        WebDriverWait(driver, 10).until(
            EC.url_contains(redirected_url)
        )
        current_url = driver.current_url
        if redirected_url in current_url:
            print("Redirection to selectTable_Siswa.php confirmed, indicating successful submission.")
            score += 20  # Full points for successful submission and correct redirection
        else:
            print("Failed to redirect after submission.")
            messages.append("Failed to redirect after submission.")
            score += 10  # Half points if the redirection does not happen as expected

    except TimeoutException:
        print("The page did not redirect in time or the expected confirmation was not found.")
        messages("The page did not redirect in time or the expected confirmation was not found.")
        score += 0  # No points if there's a timeout exception
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        messages(f"An error occurred: {str(e)}")
    finally:
        driver.quit()

    print(f"Final Score: {score} out of {total_score}")
    return score, total_score, messages
def run_test_php6(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")  # Bypass OS security model, REQUIRED for Docker and some Linux environments
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--disable-gpu")  # Applicable for headless setups, but may be deprecated soon
    options.add_argument('--disable-software-rasterizer')
    options.add_argument("--verbose")
    options.add_argument("--log-path=chrome.log")
    driver = webdriver.Chrome(options=options)
    score = 0
    max_score = 20  # Total score for checking various elements
    massages = []
    try:
        driver.get(url)

        # Check for the presence of the table
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        print("Table is present on the page.")
        score += 10  # Award points for table presence

        # Check for the "Add New Data" button and its functionality
        add_new_data_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Add New Data"))
        )
        add_new_data_button.click()  # Simulate clicking the button to navigate to the add new data page

        # Assuming the add page has a specific identifier like a form or a title
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "form"))
        )
        print("Navigated to Add New Data form successfully.")
        score += 10  # Award points for successful navigation

        # Optionally, check for a message if there's a msg parameter in the URL
        if "msg" in driver.current_url:
            message = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert"))
            )
            if message.text:
                print("Message displayed: " + message.text)
                massages.append("Message displayed: " + message.text)
                score += 10  # Award points for displaying a message

    except TimeoutException as e:
        print("An element was not found: " + str(e))
        massages.append("An element was not found: "+ str(e))
    except Exception as e:
        print("An error occurred: " +  str(e))
        massages.append("An error occurred: "+str(e))
    finally:
        driver.quit()

    print(f"Final Score: {score} out of {max_score}")
    return score, max_score, massages
def  run_test_php7(selectEmail1, selectEmail2, editedEmail1, editedEmail2, url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")  # Bypass OS security model, REQUIRED for Docker and some Linux environments
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--disable-gpu")  # Applicable for headless setups, but may be deprecated soon
    options.add_argument('--disable-software-rasterizer')
    options.add_argument("--verbose")
    options.add_argument("--log-path=chrome.log")
    driver = webdriver.Chrome(options=options)
    total = 40
    min = 0
    score = 0
    messages = []


    try:
        driver.get(url)
        # Wait for the table to load
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
        email_element = driver.find_element(By.XPATH, f"//td[contains(text(), '{selectEmail1}')]")
        parent_row = email_element.find_element(By.XPATH, "./..")
        id_element = parent_row.find_element(By.XPATH, "./td[1]")  # Assuming ID is in the first column
        student_id = id_element.text

        # Find the edit link using the student ID
        edit_link = parent_row.find_element(By.XPATH, f".//a[@href='editData_Siswa.php?id={student_id}']")
        edit_link.click()
        score += 10
        time.sleep(3)
        # Wait for the edit page to load
        # Wait for the form to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'email')))

        # Clear the existing email and enter a new one
        email_field = driver.find_element(By.NAME, 'email')
        email_field.clear()
        email_field.send_keys(editedEmail1)

        # Submit the form
        update_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Update')]")
        update_button.click()
        score += 20
        # Optionally, confirm the update was successful
        driver.get(url)

        time.sleep(3)
        # Wait for the table to load and check for the new email
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
        table_body = driver.find_element(By.TAG_NAME, 'tbody')
        rows = table_body.find_elements(By.TAG_NAME, 'tr')

        # Check for the presence of the new email and absence of the old
        emails = [row.find_element(By.XPATH, ".//td[4]").text for row in rows]  # Assuming email is in the fourth column
        print(emails)
        if editedEmail1 in emails and selectEmail1 not in emails:
            score += 10
            print("Email updated successfully and verified in the table.")
        else:
            print("Email update verification failed.")
            messages.append("Email update verification failed.")

        # loop 2

        if selectEmail2 != "null":
            total *= 2
            driver.get(url)

            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
            email_element = driver.find_element(By.XPATH, f"//td[contains(text(), '{selectEmail2}')]")
            parent_row = email_element.find_element(By.XPATH, "./..")
            id_element = parent_row.find_element(By.XPATH, "./td[1]")  # Assuming ID is in the first column
            student_id = id_element.text

            # Find the edit link using the student ID
            edit_link = parent_row.find_element(By.XPATH, f".//a[@href='editData_Siswa.php?id={student_id}']")
            edit_link.click()
            score += 10
            time.sleep(3)
            # Wait for the edit page to load
            # Wait for the form to load
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'email')))

            # Clear the existing email and enter a new one
            email_field = driver.find_element(By.NAME, 'email')
            email_field.clear()
            email_field.send_keys(editedEmail2)

            # Submit the form
            update_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Update')]")
            update_button.click()
            score += 20
            # Optionally, confirm the update was successful
            driver.get(url)
            time.sleep(3)
            # Wait for the table to load and check for the new email
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
            table_body = driver.find_element(By.TAG_NAME, 'tbody')
            rows = table_body.find_elements(By.TAG_NAME, 'tr')

            # Check for the presence of the new email and absence of the old
            emails = [row.find_element(By.XPATH, ".//td[4]").text for row in
                      rows]  # Assuming email is in the fourth column
            print(emails)
            if editedEmail2 in emails and selectEmail2 not in emails:
                score += 10
                print("Email updated successfully and verified in the table.")
            else:
                print("Email update verification failed.")
                messages.append("Email update verification failed.")
        else :
            print("Tidak Ada Email 2")
            messages.append("Tidak Ada Email 2")

        print((score / total) * 100)

    except Exception as e:
        print(f"Error navigating to edit page: {str(e)}")
        messages.append(f"Error navigating to edit page: {str(e)}")

    finally:
        driver.quit()

    print(f"Final Score: {score} out of {total}")
    return score, total, messages
def run_test_php8(selectEmail1, selectEmail2, url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")  # Bypass OS security model, REQUIRED for Docker and some Linux environments
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--disable-gpu")  # Applicable for headless setups, but may be deprecated soon
    options.add_argument('--disable-software-rasterizer')
    options.add_argument("--verbose")
    options.add_argument("--log-path=chrome.log")
    driver = webdriver.Chrome(options=options)

    total = 30
    min = 0
    score = 0
    messages = []

    try:
        driver.get(url)

        # Wait for the table to load
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
        email_element = driver.find_element(By.XPATH, f"//td[contains(text(), '{selectEmail1}')]")
        parent_row = email_element.find_element(By.XPATH, "./..")
        id_element = parent_row.find_element(By.XPATH, "./td[1]")  # Assuming ID is in the first column
        student_id = id_element.text

        # Find the edit link using the student ID
        edit_link = parent_row.find_element(By.XPATH, f".//a[@href='deleteData_Siswa.php?id={student_id}']")
        edit_link.click()
        score += 10
        time.sleep(3)

        # Optionally, confirm the update was successful
        driver.get(url)

        time.sleep(3)
        # Wait for the table to load and check for the new email
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
        table_body = driver.find_element(By.TAG_NAME, 'tbody')
        rows = table_body.find_elements(By.TAG_NAME, 'tr')

        # Check for the presence of the new email and absence of the old
        emails = [row.find_element(By.XPATH, ".//td[4]").text for row in rows]  # Assuming email is in the fourth column
        print(emails)
        if selectEmail1 not in emails:
            score += 20
            print("Email updated successfully and verified in the table.")
        else:
            print("Email update verification failed.")
            messages.append("Email update verification failed.")

        # loop 2

        if selectEmail2 != "null":
            total *= 2
            driver.get(url)

            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
            email_element = driver.find_element(By.XPATH, f"//td[contains(text(), '{selectEmail2}')]")
            parent_row = email_element.find_element(By.XPATH, "./..")
            id_element = parent_row.find_element(By.XPATH, "./td[1]")  # Assuming ID is in the first column
            student_id = id_element.text

            # Find the edit link using the student ID
            edit_link = parent_row.find_element(By.XPATH, f".//a[@href='deleteData_Siswa.php?id={student_id}']")
            edit_link.click()
            score += 10
            time.sleep(3)

            # Optionally, confirm the update was successful
            driver.get(url)

            time.sleep(3)
            # Wait for the table to load and check for the new email
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'tbody')))
            table_body = driver.find_element(By.TAG_NAME, 'tbody')
            rows = table_body.find_elements(By.TAG_NAME, 'tr')

            # Check for the presence of the new email and absence of the old
            emails = [row.find_element(By.XPATH, ".//td[4]").text for row in
                      rows]  # Assuming email is in the fourth column
            print(emails)
            if selectEmail2 not in emails:
                score += 20
                print("Email updated successfully and verified in the table.")
            else:
                print("Email update verification failed.")
                messages.append("Email update verification failed.")

        else:
            print("Tidak Ada Email 2")
            messages.append("Tidak Ada Email 2")

        print((score / total) * 100)

    except Exception as e:
        print(f"Error navigating to edit page: {str(e)}")
        messages.append(f"Error navigating to edit page: {str(e)}")

    finally:
        driver.quit()


    print(f"Final Score: {score} out of {total} points.")
    return score, total, messages

@app.route('/php/uji/LatSoal1/<path:url>')
def test_endpoint_php1(url):
    score , max, massage= run_test_php1(url)
    print(massage)
    print(score)
    return jsonify({
        'massage': massage,
        'score': score,
        'in_percent': round((score / max) * 100, 2),
        'max': max,
        'min': 0
    }), 200

@app.route('/php/uji/LatSoal2/<path:url>')
def test_endpoint_php3(url):
    score, max, massage = run_test_php3(url)
    print(massage)
    print(score)
    return jsonify({
        'massage': massage,
        'score': score,
        'in_percent': round((score / max) * 100, 2),
        'max': max,
        'min': 0
    }), 200

@app.route('/php/uji/LatSoal3/<path:url>')
def test_endpoint_php5(url):
    score, max, massage = run_test_php5(url)
    print(massage)
    print(score)
    return jsonify({
        'massage': massage,
        'score': score,
        'in_percent': round((score / max) * 100, 2),
        'max': max,
        'min': 0
    }), 200

@app.route('/php/uji/LatSoal4/<path:url>') # select
def test_endpoint_php6(url):
    score, max, massage = run_test_php6(url)
    print(massage)
    print(score)
    return jsonify({
        'massage': massage,
        'score': score,
        'in_percent': round((score / max) * 100, 2),
        'max': max,
        'min': 0
    }), 200
@app.route('/php/uji/LatSoal5/<selectEmail1>/<selectEmail2>/<editedEmail1>/<editedEmail2>/<path:url>') # editSiswa
def test_endpoint_php7(selectEmail1, selectEmail2, editedEmail1, editedEmail2, url):
    score, max, massage = run_test_php7(selectEmail1, selectEmail2, editedEmail1, editedEmail2, url)
    print(massage)
    print(score)
    return jsonify({
        'massage': massage,
        'score': score,
        'in_percent': round((score / max) * 100, 2),
        'max': max,
        'min': 0
    }), 200

@app.route('/php/uji/LatSoal6/<selectEmail1>/<selectEmail2>/<path:url>') #delete
def test_endpoint_php8(selectEmail1, selectEmail2, url):
    score, max,massage = run_test_php8(selectEmail1, selectEmail2, url)
    print(massage)
    print(score)
    return jsonify({
        'massage': massage,
        'score': score,
        'in_percent': round((score / max) * 100, 2),
        'max': max,
        'min': 0
    }), 200

@app.route('/php/uji/Prak1/<path:url>')
def test_endpoint_php2(url):
    score, max, massage = run_test_php2(url)
    print(massage)
    print(score)
    return jsonify({
        'massage': massage,
        'score': score,
        'in_percent': round((score / max) * 100, 2),
        'max': max,
        'min': 0
    }), 200

@app.route('/php/uji/Prak2/<path:url>')
def test_endpoint_php4(url):
    score, max, massage = run_test_php4(url)
    print(massage)
    print(score)
    return jsonify({
        'massage': massage,
        'score': score,
        'in_percent': round((score / max) * 100, 2),
        'max': max,
        'min': 0
    }), 200


@app.route('/react/uji/RUII2/<path:url>')
def test_endpoint1(url):
    score, max, massage = run_test1(url)
    print(massage)
    print(score)
    return jsonify({
        'massage': massage,
        'score': score,
        'in_percent': round((score / max) * 100, 2),
        'max': max,
        'min': 0
    }), 200

@app.route('/react/uji/RUII3/<path:url>')
def test_endpoint2(url):
    score,  max, massage = run_test2(url)
    print(massage)
    print(score)
    return jsonify({
        'massage': massage,
        'score': score,
        'in_percent': round((score / max) * 100, 2),
        'max': max,
        'min': 0
    }), 200

@app.route('/react/uji/RUII4/<path:url>')
def test_endpoint3(url):
    score,  max, massage = run_test3(url)
    print(massage)
    print(score)
    return jsonify({
        'massage': massage,
        'score': score,
        'in_percent': round((score / max) * 100, 2),
        'max': max,
        'min': 0
    }), 200

@app.route('/react/uji/RUII5/<path:url>')
def test_endpoint4(url):
    score, max, massage = run_test4(url)
    print(massage)
    print(score)
    return jsonify({
        'massage': massage,
        'score': score,
        'in_percent': round((score / max) * 100, 2),
        'max': max,
        'min': 0
    }), 200

@app.route('/react/uji/RUII6/<path:url>')
def test_endpoint5(url):
    score, max, massage = run_test5(url)
    print(massage)
    print(score)
    return jsonify({
        'massage': massage,
        'score': score,
        'in_percent': round((score / max) * 100, 2),
        'max': max,
        'min': 0
    }), 200



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

