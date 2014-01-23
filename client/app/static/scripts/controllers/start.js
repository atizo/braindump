'use strict';

angular.module('braind')
  .controller('StartCtrl', ['$scope', 'Restangular', function ($scope, Restangular) {
    var brainstormings = Restangular.all('api/brainstormings/');
    $scope.bs = {};
    $scope.create = function () {
      console.info($scope.bs);
      brainstormings.post($scope.bs);
    };
  }]);
