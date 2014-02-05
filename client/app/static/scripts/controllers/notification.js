'use strict';

angular.module('braind')
  .controller('NotificationCtrl', ['$scope', '$rootScope', '$location', '$routeParams', 'brainstormingService',
    function ($scope, $rootScope, $location, $routeParams, brainstormingService) {
      var brainstorming = brainstormingService.get($routeParams.brainstorming);

      brainstorming.then(function (bs) {
        $scope.bs = bs;

        $scope.subject = window.encodeURIComponent($scope.bs.question);
        $scope.body = window.encodeURIComponent('I would like to invite you to the brainstorming "' +
          $scope.bs.question +
          '"\n\nPlease follow the link in order to participate in the brainstorming:\n' +
          $scope.bs.url
        );

      }, function () {
        $location.path('/').replace();
      });

      $scope.getLink = function () {
        return $scope.bs.url;
      };
    }]);
