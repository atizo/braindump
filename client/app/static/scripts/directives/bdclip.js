'use strict';

angular.module('bdDirectives', []).
  provider('bdClip',function () {
    var self = this;
    this.path = '//cdnjs.cloudflare.com/ajax/libs/zeroclipboard/1.2.3/ZeroClipboard.swf';
    return {
      setPath: function (newPath) {
        self.path = newPath;
      },
      $get: function () {
        return {
          path: self.path
        };
      }
    }
  }).
  run(['$document', 'bdClip', function ($document, bdClip) {
    ZeroClipboard.config({
      moviePath: bdClip.path,
      trustedDomains: ['*'],
      allowScriptAccess: 'always',
      forceHandCursor: true
    });
  }]).
  directive('bdClipCopy', ['$window', 'bdClip', function ($window, bdClip) {
    return {
      scope: {
        bdClipCopy: '&',
        bdClipClick: '&'
      },
      restrict: 'A',
      link: function (scope, element, attrs) {
        // Create the clip object
        var clip = new ZeroClipboard(element);
        clip.on('load', function (client) {
          var onMousedown = function (client) {
            client.setText(scope.$eval(scope.bdClipCopy));
            if (angular.isDefined(attrs.bdClipClick)) {
              scope.$apply(scope.bdClipClick);
            }
          };
          client.on('mousedown', onMousedown);

          scope.$on('$destroy', function () {
            client.off('mousedown', onMousedown);
            client.unclip(element);
          });
        });
      }
    };
  }]);
