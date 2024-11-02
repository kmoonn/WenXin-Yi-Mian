// fetch('Text_Record_Results')
//     .then(response => response.json())
//     .then(data => {
data = text_result_data
console.log(data);
var myChart2 = echarts.init(document.getElementById("myChart2"));
xAxisData = []
seriesData = []
for (var i = 0; i < data.length; i++) {
    xAxisData.push('第' + (i + 1) + '题');
    seriesData.push(data[i][3]);
}
var option2 = {
    title: {
        text: "答案相似度"
    },
    xAxis: {
        type: 'category',
        data: xAxisData
    },
    yAxis: {
        type: 'value'
    },
    series: [
        {
            data: seriesData,
            type: 'line',
            smooth: true
        }
    ],
    toolbox: {
        show: true,
        feature: {
            mark: {show: true},
            dataView: {
                show: true,
                readOnly: true,
                title: "数据显示"
            },
            saveAsImage: {
                show: true,
                title: "保存"
            }
        }
    },
    tooltip: { // 鼠标悬浮提示框显示 X和Y 轴数据
        trigger: 'axis',
        backgroundColor: 'rgba(32, 33, 36,.7)',
        borderColor: 'rgba(32, 33, 36,0.20)',
        borderWidth: 1,
        textStyle: { // 文字提示样式
            color: '#fff',
            fontSize: '12'
        },
        axisPointer: { // 坐标轴虚线
            type: 'cross',
            label: {
                backgroundColor: '#6a7985'
            }
        }
    }
}
myChart2.setOption(option2)
var tableContainer = document.getElementById("myTable");
// 创建一个table元素
var table = document.createElement("table");

table.className = 'table table-hover'

// Create the table headings row
var thead = document.createElement("thead");
var thead_tr = document.createElement("tr");

// headingsRow.appendChild(blankHeading); // add blank cell to top left corner
for (var i = 0; i < 4; i++) {
    var heading = document.createElement("th");
    if (i == 0) {
        var headingText = document.createTextNode("问题");
        heading.appendChild(headingText);
        thead_tr.appendChild(heading);
    }
    if (i == 1) {
        var headingText = document.createTextNode("参考答案");
        heading.appendChild(headingText);
        thead_tr.appendChild(heading);
    }
    if (i == 2) {
        var headingText = document.createTextNode("你的答案");
        heading.appendChild(headingText);
        thead_tr.appendChild(heading);
    }
    if (i == 3) {
        var headingText = document.createTextNode("相似度");
        // headingText = (headingText * 100).toFixed(2) + '%'
        heading.appendChild(headingText);
        thead_tr.appendChild(heading);
    }
}
thead.appendChild(thead_tr)
table.appendChild(thead);

var tbody = document.createElement("tbody");
// Loop through the arrays and create table rows and cells
for (var i = 0; i < data.length; i++) {
    var tbody_row_tr = document.createElement("tr");
    for (var j = 0; j < 4; j++) {
        var cell = document.createElement("td");
        var cellText = '';
        if (j == 3) {
            var similarity = parseFloat(data[i][j]);
            var similarityPercentage = (similarity * 100).toFixed(2) + '%';
            cellText = document.createTextNode(similarityPercentage);
        } else {
            cellText = document.createTextNode(data[i][j]);
        }
        cell.appendChild(cellText);
        tbody_row_tr.appendChild(cell)
    }
    // console.log("newrow")
    tbody.appendChild(tbody_row_tr);
}
table.appendChild(tbody)
// Append the table to the container div element
tableContainer.appendChild(table);
wait.style.visibility = 'hidden'
// })
// .catch(error => console.error(error));