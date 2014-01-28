'use strict';

angular.module('braind')
  .controller('InviteCtrl', ['$scope', '$location', 'brainstormingService',
    function ($scope, $location, brainstormingService) {
      var brainstorming = brainstormingService.getBrainstorming();

      if (!brainstorming) {
        $location.path('/');
      }

      brainstorming.then(function (bs) {
        $scope.bs = bs;
      });

      $scope.hallo = function () {
        return 'sdfgsfdgs';
      };
    }]);
