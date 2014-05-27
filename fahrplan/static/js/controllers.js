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

.controller('mainCtrl', function($scope, $location, $rootScope, fahrplanFactory, haltestellenFactory, userFactory) {
    $scope.start_fahrzeit = moment().format('hh:mm');
    haltestellenFactory.get_haltestellen()
        .success(function (data) {
            $scope.haltestellen = data;
        });
    $scope.logout = function () {
        userFactory.logout()
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