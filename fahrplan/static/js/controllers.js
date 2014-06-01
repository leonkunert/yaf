'use strict';
angular.module('yaf.controllers', ['ngSanitize'])

.controller('rootCtrl', function($scope, $rootScope, userFactory) {
    $scope.statusSwitch = '<li><a href="/anmelden">Anmelden</a></li>';
    userFactory.status()
        .success(function (data) {
            console.log(data);
            if (data !== 'false') {
                $scope.statusSwitch = '<li><a href="/logout">Abmelden</a></li>';
                $scope.user = data;
                $scope.user.logedIn = true;
            }
        });
    $scope.logout = function () {
        userFactory.logout()
    }
})

.controller('mainCtrl', function($scope, $location, $rootScope, haltestellenFactory, userFactory) {
    $scope.query = {
        start_fahrzeit: moment().format('HH:mm')
    };
    $scope.timeFilter = function (zeit) {
        var date = moment().format('YYYY-MM-DD');
        var now  = moment(date + ' ' + $scope.query.start_fahrzeit);
        zeit     = moment(date + ' ' + zeit);
        return zeit.format('X') >= now.format('X');
    }
    haltestellenFactory.get_haltestellen()
        .success(function (data) {
            $scope.haltestellen = data;
        });
    $scope.fahrplanSuche = function (attr) {
        if (typeof attr.haltestelle === 'undefined') {
            console.log('No Haltestelle given setting default.');
            $scope.query.haltestelle = 'Bahnhof';
        }
        haltestellenFactory.get_fahrtzeiten(attr.haltestelle)
            .success(function (data) {
                console.log(data);
                $scope.fahrtzeiten = data;
            });
        haltestellenFactory.get_abfahrtszeiten(attr.haltestelle)
            .success(function (data) {
                console.log(data);
                $scope.abfahrtszeiten = data;
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