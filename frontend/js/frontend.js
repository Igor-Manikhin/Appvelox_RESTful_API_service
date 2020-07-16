let App = angular.module("AppveloxFrontApp", ["ngRoute"]);

App.service("resizeOperationData", function(){

    let data;

    this.setData= function(response_data){
        data = response_data;
    }

    this.getData = function(){
        return data;
    }
})

App.controller("mainController", function($location, $scope, $http, resizeOperationData){

    let data = {};
    let image_url;

    $scope.input_check_validator = function(event){
        target = event.target;
        switch(event.type){
            case 'click':
                if(target.value != ""){
                    radio_buttons = document.getElementsByClassName("form-check-input")
                    for(let i = 0; i < radio_buttons.length; i++){
                        radio_buttons[i].classList.remove("is-invalid");
                    }
                    let messages_block = document.querySelector('.save_format');
                    messages_block.innerHTML = "";
                }
            case 'keyup':
                if(target.value != ""){
                    target.classList.remove('is-invalid');
                }
        }
    }

    $scope.image_loader = function(input){
        let image = document.querySelector('#load_image');
        let file = input.files[0];

        if (file != undefined){
            file_field = document.querySelector('#image');
            file_field.classList.remove("is-invalid");

            let fileReader = new FileReader();

            fileReader.readAsDataURL(file)

            fileReader.onload = function(){
                image_url = fileReader.result;
                image.src = fileReader.result;
            }

            fileReader.onerror = function () {
                console.log(fileReader.error);
            }
        }
    }

    $scope.submit = function () {
        
        if ($scope.height == null && $scope.width == null){
            delete $scope.height;
            delete $scope.width;
        }

        data.image = image_url;
        data.image_size = {h: $scope.height, w: $scope.width};
        data.save_format = $scope.format;

        $http.post('http://127.0.0.1:8000/api/v1/resizeImage', data).then(function(res){
            resizeOperationData.setData(res.data);
            localStorage.removeItem('task_result');

            $location.path('/resizeImgRes');
        }, function(res){
            let result = res.data;

            for (let key of Object.keys(res.data)){
                if (key == 'save_format'){
                    radio_buttons = document.getElementsByClassName("form-check-input")
                    for(let i = 0; i < radio_buttons.length; i++){
                        radio_buttons[i].classList.add("is-invalid");
                    }    
                }
                let field = document.querySelector('#'+key);
                let messages_block = document.querySelector('.'+key);
                field.classList.add("is-invalid");
                messages_block.innerHTML = res.data[key];
            }
        });
    }
})

App.controller('resultController', function($scope, $timeout, resizeOperationData){
    time_expect_view = document.querySelector('.timer_view'); 
    link_view = document.querySelector('.result_view');

    $scope.onTimeout = function(){
        if ($scope.counter != 0){
            $scope.counter--;
            mytimeout = $timeout($scope.onTimeout,1000);
        }
        else{
            $timeout.cancel(mytimeout);
            localStorage.setItem('task_result', JSON.stringify(data));

            $scope.result_url = data['result_url'];
            $scope.download_url = data['download_url'];

            time_expect_view.classList.add("d-none");
            link_view.classList.remove("d-none");
        }
    }

    if (localStorage.getItem('task_result') != null){
        localstorage_data = JSON.parse(localStorage.getItem('task_result'));

        $scope.result_url = localstorage_data['result_url'];
        $scope.download_url = localstorage_data['download_url'];
        
        time_expect_view.classList.add("d-none");
        link_view.classList.remove("d-none");
    }
    else{
        data = resizeOperationData.getData();
        $scope.task_id = data['task_id'];
        $scope.counter = 80;
        $timeout($scope.onTimeout,1000);
    }

})

App.controller('statusController', function($scope, $http, $routeParams){
    
    $http.get('http://127.0.0.1:8000/api/v1/statusImage/' + $routeParams.id).then(function(res){
        data = res.data;

        $scope.status = data.status;
        $scope.description = data.status_info.description;

        if (typeof data.status_info.Performed !== "undefined") {
            performed_field = document.querySelector('#performed');
            performed_field.classList.remove('d-none');
            $scope.performed = data.status_info.Performed;
        }

        if (typeof data.status_info.time_spent !== "undefined") {
            time_field = document.querySelector('#time');
            time_field.classList.remove('d-none');
            $scope.time_spent = data.status_info.time_spent;
        }
    }, function(res){
        task_info_block = document.querySelector('#task_info');
        task_info_block.classList.add('d-none');

        if(res.data == '400 BAD REQUEST'){
            bad_request_message = document.querySelector('#bad_request_message');
            bad_request_message.classList.remove('d-none');
        }
        else{
            not_found_message = document.querySelector('#not_found_message');
            not_found_message.classList.remove('d-none');
        }
    })
})