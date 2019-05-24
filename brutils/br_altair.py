import altair as alt
from os.path import join as pjoin


def alt_chart_df_save(df, file_name, file_path='.', **kwargs) :
    """ file_name -> do not include the extension """
    df2 = df.reset_index()
    df2.to_csv(pjoin(file_path, file_name + 'vl.csv'))

    chart = alt.Chart(pjoin(file_path, file_name + 'vl.csv')).mark_point().encode(**kwargs)
    chart.save(pjoin(file_path, file_name + '.vl.json'))

def read_vljson(file_name, path='.') :
    # df = pd.read_csv(pjoin(path, file_name + '.csv'))
    #chart = alt.Chart(pjoin
    with open(pjoin(path, file_name + '.vl.json'), 'r') as fid :
        # json = fid.read()
        # print(json)
        chart = alt.Chart.from_json(fid.read())
    return chart


def serve_chart_loc_csv(chart, files={}) :
    # err = False
    if not isinstance(chart.data, alt.vegalite.v3.core.UrlData) :
        raise TypeError('brutils.altair.serve_chart_loc_csv: with chart: {}\nchart.data must be type alt.vegalite.v3.core.UrlData'.format(chart))
    elif not chart.data.url.endswith('.csv') :
        raise ValueError(
            'brutils.altair.serve_chart_loc_csv: with chart: {}\nchart.data.url must endwith ".csv"'.format(
                chart))

    with open(chart.data.url,'r') as fid :
        csv_contents = fid.read()

    files[chart.data.url] = ['text/csv',csv_contents]
    chart.serve(files=files)