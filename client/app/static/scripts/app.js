'use strict';

angular.module('braind', [
    'ngCookies',
    'ngResource',
    'ngSanitize',
    'ngRoute',
    'ngAnimate',
    'ngTouch',
    'restangular',
    'monospaced.elastic',
    'ui.bootstrap.modal',
    'ui.bootstrap.transition',
    'angularFileUpload',
    'bdDirectives',
    'bdFilters'
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
        .when('/glitch', {
          templateUrl: '/static/views/glitch.html',
          controller: 'GlitchCtrl'
        })
        .when('/:brainstorming/invite', {
          templateUrl: '/static/views/invite.html',
          controller: 'InviteCtrl'
        })
        .when('/:brainstorming/edit', {
          templateUrl: '/static/views/edit.html',
          controller: 'EditCtrl'
        })
        .when('/:brainstorming/notification', {
          templateUrl: '/static/views/notification.html',
          controller: 'NotificationCtrl'
        })
        .when('/:brainstorming', {
          templateUrl: '/static/views/brainstorming.html',
          controller: 'BrainstormingCtrl'
        })
        .otherwise({
          redirectTo: '/'
        });

      bdClipProvider.setPath('/static/bower_components/zeroclipboard/ZeroClipboard.swf');

      $provide.constant('brainstormingStore', angular.copy(window.brainstormingStore));
      $provide.constant('ideaStore', angular.copy(window.ideaStore));
      $provide.constant('recentBrainstormings', angular.copy(window.recentBrainstormings));
      $provide.constant('errorMsg', angular.copy(window.errorMsg));
      $provide.constant('infoMsg', angular.copy(window.infoMsg));
    }])

  .run(['$rootScope', '$location', 'errorMsg', function ($rootScope, $location, errorMsg) {

    if (errorMsg && errorMsg.length > 0) {
      $location.path('/glitch').replace();
    }

    $rootScope.user = {
      'email': angular.copy(window.email),
      'name': angular.copy(window.name)
    };

  }]);