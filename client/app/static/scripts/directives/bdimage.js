'use strict';

angular.module('braind')
  .directive('bdUpload', ['$parse', function ($parse) {

    var createImage = function (url, callback) {
      var image = new Image();
      image.onload = function () {
        callback(image);
      };
      image.src = url;
    };

    return {
      restrict: 'A',
      replace: true,
      require: 'ngModel',
      templateUrl: '/static/views/directives/image.html',
      priority: 100,

      link: function (scope, element, attr, ctrl) {
        var modelCtrl = ctrl,
          input = element.find('input'),
          img = element.find('img'),
          reader = new FileReader(),
          showInitialSrc = $parse(attr.showInitialSrc)(scope),
          initialSrc = $parse(attr.ngModel)(scope);

        modelCtrl.$name = 'image';

        // display image initially, if available
        if (showInitialSrc && initialSrc) {
          img.attr('src', initialSrc);
          scope.showPreview = true;
        }

        function showError() {
          scope.$apply(function () {
            modelCtrl.$setViewValue('');
            modelCtrl.$setValidity('', false);
            scope.showPreview = false;
            scope.error = 'Invalid image (max. 3MB)';
          });
        }

        scope.clear = function () {
          modelCtrl.$setViewValue('');
          scope.showPreview = false;
        };

        input.bind('change', function (event) {
          var file = event.target.files[0];
          reader.onload = function (ev) {
            try {
              // Try to create image to test file
              createImage(ev.target.result, angular.noop);
              img.attr('src', ev.target.result);
              scope.$apply(function () {
                modelCtrl.$setViewValue(ev.target.result);
                $parse(attr.file).assign(scope, file);
                scope.showPreview = true;
                scope.error = '';
              });
            } catch (e) {
              showError();
            }
          };

          if (!file.type.match(/image.*/) || file.size > 3 * 1024 * 1024) {
            showError();
          } else {
            reader.readAsDataURL(file);
          }
        });
      }
    };
  }]);