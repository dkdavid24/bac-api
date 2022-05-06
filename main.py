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

origins = [
    "http://localhost:3000"
]

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

    print(result)

    return result