'use strict';

angular.module('braind')
  .controller('StartCtrl', ['$scope', '$location', 'Restangular', function ($scope, $location, Restangular) {
    var brainstormings = Restangular.all('api/brainstormings/');

    $scope.reset = function () {
      $scope.bs = {
        question: '',
        creatorEmail: '',
        details: ''
      };
    };
    $scope.create = function () {
      brainstormings.post($scope.bs).then(function (brainstorming) {
        $location.path('/invite');
      });
    };
    $scope.reset();
  }]);
