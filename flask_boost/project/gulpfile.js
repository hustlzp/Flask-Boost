var gulp = require('gulp');
var tap = require('gulp-tap');
var path = require('path');
var less = require('gulp-less');
var concat = require('gulp-concat');
var watch = require('gulp-watch');
var plumber = require('gulp-plumber');
var header = require('gulp-header');
var footer = require('gulp-footer');
var batch = require('gulp-batch');

var cssRoot = 'application/static/css';
var jsRoot = 'application/static/js';

gulp.task('macros-css', function () {
    return gulp
        .src(path.join(cssRoot, '**/_*.less'))
        .pipe(plumber())
        .pipe(less({
            paths: [cssRoot]
        }))
        .pipe(concat('macros.css'))
        .pipe(gulp.dest('./application/static/macros_output/'));
});

gulp.task('macros-js', function () {
    return gulp
        .src(path.join(jsRoot, '**/_*.js'))
        .pipe(plumber())
        .pipe(header('(function () {\n"use strict";\n\n'))
        .pipe(footer('\n})();'))
        .pipe(concat('macros.js'))
        .pipe(gulp.dest('./application/static/macros_output/'));
});

gulp.task('build', ['macros-css', 'macros-js']);

gulp.task('watch', ['build'], function () {
    watch(path.join(jsRoot, '**/_*.js'), batch(function (events, done) {
        gulp.start('macros-js', done);
    }));
    watch(path.join(cssRoot, '**/_*.less'), batch(function (events, done) {
        gulp.start('macros-css', done);
    }));
});

gulp.task('default', ['build']);
