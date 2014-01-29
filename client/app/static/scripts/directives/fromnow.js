'use strict';

angular.module('braind')
  .directive('bdFromNow', ['$timeout', 'bdDate', function ($timeout, bdDate) {

    return {
      restrict: 'E',
      link: function (scope, element, attr) {
        var activeTimeout = null;

        function updateTime(value) {
          var result = bdDate.formatFromNow(value);

          element.text(result.fromNow);

          if (angular.isDefined(result.secondsUntilUpdate)) {
            activeTimeout = $timeout(function () {
              updateTime(value);
            }, result.secondsUntilUpdate * 1000, false);
          }
        }

        scope.$watch(attr.value, function (value) {
          if (!angular.isDefined(value) || value === null) {
            return;
          }

          if (activeTimeout) {
            $timeout.cancel(activeTimeout);
            activeTimeout = null;
          }

          updateTime(value);
        });
      }
    };
  }]);