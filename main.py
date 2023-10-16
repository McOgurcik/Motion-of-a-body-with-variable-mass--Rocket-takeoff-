import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle
import PySimpleGUI as sg
import math
import matplotlib as mt
import numpy as np
x0 = 50
y0 = 50
ft = 35000000
c = 0.5
s = 5
m0 = 20000
mk = 500
dt = 0.1
tp = 120
enj = False
a = 0.5
class Canvas(FigureCanvasTkAgg):
  """
    Create a canvas for matplotlib pyplot under tkinter/PySimpleGUI canvas
    """

  def __init__(self, figure=None, master=None):
    super().__init__(figure=figure, master=master)
    self.canvas = self.get_tk_widget()
    self.canvas.pack(side='top', fill='both', expand=1)
def cl():
    ax_1.cla()
    ax_2.cla()
    # fig.clf()
    canvas.draw()
def cm_to_inch(value):
  return value / 2.54
def f(ro,k):
    if ro <= 1:
        return (1-(1-k)*ro)
    else:
        return k
def v_i(a,b,ro,k,p,h,v):
    # print(p*math.exp(-2.3026 * h)*v*v)
    # return (a - b * f(ro, k) - p * math.exp(-2.3026 * h) * v * v / f(ro, k))
    return (1/f(ro,k)*(a-b*f(ro,k)-(p*math.exp(-2.3026 * h)*v*v)))
def plot_figure(a,m0,mk,enj,tp):
    ax_1.cla()
    ax_2.cla()
    # if True:
    try:
        a = float(a)
        m0 = float(m0)*1000
        s = 5
        mk = float(mk)*1000
        tp = float(tp)
        # t_b = (m0 - mk)/al
        t_b = tp
        v_b = 7.8 * 1000
        g = 9.80665
        h_b = 17 * 1000
        p0 = 1.29
        c = 0.5
        b = (t_b*g)/v_b
        p = (0.5*c*p0*s*v_b*t_b)/m0
        e = v_b*t_b/h_b
        k = mk/m0
        i = 0
        v = [0]
        t = [0]
        h = [0]
        rn = 1
        dt = t_b / 100
        while (rn>0):
            ro = t[i]/t_b
            v.append(v[i]+(dt/t_b)*(v_i(a, b, ro, k, p, h[i], v[i])))
            h.append(h[i]+(dt/t_b)*e*v[i])
            t.append(t[i]+dt)
            if v[i] >= 1 and enj == True:
                a = 0
            if ro >= 1:
                rn = rn -1
            i = i+1

    except:
        cl()
        print("err")
        return
    ax_1.set_title('График зависимости v от t', fontsize=12)
    ax_2.set_xlabel('График зависимости h от t', fontsize=12)
    ax_1.plot(t, v, color='g')
    ax_2.plot(t, h, color='r')
    canvas.draw()

layout = [
    [sg.Canvas(size=(640, 480), key='Canvas')],
    [sg.Text('a'), sg.Input(0.5,enable_events=True,k='-A-',size=(9, 1)),
    sg.Text('m0, т'), sg.Input(20000,enable_events=True,k='-M0-',size=(7, 1)),
    sg.Text('mk, т'), sg.Input(500,enable_events=True,k='-MK-',size=(7, 1)),
    sg.Text('T, c'),sg.Input(120,enable_events=True,k='-T-',size=(7, 1))],
    [sg.Checkbox('Выключить двигатель при достижении 1 к. скор.', default=False, enable_events=True, k='-ENJ-')],
    # sg.Text('S'), sg.Input(5,enable_events=True,k='-S-',size=(5, 1)),
    # sg.Text(text="xm"),
    # sg.Spin([i for i in range(-200, 200)],
    #         initial_value=50,
    #         enable_events=True,
    #         k='-X-'),
    # sg.Text(text="ym"),
    # sg.Spin([i for i in range(-200, 200)],
    #         initial_value=50,
    #         enable_events=True,
    #         k='-Y-')],
    #         [sg.Checkbox('Выключить двигатель при достижении 1 к. скор.', default=False, enable_events=True, k='-ENJ-')],
    # [[sg.Text('c'), sg.Input(0.5,enable_events=True,k='-C-',size=(5, 1)),,
    # sg.Text('dt, c'), sg.Input(0.1,enable_events=True,k='-DT-',size=(5, 1)),sg.Checkbox('Выключить двигатель при достижении 1 к. скор.', default=False, enable_events=True, k='-ENJ-')]],
    [[sg.Push(), sg.Button('go'),sg.Button('Clear'), sg.Push()]]
    ]

window = sg.Window('Свободное падение',
                   layout,
                   finalize=True,
                   resizable=True, size = (640, 520))
# plt.figure(figsize=(cm_to_inch(h_w), cm_to_inch(w_w)))
fig = Figure(figsize=(cm_to_inch(16), cm_to_inch(10.7)))
ax_1 = fig.add_subplot(2, 1, 1)
# fig.subplots_adjust(top=0.8, bottom=0.1)
ax_2 = ax_1.twinx()
ax_2 = fig.add_subplot(2, 1, 2)
canvas = Canvas(fig, window['Canvas'].Widget)
def launch():
    return plot_figure(a,m0,mk,enj,tp)
while True:

  event, values = window.read()
  # print(event)
  if event in (sg.WIN_CLOSED, 'Exit'):
    break
  elif event == '-A-':
      a = values[event]
      # launch()
  elif event == '-T-':
      tp = values[event]
      # launch()
  elif event == '-M0-':
      m0 = values[event]
      # launch()
  elif event == '-MK-':
      mk = values[event]
      # launch()
  elif event == '-ENJ-':
      enj = values[event]
      launch()
  elif event == '-Y-':
    # print(values)
      y0 = values[event]
      launch()
  elif event == '-X-':
    # print(values)
      x0 = values[event]
      launch()
  elif event == 'go':
      launch()
  elif event == 'Clear':
      cl()


window.close()
