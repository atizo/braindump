'use strict';

describe('Controller: MasonryCtrl', function () {

  // load the controller's module
  beforeEach(module('braind'));

  var MasonryCtrl,
    scope,
    localScope,
    masonryElement,
    brickElement,
    i;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope, $window) {
    scope = $rootScope.$new();
    scope.fruits = [
      {name: 'apple', height: '100px'},
      {name: 'banana', height: '50px'},
      {name: 'strawberry', height: '100px'},
      {name: 'ananas', height: '50px'},
      {name: 'mango', height: '50px'}
    ];

    masonryElement = angular.element('<div style="width: 400px;"></div>');
    angular.element($window.document.body).append(masonryElement);

    MasonryCtrl = $controller('MasonryCtrl', {
      $scope: scope,
      $element: masonryElement
    });
    MasonryCtrl.minColumnWidth = 100;
    MasonryCtrl.columnGap = 5;

    spyOn(MasonryCtrl, 'scheduleMasonry').andCallThrough();
    spyOn(MasonryCtrl, 'runMasonry').andCallThrough();
  }));

  it('should keep track of appended bricks and layout them',
    inject(function ($compile, $timeout, $window) {
      for (i = 0; i < scope.fruits.length; i += 1) {
        localScope = scope.$new();
        localScope.fruit = scope.fruits[i];

        brickElement = angular.element('<div class="fruit {{fruit.name}}" ng-bind="fruit.name" ' +
          'ng-style="{width: \'100px\', height: fruit.height}"></div>');
        masonryElement.append(brickElement);
        $compile(brickElement)(localScope);
        localScope.$digest();

        MasonryCtrl.appendBrick(brickElement, localScope.$id);
      }

      expect(MasonryCtrl.scheduleMasonry.calls.length).toEqual(5);
      expect(MasonryCtrl.runMasonry).not.toHaveBeenCalled();

      $timeout.flush();
      expect(MasonryCtrl.runMasonry.calls.length).toEqual(1);

      expect(masonryElement.find('.column').size()).toBe(4);
      expect(masonryElement.find('.column:nth(0)')[0].style.width).toBe('25%');
      expect(masonryElement.find('.column:nth(1)')[0].style.width).toBe('25%');
      expect(masonryElement.find('.column:nth(2)')[0].style.width).toBe('25%');
      expect(masonryElement.find('.column:nth(3)')[0].style.width).toBe('25%');

      expect(masonryElement.find('.column:nth(0) .fruit.apple').size()).toBe(1);
      expect(masonryElement.find('.column:nth(1) .fruit.banana').size()).toBe(1);
      expect(masonryElement.find('.column:nth(2) .fruit.strawberry').size()).toBe(1);
      expect(masonryElement.find('.column:nth(3) .fruit.ananas').size()).toBe(1);
      expect(masonryElement.find('.column:nth(1) .fruit.mango').size()).toBe(1);

      expect(masonryElement.find('.fruit.apple')[0].style.marginRight).toBe('5%');
      expect(masonryElement.find('.fruit.apple')[0].style.marginBottom).toBe('5%');

      masonryElement.css('width', '450px');
      angular.element($window).resize();
      $timeout.flush();
      expect(MasonryCtrl.runMasonry.calls.length).toEqual(2);
      expect(masonryElement.find('.column').size()).toBe(4);

      masonryElement.css('width', '500px');
      angular.element($window).resize();
      $timeout.flush();
      expect(MasonryCtrl.runMasonry.calls.length).toEqual(3);

      expect(masonryElement.find('.column').size()).toBe(5);
      expect(masonryElement.find('.column:nth(0)')[0].style.width).toBe('20%');
      expect(masonryElement.find('.column:nth(1)')[0].style.width).toBe('20%');
      expect(masonryElement.find('.column:nth(2)')[0].style.width).toBe('20%');
      expect(masonryElement.find('.column:nth(3)')[0].style.width).toBe('20%');
      expect(masonryElement.find('.column:nth(4)')[0].style.width).toBe('20%');

      expect(masonryElement.find('.column:nth(0) .fruit.apple').size()).toBe(1);
      expect(masonryElement.find('.column:nth(1) .fruit.banana').size()).toBe(1);
      expect(masonryElement.find('.column:nth(2) .fruit.strawberry').size()).toBe(1);
      expect(masonryElement.find('.column:nth(3) .fruit.ananas').size()).toBe(1);
      expect(masonryElement.find('.column:nth(4) .fruit.mango').size()).toBe(1);

      masonryElement.css('width', '350px');
      angular.element($window).resize();
      $timeout.flush();
      expect(MasonryCtrl.runMasonry.calls.length).toEqual(4);
      expect(masonryElement.find('.column').size()).toBe(3);
      expect(masonryElement.find('.column:nth(0)')[0].style.width.substr(0, 4)).toBe('33.3');
      expect(masonryElement.find('.column:nth(1)')[0].style.width.substr(0, 4)).toBe('33.3');
      expect(masonryElement.find('.column:nth(2)')[0].style.width.substr(0, 4)).toBe('33.3');

      expect(masonryElement.find('.column:nth(0) .fruit.apple').size()).toBe(1);
      expect(masonryElement.find('.column:nth(1) .fruit.banana').size()).toBe(1);
      expect(masonryElement.find('.column:nth(2) .fruit.strawberry').size()).toBe(1);
      expect(masonryElement.find('.column:nth(1) .fruit.ananas').size()).toBe(1);
      expect(masonryElement.find('.column:nth(0) .fruit.mango').size()).toBe(1);
    }
  ));
});

