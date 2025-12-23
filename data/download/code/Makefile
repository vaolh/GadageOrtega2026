YEARS := 2018 2017 2016 2015 2014 2013 2012 2011 2009 2008 2007 2006 2005

all: ../temp/venv ../output ../output/eh_2018.zip ../output/eh_2017.zip ../output/eh_2016.zip ../output/eh_2015.zip ../output/eh_2014.zip ../output/eh_2013.zip ../output/eh_2012.zip ../output/eh_2011.zip ../output/eh_2009.zip ../output/eh_2008.zip ../output/eh_2007.zip ../output/eh_2006.zip ../output/eh_2005.zip

../output:
	mkdir -p ../output

../temp:
	mkdir -p ../temp

../temp/venv: ../temp
	python3 -m venv ../temp/venv
	../temp/venv/bin/python -m pip install --upgrade pip
	../temp/venv/bin/python -m pip install selenium

../output/eh_2018.zip ../output/eh_2017.zip ../output/eh_2016.zip ../output/eh_2015.zip ../output/eh_2014.zip ../output/eh_2013.zip ../output/eh_2012.zip ../output/eh_2011.zip ../output/eh_2009.zip ../output/eh_2008.zip ../output/eh_2007.zip ../output/eh_2006.zip ../output/eh_2005.zip: | ../output ../temp/venv
	../temp/venv/bin/python download.py

clean:
	rm -rf ../output ../temp
