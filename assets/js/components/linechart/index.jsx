import React, {Component} from 'react';
import {ResponsiveXYFrame} from 'semiotic';
import { scaleTime } from 'd3-scale';
import moment from 'moment';
import { curveMonotoneX } from 'd3-shape' ;

class MonthChart extends Component {
  constructor(props) {
    super(props);
    this.parseDate = this.parseDate.bind(this);
  }

  parseDate(dateString) {
    let [month, year] = dateString.split(' ');
    return new Date(Date.parse(month + "1, " + year));
  }

  render() {
    const data = {data: this.props.data};

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
          xAccessor={d => (this.parseDate(d.month))}
          yAccessor={"count"}
          yExtent={[0,undefined]}
          xScaleType={scaleTime()}
          margin={{"top": 60, "bottom": 65, "left": 90, "right": 20}}
          axes={[
            {orient: 'left', label: { name: "Stops", location: "outside", anchor: "start", locationDistance: 60 }, ticks: 3, className: 'yscale', tickFormat: d => d },
            {orient: 'bottom', className: 'xscale', ticks: 6, tickFormat: d => moment(d).format("MM/YY")}
          ]}
          hoverAnnotation={true}
          tooltipContent={d => (<div>{d.month}: {d.count}</div>)}
        />
        </div>
      )
    }
}

export default MonthChart;
