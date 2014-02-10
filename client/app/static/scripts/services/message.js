'use strict';

angular.module('braind')
  .factory('messageService', ['infoMsg',
    function (infoMsg) {
      var show = true;

      return {
        getMsg: function () {
          if (show) {
            show = false;
            return infoMsg;
          }

          return '';
        }
      };
    }
  ]);
