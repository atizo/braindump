'use strict';

angular.module('braind')
  .controller('BrainstormingCtrl', ['$scope', 'brainstormingService', function ($scope, brainstormingService) {
    $scope.brainstorming = brainstormingService.getBrainstorming();
    $scope.ideas = brainstormingService.getIdeas();

    $scope.create = function () {

    };

    $scope.reset = function () {
      $scope.formData = {
        title: '',
        text: ''
      };
    };

    $scope.reset();
  }]);
