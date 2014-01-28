'use strict';

angular.module('braind')
  .controller('StartCtrl', ['$scope', '$location', 'Restangular', 'brainstormingService', function ($scope, $location, Restangular, brainstormingService) {
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
        brainstormingService.setBrainstorming(brainstorming);
        $location.path('/' + brainstorming.slug + '/invite');
      });
    };
    $scope.reset();
  }]);
