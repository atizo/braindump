'use strict';

angular.module('braind')
  .directive('bdFromNow', ['$timeout', 'bdDate', function ($timeout, bdDate) {

    return {
      restrict: 'A',
      link: function (scope, element, attr) {
        element.text('-');
        var unreg = bdDate.formatFromNow(attr.bdFromNow, function (formattedDate) {
          element.text(formattedDate);
        });

        scope.$on('destroy', unreg);
      }
    };
  }]);