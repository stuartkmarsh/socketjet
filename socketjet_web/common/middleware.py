class SitenameMiddleware(object):
    def process_request(self, request):
        host = request.META.get('HTTP_HOST', None)
        name = ''
        if host:
            name = host.split('.')[0] 
            name = name.split(':')[0] # incase using alternate port
            
        request.site_name = name   