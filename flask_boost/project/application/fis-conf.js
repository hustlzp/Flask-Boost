fis.config.set('project.include', ['templates/**', 'static/**']);
fis.config.set('project.exclude', ['static/**.less']);
fis.config.set('pack', {
    'pkg/libs.js': [
        'static/js/libs/jquery.min.js',
        'static/js/libs/bootstrap.min.js',
        'static/js/init.js'
    ],
    'pkg/libs.css': [
        'static/css/libs/*.css'
    ],
    'pkg/layout.css': [
        'static/css/bootstrap.theme.css',
        'static/css/common.css',
        'static/css/macros/*.css',
        'static/css/layout.css'
    ]
});
