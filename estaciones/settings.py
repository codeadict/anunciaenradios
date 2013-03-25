from django.conf import settings

JAVASCRIPT_URL = settings.STATIC_URL+'js/'
CSS_URL = getattr(settings, 'CSS_URL', settings.MEDIA_URL+'css/')

JQUERY_URL = getattr(settings, 'JQUERY_URL', '%sjs/jquery-1.6.1.min.js' % settings.STATIC_URL)
JQUERY_UI_URL = getattr(settings, 'JQUERY_UI_URL', 
                  '%sjs/jquery-ui-1.8.13.custom.min.js' % settings.STATIC_URL)
JQUERY_UI_CSS_URL = getattr(settings, 'JQUERY_UI_CSS_URL',
                  settings.STATIC_URL+'css/jquery-ui-1.8.13.custom.css')

ELRTE_ROOT_URL = getattr(settings, 'ELRTE_ROOT_URL', settings.STATIC_URL+'elrte/')
ELRTE_LANG_URL = getattr(settings, 'ELRTE_LANG_URL', ELRTE_ROOT_URL+'js/i18n/')
ELRTE_JS_ELRTE_URL = getattr(settings, 'ELRTE_JS_ELRTE_URL',
                  ELRTE_ROOT_URL+'js/elrte.min.js')
ELRTE_CSS_ELRTE_URL = getattr(settings, 'ELRTE_CSS_ELRTE_URL',
                  ELRTE_ROOT_URL+'css/elrte.min.css')