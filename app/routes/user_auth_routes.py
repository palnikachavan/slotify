from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from app.models.users import User
from app.utils.auth import generate_token
from app.tenants.database_router import get_tenant_session
from app.models.tenant import Tenant  # import Tenant model

user_auth_bp = Blueprint('user_auth', __name__)

@user_auth_bp.route('/user/register', methods=['POST'])
def register_user():
    data = request.get_json()

    tenant_id = data.get('tenant_id')
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([tenant_id, name, email, password]):
        return jsonify({'error': 'Missing fields'}), 400

    tenant = Tenant.query.get(tenant_id)
    if not tenant:
        return jsonify({'error': 'Tenant not found'}), 404

    session = get_tenant_session(tenant.db_uri)

    if session.query(User).filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400

    user = User(name=name, email=email)
    user.set_password(password)

    try:
        session.add(user)
        session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except IntegrityError:
        session.rollback()
        return jsonify({'error': 'Registration failed'}), 500


@user_auth_bp.route('/user/login', methods=['POST'])
def login_user():
    data = request.get_json()

    tenant_id = data.get('tenant_id')
    email = data.get('email')
    password = data.get('password')

    if not all([tenant_id, email, password]):
        return jsonify({'error': 'Missing fields'}), 400

    tenant = Tenant.query.get(tenant_id)
    if not tenant:
        return jsonify({'error': 'Tenant not found'}), 404

    session = get_tenant_session(tenant.db_uri)
    user = session.query(User).filter_by(email=email).first()

    if user and user.check_password(password):
        token = generate_token(user.id, tenant_id, scope='user')
        return jsonify({'token': token}), 200

    return jsonify({'error': 'Invalid credentials'}), 401
