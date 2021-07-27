# Dependencies

# Config
import config

# General
import os
import sys
from pathlib import Path
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Data
import pandas as pd

# Viz
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
import matplotlib.style as style
import matplotlib.ticker as mtick
from matplotlib.ticker import MultipleLocator

# Consts

## matplotlib
# https://stackoverflow.com/questions/53897248/matplotlib-fail-to-allocate-bitmap
matplotlib.use('Agg')

## Input
col_date = "Date"
col_price = "Price"

## Output
str_filename_base = "btc" # e.g., "btc_01.png"

# Funcs

def create_plt(
    output_filename: str, 
    
    df_data: pd.DataFrame, 
    end_date: datetime, 
    start_date: datetime = None, 

    xlim: list = None, 
    bool_xmonths: bool = True,
    bool_save: bool = True
    ):

    # get start_date if necessary
    # end_date = datetime(2020, 12, 31)
    if start_date is None:
        start_date = end_date - relativedelta(years=1) + relativedelta(days=1)

    # data
    # https://stackoverflow.com/questions/5871168/how-can-i-subtract-or-add-100-years-to-a-datetime-field-in-the-database-in-djang
    df = df_data[
        (df_data[col_date] >= start_date) & 
        (df_data[col_date] <= end_date)
    ]

    # fig
    fig, ax = plt.subplots(1, 1, figsize = (12,6))

    # style
    # https://www.dataquest.io/blog/making-538-plots/
    style.use('fivethirtyeight')

    # ax
    ax = sns.lineplot(
        x=df[col_date],
        y=df[col_price]
    )

    # remove spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # labels

    # fig.suptitle("BTC Price", fontsize=18) # add title in openshot
    # ax.set_title("BTC Price")
    
    # https://stackoverflow.com/questions/28836048/multiple-font-sizes-in-plot-title
    # https://stackoverflow.com/questions/58121461/runtimeerror-failed-to-process-string-with-tex-because-latex-could-not-be-found
    # plt.rc('text', usetex=True)
    # title = "BTC Price"
    # subtitle = f"{start_date.strftime('%b %#d, %Y')} - {end_date.strftime('%b %#d, %Y')}"
    # title_text = r"\fontsize{30pt}{3em}\selectfont{}{" + title + r"\r}{\fontsize{18pt}{3em}\selectfont{}" + subtitle + "}"
    # title_text
    # plt.title(title_text)

    # ax.set_xlabel("Date")
    ax.get_xaxis().get_label().set_visible(False)
    ax.set_ylabel("Price ($)")
    ax.yaxis.set_label_position("right")

    # y-axis formatter
    # https://stackoverflow.com/questions/67582913/plotting-time-series-in-matplotlib-with-month-names-ex-january-and-showing-ye
    max_price = df[col_price].max()
    if max_price < 10:
        # str_format = "%.2f"
        # tick = mtick.FormatStrFormatter(str_format)
        # ax.yaxis.set_major_formatter(tick)
        
        # https://matplotlib.org/stable/gallery/pyplots/dollar_ticks.html
        ax.yaxis.set_major_formatter('{x:1.2f}')
        
        # https://matplotlib.org/stable/gallery/ticks_and_spines/major_minor_demo.html
        if max_price < 0.1:
            ax.yaxis.set_major_locator(MultipleLocator(0.01))
        elif max_price < 0.2:
            ax.yaxis.set_major_locator(MultipleLocator(0.2))
        elif max_price < 1:
            ax.yaxis.set_major_locator(MultipleLocator(0.1))
        elif max_price < 2:
            ax.yaxis.set_major_locator(MultipleLocator(0.25))
        elif max_price < 10:
            ax.yaxis.set_major_locator(MultipleLocator(0.5))
        else:
            pass
            
    else:
        ax.get_yaxis().set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ','))
        )
    ax.yaxis.set_tick_params(which='both', labelleft=False, labelright=True) # move axis to right side
    
    # set ylim
    # just make space for a title
    ax.set_ylim([0, df[col_price].max()*1.1])
    
    # color specific values
    # https://stackoverflow.com/questions/4761623/how-to-change-the-color-of-the-axis-ticks-and-labels-for-a-plot-in-matplotlib
    # https://stackoverflow.com/questions/29766827/matplotlib-make-axis-ticks-label-for-dates-bold
    # https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.get_yticklabels.html
    # - "The tick label strings are not populated until a draw method has been called."
    plt.draw()
    ls_changeme = [100, 500, 1000] + [5000*x for x in range(1,15)]
    for t in ax.get_yticklabels(which="major"):
        if t.get_position()[1] in ls_changeme:
            t.set_color("orange")
            t.set_fontweight('bold')
        else:
            t.set_color("grey")

    # x-axis formatter
    
    # set xlim
    # https://stackoverflow.com/questions/21423158/how-do-i-change-the-range-of-the-x-axis-with-datetimes-in-matplotlib
    if xlim is not None:
        ax.set_xlim(xlim)
        
    # extend xlim to make room for current price text
    # print(ax.get_xlim()[0], ax.get_xlim()[1])
    ax.set_xlim(ax.get_xlim()[0], ax.get_xlim()[1]+0.1*(ax.get_xlim()[1] - ax.get_xlim()[0]))
    # ax.set_xlim(14802.8, 15203.2+0.1*(15203.2-14802.8))
    # print(ax.get_xlim()[0], ax.get_xlim()[1])

    # x ticks

    # two axes
    # main = month
    # secondary = year

    fmt_month = mdates.MonthLocator()  # Minor ticks every month.
    fmt_year = mdates.YearLocator()  # Minor ticks every year.

    ax.xaxis.set_minor_locator(fmt_month)
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%b')) # '%b' to get the names of the month
    ax.xaxis.set_major_locator(fmt_year)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))

    # fontsize for month labels
    ax.tick_params(labelsize=12, which='both')

    # create a second x-axis beneath the first x-axis to show the year in YYYY format
    sec_xaxis = ax.secondary_xaxis(-0.06)
    sec_xaxis.xaxis.set_major_locator(fmt_year)
    sec_xaxis.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    # Hide the second x-axis spines and ticks
    sec_xaxis.spines['bottom'].set_visible(False)
    sec_xaxis.tick_params(length=0, labelsize=12)

    if not bool_xmonths:
        # turn off month axis
        ax.xaxis.set_visible(False)

    # annotate
    x_min = df[col_date].min()
    x_max = df[col_date].max()
    y_for_x_max = float(df[df[col_date] == x_max][col_price])
    ax.text(
        x_max + relativedelta(days=10), 
        y_for_x_max,
        "${:,.2f}".format(y_for_x_max), 
        color='orange', 
        bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=1', fc="white", fill=True),
        ha="left",
        va="center",
        weight="bold"
    )
    
    # get halvings
    # https://stackoverflow.com/questions/993358/creating-a-range-of-dates-in-python
    for halving in ls_halving:
        if halving in pd.date_range(start=start_date,end=end_date).to_pydatetime().tolist():
            ax.axvline(x=halving, ls="--", lw=1, color="m")

    # save fig
    if bool_save:
        Path(output_filename).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(
            output_filename,
            bbox_inches='tight'
        )
    else:
        plt.show()
    
    # reset
    # plt.figure().clear()
    plt.close("all")
    
    return

# Get Data

## BTC Price

df_data = pd.read_csv(
    config.input_filename,
    parse_dates=[col_date]
)

## BTC Halving

# https://www.cmcmarkets.com/en/learn-cryptocurrencies/bitcoin-halving
ls_halving = [datetime(2012,11,28), datetime(2016,7,9)]

# Build Plots

## Get Args

bool_ramp = "-ramp" in sys.argv
bool_roll = "-roll" in sys.argv
bool_zoom = "-zoom" in sys.argv

if not any([bool_ramp, bool_roll, bool_zoom]):
    bool_ramp = True
    bool_roll = True
    bool_zoom = True

## Constants

filename_id = 1 # counter

## Ramp Up to First Year

suffix = "rr"
first_date = min(df_data['Date']) # first date = 2010-07-18
last_date = min(df_data['Date']) + relativedelta(years=1)

ls_dates = pd.date_range(start=first_date, end=last_date).to_pydatetime().tolist()

if bool_ramp:

    print(f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}: starting {suffix} ({len(ls_dates)})")

    bool_first = True
    for end_date in ls_dates:
        output_filename = os.path.join(config.output_dir, f"{str_filename_base}_{suffix}_{str(filename_id).zfill(5)}.png")
        if bool_first:
            # redo first one bc it gets messed up
            for i in range(2):
                create_plt(
                    output_filename, 
                    df_data, 
                    end_date=end_date,
                    start_date=first_date,
                    xlim=[first_date, first_date + relativedelta(years=1)]
                )
            bool_first = False
        else:
            create_plt(
                    output_filename, 
                    df_data, 
                    end_date=end_date,
                    start_date=first_date,
                    xlim=[first_date, first_date + relativedelta(years=1)]
                )
        filename_id += 1

    print(f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}: finished {suffix} ({len(ls_dates)})")

## Rolling Year Graphs

filename_id = len(ls_dates) + 1

suffix = "rr"
first_date = min(df_data['Date']) + relativedelta(years=1) # first date = 2010-07-18
last_date = max(df_data['Date'])

ls_dates = pd.date_range(start=first_date, end=last_date).to_pydatetime().tolist()

if bool_roll:

    print(f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}: starting {suffix} ({len(ls_dates)})")

    bool_first = True
    for end_date in ls_dates:
        output_filename = os.path.join(config.output_dir, f"{str_filename_base}_{suffix}_{str(filename_id).zfill(5)}.png")
        if bool_first:
            for i in range(2):
                create_plt(output_filename, df_data, end_date)
            bool_first = False
        else:
            create_plt(output_filename, df_data, end_date)
        filename_id += 1

    print(f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}: finished {suffix} ({len(ls_dates)})")

## Zoom Out

filename_id = 1 # start over counter for ffmpeg

suffix = "z"
first_date = min(df_data['Date']) # first date = 2010-07-18
last_date = max(df_data['Date']) - relativedelta(years=1) - relativedelta(days=1)

ls_dates = pd.date_range(start=first_date, end=last_date).to_pydatetime().tolist()
ls_dates.reverse()

if bool_zoom:

    print(f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}: starting {suffix} ({len(ls_dates)})")

    bool_first = True
    for add_date in ls_dates:
        output_filename = os.path.join(config.output_dir, f"{str_filename_base}_{suffix}_{str(filename_id).zfill(5)}.png")
        if bool_first:
            for i in range(2):
                create_plt(output_filename, df_data, end_date=max(df_data['Date']), start_date=add_date, bool_xmonths=False)
            bool_first = False
        else:
            create_plt(output_filename, df_data, end_date=max(df_data['Date']), start_date=add_date, bool_xmonths=False)
        filename_id += 1

    print(f"{datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}: finished {suffix} ({len(ls_dates)})")
