(function () {
  'use strict';

  angular.module('braind')
    .controller('MasonryCtrl', ['$rootScope', '$scope', '$element', '$timeout', '$window', function ($rootScope, $scope, $element, $timeout, $window) {
      var bricks = {},
        loadReg = false,
        destroyed = false,
        self = this,
        timeout = null;

      this.minColumnWidth = 220;
      this.gap = 15;



      // Make sure it's only executed once within a reasonable time-frame in
      // case multiple elements are removed or added at once.
      this.scheduleMasonry = function () {
        if (timeout) {
          $timeout.cancel(timeout);
        }
        timeout = $timeout(self.runMasonry, 30);
      };

      $rootScope.$on('bd:updateLayout', this.scheduleMasonry);

      this.runMasonry = function () {
        var columnsCount = Math.floor($element.width() / ( self.minColumnWidth + self.gap)) || 1,
          columnWidth = Math.floor(($element.width() - (columnsCount - 1) * self.gap) / columnsCount),
          columns = null,
          shortestColumn = null,
          sortedBricks;

        columns = Array.apply(null, new Array(columnsCount)).map(Number.prototype.valueOf, 0);

        // sort bricks by index from ng-repeat
        sortedBricks = _.toArray(bricks).sort(function (a, b) {
          return a.scope().$index - b.scope().$index;
        });

        // apply calculated width
        _.forOwn(sortedBricks, function (brick) {
            brick.css('width', columnWidth + 'px');
          }
        );

        // move bricks after the new width is applied
        var d = function () {
          _.forOwn(sortedBricks, function (brick) {
            var brickHeight = brick.outerHeight(true);
            shortestColumn = columns.indexOf(Math.min.apply(Math, columns));
            brick.css('transform', 'translate(' + (shortestColumn * (columnWidth) + shortestColumn * self.gap) + 'px, ' + columns[shortestColumn] + 'px)');

            // todo: make this configurable
            if(brickHeight >= 417){
              brick.addClass('limited');
            }else{
              brick.removeClass('limited');
            }

            columns[shortestColumn] += (brickHeight + self.gap);
            brick.addClass('show');
          });
          $element.css('height', Math.max.apply(Math, columns) + 'px');
        };

        $timeout(d, 1);
      };

      this.appendBrick = function (element, id) {
        if (destroyed) {
          return;
        }

        if (bricks[id] === undefined) {
          // Keep track of added elements.
          bricks[id] = element;
        }

        self.scheduleMasonry();

        // reload layout if all assets are loaded
        if(!loadReg){
          loadReg = true;
          angular.element($window).load(self.scheduleMasonry);
          $window.fontcall = self.scheduleMasonry;
        }
      };

      this.removeBrick = function (id) {
        if (destroyed) {
          return;
        }

        delete bricks[id];

        self.scheduleMasonry();
      };

      this.destroy = function () {
        destroyed = true;

        angular.element($window).unbind('resize', self.scheduleMasonry);
        angular.element($window).unbind('load', self.scheduleMasonry);

        $scope.$emit('masonry.destroyed');

        bricks = [];
      };

      angular.element($window).bind('resize', self.scheduleMasonry);
    }]).directive('masonry', function () {
      return {
        restrict: 'AE',
        controller: 'MasonryCtrl',
        link: {
          pre: function preLink(scope, element, attrs, ctrl) {
            ctrl.minColumnWidth = parseInt(attrs.minColumnWidth, 10);
            ctrl.gap = parseInt(attrs.gap, 10);
            scope.$on('$destroy', ctrl.destroy);
          }
        }
      };
    })
    .directive('masonryBrick', function () {
      return {
        restrict: 'AC',
        require: '^masonry',
        scope: true,
        link: {
          pre: function (scope, element, attrs, ctrl) {
            var id = scope.$id, index;

            ctrl.appendBrick(element, id);
            element.on('$destroy', function () {
              ctrl.removeBrick(id);
            });

            scope.$watch('$index', function () {
              if (index !== undefined && index !== scope.$index) {
                ctrl.scheduleMasonry();
              }
              index = scope.$index;
            });
          }
        }
      };
    });
}());
