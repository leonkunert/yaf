'use strict';
angular.module('yaf.controllers', [])

.controller('main', function($scope, $location, $rootScope, fahrplanFactory, haltestellenFactory, userFactory) {
    $scope.start_fahrzeit = new Date(0,0,0,13,37,0,0).toLocaleTimeString();
    haltestellenFactory.get_haltestellen()
        .success(function (data) {
            $scope.haltestellen = data;
            console.log(data);
        });
    $scope.login = function () {
        userFactory.login($scope.user)
            .success(function (data) {
                if (data.success === true) {
                    $location.path("/");
                }
            });
    };
    $scope.logout = function () {
        userFactory.logout()
            .success(function (data) {
                if (data.success === true) {
                    $location.path('/');
                }
            });
    }
});