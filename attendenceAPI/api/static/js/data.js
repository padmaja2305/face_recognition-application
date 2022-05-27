var data2, keys, values;
var csrf_token = document.getElementById("csrf_token").value;
var csrf_token_value = JSON.parse(csrf_token)["csrfmiddlewaretoken"];


function changedata() {
  //var data2 ,keys,values;
  var date = document.getElementById("start");

  var formdata = new FormData();
  formdata.append("month", date.value.split("-")[1]);
  formdata.append("year", date.value.split("-")[0]);
  formdata.append("csrfmiddlewaretoken", csrf_token_value);

  console.log(date.value);

  var requestOptions = {
    method: "POST",
    body: formdata,
    redirect: "follow",
  };

  fetch("/export", requestOptions)
    .then((response) => response.text())
    .then((result) => {
      data2 = JSON.parse(result);
      keys = data2["key1"];
      values = data2["value1"];
      console.log(keys, values);
      var options = {
        series: [
          {
            data: values,
          },
        ],
        chart: {
          type: "bar",
          height: 350,
        },
        plotOptions: {
          bar: {
            borderRadius: 4,
            horizontal: true,
          },
        },
        dataLabels: {
          enabled: false,
        },
        xaxis: {
          categories: keys,
        },
      };
      console.log(options);
      var chart = new ApexCharts(document.querySelector("#chart"), options);
      chart.render();
      console.log("done");
    })
    .catch((error) => console.log("error", error));
}

function download_csv_file() {
  var csv = data2.csv1;
  var csv2 = data2.csv2;
  var hiddenElement = document.createElement("a");
  hiddenElement.href = "data:text/csv;charset=utf-8," + encodeURI(csv);
  hiddenElement.target = "_blank";
  hiddenElement.download = "attendance.csv";
  hiddenElement.click();
}

changedata();

$("#datepicker").datepicker({
  format: "mm-yyyy",
  viewMode: "months",
  minViewMode: "months",
});


function getRequest(){
  var date = document.getElementById("start");
  var value = date.value;
  console.log(value);
  var formdata = new FormData();
  formdata.append("date", value);
  formdata.append("csrfmiddlewaretoken", csrf_token_value);

  var requestOptions = {
    method: 'POST',
    body: formdata,
    redirect: 'follow'
  };

  fetch("/data", requestOptions)
    .then(response => response.text())
    .then(result => {
      // console.log(result);
      document.open();
      document.write(result);
      document.close();
    })
    .catch(error => console.log('error', error));
}