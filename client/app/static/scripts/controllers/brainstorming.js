'use strict';

angular.module('braind')
  .controller('BrainstormingCtrl', ['$scope', 'brainstormingService', function ($scope, brainstormingService) {
    console.info(brainstormingService.getBrainstorming());
    $scope.bs = {};
  }]);
