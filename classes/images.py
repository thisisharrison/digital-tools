import requests 

class Image():
    def __init__(self, style):
        self.style = style
        self.url = ''
        self.status = ''    

    def add_url(self):
        domain = 'https://images.lululemon.com/is/image/lululemon/'
        self.url = domain + self.style.replace('-','_') + '_1'
        return self.url

    def check_status(self):
        url = self.url
        response = requests.get(url)
        self.status = response.status_code
        return self.status
    
    @property
    def print_full(self):
        return {'style': self.style, 'url': self.url, 'status': self.status}
