import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, g
import os

secret_key = os.getenv('SECRET_KEY')

def generate_token(user_id, tenant_id=None, role='user', scope='user'):
    payload = {
        'user_id': user_id,
        'role': role,
        'scope': scope,
        'exp': datetime.utcnow() + timedelta(hours=12)
    }

    if tenant_id:
        payload['tenant_id'] = tenant_id

    return jwt.encode(payload, secret_key, algorithm='HS256')


def login_required(scope=None, allowed_roles=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'error': 'Token missing'}), 401

            try:
                token = token.split(' ')[-1] 
                payload = jwt.decode(token, secret_key, algorithms=['HS256'])

                user_id = payload.get('user_id')
                token_scope = payload.get('scope')
                role = payload.get('role')
                tenant_id = payload.get('tenant_id')

                if scope and token_scope != scope:
                    return jsonify({'error': f'Unauthorized scope: expected {scope}'}), 403

                if allowed_roles and role not in allowed_roles:
                    return jsonify({'error': 'Unauthorized role'}), 403

                from app.models.tenant import Tenant
                if role == 'global_admin':
                    g.role = role
                    g.scope = token_scope
                    g.user_id = user_id

                    if scope == 'tenant':
                        impersonated_tenant_id = request.headers.get('X-Tenant-ID')
                        if not impersonated_tenant_id:
                            return jsonify({'error': 'X-Tenant-ID header required'}), 400

                        tenant = Tenant.query.get(int(impersonated_tenant_id))
                        if not tenant:
                            return jsonify({'error': 'Invalid tenant ID'}), 404

                        g.tenant = tenant

                    elif scope == 'user':
                        imp_tenant_id = request.headers.get('X-Tenant-ID')
                        imp_user_id = request.headers.get('X-User-ID')
                        if not imp_tenant_id or not imp_user_id:
                            return jsonify({'error': 'X-Tenant-ID and X-User-ID headers required'}), 400

                        tenant = Tenant.query.get(int(imp_tenant_id))
                        if not tenant:
                            return jsonify({'error': 'Invalid tenant ID'}), 404

                        g.tenant = tenant
                        g.user_id = int(imp_user_id)

                    return func(*args, **kwargs)

                if scope == 'tenant':
                    if not tenant_id:
                        return jsonify({'error': 'Tenant ID missing in token'}), 400

                    tenant = Tenant.query.get(tenant_id)
                    if not tenant:
                        return jsonify({'error': 'Invalid tenant'}), 404

                    g.tenant = tenant
                    g.user_id = user_id
                    g.role = role
                    g.scope = token_scope
                    return func(*args, **kwargs)

                if scope == 'user':
                    if not tenant_id or not user_id:
                        return jsonify({'error': 'Tenant/User ID missing in token'}), 400

                    tenant = Tenant.query.get(tenant_id)
                    if not tenant:
                        return jsonify({'error': 'Invalid tenant'}), 404

                    g.tenant = tenant
                    g.user_id = user_id
                    g.role = role
                    g.scope = token_scope
                    return func(*args, **kwargs)

                return jsonify({'error': 'Unknown access case'}), 400

            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Token expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Invalid token'}), 401

        return wrapper
    return decorator

global_admin_required = login_required(scope='tenant', allowed_roles=['global_admin'])
tenant_admin_required = login_required(scope='tenant', allowed_roles=['tenant_admin'])
user_required = login_required(scope='user', allowed_roles=['user'])
