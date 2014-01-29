'use strict';

angular.module('braind', [
    'ngCookies',
    'ngResource',
    'ngSanitize',
    'ngRoute',
    'ngAnimate',
    'restangular',
    'monospaced.elastic',
    'bdDirectives'
  ])
  .config(['$routeProvider', '$locationProvider', '$httpProvider', '$provide', 'bdClipProvider',
    function ($routeProvider, $locationProvider, $httpProvider, $provide, bdClipProvider) {
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

      bdClipProvider.setPath('/static/bower_components/zeroclipboard/ZeroClipboard.swf');

      var brainstorming = angular.copy(window.initialBrainstorming);
      $provide.constant('initialBrainstorming', brainstorming);

      var ideas = angular.copy(window.initialIdeas);
      $provide.constant('initialIdeas', ideas);
    }]);
