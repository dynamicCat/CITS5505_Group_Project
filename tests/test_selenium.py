from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time

class WebAppFunctionalTests(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()  # Make sure ChromeDriver is installed and in your PATH
        self.driver.implicitly_wait(10)  # Set implicit wait time for all elements

    def test_login_functionality(self):
        driver = self.driver
        driver.get('http://localhost:5000/auth/login')  # Your app’s login page URL
        
        # Testing for bad login attempts
        username = driver.find_element(By.NAME, 'username')
        password = driver.find_element(By.NAME, 'password')
        login_button = driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-primary')
        
        username.send_keys('wronguser')
        password.send_keys('wrongpassword')
        login_button.click()

        # Check if any error message is displayed
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "error_message"))
        )
        error_message = driver.find_element(By.ID, 'error_message').text
        self.assertIn('Invalid username or password', error_message)

        # Clear input for correct login attempt
        username.clear()
        password.clear()
        
        username.send_keys('eric')
        password.send_keys('root')
        login_button.click()

        # Verify that the login is successful and navigate to the dashboard page
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, 'h1'), 'Dashboard')
        )
        dashboard_heading = driver.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('Dashboard', dashboard_heading)

        # Navigate to other pages and verify
        driver.find_element(By.LINK_TEXT, 'Profile').click()
        profile_heading = driver.find_element(By.TAG_NAME, 'h1').text
        self.assertIn('Profile', profile_heading)

        # Responsiveness testing, changing browser window size
        driver.set_window_size(480, 800)
        driver.get('http://localhost:5000/dashboard/dashboard')
        time.sleep(1)  # Wait for page to load and possible layout adjustments
        mobile_menu_button = driver.find_element(By.ID, 'mobile_menu_button')
        self.assertTrue(mobile_menu_button.is_displayed())

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
