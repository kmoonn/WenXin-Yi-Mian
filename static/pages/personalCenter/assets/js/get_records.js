fetch('Get_Results')
    .then(response => response.json())
    .then(data => {
        console.log(data);
        data.sort(function (a, b){
            var dateA = new Date(a[2])
            var dateB = new Date(b[2])
            return dateB - dateA;
        });
        var table = document.getElementById("myTable");
        // Create the table headings row
        var thead = document.createElement("thead");
        var thead_tr = document.createElement("tr");

        for (let i = 0; i < 4; i++) {
            var heading = document.createElement("th");
            if (i == 0) {
                var headingText = document.createTextNode("编号");
                heading.appendChild(headingText);
                thead_tr.appendChild(heading);
            }
            if (i == 1) {
                var headingText = document.createTextNode("类别");
                heading.appendChild(headingText);
                thead_tr.appendChild(heading);
            }
            if (i == 2) {
                var headingText = document.createTextNode("时间");
                heading.appendChild(headingText);
                thead_tr.appendChild(heading);
            }
            if (i == 3) {
                var headingText = document.createTextNode("回顾");
                // headingText = (headingText * 100).toFixed(2) + '%'
                heading.appendChild(headingText);
                thead_tr.appendChild(heading);
            }
        }
        thead.appendChild(thead_tr)
        table.appendChild(thead);

        var tbody = document.createElement("tbody");
        for (var i = 0; i < data.length; i++) {
            var tbody_row_tr = document.createElement("tr");
            for (var j = 0; j < 4; j++) {
                var cell = document.createElement("td");
                var cellText = '';
                if (j == 0) {
                    cellText = (i+1).toString();
                    cell.appendChild(document.createTextNode(cellText));
                } else if (j == 3) {
                    var myHref = document.createElement('a');
                    myHref.id = data[i][0].toString()
                    if (data[i][1] == '模拟笔试'){
                        myHref.href = "Text_Test_Result_Record/"+data[i][0].toString()
                    }else {
                        myHref.href = "Video_Test_Result_Record/"+data[i][0].toString()
                    }
                    myHref.appendChild(document.createTextNode('查看'))
                    cell.appendChild(myHref)
                } else {
                    cellText = data[i][j]
                    cell.appendChild(document.createTextNode(cellText));
                }
                tbody_row_tr.appendChild(cell);
            }
            tbody.appendChild(tbody_row_tr)
        }
        table.appendChild(tbody)
    })
    .catch(error => console.error(error));