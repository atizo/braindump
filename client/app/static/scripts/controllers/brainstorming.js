'use strict';

angular.module('braind')
  .controller('BrainstormingCtrl', ['$scope', 'brainstormingService', 'bdDate',
    function ($scope, brainstormingService, bdDate) {
      brainstormingService.getBrainstorming().then(function (obj) {
        obj.createdFormatted = bdDate.format(obj.created);
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
          text: '',
          creatorName: ''
        };
      };

      $scope.reset();
    }]);
