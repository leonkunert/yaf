'use strict';
angular.module('yaf.controllers', [])

.controller('rootCtrl', function($scope, $rootScope, userFactory) {
    userFactory.status()
        .success(function (data) {
            if (data !== 'false') {
                $rootScope.user = data;
                $rootScope.user.logedIn = true;
            }
        });
})

.controller('mainCtrl', function($scope, $location, $rootScope, haltestellenFactory, userFactory) {
    $scope.query = {
        start_fahrzeit: moment().format('HH:mm')
    };
    haltestellenFactory.get_haltestellen()
        .success(function (data) {
            $scope.haltestellen = data;
        });
    $scope.logout = function () {
        userFactory.logout()
    }
    $scope.fahrplanSuche = function (attr) {
        console.log(attr);
        haltestellenFactory.get_fahrtzeiten(attr.haltestelle)
            .success(function (data) {
                console.log(data);
                $scope.result = data;
            });
    }
})

.controller('loginCtrl', function($scope, $location, userFactory) {
    $scope.login = function () {
        userFactory.login($scope.user)
            .success(function (data) {
                if (data === 'true') {
                    $location.path('/plan');
                }
            })
    };
})

.controller('planCtrl', function($scope, $rootScope, $location, userFactory) {
    if (typeof $rootScope.user === 'undefined') {
        $location.path('/anmelden')
    }
    $scope.message = 'hi';
});