virtualenv env -p python3
. env/bin/activate
mkdir data
mkdir temp
mkdir temp/embeddings

pip3 install karateclub
pip3 install pandas
cd data
wget https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_confirmed_usafacts.csv
wget https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_deaths_usafacts.csv
wget https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_county_population_usafacts.csv
wget http://www2.census.gov/geo/docs/reference/county_adjacency.txt
wget https://www2.census.gov/programs-surveys/demo/tables/metro-micro/2015/commuting-flows-2015/table1.xlsx
wget https://www.gstatic.com/covid19/mobility/Region_Mobility_Report_CSVs.zip
unzip Region_Mobility_Report_CSVs.zip
cd ..

python3 neighborhood_to_nx.py

