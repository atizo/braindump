'use strict';

angular.module('braind')
  .controller('InviteCtrl', ['$scope', '$rootScope', '$location', 'brainstormingService',
    function ($scope, $rootScope, $location, brainstormingService) {
      var brainstorming = brainstormingService.getBrainstorming();

      if (!brainstorming) {
        $location.path('/');
      }

      brainstorming.then(function (bs) {
        $scope.bs = bs;

        $scope.subject = window.encodeURIComponent($scope.bs.question);
        $scope.body = window.encodeURIComponent('I would like to invite you to the brainstorming "' + $scope.bs.question +'"\nPlease follow the link in order to participate in the poll:');

      });


      $scope.getLink = function () {
        return $scope.bs.url;
      };
    }]);
