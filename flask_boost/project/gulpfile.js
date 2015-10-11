var gulp = require('gulp');
var path = require('path');
var less = require('gulp-less');
var concat = require('gulp-concat');
var watch = require('gulp-watch');
var batch = require('gulp-batch');
var plumber = require('gulp-plumber');
var header = require('gulp-header');
var footer = require('gulp-footer');
var rename = require("gulp-rename");

var root = './application';

gulp.task('macros-css', function () {
    return gulp
        .src(path.join(root, 'macros/**/_*.less'))
        .pipe(plumber())
        .pipe(less({
            paths: [path.join(root, 'static/css')]
        }))
        .pipe(concat('macros.css'))
        .pipe(gulp.dest(path.join(root, 'static/output/')));
});

gulp.task('macros-js', function () {
    return gulp
        .src(path.join(root, 'macros/**/_*.js'))
        .pipe(plumber())
        .pipe(header('(function () {'))
        .pipe(footer('})();'))
        .pipe(concat('macros.js'))
        .pipe(gulp.dest(path.join(root, 'static/output/')));
});

gulp.task('pages-css', function () {
    return gulp
        .src(path.join(root, 'pages/**/*.less'))
        .pipe(plumber())
        .pipe(less({
            paths: [path.join(root, 'static/css')]
        }))
        .pipe(rename(function (path) {
            path.extname = ".css";
            return path;
        }))
        .pipe(gulp.dest(path.join(root, 'pages')));
});

gulp.task('global-css', function () {
    return gulp
        .src(path.join(root, 'static/css/**/*.less'))
        .pipe(plumber())
        .pipe(less({
            paths: [path.join(root, 'static/css')]
        }))
        .pipe(rename(function (path) {
            path.extname = ".css";
            return path;
        }))
        .pipe(gulp.dest(path.join(root, 'static/css')));
});

gulp.task('build', ['macros-css', 'macros-js', 'pages-css', 'global-css']);

gulp.task('watch', ['build'], function () {
    watch(path.join(root, 'macros/**/_*.js'), batch(function (events, done) {
        gulp.start('macros-js', done);
    }));
    watch(path.join(root, 'macros/**/_*.less'), batch(function (events, done) {
        gulp.start('macros-css', done);
    }));
    watch(path.join(root, 'pages/**/*.less'), batch(function (events, done) {
        gulp.start('pages-css', done);
    }));
    watch(path.join(root, 'static/css/**/*.less'), batch(function (events, done) {
        gulp.start('global-css', done);
    }));
});

gulp.task('default', ['build']);
