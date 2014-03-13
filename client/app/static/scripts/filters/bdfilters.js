'use strict';

angular.module('bdFilters', [])
  .filter('bdToArray',function () {
    /* Workaround for the object ordering problem:
     https://github.com/angular/angular.js/issues/1286
     */
    return function (obj) {
      var prop;

      if (!(obj instanceof Object)) {
        return obj;
      }

      return Object.keys(obj).map(function (key) {
        prop = Object.create(null);
        prop.value = key;
        return Object.defineProperty(obj[key], '$key', prop);
      });
    };
  }).filter('bdCut', function () {
    return function (value, wordwise, max, tail) {
      if (!value) {
        return '';
      }

      max = parseInt(max, 10);
      if (!max) {
        return value;
      }
      if (value.length <= max){
        return value;
      }

      value = value.substr(0, max);
      if (wordwise) {
        var lastSpace = value.lastIndexOf(' ');
        if (lastSpace !== -1) {
          value = value.substr(0, lastSpace);
        }
      }

      return value + (tail || ' …');
    };
  });
