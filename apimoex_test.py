import os
import requests
import apimoex
import matplotlib.pyplot as plt
import pandas as pd
from config import START_DATE, END_DATE, SECURITY_LIST, DATA_PATH, INTERVAL
import matplotlib.patches as mpatches
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np


pio.templates.default = "plotly_dark"


class DataManager:
    """
    Class to operate data
    _path_to_data : str, holds path to folder, there
    data is stored
    _ticket_list : list[str], holds list of current tickets in folder
    """

    @staticmethod
    def update_data(
            ticket_list=SECURITY_LIST,
            start_date=START_DATE,
            end_date=END_DATE,
            interval=INTERVAL,
            path=DATA_PATH,
    ) -> None:
        """
        Used for updating data as a class method
        Works same as get_data.py script
        """
        for security in ticket_list:
            with requests.Session() as session:
                data = apimoex.get_market_candles(
                    session,
                    security=security,
                    start=start_date,
                    interval=interval,
                    end=end_date,
                )
                whole_frame = pd.DataFrame(data)
                date, close = whole_frame["begin"], whole_frame["close"]
                attr = {"begin": date, "close": close}
                whole_frame = pd.DataFrame(attr)
                if not os.path.exists(path):
                    os.mkdir(path)
                whole_frame.to_csv(path + security + ".csv")

    def __init__(self, path=DATA_PATH) -> None:
        """
        Constructor for Data_manager object
        param: DATA_PATH - str
        """
        self._path_to_data = path
        self._ticket_list = list(
            map(lambda x: x.split(".")[0], os.listdir(DATA_PATH))
        )
        self.start_date = START_DATE
        self.end_date = END_DATE

    @property
    def ticket_list(self) -> list:
        """
        Gets list of strings
        Example -> ['YNDX', 'ALRS', 'SBER', 'MOEX']
        """
        return self._ticket_list

    def give_data(
            self, ticket: str, start_date=START_DATE, end_date=END_DATE
    ) -> tuple:
        """
        Opens up csv file and reads it to two lists
        x_axis : list of datetime.datetime objects
        y_axis : list of float numbers
        """
        with open(self._path_to_data + ticket + ".csv", newline="") as csvfile:
            content = pd.read_csv(csvfile)
            values = content.loc[
                (content["begin"] >= start_date)
                & (content["begin"] <= end_date)
                ]
            x_axis, y_axis = values["begin"], values["close"]
            return x_axis, y_axis


DataManager.update_data()
data_manager = DataManager()
fig, ax = plt.subplots(1, 1, figsize=(20, 10))
fig1,ax1 = plt.subplots()
fig2, ax2 = plt.subplots(figsize=(20, 10))
fig3, ax3 = plt.subplots(figsize=(10, 7))
columns=[]
for ticket in data_manager.ticket_list:
    dates, values = data_manager.give_data(ticket)
    dates2 = dates.apply(lambda x: x[:4])
    columns += [values]

    list1 = []
    for i in range(1, len(dates)):
        list1.append((dates[i], values[i]))
    print(list1)
    indices = np.arange(len(list1))
    dates, values = zip(*list1)
    plt.title('Scatter Data')
    ax3.bar(indices, values,label=ticket,alpha=0.5)
    plt.xticks(indices, dates, rotation='vertical')
    plt.tight_layout()

    plt.title('Scatter Data')
    fig.autofmt_xdate(rotation=45)
    ax.scatter(x=dates, y=values, label=ticket)

    plt.title('Bar Data')
    ax2.plot(dates, values, label=ticket)
    fig2.autofmt_xdate(rotation=45)

pos = np.arange(len(columns)) + 1
bp = ax1.boxplot(columns,sym='k+', positions=pos,
            notch=1, bootstrap=5000)
patch = mpatches.Patch(color='black',label=data_manager.ticket_list)
ax1.legend(handles=[patch])
ax2.legend(loc='upper left')
ax.legend(loc='upper left')
ax3.legend(loc='upper left')

plt.show()

dz = pd.DataFrame(apimoex.get_board_securities(session=requests.Session(), table='securities', columns=None))
table_dz = dz[['SECID', 'SHORTNAME', 'PREVPRICE', 'PREVWAPRICE', 'PREVDATE', 'ISSUESIZE', 'PREVLEGALCLOSEPRICE',
               'PREVADMITTEDQUOTE', 'SETTLEDATE']]
table_dz = table_dz.query('SECID in @SECURITY_LIST')
table_dz.to_excel('./teams.xlsx')