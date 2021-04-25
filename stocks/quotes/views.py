from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages
from django.shortcuts import render 


# pk_e4c317db75c8461fb6c92a1ea3c0e496

def home(request):
	import requests
	import json

	if request.method == 'POST':
		ticker = request.POST['ticker'] 
		api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_e4c317db75c8461fb6c92a1ea3c0e496")
		try:
			api = json.loads(api_request.content)
		except Exception as e:
			api = "Error..."
		return render(request, 'home.html', {'api' : api}) 

	else:
		return render(request, 'home.html', {'ticker' : "Enter a Stock Ticker Above, to get a quote."}) 


def about(request):
	return render(request, 'about.html', {})


def add_stock(request):
	import requests
	import json

	if request.method == 'POST':
		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request, ('Stock Has Been Added Successfully!'))
			return redirect('add_stock')



	else:
		ticker = Stock.objects.all()
		output = []
		for ticker_item in ticker:		
			api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_e4c317db75c8461fb6c92a1ea3c0e496")

			try:
				api = json.loads(api_request.content)
				output.append(api)
			except Exception as e:
				api = "Error..."

		return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})

def delete(request, stock_id):
	item = Stock.objects.get(pk=stock_id)
	item.delete()
	messages.success(request, ("Stock Has Been Deleted Successfully"))
	return redirect(delete_stock)

def delete_stock(request):
	ticker = Stock.objects.all()
	return render(request, 'delete_stock.html', {'ticker': ticker})

def news(request):
    import requests 
    import json
    news_api_request=requests.get("https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=7fbe44ccbd564351af262ff843fdb6d5")
    api=json.loads(news_api_request.content)
    return render(request,'news.html',{'api':api})