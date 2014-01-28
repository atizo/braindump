'use strict';

angular.module('braind', [
    'ngCookies',
    'ngResource',
    'ngSanitize',
    'ngRoute',
    'ngAnimate',
    'restangular',
    'monospaced.elastic',
    'ngClipboard'
  ])
  .config(['$routeProvider', '$locationProvider', '$httpProvider', '$provide', 'ngClipProvider',
    function ($routeProvider, $locationProvider, $httpProvider, $provide, ngClipProvider) {
      $locationProvider.html5Mode(true);
      $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
      $httpProvider.defaults.xsrfCookieName = 'csrftoken';
      $routeProvider
        .when('/', {
          templateUrl: '/static/views/main.html',
          controller: 'StartCtrl'
        })
        .when('/:brainstorming/invite', {
          templateUrl: '/static/views/invite.html',
          controller: 'InviteCtrl'
        })
        .when('/:brainstorming', {
          templateUrl: '/static/views/brainstorming.html',
          controller: 'BrainstormingCtrl'
        })
        .otherwise({
          redirectTo: '/'
        });
      ngClipProvider.setPath('/static/bower_components/zeroclipboard/ZeroClipboard.swf');


      var brainstorming = angular.copy(window.brainstorming);
      $provide.constant('brainstorming', brainstorming);

    }]);
