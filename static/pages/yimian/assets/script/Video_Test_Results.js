fetch('video_results')
    .then(response => response.json())
    .then(data => {
        // Do something with the retrieved data
        console.log(data);
        // data = [[
        //     ['机器学习和人工智能有什么关系?', '人工智能是一种使机器能够模仿人类行为的技术，而机器学习是人工智能的一个子集，它是通过向计算机提供数据并让它们在没有明确编程的情况下自己学习一些技巧来让计算机行动的科学', '人工智能是一种使机器能够模仿人类行为的技术，而机器学习是人工智能的一个子集', 0.3740838664528851],
        //     ['什么是人工智能?', '人工智能是计算机科学的一个领域，强调创造像人类一样工作和反应的智能机器', '人工智能是计算机科学的一个领域，强调创造像人类一样工作和反应的智能机器', 0.98476526],
        //     ['博弈论和ai有何关联?', '在人工智能和深度学习系统的背景下，博弈论对于实现多智能体环境中所需的一些关键功能至关重要，在多智能体环境中，不同的人工智能程序需要相互作用或竞争以实现目标', '在人工智能和深度学习系统的背景下，博弈论对于实现多智能体环境中所需的一些关键功能至关重要', 0.5738752377837661],
        //     ['建立贝叶斯模型需要多少项?', '在人工智能中建立贝叶斯模型需要三个条件，即一个条件概率和两个无条件概率', '在人工智能中建立贝叶斯模型需要三个条件，即一个条件概率和两个无条件概率', 0.87967556388],
        //     ['哪个算法反转了一个完整的分辨率策略?', '逆分辨率与完全分辨率相反，因为它是学习一阶理论的完整算法', '逆分辨率与完全分辨率相反，因为它是学习一阶理论的完整算法', 0.97666571],
        //     ['在HMM中，附加变量是在哪里添加的?', '在HMM网络中，可以将额外的状态变量添加到时间模型中', '在HMM网络中，可以将额外的状态变量添加到时间模型中', 0.987544678],
        //     ['什么是模糊逻辑实现?', '基本上，它可以在各种大小和功能的系统中实现，从小型微控制器到大型微控制器，它也可以在硬件软件中实现，或者在人工智能中两者的组合', '基本上，它可以在各种大小和功能的系统中实现，从小型微控制器到大型微控制器', 0.7865675768],
        //     ['在图像处理中，无限差分滤波器非常容易受到噪声的影响，为了解决这个问题，你可以使用哪种方法来使噪声造成的失真最小?', '图像平滑是用来减少噪声的最好方法之一，通过强迫像素更像它们的邻居，这减少了由对比度引起的任何扭曲', '图像平滑是用来减少噪声的最好方法之一，通过强迫像素更像它们的邻居，这减少了由对比度引起的任何扭曲', 0.989765774],
        //     ['什么是混淆矩阵它是如何工作的?', '混淆矩阵是一种通常用来衡量算法性能的特定表，它主要用于监督学习和非监督学习，它被称为匹配矩阵，它有两个参数，实际和预测', '混淆矩阵是一种通常用来衡量算法性能的特定表，它主要用于监督学习和非监督学习，它被称为匹配矩阵，它有两个参数，实际和预测', 0.970988779],
        //     ['解释强人工智能和弱人工智能的区别?', '强人工智能强烈声称计算机可以在与人类相同的水平上思考，而弱人工智能只是预测一些类似于人类智能的特征可以被纳入计算机，使其成为更有用的工具', '强人工智能强烈声称计算机可以在与人类相同的水平上思考，而弱人工智能只是预测一些类似于人类智能的特征可以被纳入计算机，使其成为更有用的工具', 0.8779889068585]
        // ], [10, 20, 30, 40, 50, 60, 70, 80]];
        // var ctx = document.getElementById("myChart");
        // var data2 = [10, 20, 30, 40, 50, 60, 70, 80];
        var myChart = echarts.init(document.getElementById("myChart"));
        var option = {
            title: {
                text: "情绪分析"
            },
            legend: {
                show: true,
                bottom: '0'
            },
            grid: {
                top: "10%",
                left: "10%",
                right: "10%",
                bottom: "10%"
            },
            tooltip: { // 鼠标悬浮提示框显示 X和Y 轴数据
                trigger: 'item',
                axisPointer: {
                    type: 'shadow'
                }
            },
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
            series: [
                {
                    // name: '',
                    // type: 'pie',
                    // radius: [50, 250],
                    // center: ['50%', '50%'],
                    // roseType: 'area',
                    // itemStyle: {
                    //     borderRadius: 8
                    // },
                    name: '',
                    type: 'pie',
                    radius: ['40%', '70%'],
                    avoidLabelOverlap: false,
                    itemStyle: {
                        borderRadius: 10,
                        borderColor: '#fff',
                        borderWidth: 2
                    },
                    label: {
                        show: false,
                        position: 'center'
                    },
                    emphasis: {
                        label: {
                            show: true,
                            fontSize: 40,
                            fontWeight: 'bold'
                        }
                    },
                    labelLine: {
                        show: false
                    },
                    data: [
                        {value: data[1][0], name: '愤怒'},
                        {value: data[1][1], name: '局促'},
                        {value: data[1][2], name: '害怕'},
                        {value: data[1][3], name: '高兴'},
                        {value: data[1][4], name: '悲伤'},
                        {value: data[1][5], name: '惊讶'},
                        {value: data[1][6], name: '中立'},
                        {value: data[1][7], name: '无表情'}
                    ]
                }
            ]
        }
        myChart.setOption(option);
        var myChart2 = echarts.init(document.getElementById("myChart2"));
        xAxisData = []
        seriesData = []
        for (var i = 0; i < data[0].length; i++) {
            xAxisData.push('第' + (i + 1) + '题');
            seriesData.push(data[0][i][3]);
        }
        var option2 = {
            title: {
                text: "答案相似度"
            },
            grid: {
                top: "10%",
                left: "10%",
                right: "10%",
                bottom: "10%"
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
        // Get the container div element
        var tableContainer = document.getElementById("myTable");

        // Create a table element
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
        for (var i = 0; i < data[0].length; i++) {
            var tbody_row_tr = document.createElement("tr");
            for (var j = 0; j < data[0][i].length; j++) {
                var cell = document.createElement("td");
                var cellText = '';
                if (j == 3) {
                    var similarity = parseFloat(data[0][i][j]);
                    var similarityPercentage = (similarity * 100).toFixed(2) + '%';
                    cellText = document.createTextNode(similarityPercentage);
                } else {
                    cellText = document.createTextNode(data[0][i][j]);
                }
                cell.appendChild(cellText);
                tbody_row_tr.appendChild(cell);
            }
            tbody.appendChild(tbody_row_tr);
        }
        table.appendChild(tbody)
        // Append the table to the container div element
        tableContainer.appendChild(table);
    })
    .catch(error => console.error(error));