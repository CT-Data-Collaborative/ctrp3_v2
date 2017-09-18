
////////////////////////////////
		//Setup//
////////////////////////////////

// Plugins
var gulp = require('gulp'),
      pjson = require('./package.json'),
      sass = require('gulp-sass'),
      autoprefixer = require('gulp-autoprefixer'),
      cssnano = require('gulp-cssnano'),
      rename = require('gulp-rename'),
      plumber = require('gulp-plumber'),
      pixrem = require('gulp-pixrem'),
      imagemin = require('gulp-imagemin'),
      runSequence = require('run-sequence');


// Relative paths function
var pathsConfig = function (appName) {
  this.app = "./" + (appName || pjson.name);

  return {
    app: this.app,
    templates: this.app + '/templates',
    css: this.app + '/static/css',
    sass: this.app + '/static/sass',
    fonts: this.app + '/static/fonts',
    images: this.app + '/static/images',
    js: this.app + '/static/js',
  }
};

var paths = pathsConfig();

////////////////////////////////
		//Tasks//
////////////////////////////////

// Styles autoprefixing and minification
gulp.task('styles', function() {
  return gulp.src(paths.sass + '/*.scss')
    .pipe(sass().on('error', sass.logError))
    .pipe(plumber()) // Checks for errors
    .pipe(autoprefixer({browsers: ['last 2 versions']})) // Adds vendor prefixes
    .pipe(pixrem())  // add fallbacks for rem units
    .pipe(gulp.dest(paths.css))
    .pipe(rename({ suffix: '.min' }))
    .pipe(cssnano()) // Minifies the result
    .pipe(gulp.dest(paths.css));
});


// Image compression
gulp.task('imgCompression', function(){
  return gulp.src(paths.images + '/*')
    .pipe(imagemin()) // Compresses PNG, JPEG, GIF and SVG images
    .pipe(gulp.dest(paths.images))
});

// Watch
gulp.task('watch', function() {
    gulp.watch(paths.sass + '/partials/*.scss', ['styles']);
    gulp.watch(paths.sass + '/*.scss', ['styles']);
    gulp.watch(paths.images + '/*', ['imgCompression']);
});

// Default task
gulp.task('default', function() {
    runSequence(['styles', 'imgCompression'], ['watch']);
});
