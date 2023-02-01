import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from flask import Flask, request

app=Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def upload_file():
    return '''
    <!doctype html>
    <title>Upload an excel file</title>
    <h1>Excel file upload (xlsx only)</h1>
    <form action="/split" method=post enctype=multipart/form-data>
    <p><input type=file name=file><input type=submit value=Upload>
    </form>
    '''

@app.route("/split", methods=['GET', 'POST'])
def scrape():
    if request.method == 'POST':
        print(request.files['file'])
        f = request.files['file']
        
        data = pd.read_excel(f)
    c = 1
    counter=1
    for i in range(0,len(data)//200):
        try:
            data_t = data.iloc[c:c+200,:]
        except:
            data_t = data.iloc[c:,:]
        c=c+100
        counter+=1
        data_t.to_excel('SPLIT_DATASETS/split_'+str(counter)+'.xlsx')
    return '''
    <!doctype html>
    <title>SAVED</title>
    <h1>FILES SAVED !</h1>
    '''

if __name__ == "__main__":
    app.run(port=8000)
