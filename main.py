from datetime import datetime

from fastapi import FastAPI, HTTPException
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Start FastAPI
app = FastAPI()


@app.get('/get_weather_info/{day}&{district}&{local}')
def get_weather_info(day: int, district: str, local: str):
    
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')  # Not to use the Google Chrome sandbox mechanism
    chrome_options.add_argument('--headless')  # Run without a screen
    chrome_options.add_argument('--disable-dev-shm-usage')  # Disable shared memory
    
    today = datetime.now()
    actual_day = today.day
    
    # The IPMA default application shows 10 days, counting from the current date and 9 days ahead.
    if  day < actual_day or day > actual_day + 9:
        raise HTTPException(
            status_code=404, 
            detail=f"Not found: Day out range of {actual_day} - {actual_day + 9}")  
    
    try:
        
        url = f'https://www.ipma.pt/pt/otempo/prev.localidade.hora/#{district.capitalize()}&{local.capitalize()}'
        
        # Create a Chrome webdriver
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
        
        # Make a request to IPMA
        driver.get(url)
        
        # Get the page source and parse to 'lxml'
        soup = BeautifulSoup(driver.page_source, 'lxml')
        
        # Find the 'div' with the associated day, passed at the url
        elements = soup.find_all(name='div', attrs={'id': day})
        
        contents = elements[0].contents
        
        # Fill the response structure
        api_response = {
            "date": f"{contents[0].text}",
            "sky": f"{contents[1]['title']}",
            "min_temperature": f"{contents[2].text}",
            "max_temperature": f"{contents[3].text}",
            "wind": f"{contents[4]['title']}",
            "precipitation_probability": f"{contents[6].text}",
            "uvi": f"{contents[8]['title']}"        
        }
        
        # Close the driver
        driver.quit()
        
        return api_response
    # Raises an exception if any http error happens when the request to IPMA is made.
    except HTTPException as httpe:
        raise httpe
    # Raises an 
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail="Internal Server Error") 
