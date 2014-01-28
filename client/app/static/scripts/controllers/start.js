'use strict';

angular.module('braind')
  .controller('StartCtrl', ['$scope', '$location', 'Restangular', 'brainstormingService', function ($scope, $location, Restangular, brainstormingService) {
    $scope.create = function () {
      brainstormingService.create($scope.formData).then(function (brainstorming) {
        $location.path('/' + brainstorming.slug + '/invite');
      });
    };

    $scope.reset = function () {
      $scope.formData = {
        question: '',
        creatorEmail: '',
        details: ''
      };
    };

    $scope.reset();
  }]);
