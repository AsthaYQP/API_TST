from flask import request, Flask, redirect, jsonify, Response
import requests
import json
from bs4 import BeautifulSoup


app = Flask(__name__)
pegi2 = "www.pegipegi.com/kereta-api/search/direct/"


@app.route('/')
def test(): 
	return 'success' 
	
@app.route('/kereta/<dept>/<dest>/<date>')
def getKereta(dept, dest, date):

	_asal = dept 
	_tujuan = dest
	_tanggal = date
		
	if _asal == None or _tujuan == None or _tanggal == None: 
		return(Response('Parameter tidak tepat', 400))
		
	_url = requests.get('https://' + pegi2 + _asal + '/' + _tujuan + '/' + _tanggal + '/1/0/EBK')
	
	_textdata = BeautifulSoup(_url.text, 'html.parser')
	_error = _textdata.find('tr', attrs = {'class' : 'odd'})
	
	if _error:
		return(Response('Kereta tidak ditemukan', 404))
		
	_result = _textdata.find('tbody', attrs = {'class' : 'listSearchResult detailOrder active'})
	traindata = []
	_temp = []
		
	for tr in _result: 
		_temp = json.loads(tr.attrs["data-train", "data-trainno", "data-orig", "data-dest", "data-deptime"]) 
		traindata.append(_temp)
		del _temp[:]
		
	return traindata

if __name__ == '__main__': 
	app.run()
			
		
		
		
		
		
		