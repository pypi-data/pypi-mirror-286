import requests

class InsurancePremiumCalculator:
    def calculate_premium(self, age, health_status, country_code):
        percentage_increase = 0
        risk_score = self.fetch_country_risk(country_code)
        if age > 50 and risk_score > 3:
            if health_status == "heart":
                percentage_increase = 25
            elif health_status == "diabetes":
                percentage_increase = 20
            else:
                percentage_increase = 15
        elif age <= 50 and risk_score <= 3:
            if health_status == "heart":
                percentage_increase = 10
            elif health_status == "diabetes":
                percentage_increase = 5
            else:
                percentage_increase = 3
        else:
            if health_status == "heart":
                percentage_increase = 20
            elif health_status == "diabetes":
                percentage_increase = 15
            else:
                percentage_increase = 10

        return percentage_increase

    def fetch_country_risk(self, country_code):
        url = f"https://www.travel-advisory.info/api?countrycode={country_code}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            score = data.get('data', {}).get(country_code.upper(), {}).get('advisory', {}).get('score', 0)
            return score
        except requests.RequestException as e:
            print(f"Error fetching risk score: {e}")
            return 0