'use strict';

angular.module('braind')
  .directive('bdIdea', ['brainstormingService', function (brainstormingService) {

    return {
      restrict: 'E',
      templateUrl: '/static/views/directives/bdidea.html',
      scope:{
        resource: '=',
        limitText: '@',
        dynamicTextSize: '@',
        hideRatings: '@'
      },
      link: function (scope) {
        var titleTextWatch = null;

        if (scope.dynamicTextSize) {
          titleTextWatch = scope.$watchCollection('[resource.title, resource.text]', function() {
            var l = scope.resource.title.length + scope.resource.text.length;
            if (l <= 25) {
              scope.sizeClass =  'size-5';
            } else if (l <= 50) {
              scope.sizeClass =  'size-4';
            } else if (l <= 150) {
              scope.sizeClass =  'size-3';
            } else if (l <= 300) {
              scope.sizeClass =  'size-2';
            } else {
              scope.sizeClass =  'size-1';
            }
          });

          // necessary to clean up watch?
          scope.$on('$destroy', titleTextWatch);
        } else {
          scope.sizeClass = '';
        }

        scope.rate = function (event) {
          event.stopPropagation();
          brainstormingService.rateIdea(scope.resource.brainstorming, scope.resource.id);
        };
      }
    };
  }]);