import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService

class WebAppFunctionalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_driver_path = ChromeDriverManager().install()
        cls.driver = webdriver.Chrome(service=ChromeService(executable_path=chrome_driver_path))
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def retry_find_element(self, by, value):
        for _ in range(3):
            try:
                return self.driver.find_element(by, value)
            except StaleElementReferenceException:
                continue
        raise NoSuchElementException(f"Element not found: {value}")

    def retry_click_element(self, by, value):
        for _ in range(3):
            try:
                element = self.driver.find_element(by, value)
                element.click()
                return
            except StaleElementReferenceException:
                continue
        raise NoSuchElementException(f"Element not found: {value}")

    def test_login_functionality(self):
        driver = self.driver
        driver.get('http://localhost:5000/auth/login')

        # Testing for bad login attempts
        username = self.retry_find_element(By.NAME, 'username')
        password = self.retry_find_element(By.NAME, 'password')
        login_button = self.retry_find_element(By.CSS_SELECTOR, 'button.btn.btn-primary')

        username.send_keys('wronguser')
        password.send_keys('wrongpassword')
        self.retry_click_element(By.CSS_SELECTOR, 'button.btn.btn-primary')

        try:
            # Check if any error message is displayed
            WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "custom-alert"))
            )
            error_message = self.retry_find_element(By.CLASS_NAME, 'custom-alert').text
            self.assertIn('Invalid username or password', error_message)
        except TimeoutException as e:
            print("TimeoutException occurred: ", e)
            print("Page source: ")
            print(driver.page_source)
            raise
        except Exception as e:
            print("Exception occurred: ", e)
            print("Page source: ")
            print(driver.page_source)
            raise

        # Clear input for correct login attempt
        username = self.retry_find_element(By.NAME, 'username')
        password = self.retry_find_element(By.NAME, 'password')
        username.clear()
        password.clear()

        username.send_keys('eric')
        password.send_keys('root')
        self.retry_click_element(By.CSS_SELECTOR, 'button.btn.btn-primary')

        try:
            # Verify that the login is successful and navigate to the dashboard page
            WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, "//h2[text()='My Requests']"))
            )
            dashboard_heading = self.retry_find_element(By.XPATH, "//h2[text()='My Requests']").text
            self.assertIn('My Requests', dashboard_heading)
        except TimeoutException as e:
            print("TimeoutException occurred: ", e)
            print("Page source: ")
            raise
        except Exception as e:
            print("Exception occurred: ", e)
            print("Page source: ")
            raise

        # Navigate to the profile page
        self.retry_click_element(By.CSS_SELECTOR, 'a.nav-link[href="/profile/update_profile"]')
        try:
            WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, "//h2[text()='Update Your Profile:']"))
            )
            profile_heading = self.retry_find_element(By.XPATH, "//h2[text()='Update Your Profile:']").text
            self.assertIn('Update Your Profile:', profile_heading)
        except TimeoutException as e:
            print("TimeoutException occurred: ", e)
            print("Page source: ")
            raise
        except Exception as e:
            print("Exception occurred: ", e)
            print("Page source: ")
            raise

        # Responsiveness testing, changing browser window size
        driver.set_window_size(480, 800)
        driver.get('http://localhost:5000/dashboard/dashboard')
        try:
            WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.ID, 'burger'))
            )
            burger_button = self.retry_find_element(By.ID, 'burger')
            self.assertTrue(burger_button.is_displayed())
        except TimeoutException as e:
            print("TimeoutException occurred: ", e)
            print("Page source: ")
            raise
        except Exception as e:
            print("Exception occurred: ", e)
            print("Page source: ")
            raise

if __name__ == "__main__":
    unittest.main()
