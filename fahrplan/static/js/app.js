'use strict';
angular.module('yaf', [
    'yaf.controllers',
    'yaf.factories',
    'ngRoute'
])

.config(function ($locationProvider, $routeProvider) {
    $locationProvider.html5Mode(true);
    $routeProvider
        .when('/', {templateUrl: '/static/partials/index.html', controller: 'mainCtrl'})
        .when('/anmelden', {templateUrl: '/static/partials/login.html', controller: 'loginCtrl'})
        .when('/plan', {templateUrl: '/static/partials/plan.html', controller: 'planCtrl'})
        .otherwise({redirectTo: '/'});
});