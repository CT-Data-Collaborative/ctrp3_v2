import React, {Component} from 'react';
import {ResponsiveXYFrame} from 'semiotic';
import { scaleTime } from 'd3-scale';
import { curveMonotoneX } from 'd3-shape' ;

class TimeSeriesChart extends Component {
  constructor(props) {
    super(props);
    this.datetimeParser = props.datetimeParser.bind(this);
  }

  render() {
    const data = {data: this.props.data};
    console.log(this.props.xAccessor)
    return (
        <div style={{ width: '100%', height: '200px', marginBottom: '4rem'}}>
        <ResponsiveXYFrame
          size={[undefined,250]}
          responsiveWidth={true}
          responsiveHeight={false}
          lineType={{ type: 'line', interpolator: curveMonotoneX }}
          lines={data}
          lineDataAccessor="data"
          lineStyle={d => ({fill: '#4670A7', fillOpacity: 0.5, stroke: '#4670A7', strokeWidth: '3px'})}
          xAccessor={d => (this.datetimeParser(d[this.props.xAccessor]))}
          yAccessor={d => d[this.props.yAccessor]}
          yExtent={[0,undefined]}
          xScaleType={scaleTime()}
          margin={{"top": 60, "bottom": 65, "left": 90, "right": 20}}
          axes={[
            { orient: 'left', label: { name: "Stops", location: "outside", anchor: "start", locationDistance: 60 }, className: 'yscale', tickFormat: d => d },
            { orient: 'bottom', className: 'xscale', ticks: 6, tickFormat: d => this.props.xTickFormatter(d) }
          ]}
          hoverAnnotation={true}
          tooltipContent={d => (<div>{d[this.props.xAccessor]}: {d[this.props.yAccessor]}</div>)}
        />
        </div>
      )
    }
}

export default TimeSeriesChart;
