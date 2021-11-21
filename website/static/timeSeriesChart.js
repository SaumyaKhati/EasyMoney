import React from 'react'
import ReactApexChart from 'react-apexcharts'

class timeSeriesChart extends React.Component {
    constructor(props) {
        super(props);

        this.state = {

            series: [{
                name: 'Spending',
                data: dates
            }],
            options: {
                chart: {
                    type: 'area',
                    stacked: false,
                    height: 350,
                    zoom: {
                        type: 'x',
                        enabled: true,
                        autoScaleYaxis: true
                    },
                    toolbar: {
                        autoSelected: 'zoom'
                    }
                },
                dataLabels: {
                    enabled: false
                },
                markers: {
                    size: 0,
                },
                title: {
                    text: 'Stock Price Movement',
                    align: 'left'
                },
                fill: {
                    type: 'gradient',
                    gradient: {
                        shadeIntensity: 1,
                        inverseColors: false,
                        opacityFrom: 0.5,
                        opacityTo: 0,
                        stops: [0, 90, 100]
                    },
                },
                yaxis: {
                    labels: {
                        formatter: function (val) {
                            return (val / 1000000).toFixed(0);
                        },
                    },
                    title: {
                        text: '$'
                    },
                },
                xaxis: {
                    type: 'datetime',
                },
                tooltip: {
                    shared: false,
                    y: {
                        formatter: function (val) {
                            return (val / 1000000).toFixed(0);
                        }
                    }
                }
            },
        };
    }

    render() {
        return (
            <>
            <Container>
                <Row>
                    <Col>
                    <ReactApexChart options={this.state.options} series={this.state.series} type="area" height={350} />
                    </Col>
                </Row>
            </Container>
            </>
        )
    }
}

const domContainer = document.querySelector('#chart');
ReactDOM.render(e(timeSeriesChart), domContainer);
