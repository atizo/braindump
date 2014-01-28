'use strict';

angular.module('braind')
  .controller('InviteCtrl', ['$scope', '$location', 'brainstormingService',
    function ($scope, $location, brainstormingService) {
      $scope.bs = brainstormingService.getBrainstorming();

      if (!$scope.bs) {
        $location.path('/');
      }

      $scope.hallo = function () {
        return 'sdfgsfdgs';
      };
    }]);
