from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import pandas as pd

data = {
    2014 : pd.read_csv('data/2014_final.csv'),
    2015 : pd.read_csv('data/2015_final.csv'),
    2016 : pd.read_csv('data/2016_final.csv'),
    2017 : pd.read_csv('data/2017_final.csv'),
    2018 : pd.read_csv('data/2018_final.csv'),
    2019 : pd.read_csv('data/2019_final.csv'),
    2020 : pd.read_csv('data/2020_final.csv'),
    2021 : pd.read_csv('data/2021_final.csv')
}

app = FastAPI();

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {"messege": "Hello World"}


@app.get("/api/urban-rural-by-year")
async def urbanRuralByYear():
    result = []

    # urban
    for year, value in data.items():
        urban = value[value['medium'] == "Urban"]

        avg = np.average(
                    urban[urban['avg'].notnull()].avg
                )
        

        result.append(
            {
                "id" : "urban",
                "x" : year,
                "y" : round(avg, 2)
            }
        )

    # rural
    for year, value in data.items():
        rural = value[value['medium'] == "Rural"]

        avg = np.average(
                    rural[rural['avg'].notnull()].avg
                )
        

        result.append(
            {
                "id" : "rural",
                "x" : year,
                "y" : round(avg, 2)
            }
        )

    return result


@app.get("/api/county/{county}")
async def countyByYear(county):
    result = []

    for year, value in data.items():
        tmp = value[value['county']  == county]

        avg = np.average(
            tmp[tmp['avg'].notnull()].avg
        )

        result.append(
            {
                "id" : county,
                "x" : year,
                "y" : round(avg, 2)
            }
        )

    return result

@app.get("/api/county/{county}/pass-rate")
async def countyPassRate(county):
    result = []

    for year, value in data.items():
        tmp = value[value['county']  == county]
        passed_list = tmp[tmp['passed'] == True]

        all = len(tmp)
        if all == 0:
            return []

        passed = len(passed_list)

        result.append(
            {
                "id" : county,
                "x" : year,
                "y" : round( passed / all, 4) 
            }
        )

    return result

@app.get("/api/current-previous-gen")
async def generation():
    result = []

    # previous generation
    for year, value in data.items():
        tmp = value[value['previous_prom'] != True]

        passed_list = tmp[tmp['passed'] == True]

        all = len(tmp)

        passed = len(passed_list)

        result.append(
            {
                "id" : "Previous",
                "x" : year,
                "y" : round( passed / all, 2)
            }
        )

    # current generation
    for year, value in data.items():
        tmp = value[value['previous_prom'] != False]

        passed_list = tmp[tmp['passed'] == True]

        all = len(tmp)

        passed = len(passed_list)

        result.append(
            {
                "id" : "Current",
                "x" : year,
                "y" : round( passed / all, 2)
            }
        )


    return result


@app.get("/api/subject-pass-rate")
async def subjectPassRate():
    result = []

    # ro
    for year, value in data.items():
        all = value[value['rom_grade'].notnull()]
        passed = all[all['rom_grade'] >= 5]

        perc = len(passed) / len(all)

        result.append(
            {
                "id" : "RO",
                "x" : year,
                "y" : round(perc, 2)
            }
        )

    # math
    for year, value in data.items():
        man = value[value['mandatory'] == "Matematica"]

        all = man[man['mandatory'].notnull()]
        passed = all[all['mandatory_grade'] >= 5]

        perc = len(passed) / len(all)

        result.append(
            {
                "id" : "MAT",
                "x" : year,
                "y" : round(perc, 2)
            }
        )

    # Ist
    for year, value in data.items():
        man = value[value['mandatory'] == "Istorie"]

        all = man[man['mandatory'].notnull()]
        passed = all[all['mandatory_grade'] >= 5]

        perc = len(passed) / len(all)

        result.append(
            {
                "id" : "IST",
                "x" : year,
                "y" : round(perc, 2)
            }
        )

    # Choice
    for year, value in data.items():
        all = value[value['choice_grade'].notnull()]
        passed = all[all['choice_grade'] >= 5]

        perc = len(passed) / len(all)

        result.append(
            {
                "id" : "Choice",
                "x" : year,
                "y" : round(perc, 2)
            }
        )

    # Native
    for year, value in data.items():
        all = value[value['native_grade'].notnull()]
        passed = all[all['native_grade'] >= 5]

        perc = len(passed) / len(all)

        result.append(
            {
                "id" : "NAT",
                "x" : year,
                "y" : round(perc, 2)
            }
        )

    return result
