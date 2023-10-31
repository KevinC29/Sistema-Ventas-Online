from pyramid.authentication import AuthTktCookieHelper
from pyramid.authorization import (
    ACLHelper,
    Authenticated,
    Everyone,
    Allow,
    Authenticated,
)
# from pyramid.security import , Everyone, 
from pyramid.csrf import CookieCSRFStoragePolicy
from pyramid.request import RequestLocalCache

from . import models


# class MySecurityPolicy:
#     def __init__(self, secret):
#         self.authtkt = AuthTktCookieHelper(secret)
#         self.identity_cache = RequestLocalCache(self.load_identity)
#         self.acl = ACLHelper()

#     def load_identity(self, request):
#         identity = self.authtkt.identify(request)
#         if identity is None:
#             return None

#         userid = identity['userid']
#         user = request.dbsession.query(models.User).get(userid)
#         return user

#     def identity(self, request):
#         return self.identity_cache.get_or_create(request)

#     def authenticated_userid(self, request):
#         user = self.identity(request)
#         if user is not None:
#             return user.id

#     def remember(self, request, userid, **kw):
#         return self.authtkt.remember(request, userid, **kw)

#     def forget(self, request, **kw):
#         return self.authtkt.forget(request, **kw)

#     def permits(self, request, context, permission):
#         principals = self.effective_principals(request)
#         return self.acl.permits(context, principals, permission)

#     def effective_principals(self, request):
#         principals = [Everyone]
#         user = self.identity(request)
#         if user is not None:
#             principals.append(Authenticated)
#             principals.append('u:' + str(user.id))
#             principals.append('role:' + user.role)
#         return principals



class RootFactory:

    def __init__(self, request):
        pass

    def __acl__(self):
        return [
            # (Allow, Everyone, 'view'),  # Permite a todos ver
            (Allow, Authenticated, 'view'),  # Permite a usuarios autenticados editar
            (Allow, 'role:editor', ('create', 'edit', 'delete')),  # Permite a usuarios con rol 'editor' acceso de administrador
            (Allow, 'role:basic', ('create', 'edit'))  # Permite a usuarios con rol 'basic' acceso de administrador
        ]

    

def includeme(config):
    settings = config.get_settings()

    # config.set_csrf_storage_policy(CookieCSRFStoragePolicy())
    # config.set_default_csrf_options(require_csrf=True)

    # config.set_security_policy(MySecurityPolicy(settings['auth.secret']))

    # Configuración de la política de autorización
    config.set_root_factory(RootFactory)


# import redis
# from pyramid.config import Configurator
# from pyramid.security import Allow, Authenticated
# from pyramid.session import UnencryptedCookieSessionFactoryConfig

# # Configuración de la conexión Redis
# redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# # Factory para obtener una nueva conexión a Redis por solicitud
# def get_redis(request):
#     return redis_client

# # Clase para la fábrica de contexto de raíz (RootFactory)
# class RootFactory:
#     __acl__ = [
#         (Allow, Authenticated, 'view'),
#     ]

# # Configuración de la sesión en Pyramid para usar Redis
# session_factory = UnencryptedCookieSessionFactoryConfig('secret')
# session_factory['redis'] = get_redis

# def includeme(config):
#     config.set_root_factory(RootFactory)
#     config.set_session_factory(session_factory)