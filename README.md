# DiscoverDNAustria - Readme

Python code fragt 1x am Tag um 16:30 durch eine Github Action durch, welche das main.py file mit python durchlaufen lässt.

Main.py fragt Daten von der [GoogleTabelle](https://docs.google.com/spreadsheets/d/1MUk8bcxuXxcrgz4IR4HbqouWXa3fFfKb38k2SM2AdQ8/edit?gid=1041016962#gid=1041016962) ab und baut daraus die JSON auf. Dann wird die JSON im repository abgelegt (output.json).

Der Fetcher von DiscoverDN Austria holt sich das file dann von dort.
