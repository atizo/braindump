'use strict';

angular.module('braind')
  .controller('BrainstormingCtrl', ['$scope', '$routeParams', '$location', '$rootScope', '$upload', 'brainstormingService', 'bdDate',
    function ($scope, $routeParams, $location, $rootScope, $upload, brainstormingService, bdDate) {

      var bsid = $routeParams.brainstorming;
      $scope.file = null;

      brainstormingService.get(bsid).then(function (obj) {
        obj.createdFormatted = bdDate.format(obj.created);
        $scope.brainstorming = obj;
      }, function () {
        $location.path('/').replace();
      });

      brainstormingService.getIdeas(bsid).then(function (ideas) {
        $scope.ideasRaw = ideas;
      });

      $scope.$watchCollection('ideasRaw', function (ideas) {
        ideas = _.toArray(ideas);
        _.each(ideas, function (idea) {
          idea.createdDate = idea.created ? new Date(idea.created) : 0;
        });
        $scope.ideas = _.sortBy(ideas, function (o) {
          return -o.createdDate;
        });
      });

      $scope.create = function () {
        $scope.loading = true;
        brainstormingService.postIdea(bsid, $scope.formData, $scope.file).then(function () {
          $scope.user.name = $scope.formData.creatorName;
          $scope.reset();
          $scope.fullform = false;
        })['finally'](function () {
          $scope.loading = false;
        });
      };

      $scope.formCancel = function () {
        $scope.fullform = false;
        $scope.reset();
      };

      $scope.openDetail = function (evt) {
        var ss = angular.element(evt.target).closest('div.bd-idea').attr('iid');
        brainstormingService.getIdea(bsid, ss).then(function (idea) {
          $rootScope.$broadcast('bd:mopen', idea);
        });
      };

      $scope.toolBar = [
        {href: '/' + bsid + '/export', 'class': 'icon-download', title: 'Export', target: '_self'},
        {href: '/' + bsid + '/notification', 'class': 'icon-star', title: 'Notifcations'}
      ];

      $scope.editLink = '/' + bsid + '/edit';

      $scope.reset = function () {
        $scope.file = null;
        $scope.formData = {
          image: '',
          title: '',
          text: '',
          creatorName: $scope.user.name
        };
      };

      $scope.reset();
    }])
  .controller('IdeaDetailCtrl', ['$scope', '$window', '$rootScope', '$timeout', 'brainstormingService',
    function ($scope, $window, $rootScope, $timeout, brainstormingService) {

      $rootScope.$on('bd:mopen', function (data, idea) {
        $scope.ideaDetail = idea;
        $scope.editMode = false;
      });


      $scope.close = function () {
        $rootScope.$broadcast('bd:mclose');
      };

      $scope.rate = function () {
        if (!$scope.ideaDetail.canEdit) {
          brainstormingService.rateIdea($scope.ideaDetail.brainstorming, $scope.ideaDetail.id);
        }
      };

      $scope.deleteIdea = function () {
        if ($window.confirm('Do you really want to delete this idea?')) {
          brainstormingService.deleteIdea($scope.ideaDetail.brainstorming, $scope.ideaDetail.id);
          $rootScope.$broadcast('bd:mclose');
        }
      };

      $scope.startEdit = function () {
        var doc = angular.element($window.document);

        $scope.formData = _.clone($scope.ideaDetail);
        $scope.editMode = true;
        $scope.img = {imageFile: null};

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
        $scope.loading = true;
        brainstormingService.updateIdea($scope.ideaDetail.brainstorming,
            $scope.ideaDetail.id,
            $scope.formData,
            $scope.img.imageFile)
          .then(function () {
          $scope.user.name = $scope.formData.creatorName;
          $scope.editMode = false;
          $rootScope.$broadcast('bd:updateLayout');
        })['finally'](function () {
          $scope.loading = false;
        });
      };
    }]);
