```chartsview
#-----------------#
#- chart type    -#
#-----------------#
type: DualAxes

#-----------------#
#- chart data    -#
#-----------------#
data: <* GCPL_data.csv *>, <* GCPL_data.csv *>

#-----------------#
#- chart options -#
#-----------------#
options:
  xField: '(Q-Qo)/mA.h'
  yField: ['Ecell/V', 'Efficiency/%']
  yAxis:
    title:
      text: Amplitude'
      style:
         fontSize: 16
    line:
      style:
        stroke: '#aaa'
    tickLine:
      style:
        lineWidth: 2
        stroke: '#aaa'
        length: 5
  geometryOptions:
    - geometry: 'line'
    - geometry: 'line'
      lineStyle:
        lineWidth: 2
```