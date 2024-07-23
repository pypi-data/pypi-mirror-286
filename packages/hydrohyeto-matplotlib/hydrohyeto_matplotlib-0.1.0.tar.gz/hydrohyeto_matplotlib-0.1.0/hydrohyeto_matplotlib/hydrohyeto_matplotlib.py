from matplotlib import cm, pyplot as plt
import japanize_matplotlib
import matplotlib.dates as mdates
import datetime

def hydrohyeto(datasets, **kwargs):

    default_kwargs = {
        'name_rain': '時間雨量_盛岡',
        'name_pred': '時刻水位_四十四田',
        'name_real': '時刻水位_御所',
        'label_rain': 'Rainfall',
        'label_pred': 'Proposed',
        'label_real': 'Obs',
        'x_interval_hour': 1,
        'title': '',
        'rain_ylim': (0, 60),
        'lable_y1': 'Inflow$(m^{3}/s)$',
        'lable_y2': 'Rainfall(mm/h)'
    }

    kwargs = default_kwargs | kwargs
    
    date_list = datasets.index
    rain_val_list = datasets[kwargs['name_rain']]
    pred_y = datasets[kwargs['name_pred']]
    real_y = datasets[kwargs['name_real']]
    
    # 表示間隔
    interval = datetime.timedelta(hours=kwargs['x_interval_hour'])

    fig, ax = plt.subplots(figsize=(6, 3.5))
    fig.autofmt_xdate()
    
    # 流量
    ax.plot(date_list, pred_y, linestyle="solid", color='red', label=kwargs['label_pred'])
    ax.plot(date_list, real_y, linestyle="dotted", color='black', label=kwargs['label_real'])

    # 雨量
    ax2 = ax.twinx()
    ax2.bar(date_list, list(rain_val_list), color='blue', alpha=0.4, width=interval, label=kwargs['label_rain'])
    ax2.set_ylim(kwargs['rain_ylim'])
    ax2.invert_yaxis()

    # 軸ラベルの設定
    ax.set_ylabel(kwargs['lable_y1'], size=10)
    ax2.set_ylabel(kwargs['lable_y2'], size=10)

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d\n%H:%M'))

    if len(kwargs['title']) > 0:
        ax.set_title(kwargs['title'], loc='left', y=0.85)
    
    
    # ラベル
    # -----------------------------------------
    lines_1, labels_1 = ax.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    lines = lines_1 + lines_2
    labels = labels_1 + labels_2
    
    if len(lines) == 4:
        ax.legend(
            [
                lines[1],
                lines[0],
                lines[3],
                lines[2],
            ],
            [
                labels[1],
                labels[0],
                labels[3],
                labels[2],
            ]

        )
    else:
        ax.legend(
            [
                lines[1],
                lines[0],
                lines[2],
            ],
            [
                labels[1],
                labels[0],
                labels[2],
            ]

        )
    # -----------------------------------------
    return fig

