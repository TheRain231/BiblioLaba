from BiblioLabaApp import *
from Helpers.dataManager import *

dataManager = DataManager()
dataManager.loadData()

app = BiblioLabaApp(dataManager)
app.loop()
