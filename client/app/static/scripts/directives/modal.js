(function () {
  'use strict';

  angular.module('braind')
    .directive('bdModal', ['$window', '$rootScope', function ($window, $rootScope) {
      return {
        restrict: 'C',
        scope: {},
        link: {
          pre: function (scope, element) {

            var closeModal = function () {
              element.css('display', 'none');
              angular.element('.bd-backdrop').css('display', 'none');
              angular.element('body').removeClass('modal-open');
            };

            var close = function (evt) {
              if (evt.target === evt.currentTarget) {
                evt.preventDefault();
                evt.stopPropagation();
                closeModal();
              }
            };

            element.bind('click', close);

            var setMaxHeight = function () {
              var maxContainer = element.find('.height-limit');
              var vh = angular.element($window).height();
              maxContainer.css('max-height', (vh - 80 - 46) + 'px');
            };

            $rootScope.$on('bd:mopen', function () {
              setMaxHeight();
              element.css('display', 'block');
              angular.element('.bd-backdrop').css('display', 'block');
              angular.element('body').addClass('modal-open');
            });

            $rootScope.$on('bd:mclose', function () {
              closeModal();
            });

            angular.element($window).bind('resize', setMaxHeight);

            element.on('$destroy', function () {
              angular.element($window).unbind('resize', setMaxHeight);
              element.unbind('click', close);
            });
          }
        }
      };
    }]);
}());
