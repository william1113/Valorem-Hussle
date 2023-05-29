from flask import render_template

class Pages:
    def __init__(self, app,name, htmlFile):
        self.app = app
        self.name = name
        self.htmlFile = htmlFile
        
    def createPage(self):
        @self.app.route(f'/{self.name}', methods=['GET', 'POST'])
        def page():
            return render_template(f'{self.htmlFile}')
        
    


