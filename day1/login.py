from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://scholar.parvam.in/student/login")

wait = WebDriverWait(driver, 10)

email = wait.until(EC.presence_of_element_located((By.NAME, "email_id")))
email.send_keys("afreen@gmail.com")

password = wait.until(EC.presence_of_element_located((By.NAME, "password")))
password.send_keys("afreen123@")

login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
login_btn.click()

# Wait for page change
wait.until(lambda d: d.current_url != "http://example.com/login")

print("Logged in successfully!")

# Keep browser open
input("Press Enter to close browser...")
driver.quit()