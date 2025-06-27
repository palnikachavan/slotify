from flask import Blueprint, jsonify, request
from app.models.tenant import Tenant
from app.models.service import Service
from app.models.users import User
from app.models.slot_user import SlotUser
from app.utils.auth import global_admin_required
from app.tenants.database_router import get_tenant_session

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/tenants', methods=['GET'])
@global_admin_required
def list_tenants():
    tenants = Tenant.query.all()
    return jsonify([{
        'id': t.id,
        'name': t.name,
        'email': t.email,
        'db_uri': t.db_uri
    } for t in tenants]), 200

@admin_bp.route('/tenants-services', methods=['GET'])
@global_admin_required
def list_services_per_tenant():
    tenants = Tenant.query.all()
    all_services = []

    for tenant in tenants:
        if not tenant.db_uri:
            continue

        session = get_tenant_session(tenant.db_uri)
        services = session.query(Service).all()
        all_services.append({
            'tenant': tenant.name,
            'services': [{'id': s.id, 'name': s.name, 'description': s.description} for s in services]
        })

    return jsonify(all_services), 200

@admin_bp.route('/tenants-users', methods=['GET'])
@global_admin_required
def list_users_per_tenant():
    tenants = Tenant.query.all()
    all_users = []

    for tenant in tenants:
        if not tenant.db_uri:
            continue

        session = get_tenant_session(tenant.db_uri)
        users = session.query(User).all()
        all_users.append({
            'tenant': tenant.name,
            'users': [{'id': u.id, 'name': u.name, 'email': u.email} for u in users]
        })

    return jsonify(all_users), 200
