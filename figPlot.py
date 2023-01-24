import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from pdfPlot import SaveReport


def PLOT(df, name):
    for d in df:
        if "5G KPI Total Info Layer1 PDSCH Throughput [Mbps]" in d:
            df_data = d
    # ******************************************************************************************************** #
    # **********************************************[ DATA KPI ]********************************************** #
    # ******************************************************************************************************** #
    df_data["AutoCallSummary Status"] = df_data["AutoCallSummary Status"].interpolate(method="pad")
    df_data = df_data[df_data["AutoCallSummary Status"] == "Traffic"]

    df_data = df_data.drop(df_data[df_data["5G KPI PCell RF Serving SS-RSRP [dBm]"] == 0].index)
    df_data = df_data.drop(df_data[df_data["5G KPI PCell RF Serving SS-SINR [dB]"] == 0].index)
    df_data = df_data.drop(df_data[df_data["5G KPI PCell Layer1 DL MCS (Avg)"] == 0].index)
    df_data = df_data.drop(df_data[df_data["5G KPI PCell Layer1 UL MCS (Avg)"] == 0].index)
    df_data = df_data.drop(df_data[df_data["5G KPI PCell Layer1 DL BLER [%]"] == 0].index)
    df_data = df_data.drop(df_data[df_data["5G KPI PCell Layer1 UL BLER [%]"] == 0].index)

    # Make Data Fig Subplots
    fig = make_subplots(
        rows=4, cols=2,
        subplot_titles=("5G KPI PCell RF Serving SS-RSRP [dBm]",
                        "5G KPI PCell RF Serving SS-SINR [dB]",
                        "5G KPI Total Info Layer1 PDSCH Throughput [Mbps]",
                        "5G KPI Total Info Layer1 PUSCH Throughput [Mbps]",
                        "5G KPI PCell Layer1 DL MCS (Avg)",
                        "5G KPI PCell Layer1 UL MCS (Avg)",
                        "5G KPI PCell Layer1 DL BLER [%]",
                        "5G KPI PCell Layer1 UL BLER [%]"
                        )
    )

    fig.add_trace(
        go.Bar(x=["AVG", "MIN", "MAX"], y=[df_data["5G KPI PCell RF Serving SS-RSRP [dBm]"].dropna().mean().round(2),
                                           df_data["5G KPI PCell RF Serving SS-RSRP [dBm]"].dropna().min().round(4),
                                           df_data["5G KPI PCell RF Serving SS-RSRP [dBm]"].dropna().max().round(2)],
               legendgroup="DATA RF", legendgrouptitle_text="<b>DATA RF<b>",
               text=[df_data["5G KPI PCell RF Serving SS-RSRP [dBm]"].dropna().mean().round(2),
                     df_data["5G KPI PCell RF Serving SS-RSRP [dBm]"].dropna().min().round(4),
                     df_data["5G KPI PCell RF Serving SS-RSRP [dBm]"].dropna().max().round(2)], name="RSRP"),
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(x=["AVG", "MIN", "MAX"], y=[df_data["5G KPI PCell RF Serving SS-SINR [dB]"].dropna().mean().round(2),
                                           df_data["5G KPI PCell RF Serving SS-SINR [dB]"].dropna().min().round(4),
                                           df_data["5G KPI PCell RF Serving SS-SINR [dB]"].dropna().max().round(2)],
               legendgroup="DATA RF", text=[df_data["5G KPI PCell RF Serving SS-SINR [dB]"].dropna().mean().round(2),

                                            df_data["5G KPI PCell RF Serving SS-SINR [dB]"].dropna().min().round(4),
                                            df_data["5G KPI PCell RF Serving SS-SINR [dB]"].dropna().max().round(2)],
               name="SINR"),
        row=1, col=2
    )

    fig.add_trace(
        go.Bar(x=["AVG", "MIN", "MAX"],
               y=[df_data["5G KPI Total Info Layer1 PUSCH Throughput [Mbps]"].dropna().mean().round(2),
                  df_data["5G KPI Total Info Layer1 PUSCH Throughput [Mbps]"].dropna().min().round(4),
                  df_data["5G KPI Total Info Layer1 PUSCH Throughput [Mbps]"].dropna().max().round(2)],
               legendgroup="UL", legendgrouptitle_text="<b>Uplink Data<b>",
               text=[df_data["5G KPI Total Info Layer1 PUSCH Throughput [Mbps]"].dropna().mean().round(2),
                     df_data["5G KPI Total Info Layer1 PUSCH Throughput [Mbps]"].dropna().min().round(4),
                     df_data["5G KPI Total Info Layer1 PUSCH Throughput [Mbps]"].dropna().max().round(2)], name="UL"),
        row=2, col=2
    )

    fig.add_trace(
        go.Bar(x=["AVG", "MIN", "MAX"],
               y=[df_data["5G KPI Total Info Layer1 PDSCH Throughput [Mbps]"].dropna().mean().round(2),
                  df_data["5G KPI Total Info Layer1 PDSCH Throughput [Mbps]"].dropna().min().round(4),
                  df_data["5G KPI Total Info Layer1 PDSCH Throughput [Mbps]"].dropna().max().round(2)],
               legendgroup="DL", legendgrouptitle_text="<b>Downlink Data<b>",
               text=[df_data["5G KPI Total Info Layer1 PDSCH Throughput [Mbps]"].dropna().mean().round(2),
                     df_data["5G KPI Total Info Layer1 PDSCH Throughput [Mbps]"].dropna().min().round(5),
                     df_data["5G KPI Total Info Layer1 PDSCH Throughput [Mbps]"].dropna().max().round(2)], name="DL"),
        row=2, col=1
    )
    fig.add_trace(
        go.Bar(x=["AVG", "MIN", "MAX"], y=[df_data["5G KPI PCell Layer1 DL MCS (Avg)"].dropna().mean().round(2),
                                           df_data["5G KPI PCell Layer1 DL MCS (Avg)"].dropna().min().round(4),
                                           df_data["5G KPI PCell Layer1 DL MCS (Avg)"].dropna().max().round(2)],
               legendgroup="DL", text=[df_data["5G KPI PCell Layer1 DL MCS (Avg)"].dropna().mean().round(2),
                                       df_data["5G KPI PCell Layer1 DL MCS (Avg)"].dropna().min().round(4),
                                       df_data["5G KPI PCell Layer1 DL MCS (Avg)"].dropna().max().round(2)], name="DL MCS"),
        row=3, col=1
    )

    fig.add_trace(
        go.Bar(x=["AVG", "MIN", "MAX"], y=[df_data["5G KPI PCell Layer1 UL MCS (Avg)"].dropna().mean().round(2),
                                           df_data["5G KPI PCell Layer1 UL MCS (Avg)"].dropna().min().round(4),
                                           df_data["5G KPI PCell Layer1 UL MCS (Avg)"].dropna().max().round(2)],
               legendgroup="UL", text=[df_data["5G KPI PCell Layer1 UL MCS (Avg)"].dropna().mean().round(2),
                                       df_data["5G KPI PCell Layer1 UL MCS (Avg)"].dropna().min().round(4),
                                       df_data["5G KPI PCell Layer1 UL MCS (Avg)"].dropna().max().round(2)], name="UL MCS"),
        row=3, col=2
    )

    fig.add_trace(
        go.Bar(x=["AVG", "MIN", "MAX"], y=[df_data["5G KPI PCell Layer1 DL BLER [%]"].dropna().mean().round(2),
                                           df_data["5G KPI PCell Layer1 DL BLER [%]"].dropna().min().round(4),
                                           df_data["5G KPI PCell Layer1 DL BLER [%]"].dropna().max().round(2)],
               legendgroup="DL",
               text=[df_data["5G KPI PCell Layer1 DL BLER [%]"].dropna().mean().round(2),
                     df_data["5G KPI PCell Layer1 DL BLER [%]"].dropna().min().round(4),
                     df_data["5G KPI PCell Layer1 DL BLER [%]"].dropna().max().round(2)], name="DL BLER"),
        row=4, col=1
    )

    fig.add_trace(
        go.Bar(x=["AVG", "MIN", "MAX"], y=[df_data["5G KPI PCell Layer1 UL BLER [%]"].dropna().mean().round(2),
                                           df_data["5G KPI PCell Layer1 UL BLER [%]"].dropna().min().round(4),
                                           df_data["5G KPI PCell Layer1 UL BLER [%]"].dropna().max().round(2)],
               legendgroup="UL",
               text=[df_data["5G KPI PCell Layer1 UL BLER [%]"].dropna().mean().round(2),
                     df_data["5G KPI PCell Layer1 UL BLER [%]"].dropna().min().round(4),
                     df_data["5G KPI PCell Layer1 UL BLER [%]"].dropna().max().round(2)], name="UL BLER"),
        row=4, col=2
    )

    fig.update_layout(
        showlegend=False,
        template='plotly_dark',
        title={
            'text': "<b> " + str(
                name) + " - Data KPI<b>"})

    Data_Fig = fig

    # ******************************************************************************************************** #
    # ******************************************[ Protocol KPI ]********************************************** #
    # ******************************************************************************************************** #

    s = df_data["5G KPI PCell Layer1 RACH Result"].value_counts()
    df_rach_count = s.to_frame(name='Count')

    s = df_data["5G KPI Total Info DL CA Type"].value_counts()
    df_ca_count = s.to_frame(name='Count')

    s = df_data["5G KPI PCell Layer1 RACH Reason"].value_counts()
    df_RACH_Reason_count = s.to_frame(name='Count')

    s = df_data["5G KPI PCell RF Band"].value_counts()
    df_BAND_count = s.to_frame(name='Count')

    # Make Protocol Fig Subplots
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"type": "bar"}, {"type": "bar"}], [{"type": "bar"}, {"type": "bar"}]],
        subplot_titles=(
            "5G KPI PCell Layer1 RACH Result", "5G KPI Total Info DL CA Type", "5G KPI PCell Layer1 RACH Reason",
            "5G KPI PCell RF Band")
    )

    df_rach_count['Percentage'] = round((df_rach_count['Count'] / df_rach_count['Count'].sum()) * 100, 0)
    fig.add_trace(
        go.Bar(y=df_rach_count['Count'], x=df_rach_count.index, legendgroup="RACH Results",
               legendgrouptitle_text="<b>5G KPI PCell Layer1 RACH Result<b>",
               name="RACH Results",
               text=['[{}]  {:.0%}'.format(v, p / 100) for v, p in
                     zip(df_rach_count['Count'], df_rach_count['Percentage'])]
               ),

        row=1, col=1
    )

    df_ca_count['Percentage'] = round((df_ca_count['Count'] / df_ca_count['Count'].sum()) * 100, 0)
    fig.add_trace(
        go.Bar(y=df_ca_count['Count'], x=df_ca_count.index, legendgroup="CA",
               legendgrouptitle_text="<b>5G KPI Total Info DL CA Type<b>",
               text=['[{}]  {:.0%}'.format(v, p / 100) for v, p in zip(df_ca_count['Count'], df_ca_count['Percentage'])]
               ),
        row=1, col=2
    )

    df_RACH_Reason_count['Percentage'] = round(
        (df_RACH_Reason_count['Count'] / df_RACH_Reason_count['Count'].sum()) * 100, 0)
    fig.add_trace(
        go.Bar(y=df_RACH_Reason_count['Count'], x=df_RACH_Reason_count.index, legendgroup="RACH",
               legendgrouptitle_text="<b>5G KPI PCell Layer1 RACH Reason<b>",
               text=['[{}]  {:.0%}'.format(v, p / 100) for v, p in
                     zip(df_RACH_Reason_count['Count'], df_RACH_Reason_count['Percentage'])],
               name="RACH Reason"),
        row=2, col=1
    )

    df_BAND_count['Percentage'] = round((df_BAND_count['Count'] / df_BAND_count['Count'].sum()) * 100, 0)
    fig.add_trace(
        go.Bar(y=df_BAND_count['Count'], x=df_BAND_count.index, legendgroup="BAND",
               legendgrouptitle_text="<b>5G KPI PCell RF Band<b>", text=['[{}]  {:.0%}'.format(v, p / 100) for v, p in
                                                                         zip(df_BAND_count['Count'],
                                                                             df_BAND_count['Percentage'])],
               name="5G KPI PCell RF Band"),
        row=2, col=2
    )

    fig.update_traces(textfont_size=15, textangle=0, cliponaxis=False)

    fig.update_layout(
        showlegend=False,
        template='plotly_dark',
        title={
            'text': "<b>" + str(name) + " - Protocol KPI<b>"})

    Protocol_Fig = fig

    # ******************************************************************************************************** #
    # ******************************************[ Voice KPI ]************************************************* #
    # ******************************************************************************************************** #

    px.set_mapbox_access_token(open("./assets/map.mapbox_token").read())

    for d in df:
        if "Voice Call" in d:
            df_voice = d


    df_voice = df_voice.replace(to_replace="5G-NR_SA(2CA)", value="5G-NR_SA")
    df_voice = df_voice.replace(to_replace="LTE(2CA)", value="LTE")
    df_voice = df_voice.replace(to_replace="End By Pause", value="No Page")
    df_voice = df_voice.replace(to_replace="End By User", value="Success")

    # Make Voice Fig Subplots
    RSRP_fig = px.scatter_mapbox(df_voice, lat="GPS Lat", lon="GPS Lon", color="5G KPI PCell RF Serving SS-RSRP [dBm]",
                                 color_continuous_scale=[(0, "red"), (0.5, "yellow"), (1, "green")], size_max=20,
                                 zoom=11.5,
                                 labels={"5G KPI PCell RF Serving SS-RSRP [dBm]": "<b>RSRP [dBm]<b>"})

    RSRP_fig.update_layout(mapbox_style="dark", template='plotly_dark', title={
        'text': "<b>" + str(name) + " - RSRP - MAP<b>"})

    RSRP_Map_fig = RSRP_fig

    SINR_fig = px.scatter_mapbox(df_voice, lat="GPS Lat", lon="GPS Lon", color="5G KPI PCell RF Serving SS-SINR [dB]",
                                 color_continuous_scale=[(0, "red"), (0.5, "yellow"), (1, "green")], size_max=20,
                                 zoom=11.5,
                                 labels={"5G KPI PCell RF Serving SS-SINR [dB]": "<b>SINR [dB]<b>"})

    SINR_fig.update_layout(mapbox_style="dark", template='plotly_dark', title={
        'text': "<b>" + str(name) + " - SINR - MAP<b>"})

    SINR_Map_fig = SINR_fig

    df_site = pd.read_excel("OKC_SITES.xlsx", index_col=None)
    df_voice_map = pd.concat([df_voice, df_site])

    df_voice_map["GPS Lon"] = df_voice_map["GPS Lon"].fillna(method='ffill')
    df_voice_map["GPS Lat"] = df_voice_map["GPS Lat"].fillna(method='ffill')

    map_df = df_voice_map[df_voice_map['Voice Call'].notna()]
    map_df['dummy_column_for_size'] = 1.
    results_fig = px.scatter_mapbox(map_df, lat="GPS Lat", lon="GPS Lon", text="Voice Call", color="Voice Call",
                                    size='dummy_column_for_size', size_max=20, zoom=11.8,
                                    labels={"Voice Call": "<b>VoNR Results<b>"})

    # results_fig.data[i].text = [e if e == 'Success' else '' for e in results_fig.data[i]]
    Ignor_Array = ['Success', 'Setup Fail', 'Drop', 'Error', 'End By User', 'SkipCall']
    for i in range(len(results_fig.data)):
        if results_fig.data[i].name in Ignor_Array:
            if results_fig.data[i].name == 'Success':
                results_fig.data[i].text = ''
                results_fig.data[i].marker = {'color': 'green'}
            elif results_fig.data[i].name == 'Setup Fail':
                results_fig.data[i].text = ''
                results_fig.data[i].marker = {'color': 'red'}
            elif results_fig.data[i].name == 'Drop':
                results_fig.data[i].text = ''
                results_fig.data[i].marker = {'color': 'blue'}
            else:
                results_fig.data[i].showlegend = False
                results_fig.data[i].legendgroup = 'SKIP'
                results_fig.data[i].text = ''
                results_fig.data[i].marker = {'color': 'rgba(0,0,0,0)'}

        else:
            results_fig.data[i].text = str(results_fig.data[i].text)
            results_fig.data[i].showlegend = False
            results_fig.data[i].legendgroup = 'gNB'
            results_fig.data[i].marker = {'color': 'rgba(0,0,0,.3)', 'size': [15], 'sizemode': 'area', 'sizeref': 0.0025}

    results_fig.update_layout(mapbox_style="dark", template='plotly_dark', title={'text': "<b>Voice Call - MAP<b>"},  mapbox={'center': {'lat':35.40636772804942,'lon':-97.49471149726844}})

    Results_Map_fig = results_fig

    df_voice["GPS Lon"] = df_voice["GPS Lon"].fillna(method='ffill')
    df_voice["GPS Lat"] = df_voice["GPS Lat"].fillna(method='ffill')


    map_df = df_voice[df_voice['Event Technology'].notna()]

    tech_results_fig = px.scatter_mapbox(map_df, lat="GPS Lat", lon="GPS Lon", color="Event Technology", size_max=20,
                                         zoom=11.8,
                                         labels={"Event Technology": "<b>Event Technology<b>"})

    tech_results_fig.update_layout(mapbox_style="dark", template='plotly_dark', title={
        'text': "<b>" + str(name) + " - Event Technology - MAP<b>"})

    Tech_results_fig = tech_results_fig

    # Getting the string count of call result to int
    s = df_voice["Voice Call"].value_counts()
    # Make a DF from call results
    df_voice_count = s.to_frame(name='Count')

    # Getting the string count of call result to int
    s = df_voice["Event Technology"].value_counts()
    # Make a DF from call results
    df_tech_count = s.to_frame(name='Count')

    # Getting the string count of call result to int
    s = df_voice["5G-NR RRC NR MCG Mobility Statistics Intra-NR HandoverResult"].value_counts()
    # Make a DF from call results
    df_HO_count = s.to_frame(name='Count')

    fig = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "pie"}, {"type": "pie"}]],
        subplot_titles=("<b>Voice Call<b> <br>  <br>",
                        "<b>Event Technology<b> <br>  <br>",
                        )
    )

    fig.add_trace(
        go.Pie(values=df_voice_count['Count'], labels=df_voice_count.index, legendgroup="CALL",
               legendgrouptitle_text="<b>Voice Call<b>", name="Call Results"),
        row=1, col=1
    )

    fig.add_trace(
        go.Pie(values=df_tech_count['Count'], labels=df_tech_count.index, legendgroup="TECH",
               legendgrouptitle_text="<b>Event Technology<b>", name="Technology"),
        row=1, col=2
    )

    fig.update_traces(textposition='auto', textinfo='value+percent+label')

    fig.update_layout(
        showlegend=False,
        template='plotly_dark',
        title={'text': "<b>" + str(name) + " - Voice KPI<b>"}
    )

    PIE_Call_Fig = fig

    fig = make_subplots(
        rows=3, cols=2,
        specs=[[{"type": "bar"}, {"type": "bar"}], [{"type": "bar"}, {"type": "bar"}], [{'colspan': 2}, None]],
        subplot_titles=("RSRP",
                        "5G-NR HO Results",
                        "SINR",
                        "MOS",
                        "MOS Graph"
                        )
    )

    df_HO_count['Percentage'] = round((df_HO_count['Count'] / df_HO_count['Count'].sum()) * 100, 0)
    fig.add_trace(
        go.Bar(y=df_HO_count['Count'], x=df_HO_count.index, legendgroup="HO",
               legendgrouptitle_text="<b>5G-NR Handover Result<b>", name="5G-NR Handover Result",
               text=['[{}]  {:.0%}'.format(v, p / 100) for v, p in
                     zip(df_HO_count['Count'], df_HO_count['Percentage'])], ),
        row=1, col=2
    )

    fig.add_trace(
        go.Bar(x=["AVG", "MAX", "MIN"], y=[df_voice["5G KPI PCell RF Serving SS-RSRP [dBm]"].mean().round(2),
                                           df_voice["5G KPI PCell RF Serving SS-RSRP [dBm]"].min().round(4),
                                           df_voice["5G KPI PCell RF Serving SS-RSRP [dBm]"].max().round(2)],
               legendgroup="Voice RF", legendgrouptitle_text="<b>Voice RF<b>",
               text=[df_voice["5G KPI PCell RF Serving SS-RSRP [dBm]"].mean().round(2),
                     df_voice["5G KPI PCell RF Serving SS-RSRP [dBm]"].min().round(4),
                     df_voice["5G KPI PCell RF Serving SS-RSRP [dBm]"].max().round(2)], name="RSRP"),
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(x=["AVG", "MIN", "MAX"], y=[df_voice["5G KPI PCell RF Serving SS-SINR [dB]"].mean().round(2),
                                           df_voice["5G KPI PCell RF Serving SS-SINR [dB]"].min().round(4),
                                           df_voice["5G KPI PCell RF Serving SS-SINR [dB]"].max().round(2)],
               legendgroup="Voice RF", text=[df_voice["5G KPI PCell RF Serving SS-SINR [dB]"].mean().round(2),
                                             df_voice["5G KPI PCell RF Serving SS-SINR [dB]"].min().round(4),
                                             df_voice["5G KPI PCell RF Serving SS-SINR [dB]"].max().round(2)],
               name="SINR"),
        row=2, col=1
    )

    fig.add_trace(
        go.Bar(x=["AVG", "MIN", "MAX"], y=[df_voice["MOS P863(POLQA)"].mean().round(2),
                                           df_voice["MOS P863(POLQA)"].min().round(4),
                                           df_voice["MOS P863(POLQA)"].max().round(2)],
               legendgroup="Voice RF", text=[df_voice["MOS P863(POLQA)"].mean().round(2),
                                             df_voice["MOS P863(POLQA)"].min().round(4),
                                             df_voice["MOS P863(POLQA)"].max().round(2)], name="POLQA"),
        row=2, col=2
    )
    fig.add_trace(
        go.Scatter(x=df_voice['TIME_STAMP'], y=df_voice["MOS P863(POLQA)"],
                   mode='lines+markers',
                   connectgaps=True,
                   name='POLQA Graph'),

        row=3, col=1
    )

    fig.update_layout(
        showlegend=False,
        template='plotly_dark',
        title={'text': "<b>" + str(name) + " - Voice KPI<b>"})

    BAR_Call_Fig = fig
    SaveReport([Protocol_Fig, Data_Fig, PIE_Call_Fig,Results_Map_fig,Tech_results_fig,BAR_Call_Fig, RSRP_Map_fig, SINR_Map_fig], name)

