import QtQuick 2.0
import "QMLChartData.js" as ChartsData
import "QChartJsTypes.js" as ChartTypes


Rectangle {
    color: "#ffffff"
    property int chart_width: 300
    property int chart_height: 300
    property int chart_spacing: 20
    property int text_height: 80
    property int row_height: 8

    width: chart_width * 4 + 3 * chart_spacing
    height: chart_height * 2 + chart_spacing + 2 * row_height + text_height

    Grid {
        id: layout
        anchors.fill: parent
        columns: 4
        spacing: chart_spacing

        QChartJs {
            id: chart_line
            width: chart_width
            height: chart_height
            chartType: ChartTypes.QChartJSTypes.LINE
            chartData: ChartsData.ChartLineData
            animation: true
            chartAnimationEasing: Easing.InOutElastic
            chartAnimationDuration: 2000
        }

        QChartJs {
            id: chart_bar
            width: chart_width
            height: chart_height
            chartType: ChartTypes.QChartJSTypes.BAR
            chartData: ChartsData.ChartBarData
            animation: true
            chartAnimationEasing: Easing.InOutElastic
            chartAnimationDuration: 2000
        }

        QChartJs {
            id: chart_doughnut
            width: chart_width
            height: chart_height
            chartType: ChartTypes.QChartJSTypes.DOUGHNUT
            chartData: ChartsData.ChartDoughnutData
            animation: true
            chartAnimationEasing: Easing.InOutElastic
            chartAnimationDuration: 2000
        }

        QChartJs {
            id: chart_pie
            width: chart_width
            height: chart_height
            chartType: ChartTypes.QChartJSTypes.PIE
            chartData: ChartsData.ChartPieData
            animation: true
            chartAnimationEasing: Easing.InOutElastic
            chartAnimationDuration: 2000
        }

        QChartJs {
            id: chart_polar
            width: chart_width
            height: chart_height
            chartType: ChartTypes.QChartJSTypes.POLARAREA
            chartData: ChartsData.ChartPolarData
            animation: true
            chartAnimationEasing: Easing.InOutElastic
            chartAnimationDuration: 2000
        }

        QChartJs {
            id: chart_radar
            width: chart_width
            height: chart_height
            chartType: ChartTypes.QChartJSTypes.RADAR
            chartData: ChartsData.ChartRadarData
            animation: true
            chartAnimationEasing: Easing.InOutElastic
            chartAnimationDuration: 2000
        }

        QChartJs {
            id: chart_stack_bar
            width: chart_width
            height: chart_height
            chartType: ChartTypes.QChartJSTypes.STACKED_BAR
            chartData: ChartsData.StackedBarData
            animation: true
            chartAnimationEasing: Easing.InOutElastic
            chartAnimationDuration: 2000
        }
    }
}
