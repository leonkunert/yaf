'use strict';
angular.module('yaf.controllers', [])

.controller('rootCtrl', function($scope, $rootScope, userFactory) {
    $rootScope.statusSwitch = '<li><a href="/anmelden">Anmelden <i class="fa fa-fw fa-sign-in fa-lg"></i></a></li>';
    userFactory.status()
        .success(function (data) {
            console.log(data);
            if (data !== 'false') {
                $rootScope.statusSwitch = '<li class="active"><a>Hallo '+data.username+'</a></li><li><a href="/plan">Dienstplan <i class="fa fa-fw fa-briefcase fa-lg"></i></a></li><li><a href="#" title="Abmelden">Abmelden <i class="fa fa-fw fa-sign-out fa-lg"></i></a></li>';
                $rootScope.user = data;
                $rootScope.user.logedIn = true;
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
        var now  = moment(date + ' ' + $scope.query.start_fahrzeit, 'YYYY-MM-DD hh:mm');
        zeit     = moment(date + ' ' + zeit, 'YYYY-MM-DD hh:mm');
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

.controller('loginCtrl', function($scope, $rootScope, $location, userFactory) {
    if (typeof $rootScope.user !== 'undefined') {
        $location.path('/plan')
    }
    $scope.login = function () {
        userFactory.login($scope.user)
            .success(function (data) {
                if (data !== 'false') {
                    $rootScope.user = data;
                    $rootScope.statusSwitch = '<li class="active"><a>Hallo '+data.username+'</a></li><li><a href="/plan">Dienstplan <i class="fa fa-fw fa-briefcase fa-lg"></i></a></li><li><a href="#" title="Abmelden">Abmelden <i class="fa fa-fw fa-sign-out fa-lg"></i></a></li>';
                    $location.path('/plan');
                }
            })
    };
})

.controller('planCtrl', function($scope, $rootScope, $location, userFactory) {
    if (typeof $rootScope.user === 'undefined') {
        $location.path('/anmelden')
    }
    userFactory.get_dienstplan()
        .success(function (data) {
            $scope.dienstplan = data;
            console.log(data);
        })
    $scope.message = 'Hallo';
});