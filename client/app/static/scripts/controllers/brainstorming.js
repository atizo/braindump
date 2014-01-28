'use strict';

angular.module('braind')
  .controller('BrainstormingCtrl', ['$scope', 'brainstormingService', function ($scope, brainstormingService) {
    brainstormingService.getBrainstorming().then(function (obj) {
      $scope.brainstorming = obj;
    });
    brainstormingService.getIdeas().then(function(obj) {
      $scope.ideas = obj;
    });

    $scope.create = function () {
      brainstormingService.createIdea($scope.formData);
      $scope.reset();
      $scope.fullform = false;
    };

    $scope.reset = function () {
      $scope.formData = {
        title: '',
        text: ''
      };
    };

    $scope.reset();
  }]);
