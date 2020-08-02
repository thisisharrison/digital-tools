import requests 

class Image():
    def __init__(self, style):
        self.style = style
        self.url = ''
        self.status = ''
        self.status_read = ''    

    def add_url(self):
        domain = 'https://images.lululemon.com/is/image/lululemon/'
        self.url = domain + self.style.replace('-','_') + '_1'
        return self.url

    def check_status(self):
        url = self.url
        response = requests.get(url)
        self.status = response.status_code
        if self.status == 200:
            self.status_read = "Exist"
        elif self.status == 403:
            self.status_read = "Not Exist"
        else:
            self.status_read = "Error"
        return self.status
    
    @property
    def print_full(self):
        return {'style': self.style, 'url': self.url, 'status': self.status, 'status_read': self.status_read}
