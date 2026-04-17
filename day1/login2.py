import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load CSV file
data = pd.read_csv("users.csv")

# Start browser
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 15)

for index, row in data.iterrows():
    email_value = row['email']
    password_value = row['password']

    driver.get("https://scholar.parvam.in/student/login")

    try:
        # Enter email
        email = wait.until(EC.presence_of_element_located((By.NAME, "email_id")))
        email.clear()
        email.send_keys(email_value)

        # Enter password
        password = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        password.clear()
        password.send_keys(password_value)

        # Click login
        login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        login_btn.click()

        # Wait for login
        wait.until(lambda d: d.current_url != "http://example.com/login")

        print(f"✅ Login success for: {email_value}")

    except Exception as e:
        print(f"❌ Failed for: {email_value} | Error: {e}")

# Keep open
input("Press Enter to close...")
driver.quit()