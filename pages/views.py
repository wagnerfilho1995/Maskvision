import csv
import pandas as pd
from django.shortcuts import render, redirect
from .forms import AmplifierForm
from .forms import DocumentForm, ModeloForm, RequestPredictionForm
from .models import Amplifier, State, Document, Modelo, RequestPrediction
from django.http import HttpResponse
from plotly.offline import plot
from plotly.offline import iplot, init_notebook_mode
import plotly.graph_objs as go
import numpy as np
from pathlib import Path
import os
from decimal import Decimal
import shutil
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .nnPrediction import execute

def download(request, file_name):
    response = HttpResponse(mimetype='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
    response['X-Sendfile'] = smart_str(settings.MEDIA_ROOT + file_name)
    return response

def process_file(file_handle):
    # Leitura e ajuste da virgula pelo ponto, nos valores
    data_frame = pd.read_csv(file_handle, sep=';')
    data_frame = data_frame.replace({',': '.'}, regex=True)
    
    # Filtrando colunas do csv
    pin = data_frame["Pin Total OSA (dBm)"].values
    pout = data_frame["Pout Total OSA (dBm)"].values

    # Ler 47 colunas a partir da coluna 7 -> Freq. Canal (Hz)
    freq = []
    ganho = []
    noise_figure = []

    # For de iterações linha a linha do data frame (csv)
    for _index, row in data_frame.iterrows():
        #   Lendo as colunas da linha pelo nome setado no like="freq. Canal(Hz)"
        r = row.filter(like='Freq. Canal (Hz)').astype(float)
        freq.append(list(dict(r).values()))
        s = row.filter(like='Ganho Canal (dBm)').astype(float)
        ganho.append(list(dict(s).values()))
        t = row.filter(like='NF Canal (dB)').astype(float)
        noise_figure.append(list(dict(t).values()))

    return pin, pout, freq, ganho, noise_figure

def create_states(pin_total, pout_total, amp, frequency_ch_total, g, nf):
    # Vamos criar uma lista de states, de acordo com pin e pout do Amplificador
    states = []
    for pin, pout, frequency_ch, ganho, nf in zip(pin_total, pout_total, frequency_ch_total, g, nf):
        # Criando objeto state
        state = State(amplifier=amp, pin_total=pin, pout_total=pout, frequency_ch=frequency_ch, ganho=ganho, nf=nf)
        states.append(state)
    # Estou salvando no banco a lista de states criada no for acima
    State.objects.bulk_create(states)

def home(request):
    return render(request, "home.html", {})

def novo_amplificador(request):
    form = AmplifierForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        amp = form.save()
        pin, pout, frequency_ch, ganho, nf = process_file(amp.mask)
        create_states(pin, pout, amp, frequency_ch, ganho, nf)
        return redirect('amplificadores')
    return render(request, "novo_amplificador.html", {"form" : form}) 

def novo_modelo(request):
    form = ModeloForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        mod = form.save()
        return redirect('treino')
    return render(request, "novo_modelo.html", {"form" : form}) 

def amplifiers(request):
    return render(request, "amplificadores.html", {"amplificadores" : Amplifier.objects.all()})

def detail_amplifier(request, id):

    amp = Amplifier.objects.get(id=id)
    states = State.objects.filter(amplifier=amp)
    print("DETALHE")
    Pin_Total = [state.pin_total for state in states]
    Pout_Total = [state.pout_total for state in states]
    #="/resultados/%f/%f">Análise Ganho vs F. Ruído<a>'%(x,y) for x,y in zip(Pin_Total, Pout_Total)]
    text = ['Ganho: %.2f'%(y-x) for x, y in zip(Pin_Total, Pout_Total)]
    print(len(Pin_Total))
    print(len(Pout_Total))
    gain = []
    for pin, pout in zip(Pin_Total, Pout_Total):
        gain.append(pout-pin)

    scatter = go.Scatter(
        x=Pin_Total,
        y=Pout_Total,
        mode="markers",
        marker=dict(size=11, color=gain, colorscale="Portland", showscale=True),
        text=text,
    )
    layout = go.Layout(
        title='Pin x Pout',
        autosize=True,
        hovermode='closest',
        xaxis=dict(
            title='Input Power (dBm)',
            ticklen=5,
            zeroline=False,
            gridwidth=2,
        ),
        yaxis=dict(
            title='Output Power (dBm)',
            ticklen=5,
            zeroline=False,
            gridwidth=2,
        )
    )
    data = [scatter,]
    return render(
        request,
        'detail_amplifier.html',
        {
            'id': id,
            'amp': amp,
            'grafico': plot(
                {
                    'data': data,
                    'layout': layout
                }, 
                auto_open=False,
                output_type='div'
            )
        }
    )

def about(request):
    my_name = "Olá, meu nome é Wagner Williams"
    return render(request, "sobre.html", {"my_name" : my_name})

def treino(request):  
    return render(request, "treino.html", {"modelos" : Modelo.objects.all()})

def visualize_erro(request, id):  
    
    mod = Modelo.objects.get(id=id)
    model_type = mod.amplifier.reference

    
    lines = []
    # Lendo linha por linha do txt
    for line in mod.file_txt:
        lines.append(line.split())

    print(lines[3])
    # Erro na linha 4 do arquivo txt
    erro = []
    for value in lines[3]:
        print(value)
        erro.append(float(value))

    # Epoca na linha 5 do arquivo txt
    epoca = []
    for value in lines[4]:
        epoca.append(int(value))

    # BoxPlot na linha 6 do arquivo txt
    boxp = []
    for value in lines[5]:
        boxp.append(float(value))
    
    #epoca = np.arange(200)
    #erro = np.random.rand(200)
    scatter_epocaerro = go.Scatter(
        x=epoca,
        y=erro,
        mode="markers",
        marker=dict(size=12),
        name='Treinamento'
    )
    
    layout = go.Layout(
        title='Erro Médio Quadrático',
        autosize=True,
        hovermode='closest',
        xaxis=dict(
            title='Epocas',
            ticklen=5,
            zeroline=False,
            gridwidth=2,
        ),
        yaxis=dict(
            title='Erro',
            ticklen=5,
            zeroline=False,
            gridwidth=2,
           # range=[0, maxro)*1.2]
        ),
    )
    
    box_erro = go.Box(y=boxp)

    boxlayout = go.Layout(
        title='Erro Médio Absoluto',
        autosize=True,
        hovermode='closest',
        yaxis=dict(
            title='dB'
           # range=[0, maxro)*1.2]
        ),
    )

    data = [scatter_epocaerro]
    databox = [box_erro]
   
    return render(
        request,
        'visualize_erro.html',
        {
            'grafico': plot(
                {
                    'data': data,
                    'layout': layout
                },
                auto_open=False,
                output_type='div'
            ),
            'boxplot':plot(
                {
                    'data':databox,
                    'layout':boxlayout
                },
                auto_open=False,
                output_type='div'
            ),
            'erro': lines[3],
            'epocas': lines[4]
        }
    )
    #return render(request, "visualize_erro.html",  {'id' : id, 'modelo' : model_type})

def result(request, id, x, y):

    amp = Amplifier.objects.get(id=id)
    state = State.objects.get(amplifier=amp, pin_total=x,pout_total=y)
    frequency = state.frequency_ch
    ganho = state.ganho
    nf = state.nf

    scatter_ganho = go.Scatter(
                      x = frequency,
                      y  = ganho,
                      mode="markers",
                      marker = dict(size = 12),
                      name = 'Gain'
                      )

    scatter_nf = go.Scatter(
                      x = frequency,
                      y  = nf,
                      mode="markers",
                      marker = dict(size = 12),
                      name = 'Noise Figure'
                      )
    layout= go.Layout(
        title = 'Channel Frequency x Gain / NF',
        autosize=True,
        hovermode='closest',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis= dict(
              title= 'Channel Frequency (THz)',
              ticklen= 5,
              zeroline= False,
              gridwidth= 2,
          ),
        yaxis= dict(
            title= 'dB',
            ticklen= 5,
            zeroline= False,
            gridwidth= 2,
            range=[0, 30]
          ),
    )

    data = [scatter_ganho, scatter_nf]

    #form = DocumentForm(request.POST or None, request.FILES or None)
    form = RequestPredictionForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        print('entrei')
        req = form.save()
        return redirect ('compare', id=id,x=x,y=y, doc=req.id)

    return render(request, 'result.html', {'state' : state, 'amplificadores' : Amplifier.objects.all(), 'amp' : amp, 'grafico' : plot({ 'data' : data, 'layout': layout }, auto_open = False, output_type = 'div'), 'form' : form})


def compare(request, id, x, y, doc):
    # View que apresenta a comparação

    amp = Amplifier.objects.get(id=id)
    state = State.objects.get(amplifier=amp, pin_total=x, pout_total=y)
    frequency = state.frequency_ch
    ganho = state.ganho
    nf = state.nf

    #doc = Document.objects.get(id=doc)
    doc = RequestPrediction.objects.get(id=doc)
    pathdoc = doc.pin_signal.path
    scatter_ganho = go.Scatter(
        x=frequency,
        y=ganho,
        mode="markers",
        marker=dict(size=12),
        name='Gain'
    )

    scatter_nf = go.Scatter(
        x=frequency,
        y=nf,
        mode="markers",
        marker=dict(size=12),
        name='Noise Figure'
    )

    layout = go.Layout(
        title='Channel Frequency x Gain / NF',
        autosize=True,
        hovermode='closest',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            title='Channel Frequency (THz)',
            ticklen=5,
            zeroline=False,
            gridwidth=2,
        ),
        yaxis=dict(
            title='dB',
            ticklen=5,
            zeroline=False,
            gridwidth=2,
        ),
    )
    
    #pin = pin.replace({',': '.'}, regex=True)
    #leitura = pd.read_csv(str(doc.file_input), header=None, delim_whitespace=True)
    leitura = pd.read_csv(str(doc.pin_signal.path), header=None, delim_whitespace=True)
 
    scatters = []
    rgb = ["#e84118", "#44bd32", "#0097e6"]
    symbols = ["circle", "square", "diamond", "cross"]

    count = 1
    print("PIN")
    for pin in leitura.values:
        print(pin)
        scatters.append(
            go.Scatter(
            x=frequency,
            y=pin,
            mode="markers",
            marker_symbol=symbols[count-1],
            marker=dict(
                size=9,
                color=rgb[(count-1)%3]
            ),
            name='Sinal:  ('+str(count)+')'
            )        
        )
        count += 1

    # Chamando codigo de predicao do allan
    saidas = execute(str(doc.modelo.file_h5.path), str(doc.modelo.file_txt.path), str(doc.pin_signal.path))
    
    count = 1
    print("POUT")
    for pout in saidas:
        print(pout)
        scatters.append(
            go.Scatter(
            x=frequency,
            y=pout,
            mode="markers",
            marker_symbol=symbols[count-1],
            marker=dict(
                size=9,
                color=rgb[(count-1)%3]
                ),
            name='Saída: ('+str(count)+')'
            )
        )
        count += 1

    os.remove(str(doc.modelo.file_h5.path))
    os.remove(str(doc.pin_signal.path))

    layout2 = go.Layout(
        title='Channel Frequency x Pout ',
        autosize=True,
        hovermode='closest',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            title='Channel Frequency (THz)',
            ticklen=5,
            zeroline=False,
        ),
        yaxis=dict(
            title='Pins e Pouts',
            ticklen=5,
            zeroline=False,
        ),
    )
    data = [scatter_ganho, scatter_nf]
    data_compare = scatters
    
    return render(
        request,
        'compare.html',
        {
            'x': x,
            'y': y,
            'state' : state,
            'amp' : amp,
            'grafico' : plot(
                { 
                    'data' : data,
                    'layout': layout 
                }, 
                auto_open=False,
                output_type='div'
            ),
            'grafico2' : plot(
                { 
                    'data' : data_compare,
                    'layout': layout2
                },
                auto_open=False,
                output_type='div'
            )
        }
    )