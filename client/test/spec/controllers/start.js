'use strict';

describe('Controller: MainCtrl', function () {

  // load the controller's module
  beforeEach(module('braind'));

  var MainCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    MainCtrl = $controller('StartCtrl', {
      $scope: scope
    });
  }));

  it('should attach an empty brainstorming to the scope', function () {
    var empty = {
      question: '',
      creatorEmail: '',
      details: ''
    };
    expect(scope.formData).toEqual(empty);
  });
});
