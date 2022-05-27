var data ;
        var csrf_token = document.getElementById("csrf_token").value;
        var csrf_token_value = JSON.parse(csrf_token)['csrfmiddlewaretoken']
        
        var formdata = new FormData();
        formdata.append("month", "5");
        formdata.append("csrfmiddlewaretoken", csrf_token_value);
        
        var requestOptions = {
          method: 'POST',
          body: formdata,
          redirect: 'follow'
        };
        
        fetch("/export", requestOptions)
          .then(response => response.text())
          .then(result => {
            console.log(result);
            data = JSON.parse(result);
            
          })
        .catch(error => console.log('error', error));
  
  
        function download_csv_file() {
            var csv = data.csv1;
            var csv2 = data.csv2;
  
            var hiddenElement = document.createElement('a');  
            hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv);  
            hiddenElement.target = '_blank';  
            hiddenElement.download = 'attendance.csv';  
            hiddenElement.click();
          }