var input1 = document.getElementById("input1");
        var input2 = document.getElementById("input2");
        var input3 = document.getElementById("input3");
        var input6 = document.getElementById("input6");
        var csrf_token = document.getElementById("csrf_token").value;
        var csrf_token_value = JSON.parse(csrf_token)['csrfmiddlewaretoken']
        
        function ValidateEmail(mail) 
            {
                if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(mail))
            {
                return (true)
            }
                alert("You have entered an invalid email address!")
                return (false)
            }

        function submitform1(){
            if (input3.value != input2.value){
                console.log(input1.value)
                alert("Password not match");
                return false;
            }
            else if (ValidateEmail(input1.value) == false){
                return false
            }
            else {
                var formdata = new FormData();
                formdata.append("username", input1.value);
                formdata.append("password", input2.value);
                formdata.append("name", input6.value);
                formdata.append("csrfmiddlewaretoken", csrf_token_value);
                var requestOptions = {
                    method: 'POST',
                    body: formdata,
                    redirect: 'follow'
                  };
                  fetch("/signup", requestOptions)
                  .then(response => response.text())
                  .then(result => {
                    if (result == "{\"message\": \"User created\"}"){
                        console.log("matched");
                        alert("Sign up successful!");
                        //window.location.href = "http://127.0.0.1:8000";
                    }
                    else if (result == "{\"message\": \"User already exists\"}"){
                        alert("User already exists");
                    }
                    else{
                        alert("Username or Password is incorrect");
                    }
                  })
                  .catch(error => console.log('error', error));
            }
        }

        function submitLoginForm(){
            var input4 = document.getElementById("input4");
            var input5 = document.getElementById("input5");
            var csrf_token_2 = document.getElementById("csrf_token_2").value;
            var csrf_token_value_2 = JSON.parse(csrf_token_2)['csrfmiddlewaretoken']

            var formdata = new FormData();
            formdata.append("username", input4.value);
            formdata.append("password", input5.value);
            formdata.append("csrfmiddlewaretoken", csrf_token_value_2);

            var requestOptions = {
            method: 'POST',
            body: formdata,
            redirect: 'follow'
            };

            fetch("/login", requestOptions)
            .then(response => response.text())
            .then(result => {
                console.log(result)
                if (result == "{\"message\": \"User logged in\"}"){
                    console.log("matched");
                    window.location.href = "/";
                }
                else{
                    alert("Username or Password is incorrect");
                }
            })
            .catch(error => console.log('error', error));
        }
