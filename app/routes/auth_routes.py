from flask import Blueprint, request, jsonify
from app import db
from app.models.tenant import Tenant
from app.tenants.database_router import setup_tenant_schema, create_database_if_not_exists
import jwt, datetime, os
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)
SECRET = os.getenv('SECRET_KEY')

@auth_bp.route('/register', methods=['POST'])
def register_tenant():
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']
    db_uri = f"postgresql://postgres:example@localhost/{data['db_uri']}"

    if Tenant.query.filter_by(email=email).first():
        return jsonify({'error': 'Tenant already exists'}), 400

    try:
        create_database_if_not_exists(db_uri)
    except Exception as e:
        return jsonify({"error": f"Could not create database: {str(e)}"}), 500

    tenant = Tenant(name=name, email=email, db_uri=db_uri, role='tenant_admin')
    tenant.password_hash = generate_password_hash(password)
    db.session.add(tenant)
    db.session.commit()

    try:
        setup_tenant_schema(db_uri)
    except Exception as e:
        return jsonify({"error": f"Failed to create tenant tables: {str(e)}"}), 500

    return jsonify({'message': 'Tenant registered and schema initialized'}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    tenant = Tenant.query.filter_by(email=email).first()
    if not tenant or not check_password_hash(tenant.password_hash, password):
        return jsonify({'error': 'Invalid email or password'}), 401

    token_payload = {
        'tenant_id': tenant.id,
        'user_id': tenant.id,
        'scope': 'tenant',
        'role': tenant.role, 
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(token_payload, SECRET, algorithm='HS256')

    return jsonify({
        'access_token': token,
        'tenant_name': tenant.name,
        'db_uri': tenant.db_uri
    }), 200
    
@auth_bp.route('/admin/login', methods=['POST'])
def login_global_admin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Missing credentials'}), 400

    # Load admin credentials from .env
    admin_email = os.getenv('GLOBAL_ADMIN_EMAIL')
    admin_password = os.getenv('GLOBAL_ADMIN_PASSWORD')

    if email != admin_email or password != admin_password:
        return jsonify({'error': 'Invalid credentials'}), 401

    token_payload = {
        'user_id': 0,
        'scope': 'tenant',
        'role': 'global_admin',
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)
    }

    token = jwt.encode(token_payload, SECRET, algorithm='HS256')

    return jsonify({
        'access_token': token,
        'email': email,
        'role': 'global_admin'
    }), 200