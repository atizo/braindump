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

      $scope.getIdeaSizeClassName = function (idea) {
        var l = idea.title.length + idea.text.length;
        if (l <= 25) {
          return 'length-25';
        }
        if (l <= 50) {
          return 'length-50';
        }
        if (l <= 150) {
          return 'length-150';
        }
        if (l <= 300) {
          return 'length-300';
        }
        return '';
      };

      $scope.create = function () {
        brainstormingService.createIdea($scope.formData).then(function () {
          $scope.user.name = $scope.formData.creatorName;
          $scope.reset();
          $scope.fullform = false;
        });
      };

      $scope.reset = function () {
        $scope.formData = {
          title: '',
          text: '',
          creatorName: $scope.user.name
        };
      };

      $scope.reset();
    }]);
