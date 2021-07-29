import streamlit as st

class MultiApp:
    
    def __init__(self):
        self.apps = []
        

    def add_app(self,title,func='nothing'):
        self.apps.append({"title":title,"function":func})
    
    def run(self):
        app = st.sidebar.radio('Browse', self.apps, format_func=lambda app: app['title'])
        app["function"]()