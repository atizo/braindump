(function () {
  'use strict';

  angular.module('braind')
    .controller('MasonryCtrl',function controller($scope, $element, $timeout, $window) {
      var bricks = {};
      var destroyed = false;
      var self = this;
      var timeout = null;

      this.columnWidth = 100;
      this.gap = 5;

      // Make sure it's only executed once within a reasonable time-frame in
      // case multiple elements are removed or added at once.
      this.scheduleMasonry = function () {
        if (timeout) {
          $timeout.cancel(timeout);
        }
        timeout = $timeout(self.runMasonry, 30);
      };

      this.runMasonry = function () {
        var columnsCount = Math.floor(($element.width() + self.gap) / (self.columnWidth + self.gap)) || 1,
          columnsWidth = columnsCount * self.columnWidth + (columnsCount - 1) * self.gap,
          columns = Array.apply(null, new Array(columnsCount)).map(Number.prototype.valueOf, 0),
          shortestColumn = null,
          initialGap = columnsCount > 1 ? Math.floor(($element.width() - columnsWidth) / 2) : 0;

        _.forOwn(bricks, function (brick) {
            shortestColumn = columns.indexOf(Math.min.apply(Math, columns));

            if (columnsCount > 1) {
              brick.css('transform', 'translate(' +
                (initialGap + shortestColumn * (self.columnWidth + self.gap)) + 'px, ' +
                columns[shortestColumn] + 'px)');
            } else {
              brick.css('transform', '');
            }
            brick.toggleClass('fluid', columnsCount === 1);

            columns[shortestColumn] += brick.outerHeight() + self.gap;
          }
        );

        if (columnsCount > 1) {
          $element.css('height', Math.max.apply(Math, columns) + 'px');
        } else {
          $element.css('height', '');
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

      this.removeBrick = function (id, element) {
        if (destroyed) {
          return;
        }

        delete bricks[id];
        $element.masonry('remove', element);
        self.scheduleMasonry();
      };

      this.destroy = function () {
        destroyed = true;

        angular.element($window).unbind('resize', self.scheduleMasonry);

        if ($element.data('masonry')) {
          // Gently uninitialize if still present
          $element.masonry('destroy');
        }
        $scope.$emit('masonry.destroyed');

        bricks = [];
      };

      this.reload = function () {
        $element.masonry();
        $scope.$emit('masonry.reloaded');
      };

      angular.element($window).bind('resize', self.scheduleMasonry);
    }).directive('masonry',function masonryDirective() {
      return {
        restrict: 'AE',
        controller: 'MasonryCtrl',
        link: {
          pre: function preLink(scope, element, attrs, ctrl) {
            ctrl.columnWidth = parseInt(attrs.columnWidth, 10);
            ctrl.gap = parseInt(attrs.gap, 10);
            scope.$on('$destroy', ctrl.destroy);
          }
        }
      };
    }).directive('masonryBrick', function masonryBrickDirective() {
      return {
        restrict: 'AC',
        require: '^masonry',
        scope: true,
        link: {
          pre: function preLink(scope, element, attrs, ctrl) {
            var id = scope.$id, index;
            console.log(id);

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
