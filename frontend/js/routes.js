App.config(function($routeProvider, $locationProvider){
    $routeProvider.when('/', {
        templateUrl:'views/main_page.html',
        controller:'mainController'
    })
    .when('/resizeImgRes', {
        templateUrl:'views/resize_image_result.html',
        controller:'resultController'
    })
    .when('/statusTask/:id', {
        templateUrl:'views/status_task_page.html',
        controller:'statusController'
    })

    $locationProvider.html5Mode(true);
    $locationProvider.hashPrefix('!');
});