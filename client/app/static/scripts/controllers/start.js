'use strict';

angular.module('braind')
  .controller('StartCtrl', ['$scope', 'Restangular', function ($scope, Restangular) {
    var brainstormings = Restangular.all('api/brainstormings/');

    $scope.reset = function () {
      $scope.bs = {
        question: '',
        creatorEmail: '',
        details: ''
      };
    };
    $scope.create = function () {
      brainstormings.post($scope.bs);
    };
    $scope.reset();
  }]);
