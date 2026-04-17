from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Start browser
driver = webdriver.Chrome()

# Open login page (replace with your actual URL)
driver.get("https://scholar.parvam.in/student/login")

# Maximize window
driver.maximize_window()

# Wait handler
wait = WebDriverWait(driver, 15)

try:
    # Enter email (use valid email format)
    email = wait.until(EC.presence_of_element_located((By.NAME, "email_id")))
    email.clear()
    email.send_keys("kulsumafreen91@gmail.com")

    # Enter password
    password = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    password.clear()
    password.send_keys("Afreen0285@")

    # Click login button
    login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
    login_btn.click()

    # Wait for page to change after login
    wait.until(lambda d: d.current_url != "http://example.com/login")

    print("✅ Login Successful!")

except Exception as e:
    print("❌ Error during login:", e)

# Keep browser open (IMPORTANT)
input("Press Enter to close browser...")

# Close browser manually
driver.quit()