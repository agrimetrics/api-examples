from datetime import date

import numpy
import pandas

import matplotlib.pyplot as plt


if __name__ == "__main__":
    print("This file is a library for use by the other examples. Run on its own, it will do nothing,")


def plot_stacked_bar_chart(data, x, y, labels, title="Stacked bar chart"):
    fig = plt.figure()
    ax = plt.subplot(111)
    data.plot(x=x, y=y, kind='bar', stacked=True, ax=ax)
    chartBox = ax.get_position()
    ax.set_position([chartBox.x0, chartBox.y0, chartBox.width*0.6, chartBox.height])
    ax.legend(labels=labels, loc='upper center', bbox_to_anchor=(1.45, 0.8), shadow=True, ncol=1)

    standardise_plot_layout(ax)

    fig.suptitle(title)

    plt.show()


def plot_pie_chart(data, labels, title="Pie chart"):
    fig, ax = plt.subplots()

    ax.pie(
        data,
        autopct='%1.1f%%',
        shadow=True,
        startangle=90
    )

    ax.legend(labels, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    # remove y label
    ax.set_ylabel('')

    fig.suptitle(title)

    plt.show()


def plot_multiple_timeseries_by_year(data, title="Multiple timeseries by year"):
    result_num = data.resultIndex.unique()
    fig, axs = plt.subplots(len(result_num), sharex=True)

    ticklabels = get_monthly_ticks_for_series(data.index.month.unique())

    for i, result in enumerate(result_num):
        result_data = data[data.resultIndex == result]
        pt = pandas.pivot_table(
            result_data,
            index=result_data.index.month,
            columns=result_data.index.year,
            values='value',
            aggfunc='sum'
        )
        axs[i].plot(pt)
        axs[i].grid(False)
        axs[i].set_xticks(numpy.arange(1,13))

        # add monthlabels to the xaxis
        axs[i].set_xticklabels(ticklabels)

    standardise_plot_layout(axs)

    fig.suptitle(title)

    plt.show()


def box_plot_multiple_timeseries_by_freq(data, frequencies, labels=[], title="Box plot"):
    # horizontal plots
    fig, axs = plt.subplots(1, len(frequencies))

    for i, freq in enumerate(frequencies):
        data[[freq, 'value']].boxplot(by=freq, ax=axs[i])
        axs[i].title.set_text(labels[i] if len(labels) > i else '')

    standardise_plot_layout(axs)

    fig.suptitle(title)

    plt.show()


def plot_timeseries(data, title="Timeseries"):
    fig, ax = plt.subplots()

    data.plot(y='value', kind='line', stacked=False, ax=ax, legend=False)
    fig.suptitle(title)

    standardise_plot_layout(ax)
    plt.show()


def get_monthly_ticks_for_series(data):
    return [date(1900, item, 1).strftime('%b') for item in data]


def standardise_plot_layout(axs):
    if type(axs) == numpy.ndarray:
        for ax in axs:
            set_axis_to_default(ax)
    else:
        set_axis_to_default(axs)


def set_axis_to_default(axis):
    axis.spines['right'].set_visible(False)
    axis.spines['top'].set_visible(False)
    axis.grid(False)
