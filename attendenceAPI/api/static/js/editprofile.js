function updateProfile(){
    var name = document.getElementById("input_name").value;
    var lastname = document.getElementById("input_lastname").value;
    var mobilenum = document.getElementById("input_mobilenum").value;
    var address = document.getElementById("input_address").value;
    var pincode = document.getElementById("input_pincode").value;
    var fileInput = document.getElementById('input_file') 
    var class_sec = document.getElementById("input_class").value;

    var csrf_token = document.getElementById("csrf_token").value;
    var csrf_token_value = JSON.parse(csrf_token)['csrfmiddlewaretoken']
    
    var formdata = new FormData();
    formdata.append("name", name);
    formdata.append("phone", mobilenum);
    formdata.append("last_name", lastname);
    formdata.append("pin", pincode);
    formdata.append("address", address);
    formdata.append("class_sec", class_sec);
    formdata.append("csrfmiddlewaretoken", csrf_token_value);

    if (fileInput.files.length == 1 ){
        formdata.append("profile_img", fileInput.files[0], fileInput.files[0].name );
    }

    var requestOptions = {
    method: 'POST',
    body: formdata,
    redirect: 'follow'
    };

    fetch("/editprofile", requestOptions)
    .then(response => response.text())
    .then(result => {
        console.log(result);
        alert("Profile Updated Successfully");
        window.location.href = "/profile";
    })
    .catch(error => console.log('error', error));
}