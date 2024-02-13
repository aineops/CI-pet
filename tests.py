import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from faker import Faker

# Fixture pour initialiser et fermer le navigateur
@pytest.fixture(scope="module")
def driver():
    print("Démarrage du test Selenium...")
    options = Options()
    options.add_argument('--headless')  # Activer le mode headless
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.maximize_window()
    yield driver
    driver.quit()
    print("Test Selenium terminé.")

# Fixture pour générer des données fictives
@pytest.fixture(scope="module")
def fake():
    return Faker()

# Fixture pour créer l'objet WebDriverWait
@pytest.fixture(scope="module")
def wait(driver):
    return WebDriverWait(driver, 10)

# Test pour vérifier la présence de l'onglet 'Home'
def test_home_tab_displayed(driver, wait):
    driver.get("http://localhost:8080/")
    home_tab = wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Home']")))
    assert home_tab.is_displayed(), "L'onglet 'Home' n'est pas affiché."

# Test du processus d'inscription
def test_registration_process(driver, wait, fake):
    try:
        driver.get("http://localhost:8080/")
        
        # Cliquez sur le bouton pour accéder à l'inscription
        button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@role='button']")))
        button.click()
        
        # Accéder à la page d'inscription
        register_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Register']")))
        register_link.click()

        # Remplir le formulaire d'inscription avec des données fictives
        first_name = wait.until(EC.element_to_be_clickable((By.NAME, "firstName")))
        first_name.send_keys(fake.first_name())

        last_name = wait.until(EC.element_to_be_clickable((By.NAME, "lastName")))
        last_name.send_keys(fake.last_name())

        address = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='address']")))
        address.send_keys(fake.street_address())

        city = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='city']")))
        city.send_keys(fake.city())

        phoneNumber = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='905554443322']")))
        phoneNumber.send_keys(fake.numerify(text='############'))

        # Soumettre le formulaire
        submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        submit_button.click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Veterinarians']"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//h2[normalize-space()='Veterinarians']")))

    except Exception as e:
        print(f"Une erreur s'est produite lors du test : {e}")
        raise
        
