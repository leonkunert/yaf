'use strict';
angular.module('yaf.controllers', [])

.controller('main', function($scope, fahrplanFactory, haltestellenFactory) {
    $scope.start_fahrzeit = new Date(0,0,0,13,37,0,0).toLocaleTimeString();
    haltestellenFactory.autocomplte('')
        .success(function (data) {
            console.log(data);
        });
});