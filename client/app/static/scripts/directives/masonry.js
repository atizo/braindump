(function () {
  'use strict';

  angular.module('braind')
    .controller('MasonryCtrl', ['$scope', '$element', '$timeout', '$window', function ($scope, $element, $timeout, $window) {
      var bricks = {},
        destroyed = false,
        self = this,
        timeout = null,
        previousColumnsCount = null;

      this.minColumnWidth = 100;
      this.gapPercentage = 5;

      // Make sure it's only executed once within a reasonable time-frame in
      // case multiple elements are removed or added at once.
      this.scheduleMasonry = function () {
        if (timeout) {
          $timeout.cancel(timeout);
        }
        timeout = $timeout(self.runMasonry, 30);
      };

      this.runMasonry = function () {
        var columnsCount = Math.floor($element.width() / self.minColumnWidth) || 1,
          columns = null,
          shortestColumn = null;

        if (columnsCount !== previousColumnsCount ||
            Object.keys(bricks).length !== $element.find('> .column > *')) {
          columns = Array.apply(null, new Array(columnsCount)).map(Number.prototype.valueOf, 0);

          while ($element.find('> .column').size() < columnsCount) {
            // need to add columns
            $element.append('<div class="column"></div>');
          }

          _.forOwn(bricks, function (brick) {
              shortestColumn = columns.indexOf(Math.min.apply(Math, columns));

              // move brick to shortest column
              $element.find('> .column:nth(' + shortestColumn + ')').append(brick);

              columns[shortestColumn] += brick.outerHeight() + self.gapPercentage;
            }
          );

          // remove possible unused columns
          $element.find('> .column:gt(' + (columnsCount - 1) + ')').remove();

          // apply new percentages
          $element.find('> .column').css('width', (100 / columnsCount) + '%');
          $element.find('> .column:lt(' + (columnsCount - 1) + ') > *').css('margin-right', self.gapPercentage + '%');
          $element.find('> .column:nth(' + (columnsCount - 1) + ') > *').css('margin-right', '');
          $element.find('> .column > *').css('margin-bottom', self.gapPercentage + '%');

          // apply brick size classes
          $element.find('> .column > *').toggleClass('narrow',
            $element.width() / self.minColumnWidth % 1 <= 0.5);
          $element.find('> .column > *').toggleClass('wide',
            $element.width() / self.minColumnWidth % 1 > 0.5);

          previousColumnsCount = columnsCount;
        }
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

        $scope.$emit('masonry.destroyed');

        bricks = [];
      };

      this.reload = function () {
        $element.masonry();
        $scope.$emit('masonry.reloaded');
      };

      angular.element($window).bind('resize', self.scheduleMasonry);
    }]).directive('masonry', function () {
      return {
        restrict: 'AE',
        controller: 'MasonryCtrl',
        link: {
          pre: function preLink(scope, element, attrs, ctrl) {
            ctrl.minColumnWidth = parseInt(attrs.minColumnWidth, 10);
            ctrl.gapPercentage = parseInt(attrs.gapPercentage, 10);
            scope.$on('$destroy', ctrl.destroy);
          }
        }
      };
    }).directive('masonryBrick', function () {
      return {
        restrict: 'AC',
        require: '^masonry',
        scope: true,
        link: {
          pre: function preLink(scope, element, attrs, ctrl) {
            var id = scope.$id, index;

            ctrl.appendBrick(element, id);
            element.on('$destroy', function () {
              ctrl.removeBrick(id, element);
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
