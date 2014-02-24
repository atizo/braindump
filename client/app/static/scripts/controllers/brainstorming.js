'use strict';

angular.module('braind')
  .controller('BrainstormingCtrl', ['$scope', '$routeParams', '$location', '$modal', 'brainstormingService', 'bdDate',
    function ($scope, $routeParams, $location, $modal, brainstormingService, bdDate) {

      var bsid = $routeParams.brainstorming;

      brainstormingService.get(bsid).then(function (obj) {
        obj.createdFormatted = bdDate.format(obj.created);
        $scope.brainstorming = obj;
      }, function () {
        $location.path('/').replace();
      });
      brainstormingService.getIdeas(bsid).then(function (obj) {
        $scope.ideas = obj;
      });

      $scope.create = function () {
        brainstormingService.postIdea(bsid, $scope.formData).then(function () {
          $scope.user.name = $scope.formData.creatorName;
          $scope.reset();
          $scope.fullform = false;
        });
      };

      $scope.openDetail = function (idea) {
        var modalScope = $scope.$new();
        modalScope.idea = idea;
        $modal.open({
          templateUrl: '/static/views/idea-modal.html',
          controller: 'IdeaDetailCtrl',
          scope: modalScope
        });
      };

      $scope.toolBar = [
        {href: '/' + bsid + '/notification', class: 'star'},
        {href: '/' + bsid + '/edit', class: 'edit'}
      ];

      $scope.reset = function () {
        $scope.formData = {
          title: '',
          text: '',
          creatorName: $scope.user.name
        };
      };

      $scope.reset();
    }])
  .controller('IdeaDetailCtrl', ['$scope', '$modalInstance', '$window', '$timeout', 'brainstormingService',
    function ($scope, $modalInstance, $window, $timeout, brainstormingService) {
      $scope.editMode = false;

      $scope.close = function () {
        $modalInstance.close();
      };

      $scope.rate = function () {
        brainstormingService.rateIdea($scope.idea.brainstorming, $scope.idea.id);
      };

      $scope.delete = function () {
        if ($window.confirm('Do you really want to delete this idea?')) {
          brainstormingService.deleteIdea($scope.idea.brainstorming, $scope.idea.id);
          $modalInstance.close();
        }
      };

      $scope.startEdit = function () {
        var doc = angular.element($window.document);

        $scope.formData = _.clone($scope.idea);
        $scope.editMode = true;

        // select first field with content, after digest loop is finished
        $timeout(function () {
          if ($scope.formData.title) {
            doc.find('.modal form .title').focus();
          } else if ($scope.formData.text) {
            doc.find('.modal form .text').focus();
          }
        }, 0);
      };

      $scope.cancelEdit = function () {
        $scope.editMode = false;
      };

      $scope.saveEdit = function () {
        brainstormingService.updateIdea($scope.idea.brainstorming, $scope.idea.id, $scope.formData).then(function () {
          $scope.user.name = $scope.formData.creatorName;
          $scope.editMode = false;
        });
      };
    }]);
