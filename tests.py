import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from faker import Faker

print("Démarrage du test Selenium...")
options = Options()
options.add_argument('--headless')  # Activer le mode headless

# Créer une instance du pilote Chrome avec les options spécifiées
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 10)
fake = Faker()

try:
    print("Test Selenium en cours...")
    driver.maximize_window()
    # Naviguer vers la page d'accueil de l'application
    driver.get("http://localhost:8080/")


    # Vérifier la présence de l'onglet 'Home' et naviguer dans l'application
    home_tab = wait.until(EC.presence_of_element_located((By.XPATH, "//span[normalize-space()='Home']")))
    # S'assurer que l'onglet Home est bien présent
    assert home_tab.is_displayed(), "L'onglet 'Home' n'est pas affiché."

    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@role='button']")))
    button.click()
    
    register_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Register']")))
    register_link.click()

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

    # Soumettre le formulaire et naviguer à travers l'application
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Veterinarians']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//h2[normalize-space()='Veterinarians']")))

    def tearDown(self):
        self.driver.quit()
        print("Test Selenium terminé.")

finally:
    # Ferme le navigateur après avoir terminé les tests
    driver.quit()
