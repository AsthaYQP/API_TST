from flask import request, Flask, redirect, jsonify, Response
import requests
import json
from bs4 import BeautifulSoup


app = Flask(__name__)
pegi2 = "www.pegipegi.com/kereta-api/search/direct/"
app.config['DEBUG'] = True

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
		
	
	
	
	_element = _textdata.find_all('tr')
	traindata = []
	_temp = {}
		
	for tr in _element:
		if tr.attrs['class'] == 'searchResultBody odd' or tr.attrs['class'] == 'searchResultBody even' :
			name = str(tr.attrs["data-train"])
			id = str(tr.attrs['data-trainno'])
			dept_st = str(tr.attrs['data-orig'])
			dest_st = str(tr.attrs['data-dest'])
			dept_time = str(tr.attrs['data-deptime'])
			_temp.update({'name' : name, 'id' : id, 'dept_st' : dept_st, 'dest_st' : dest_st, 'dept_time' : dept_time})
			traindata.append(_temp.copy())
			for key in _temp: 
				del _temp[key]
		
	
	return jasonify(traindata)

if __name__ == '__main__': 
	app.run()
			
		
		
		
		
		
		
