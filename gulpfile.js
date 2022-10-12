const { src, dest, watch, parallel, series } = require("gulp");
const scss = require("gulp-sass")(require('sass'));
const concat = require("gulp-concat");
const autoprefixer = require("gulp-autoprefixer");
const uglify = require("gulp-uglify");
const imagemin = require("gulp-imagemin");
const svgmin = require("gulp-svgmin");
const svgSprite = require("gulp-svg-sprite");
const cheerio = require("gulp-cheerio");
const replace = require("gulp-replace");
const del = require("del");
const browserSync = require("browser-sync").create();

const browsersync = () => {
  browserSync.init({
    proxy: 'localhost:8000',
    // server: {
    //   baseDir: "app_crm/static",
    // },
    notify: false,
    browser: "google chrome",
  });
};

const styles = () => {
  return src("app_crm/static/scss/style.scss")
    .pipe(scss({ outputStyle: "compressed" }))
    .pipe(concat("dataTables.min.css"))
    .pipe(concat("app_crm/static/vendor/fontawesome-free/css/all.min.css"))
    .pipe(concat("styles.min.css"))
    .pipe(
      autoprefixer({
        overrideBrowserslist: ["last 10 versions"],
        grid: true,
      })
    )
    .pipe(dest("app_crm/static/css"))
    .pipe(browserSync.stream());
};

const images = () => {
  return src("app_crm/static/img/**/*.*")
    .pipe(
      imagemin([
        imagemin.gifsicle({ interlaced: true }),
        imagemin.mozjpeg({ quality: 75, progressive: true }),
        imagemin.optipng({ optimizationLevel: 5 }),
        imagemin.svgo({
          plugins: [{ removeViewBox: true }, { cleanupIDs: false }],
        }),
      ])
    )
    .pipe(dest("app_crm/static/img"));
};

const svg = () => {
  return src(["app_crm/static/img/icons/*.svg", "!app_crm/static/img/icons/sprite.svg"])
    .pipe(
      svgmin({
        js2svg: {
          pretty: true,
        },
      })
    )
    .pipe(
      cheerio({
        run: ($) => {
          $("[fill]").removeAttr("fill");
          $("[stroke]").removeAttr("stroke");
          $("[style]").removeAttr("style");
        },
        parserOptions: { xmlMode: true },
      })
    )
    .pipe(replace("&gt;", ">"))
    .pipe(
      svgSprite({
        mode: {
          stack: {
            sprite: "../sprite.svg",
          },
        },
      })
    )
    .pipe(dest("app_crm/static/img/icons"));
};

const scripts = () => {
  return src([
    "node_modules/jquery/dist/jquery.js",
    "app_crm/static/js/dataTables.min.js",
    "app_crm/static/js/main.js",
  ])
    .pipe(concat("main.min.js"))
    .pipe(uglify())
    .pipe(dest("app_crm/static/js"))
    .pipe(browserSync.stream());
};

const cleanDist = () => {
  return del("dist");
};

const build = () => {
  return src(["app/**/*.html", "app/css/styles.min.css", "app/js/main.min.js"], { base: "app" }).pipe(dest("dist"));
};

const watcher = () => {
  watch(["app_crm/static/scss/**/*.scss"], styles);
  watch(["app_crm/static/js/**/*.js", "!app_crm/static/js/main.min.js"], scripts);
  watch(["app_crm/templates/**/*.html"]).on("change", browserSync.reload);
  watch(["app_crm/static/img/icons/*.svg", "!app_crm/static/img/icons/sprite.svg"], svg);
};

exports.styles = styles;
exports.scripts = scripts;
exports.browsersync = browsersync;
exports.images = images;
exports.cleanDist = cleanDist;
exports.watcher = watcher;
exports.svg = svg;

exports.build = series(cleanDist, images, build);
exports.default = parallel(styles, scripts, svg, browsersync, watcher);
