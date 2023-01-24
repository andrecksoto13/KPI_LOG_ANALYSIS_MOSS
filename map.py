import plotly.express as px
import pandas as pd

df_voice = pd.read_excel("VOICE_MOSQ_DATA_Fav.xlsx", index_col=None)

df_site = pd.read_excel("OKC_SITES.xlsx", index_col=None)

df_voice = pd.concat([df_voice, df_site])



px.set_mapbox_access_token(open("./assets/map.mapbox_token").read())

df_voice["GPS Lon"] = df_voice["GPS Lon"].fillna(method='ffill')
df_voice["GPS Lat"] = df_voice["GPS Lat"].fillna(method='ffill')

map_df = df_voice[df_voice['Voice Call'].notna()]
map_df['dummy_column_for_size'] = 1.
results_fig = px.scatter_mapbox(map_df, lat="GPS Lat", lon="GPS Lon", text="Voice Call", color="Voice Call",
                                size='dummy_column_for_size', size_max=20, zoom=11.8,
                                labels={"Voice Call": "<b>VoNR Results<b>"})

#results_fig.data[i].text = [e if e == 'Success' else '' for e in results_fig.data[i]]
Ignor_Array = ['Success', 'Setup Fail', 'Drop', 'Error', 'End By User']
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
            results_fig.data[i].marker = {'color': 'rgba(0,0,0,0)'}

    else:
        results_fig.data[i].text =  str(results_fig.data[i].text)
        results_fig.data[i].showlegend = False
        results_fig.data[i].legendgroup = 'gNB'
        results_fig.data[i].marker = {'color': 'rgba(0,0,0,.3)', 'size': [5], 'sizemode': 'area', 'sizeref': 0.0025}





results_fig.update_layout(mapbox_style="dark", template='plotly_dark', title={'text': "<b>Voice Call - MAP<b>"}, mapbox={'center': {'lat':35.40636772804942,'lon':-97.49471149726844}})




results_fig.show()

