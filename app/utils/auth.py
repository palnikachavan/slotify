import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, g
import os

secret_key = os.getenv('SECRET_KEY')


def generate_token(user_id, tenant_id=None, scope='tenant'):
    payload = {
        'user_id': user_id,
        'scope': scope,
        'exp': datetime.utcnow() + timedelta(hours=12)
    }

    if tenant_id:
        payload['tenant_id'] = tenant_id

    return jwt.encode(payload, secret_key, algorithm='HS256')


def login_required(scope='tenant'):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'error': 'Token missing'}), 401

            try:
                token = token.split(' ')[-1]  # Handles "Bearer <token>" format
                payload = jwt.decode(token, secret_key, algorithms=['HS256'])
                # print("\n\n\nDecoded JWT payload:", payload)
                if payload.get('scope') != scope:
                    return jsonify({'error': 'Unauthorized scope'}), 403

                from app.models.tenant import Tenant  # Delay import to avoid circular dependency

                # 🔐 Handle user token
                if scope == 'user':
                    user_id = payload.get('user_id')
                    tenant_id = payload.get('tenant_id')

                    if not user_id or not tenant_id:
                        return jsonify({'error': 'Invalid token: user_id or tenant_id missing'}), 400

                    tenant = Tenant.query.get(tenant_id)
                    if not tenant:
                        return jsonify({'error': 'Invalid tenant'}), 401
                    
                    
                    g.user_id = user_id
                    g.tenant = tenant

                # 🔐 Handle tenant token
                elif scope == 'tenant':
                    tenant_id = payload.get('tenant_id')

                    if not tenant_id:
                        return jsonify({'error': 'Invalid token: tenant_id missing'}), 400

                    tenant = Tenant.query.get(tenant_id)
                    if not tenant:
                        return jsonify({'error': 'Invalid tenant'}), 401

                    g.tenant = tenant

                return func(*args, **kwargs)

            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Token expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Invalid token'}), 401

        return wrapper
    return decorator

tenant_required = login_required(scope='tenant')
user_required = login_required(scope='user')
